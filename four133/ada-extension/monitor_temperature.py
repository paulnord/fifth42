#!/usr/bin/env python3
"""Read-only CPU thermal trace alongside an existing search; no load generation."""
import argparse,csv,json,os,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=120);p.add_argument('--interval',type=float,default=2);a=p.parse_args()
    if not 1<=a.seconds<=28800 or not 1<=a.interval<=60:p.error('seconds must be 1..28800 and interval 1..60')
    hwmon=next(h for h in Path('/sys/class/hwmon').glob('hwmon*') if (h/'name').exists() and (h/'name').read_text().strip()=='k10temp')
    sensors={}
    for item in hwmon.glob('temp*_input'):
        label=item.with_name(item.name.replace('_input','_label'))
        if label.exists():sensors[label.read_text().strip()]=item
    assert 'Tctl' in sensors
    job=Path(json.loads((ROOT/'jobs/latest.json').read_text())['job'])
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder=job/'telemetry'/stamp;folder.mkdir(parents=True,exist_ok=False)
    columns=['timestamp_utc','trace_seconds','job_seconds','Tctl_c','Tccd1_c','Tccd2_c','load_1m','active_workers','search_status']
    records=[];start=time.monotonic();next_sample=start;last_report=-10
    print(f'Trace directory: {folder}',flush=True)
    with (folder/'temperature.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
        while True:
            now=time.monotonic()
            state=json.loads((job/'progress.json').read_text())
            temperatures={name:float(path.read_text().strip())/1000 for name,path in sensors.items()}
            row=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),trace_seconds=round(now-start,3),job_seconds=round(time.time()-state['started_unix'],3),Tctl_c=temperatures['Tctl'],Tccd1_c=temperatures.get('Tccd1'),Tccd2_c=temperatures.get('Tccd2'),load_1m=os.getloadavg()[0],active_workers=state['active_workers'],search_status=state['status'])
            writer.writerow(row);f.flush();records.append(row)
            temp=folder/'current.json.tmp';temp.write_text(json.dumps(row,indent=2)+'\n');os.replace(temp,folder/'current.json')
            if now-start-last_report>=10:
                print(f'{row["timestamp_utc"]}  Tctl={row["Tctl_c"]:.2f} C  CCD1={row["Tccd1_c"]} C  CCD2={row["Tccd2_c"]} C  load={row["load_1m"]:.2f}  workers={row["active_workers"]}',flush=True);last_report=now-start
            if now-start>=a.seconds:break
            next_sample+=a.interval;time.sleep(max(0,min(next_sample,start+a.seconds)-time.monotonic()))
    summary=dict(sensor='k10temp Tctl',samples=len(records),duration_seconds=records[-1]['trace_seconds'],first_c=records[0]['Tctl_c'],last_c=records[-1]['Tctl_c'],minimum_c=min(r['Tctl_c'] for r in records),maximum_c=max(r['Tctl_c'] for r in records),mean_c=sum(r['Tctl_c'] for r in records)/len(records),job_started_at=state['started_at'],trace_started_at=records[0]['timestamp_utc'],initial_idle_baseline_recorded=False)
    (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':11})
    fig,ax=plt.subplots(figsize=(10,4.8),layout='constrained')
    for key,label,color in [('Tctl_c','CPU Tctl','#d04734'),('Tccd1_c','CCD 1','#2678b2'),('Tccd2_c','CCD 2','#34966d')]:
        if all(r[key] is not None for r in records):ax.plot([r['trace_seconds'] for r in records],[r[key] for r in records],label=label,color=color,linewidth=1.8)
    ax.set(xlabel='Seconds since temperature recording began',ylabel='Temperature (°C)',title='ADA CPU temperature during four133 search — 16 workers')
    ax.grid(alpha=.2);ax.legend(loc='best');ax.text(.01,-.23,f'Trace began {records[0]["job_seconds"]/60:.1f} minutes after search start; initial warm-up was not recorded.',transform=ax.transAxes,color='#555555',fontsize=9)
    fig.savefig(folder/'temperature.png',dpi=160);plt.close(fig)
    (job/'telemetry/latest.json').write_text(json.dumps(dict(directory=str(folder),**summary),indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    print(f'Plot: {folder}/temperature.png',flush=True)

if __name__=='__main__':main()

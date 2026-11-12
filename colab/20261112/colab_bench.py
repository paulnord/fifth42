"""Portable stdlib-only native-packet replay. No planner, ledger or search job."""
from pathlib import Path
from math import prod
import argparse,hashlib,json,os,platform,random,statistics,subprocess,time
from engine_session import EngineSession
ROOT=Path(__file__).resolve().parent

def sha(data):return hashlib.sha256(data).hexdigest()
def save(path,value):
    path.parent.mkdir(exist_ok=True);temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(path)

def tasks(packet):
    lines=packet.splitlines();header=lines[0].split()
    if len(header)!=4 or header[0]!='LATTICE_GPU_V1' or int(header[1])!=0:raise ValueError('Constant-cap packet required')
    cap,count=map(int,header[2:]);result=[]
    if not 0<=count<=4096 or len(lines)!=count+1:raise ValueError('Invalid native task count')
    for index,line in enumerate(lines[1:]):
        values=list(map(int,line.split()))
        if len(values)!=15 or values[0]!=index:raise ValueError('Task order/shape mismatch')
        _,lo,hi,*tail=values;j=tuple(tail[:3]);u=tuple(tuple(tail[3+i:6+i]) for i in (0,3,6))
        if not 1<=lo<=hi<=200000000000 or any(x<0 for x in j):raise ValueError('Invalid native bounds')
        points=prod(2*x+1 for x in j)
        if points>10000000:raise ValueError('Per-task point limit exceeded')
        for col in range(3):
            if sum(j[i]*abs(u[i][col]) for i in range(3))>2**63-1:raise ValueError('Transform overflow')
        result.append(dict(lo=lo,hi=hi,J=j,U=u,points=points,line=line))
    if sum(t['points'] for t in result)>50000000:raise ValueError('Packet point limit exceeded')
    return cap,result

def normalized(response):
    return dict(points_visited=response['points_visited'],counts=response['counts'],
        hits=sorted(response['hits'],key=lambda h:(h['task'],h['linear'],h['a'],h['b'],h['c'])))

def verify(packet,response,backend,expected):
    cap,ts=tasks(packet)
    if response.get('backend')!=backend or response.get('box_complete') is not True:raise ValueError('Incomplete/wrong backend')
    if type(response.get('points_visited')) is not int or response['points_visited']!=sum(t['points'] for t in ts):raise ValueError('Incomplete total count')
    if not isinstance(response.get('counts'),list) or len(response['counts'])!=len(ts):raise ValueError('Missing task counts')
    for i,(count,t) in enumerate(zip(response['counts'],ts)):
        if any(type(count.get(k)) is not int for k in ('id','expected','visited')):raise ValueError('Count type')
        if count!=dict(id=i,expected=t['points'],visited=t['points']):raise ValueError('Incomplete per-task count')
    if not isinstance(response.get('hits'),list):raise ValueError('Invalid hit array')
    seen=set()
    for hit in response['hits']:
        if any(type(hit.get(k)) is not int for k in ('task','linear','a','b','c')):raise ValueError('Hit type')
        index=hit['task'];linear=hit['linear'];key=(index,linear)
        if key in seen or not 0<=index<len(ts) or not 0<=linear<ts[index]['points']:raise ValueError('Duplicate/invalid candidate')
        seen.add(key);t=ts[index];coeff=[];remainder=linear
        for j in t['J']:coeff.append(remainder%(2*j+1)-j);remainder//=2*j+1
        c,a,b=[sum(coeff[i]*t['U'][i][col] for i in range(3)) for col in range(3)]
        if (a,b,c)!=(hit['a'],hit['b'],hit['c']) or not t['lo']<=c<=t['hi'] or not 1<=a<=b<c:
            raise ValueError('Exact reconstruction/domain mismatch')
        if abs(a**5+b**5-c**5)>cap:raise ValueError('Exact residual mismatch')
    if normalized(response)!=expected:raise ValueError('Independent GMP counts/hits differ')

def combine(rows):
    requests=[];pending=[];points=0;cap=None
    def flush():
        if not pending:return
        total_tasks=[];expected=dict(points_visited=0,counts=[],hits=[]);routes=[]
        for row in pending:
            _,ts=tasks(row['packet']);offset=len(total_tasks);total_tasks.extend(ts)
            routes.append(dict(name=row['name'],original_packet_sha256=row['packet_sha256'],first_task=offset,task_count=len(ts)))
            expected['points_visited']+=row['expected']['points_visited']
            expected['counts'].extend(dict(c,id=c['id']+offset) for c in row['expected']['counts'])
            expected['hits'].extend(dict(h,task=h['task']+offset) for h in row['expected']['hits'])
        packet=f'LATTICE_GPU_V1 0 {cap} {len(total_tasks)}\n'+'\n'.join(
            str(i)+' '+t['line'].split(' ',1)[1] for i,t in enumerate(total_tasks))+'\n'
        requests.append(dict(packet=packet,expected=expected,routes=routes,points=points))
    for row in rows:
        rowcap,ts=tasks(row['packet'])
        if pending and (rowcap!=cap or points+row['points']>50000000 or
                        sum(len(tasks(r['packet'])[1]) for r in pending)+len(ts)>4096):
            flush();pending=[];points=0
        cap=rowcap;pending.append(row);points+=row['points']
    flush();return requests

def hardware():
    out=dict(python=platform.python_version(),platform=platform.platform(),
        logical_cpus=os.cpu_count(),available_cpu_affinity=len(os.sched_getaffinity(0)))
    mem=dict(line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())
    out['system_ram_gib']=int(mem['MemTotal'].split()[0])/1024**2
    for key,cmd in [('gpu',['nvidia-smi']),('nvcc',['nvcc','--version'])]:
        try:out[key]=subprocess.run(cmd,text=True,capture_output=True,timeout=10).stdout
        except FileNotFoundError:out[key]='unavailable'
    return out

def main(args):
    start=time.monotonic();deadline=start+args.max_seconds
    data=ROOT/'data/packets.jsonl';meta=json.loads((ROOT/'data/export.json').read_text())
    if sha(data.read_bytes())!=meta['packet_file_sha256']:raise ValueError('Packet export identity differs')
    rows=[json.loads(line) for line in data.read_text().splitlines()]
    for row in rows:
        if sha(row['packet'].encode())!=row['packet_sha256']:raise ValueError('Packet checksum mismatch')
        cap,ts=tasks(row['packet'])
        if cap!=row['cap'] or sum(t['points'] for t in ts)!=row['points']:raise ValueError('Packet metadata differs')
    group_rows={g:[r for r in rows if r['group']==g] for g in ('realistic','tiny')}
    requests={g:combine(rs) for g,rs in group_rows.items()}
    identical={g:[r['packet'] for r in group_rows[g]]==[r['packet'] for r in requests[g]] for g in group_rows}
    report=dict(status='running',TEST_ONLY=True,new_scientific_coverage=False,backend=args.backend,
        hardware=hardware(),packet_export_sha256=sha(data.read_bytes()),trials=[],
        compute_units_per_hour_observed_by_user=args.units_per_hour,
        sizes={g:dict(original_packets=len(rs),combined_requests=len(requests[g]),requests_byte_identical=identical[g],points=sum(r['points'] for r in rs),
            packet_points=[r['points'] for r in rs],task_counts=[len(tasks(r['packet'])[1]) for r in rs]) for g,rs in group_rows.items()},
        limitations='Prepared packet replay only. CPU planning, network transfer, durable cloud checkpoints and production journal costs are not included. No new search coverage.')
    target=ROOT/'results'/f'benchmark-{args.backend}.json';save(target,report)
    binary=ROOT/'bin'/('scaling_gpu' if args.backend=='gpu' else 'scaling_cpu')
    backend='gpu' if args.backend=='gpu' else 'emulated'
    def remaining():
        left=deadline-time.monotonic()
        if left<=0:raise TimeoutError('Overall benchmark deadline reached')
        return min(30,left)
    try:
        with EngineSession([str(binary)],backend,deadline) as engine:
            report['engine_startup_seconds']=engine.startup_seconds
            for row in rows: # independent supplied GMP reference checked on every input
                response,_=engine.run(row['packet'],timeout=remaining());verify(row['packet'],response,backend,row['expected'])
            report['all_original_packet_counts_and_hits_equal_gmp']=True
            if args.verify_gmp:
                for row in rows:
                    ref=subprocess.run([str(ROOT/'bin/gmp_reference')],input=row['packet'],text=True,
                        capture_output=True,check=True,timeout=remaining())
                    verify(row['packet'],json.loads(ref.stdout),'emulated',row['expected'])
                report['fresh_local_gmp_all_packets']=True
            rng=random.Random(42)
            for repeat in range(args.repeats):
                for group in ('realistic','tiny'):
                    variants=['separate'] if identical[group] else ['separate','combined'];rng.shuffle(variants)
                    for variant in variants:
                        selected=group_rows[group] if variant=='separate' else requests[group]
                        began=time.perf_counter();rpc=kernel=engine_time=0.
                        for request in selected:
                            response,duration=engine.run(request['packet'],timeout=remaining())
                            rpc+=duration;kernel+=response.get('kernel_seconds',0) or 0
                            engine_time+=response.get('engine_seconds',0) or 0
                            verify(request['packet'],response,backend,request['expected'])
                        report['trials'].append(dict(repeat=repeat,group=group,variant=variant,
                            total_replay_seconds=time.perf_counter()-began,rpc_seconds=rpc,
                            kernel_seconds=kernel,engine_seconds=engine_time,
                            requests=len(selected),verified_points=sum(r['points'] for r in selected)))
                        save(target,report)
            # A false completion must be rejected even for a nonempty control.
            control=next(r for r in rows if r['group']=='control')
            response,_=engine.run(control['packet'],timeout=remaining())
            try:verify(control['packet'],dict(response,points_visited=response['points_visited']-1),backend,control['expected'])
            except ValueError:report['incomplete_response_rejected']=True
            else:raise AssertionError('Incomplete response accepted')
        report['summary']={}
        for group in ('realistic','tiny'):
            variants=['separate'] if identical[group] else ['separate','combined']
            medians={v:statistics.median(r['total_replay_seconds'] for r in report['trials'] if r['group']==group and r['variant']==v)
                for v in variants}
            report['summary'][group]=dict(medians=medians,
                separate_over_combined=None if identical[group] else medians['separate']/medians['combined'],
                conclusion='Request streams are byte-identical; no distinct coalescing performance claim.' if identical[group] else 'Distinct request streams; engine-only replay comparison.')
        report['status']='passed'
    except BaseException as error:
        report.update(status='failed',error=repr(error));raise
    finally:
        report['elapsed_seconds']=time.monotonic()-start;save(target,report)
    print(json.dumps({k:report[k] for k in ('status','backend','sizes','summary','elapsed_seconds')},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--backend',choices=['cpu','gpu'],default='cpu')
    parser.add_argument('--repeats',type=int,default=5);parser.add_argument('--max-seconds',type=float,default=180)
    parser.add_argument('--verify-gmp',action='store_true');parser.add_argument('--units-per-hour',type=float)
    args=parser.parse_args()
    if not 1<=args.repeats<=20 or not 0<args.max_seconds<=600:parser.error('Bounded repetitions/time required')
    main(args)

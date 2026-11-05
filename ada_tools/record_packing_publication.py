"""Import the verified publication commit locally and save its receipt."""
from datetime import datetime
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess

root=Path('/home/pnord/fifth-lattice-optimizations-ada-20261105')
repo=Path('/home/pnord/fifth42-lattice-optimizations-91bb89b')
data=json.loads((root/'github-packing-remote-commit.json').read_text())
parent='34f9f52816863d619bc0fafd30265c27c73eb8be'
expected='c64f17b01f23389d714825388682af69a93cbd3d'
assert data['sha']==expected
assert [p['sha'] for p in data['parents']]==[parent]
assert not data.get('verification',{}).get('signature')

def git(*args,input=None):
    return subprocess.run(['git',*args],cwd=repo,input=input,capture_output=True,check=True).stdout.decode().strip()

assert git('rev-parse','HEAD')==parent
assert git('write-tree')==data['tree']['sha']
headers=['tree '+data['tree']['sha'],'parent '+parent]
people=[]
for label in ('author','committer'):
    person=data[label]
    epoch=int(datetime.fromisoformat(person['date'].replace('Z','+00:00')).timestamp())
    people.append(f"{label} {person['name']} <{person['email']}> {epoch}")
matched=[]
for author_zone,committer_zone in product(('-0600','+0000'),repeat=2):
    for message in (data['message'],data['message']+'\n'):
        raw=('\n'.join(headers+[people[0]+' '+author_zone,people[1]+' '+committer_zone])+'\n\n'+message).encode()
        actual=hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual==expected:matched.append(raw)
assert len(matched)==1,'Cannot reconstruct exact remote commit'
assert git('hash-object','-t','commit','-w','--stdin',input=matched[0])==expected
git('update-ref','HEAD',expected,parent)
assert git('status','--porcelain')=='','Publication checkout is not clean'
receipt=dict(status='published',commit=expected,parent=parent,tree=data['tree']['sha'],
    branch='handoff/fifth-lattice-optimizations-20261105',published_files=60,
    report_url=f'https://github.com/paulnord/fifth42/blob/{expected}/ada_validation/lattice-packing-20261105/README.md',
    remote_head_verified=True,local_tree_matches_published_tree=True,local_checkout_clean=True)
(root/'github-packing-published.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))

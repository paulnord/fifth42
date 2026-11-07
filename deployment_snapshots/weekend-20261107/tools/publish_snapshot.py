"""Publish a checksum-verified setup snapshot without disturbing status writers."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',required=True,type=Path)
    parser.add_argument('--workdir',required=True,type=Path)
    parser.add_argument('--prefix',default='deployment_snapshots/weekend-20261107')
    parser.add_argument('--branch',default='handoff/fifth-lattice-optimizations-20261105')
    parser.add_argument('--tag',default='weekend-setup-20261107')
    parser.add_argument('--skip-tag',action='store_true',help='Publish a preliminary capture; final capture gets the fixed tag')
    parser.add_argument('--remote',default='git@github.com:paulnord/fifth42.git')
    parser.add_argument('--ssh-key',default='/home/pnord/.ssh/fifth42_status_20261105')
    parser.add_argument('--known-hosts',default='/home/pnord/fifth-lattice-gpu/github_known_hosts')
    args=parser.parse_args();snapshot=args.snapshot.resolve();work=args.workdir.resolve()
    if Path(args.prefix).is_absolute() or '..' in Path(args.prefix).parts:raise ValueError('Invalid backup prefix')
    expected={}
    for line in (snapshot/'SHA256SUMS').read_text().splitlines():
        wanted,name=line.split('  ',1)
        if digest(snapshot/name)!=wanted:raise RuntimeError('Snapshot checksum mismatch: '+name)
    files=sorted(path for path in snapshot.rglob('*') if path.is_file())
    if any(path.is_symlink() for path in files):raise RuntimeError('Symlink in snapshot')
    environment=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_AUTHOR_NAME='Ada lattice setup backup',
                     GIT_COMMITTER_NAME='Ada lattice setup backup',
                     GIT_AUTHOR_EMAIL='ada-lattice@users.noreply.github.com',
                     GIT_COMMITTER_EMAIL='ada-lattice@users.noreply.github.com',
                     GIT_SSH_COMMAND=shlex.join(['ssh','-i',args.ssh_key,'-o','IdentitiesOnly=yes',
                       '-o','IdentityAgent=none','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
                       '-o','ConnectTimeout=10','-o','UserKnownHostsFile='+args.known_hosts]))
    def git(repo,*command,data=None,env=None,check=True):
        result=subprocess.run(['git','--git-dir',str(repo),*command],input=data,text=True,
                              capture_output=True,timeout=180,env=dict(environment,**(env or {})))
        if check and result.returncode:raise RuntimeError('git '+command[0]+': '+result.stderr.strip())
        return result
    repo=work/'repository.git'
    git(repo,'init','--bare',str(repo))
    if not args.skip_tag:
        existing=git(repo,'ls-remote','--tags',args.remote,'refs/tags/'+args.tag).stdout.strip()
        if existing:raise RuntimeError('Backup tag already exists; choose a fresh tag, never overwrite it')
    index_rows=[]
    for path in files:
        name=str(path.relative_to(snapshot))
        if any(c in name for c in ('\n','\t','\0')):raise ValueError('Unsupported snapshot filename')
        blob=git(repo,'hash-object','-w',str(path)).stdout.strip()
        mode='100755' if path.stat().st_mode&0o111 else '100644'
        expected[name]=dict(sha256=digest(path),blob_sha=blob,mode=mode)
        index_rows.append(mode+' '+blob+'\t'+args.prefix+'/'+name+'\n')
    commit=None
    for attempt in range(4):
        git(repo,'fetch','--depth=1',args.remote,'refs/heads/'+args.branch)
        parent=git(repo,'rev-parse','FETCH_HEAD').stdout.strip()
        with tempfile.TemporaryDirectory(dir=work) as temporary:
            env={'GIT_INDEX_FILE':str(Path(temporary)/'index')}
            git(repo,'read-tree',parent,env=env)
            git(repo,'update-index','--index-info',data=''.join(index_rows),env=env)
            tree=git(repo,'write-tree',env=env).stdout.strip()
            message=('Back up exact running Ada and Boole worker setup\n\n'
                     'Preserve frozen sources, native builds, runtime pins, user services, '
                     'NFS/reporting configuration and restore instructions. Running searches '
                     'and periodic status paths remain independent.\n')
            commit=git(repo,'commit-tree',tree,'-p',parent,data=message).stdout.strip()
        pushed=git(repo,'push','--porcelain',args.remote,commit+':refs/heads/'+args.branch,check=False)
        if pushed.returncode==0:break
        remote_head=git(repo,'ls-remote',args.remote,'refs/heads/'+args.branch).stdout.split()
        if not remote_head or remote_head[0]==parent or attempt==3:
            raise RuntimeError('Backup push failed: '+pushed.stderr.strip())
    if not args.skip_tag:
        git(repo,'update-ref','refs/tags/'+args.tag,commit)
        git(repo,'push','--porcelain',args.remote,'refs/tags/'+args.tag)
    # A new repository proves the bytes are retrievable from the remote, not
    # merely present in our staging object database.
    verify=work/'remote-verification.git'
    git(verify,'init','--bare',str(verify))
    git(verify,'fetch','--depth=1',args.remote,commit if args.skip_tag else 'refs/tags/'+args.tag)
    actual_commit=git(verify,'rev-parse','FETCH_HEAD').stdout.strip()
    if actual_commit!=commit:raise RuntimeError('Remote tag targets a different commit')
    found={}
    tree_output=git(verify,'ls-tree','-r',commit,'--',args.prefix+'/').stdout
    for line in tree_output.splitlines():
        meta,name=line.split('\t',1);mode,kind,sha=meta.split()
        name=name.removeprefix(args.prefix+'/');found[name]=dict(mode=mode,blob_sha=sha)
    if set(found)!=set(expected):raise RuntimeError('Remote backup file inventory differs')
    for name,item in expected.items():
        if found[name]!={key:item[key] for key in ('mode','blob_sha')}:
            raise RuntimeError('Remote blob/mode mismatch: '+name)
        result=subprocess.run(['git','--git-dir',str(verify),'cat-file','blob',item['blob_sha']],
                              capture_output=True,timeout=30,check=True,env=environment)
        if hashlib.sha256(result.stdout).hexdigest()!=item['sha256']:
            raise RuntimeError('Remote bytes differ: '+name)
    record=dict(status='published_and_remotely_verified',commit=commit,tag=None if args.skip_tag else args.tag,
                branch=args.branch,prefix=args.prefix,files=len(expected),
                sha256_verified_files=len(expected),url='https://github.com/paulnord/fifth42/tree/'+(commit if args.skip_tag else args.tag)+'/'+args.prefix)
    (work/'publication-receipt.json').write_text(json.dumps(record,indent=2)+'\n')
    (work/'remote-file-inventory.json').write_text(json.dumps(expected,indent=2)+'\n')
    print(json.dumps(record,indent=2),flush=True)


if __name__=='__main__':main()

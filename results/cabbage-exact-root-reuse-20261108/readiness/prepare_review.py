from pathlib import Path
import hashlib,json,shutil,subprocess
root=Path(__file__).resolve().parent
repo=Path('/home/pnord/scratch/saved-root-pAjTHBhR/repo')
prior=Path('/home/pnord/scratch/saved-root-followup-DL829jCa')
review=root/'review-bundle';review.mkdir()
for variant in ('baseline','candidate'):
 target=review/variant
 shutil.copytree(prior/variant/'source/lattice_prototype',target/'source/lattice_prototype',ignore=shutil.ignore_patterns('__pycache__'))
 shutil.copytree(prior/variant/'source/lattice_gpu',target/'source/lattice_gpu',ignore=shutil.ignore_patterns('__pycache__','bin'))
(review/'native').mkdir();shutil.copytree(prior/'device/src',review/'native/src');shutil.copytree(prior/'device/vendor',review/'native/vendor')
(review/'bin').mkdir()
shutil.copy2(prior/'device/bin/scaling_gpu',review/'bin/scaling_gpu')
shutil.copy2(prior/'native/bin/gmp_reference',review/'bin/gmp_reference')
original=repo/'deployment_snapshots/weekend-20261107/ada/worker/ada_export_store.py'
shutil.copy2(original,review/'upstream_ada_export_store.py')
testroot='/mnt/nfs_share/TEST_ONLY_cabbage_saved_root_20261108_Ija5nMHk'
s=original.read_text();assert s.count("elif host=='boole':")==1
s=s.replace("elif host=='boole':", "elif host in ('boole','cabbage'):")
s=s.replace("test=Path('/mnt/nfs_share/TEST_ONLY_ada_export_adapter_20261107_ada')",f"test=Path('{testroot}')")
s=s.replace("This deployment supports only the actual Ada and Boole hosts", "This staged deployment supports the actual Ada, Boole and Cabbage hosts")
(review/'cabbage_export_store.py').write_text(s)
(root/'nfs-root.txt').write_text(testroot+'\n')
(root/'cabbage-storage.patch').write_text(subprocess.run(['diff','-U1','--label','upstream/ada_export_store.py','--label','candidate/cabbage_export_store.py',str(original),str(review/'cabbage_export_store.py')],capture_output=True,text=True).stdout)
files={str(p.relative_to(review)):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(review.rglob('*')) if p.is_file()}
manifest=dict(schema=1,status='STAGED_REVIEW_ONLY',production_launch_authorized=False,production_coverage=False,source_commit='be5fcb6d5818d70035a9f2a8f31812f5f1f8b53f',base_commit='da4e1e312ce1558c9d8cf027c009f8b400f22b83',target='cabbage',python='/home/pnord/scratch/saved-root-pAjTHBhR/venv/bin/python',test_namespace=testroot,files=files,changes=['Saved-root two-file Python patch (candidate only).','Shared native engine uses already validated 200-billion guard.','Storage adapter adds actual Cabbage NFS-client verification and the new private test namespace; Store protocol unchanged.'])
(review/'STAGED-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Staged',len(files),'files; test namespace',testroot)

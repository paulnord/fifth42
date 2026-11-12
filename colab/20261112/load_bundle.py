"""Reconstruct and verify the bundle from a checked-out GitHub directory."""
from pathlib import Path
import argparse,base64,hashlib,json,tarfile,io

def unpack(payload,manifest,destination):
    if hashlib.sha256(payload).hexdigest()!=manifest['archive_sha256']:
        raise ValueError('Archive checksum mismatch')
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
    with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as archive:
        seen=set()
        for member in archive.getmembers():
            rel=Path(member.name)
            if not member.isfile() or rel.is_absolute() or '..' in rel.parts or member.name in seen:
                raise ValueError('Unsafe or duplicate archive entry')
            seen.add(member.name);target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    for line in (destination/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((destination/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Extracted file checksum mismatch: '+name)
    return destination

def main(destination):
    root=Path(__file__).resolve().parent;manifest=json.loads((root/'transport/manifest.json').read_text())
    chunks=[]
    for entry in manifest['chunks']:
        raw=(root/'transport'/entry['name']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Chunk checksum mismatch')
        chunks.append(raw)
    payload=base64.b64decode(b''.join(chunks),validate=True)
    print(unpack(payload,manifest,destination))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--destination',default='fifth42-colab-runtime')
    main(parser.parse_args().destination)

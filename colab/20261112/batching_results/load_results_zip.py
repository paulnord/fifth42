"""Reconstruct the original Colab result ZIP from repository-sized text chunks."""
from pathlib import Path
import argparse
import base64
import hashlib
import json


def main(output):
    root = Path(__file__).resolve().parent / "transport"
    manifest = json.loads((root / "MANIFEST.json").read_text())
    parts = []
    for entry in manifest["chunks"]:
        name = entry["name"]
        if Path(name).name != name:
            raise ValueError("Unsafe chunk name")
        data = (root / name).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Result transport checksum mismatch")
        parts.append(data)
    data = base64.b64decode(b"".join(parts), validate=True)
    if len(data) != manifest["zip_bytes"] or hashlib.sha256(data).hexdigest() != manifest["zip_sha256"]:
        raise ValueError("Result ZIP identity differs")
    with Path(output).open("xb") as stream:
        stream.write(data)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("Fifth42_Batching_Results.zip"))
    main(parser.parse_args().output)

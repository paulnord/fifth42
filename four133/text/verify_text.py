#!/usr/bin/env python3
"""Verify the mirrored text files; this is not a production-log audit."""
import hashlib
import json
from pathlib import Path, PurePosixPath

root = Path(__file__).resolve().parent
manifest = json.loads((root / "INVENTORY.json").read_text())
for record in manifest["files"]:
    relative = PurePosixPath(record["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe inventory path")
    data = (root / relative).read_bytes()
    data.decode("utf-8")
    if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
        raise ValueError(f"Mismatch: {relative}")
print(f"Verified {len(manifest['files'])} unchanged text files. Raw production logs are not included.")

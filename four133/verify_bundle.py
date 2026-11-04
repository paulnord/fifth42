#!/usr/bin/env python3
"""Verify the frozen evidence chain without extracting or executing its files."""
import hashlib
import io
import json
import tarfile
from pathlib import Path, PurePosixPath

ARCHIVE = Path(__file__).resolve().parent / "four133_4000000_reproduction.tar.gz"
EXPECTED_SHA256 = "2cfc019a955a8e5518ff027bf11c8585f0e197b6a9030c4b02dfd5a56ee5a050"
EXPECTED_BYTES = 5749673


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_archive(data, prefix):
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        require(len(names) == len(set(names)), "Duplicate archive member")
        for member in members:
            path = PurePosixPath(member.name)
            require(not path.is_absolute() and ".." not in path.parts,
                    "Unsafe archive member path")
            require(member.isfile() or member.isdir(), "Unexpected archive member type")
        manifest = json.load(archive.extractfile(f"{prefix}/manifest.json"))
        for name, record in manifest["files"].items():
            payload = archive.extractfile(f"{prefix}/{name}").read()
            require(len(payload) == record["bytes"], f"Size mismatch: {prefix}/{name}")
            require(digest(payload) == record["sha256"], f"Hash mismatch: {prefix}/{name}")
        print(f"{prefix}: verified {len(manifest['files'])} manifest-listed files")
        prior = manifest.get("prior_archive")
        if prior is not None:
            payload = archive.extractfile(prior["name"]).read()
            require(len(payload) == prior["bytes"], "Prior archive size mismatch")
            require(digest(payload) == prior["sha256"], "Prior archive hash mismatch")
            next_prefix = ("four133_3000000" if prefix == "four133_4000000"
                           else "four133_extension")
            verify_archive(payload, next_prefix)


def main():
    data = ARCHIVE.read_bytes()
    require(len(data) == EXPECTED_BYTES, "Top-level archive size mismatch")
    require(digest(data) == EXPECTED_SHA256, "Top-level archive SHA-256 mismatch")
    verify_archive(data, "four133_4000000")
    print("Full-chain integrity verified. No binaries executed; no search performed.")


if __name__ == "__main__":
    main()

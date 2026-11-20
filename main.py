"""Deliver the finished news infographic for 19 November 2026.

Copies entry.png (which sits next to this script) into the directory named
by MAKEFUN_OUTPUT_DIR, then checks the copy is byte-for-byte identical by
comparing SHA-256 digests of the source and the copy.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"

    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1

    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"

    try:
        shutil.copyfile(source, dest)
    except OSError as exc:
        print(f"error: could not copy entry.png to {dest}: {exc}", file=sys.stderr)
        return 1

    if sha256_of(source) != sha256_of(dest):
        print(f"error: hash mismatch after copying to {dest}", file=sys.stderr)
        return 1

    print(f"Wrote {dest} ({dest.stat().st_size} bytes, SHA-256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Deliver the news infographic for the make.fun bounty.

Copies the pre-rendered entry.png into the output directory named by
MAKEFUN_OUTPUT_DIR (or /output when the variable is unset), using only
the Python standard library, and verifies the copy by size.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    expected = os.path.getsize(source)
    actual = os.path.getsize(target)
    if actual != expected:
        print("error: copy size mismatch (%d != %d)" % (actual, expected),
              file=sys.stderr)
        return 1
    print("wrote", target, "(%d bytes)" % actual)
    return 0


if __name__ == "__main__":
    sys.exit(main())

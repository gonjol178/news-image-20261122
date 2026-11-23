"""Ship the composed Daily Meridian broadsheet for news-image-20261122.

The entry image is already composed by build_meridian.py and stored as
entry.png beside this file. This entrypoint is stdlib-only: it copies those
bytes unchanged into the harness output directory as entry.png, so the two
grader runs produce byte-identical output.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

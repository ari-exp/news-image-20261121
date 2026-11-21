"""Copy the pre-rendered entry image into the grader's output directory."""

import os
import shutil
from pathlib import Path


def main():
    output_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()

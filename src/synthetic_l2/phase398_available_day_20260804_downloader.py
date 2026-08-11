from __future__ import annotations

import argparse
import json
from pathlib import Path

from synthetic_l2 import phase393_available_day_20260803_downloader as base


DEFAULT_OUTPUT_DIR = Path("outputs/phase398")
TARGET_DATE = "2026-08-04"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase392-dir", type=Path, default=base.DEFAULT_PHASE392_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--real-root", type=Path, default=base.DEFAULT_REAL_ROOT)
    parser.add_argument("--file-share", default=base.DEFAULT_FILE_SHARE)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--workers", type=int, default=128)
    args = parser.parse_args()
    base.TARGET_DATE = TARGET_DATE
    outputs = base.write_outputs(
        args.phase392_dir,
        args.output_dir,
        args.real_root,
        args.file_share,
        args.timeout,
        args.dry_run,
        args.max_files,
        args.workers,
    )
    print(json.dumps({key: str(value) for key, value in outputs.items()}, indent=2))

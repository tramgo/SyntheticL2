from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from synthetic_l2.phase42_native_full_year_l2_experiment import main  # noqa: E402


if __name__ == "__main__":
    main()

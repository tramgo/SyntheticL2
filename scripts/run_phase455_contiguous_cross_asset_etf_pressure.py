from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthetic_l2.phase455_contiguous_cross_asset_etf_pressure import main


if __name__ == "__main__":
    main()

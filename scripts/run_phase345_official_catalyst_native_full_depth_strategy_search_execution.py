from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthetic_l2.phase345_official_catalyst_native_full_depth_strategy_search_execution import main


if __name__ == "__main__":
    main()

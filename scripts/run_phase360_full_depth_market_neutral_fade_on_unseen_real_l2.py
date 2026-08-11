from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthetic_l2.phase360_full_depth_market_neutral_fade_on_unseen_real_l2 import main


if __name__ == "__main__":
    main()

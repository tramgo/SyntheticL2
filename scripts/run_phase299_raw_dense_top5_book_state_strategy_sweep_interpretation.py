from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthetic_l2.phase299_raw_dense_top5_book_state_strategy_sweep_interpretation import main


if __name__ == "__main__":
    main()

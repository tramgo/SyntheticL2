from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from synthetic_l2.phase226_cost_aware_event_label_materialization_dry_run import main


if __name__ == "__main__":
    main()

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from synthetic_l2.phase28_richer_event_label_support import main  # noqa: E402


if __name__ == "__main__":
    main()

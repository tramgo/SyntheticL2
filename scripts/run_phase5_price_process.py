from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from synthetic_l2.phase5_price_process import main  # noqa: E402


if __name__ == "__main__":
    main()

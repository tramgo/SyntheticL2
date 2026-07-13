from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from synthetic_l2.phase11_strategy_modules import main  # noqa: E402


if __name__ == "__main__":
    main()

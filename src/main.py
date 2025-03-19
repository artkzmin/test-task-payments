import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api import start_app


def main() -> None:
    start_app()


if __name__ == "__main__":
    main()

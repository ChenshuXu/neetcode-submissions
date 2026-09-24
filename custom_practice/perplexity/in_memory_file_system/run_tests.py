from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli
from solution import FileSystem
from test_cases import TEST_CASES


def run_candidate(operations):
    filesystem = FileSystem()
    outputs = []
    for name, argument in operations:
        if name not in {"mkdir", "touch", "ls", "rm", "rmdir", "cd", "execute"}:
            raise ValueError(f"Unknown test operation: {name}")
        outputs.append(getattr(filesystem, name)(argument))
    return outputs


if __name__ == "__main__":
    raise SystemExit(run_cli(run_candidate, TEST_CASES))

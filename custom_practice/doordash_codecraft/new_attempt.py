"""Create a fresh, non-overwriting Code Craft attempt directory."""

import argparse
import hashlib
from pathlib import Path
import re
import shlex
import shutil
from typing import Dict, Tuple


PACK_ROOT = Path(__file__).resolve().parent
ATTEMPTS_ROOT = PACK_ROOT / "attempts"

KATAS: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "dasher-pay": (
        "kata_01_dasher_pay",
        ("COLD_PROMPT.md", "dasher_pay.py", "test_dasher_pay.py"),
    ),
    "bootstrap": (
        "kata_02_bootstrap",
        ("COLD_PROMPT.md", "bootstrap.py", "test_bootstrap.py"),
    ),
}

# Filled from the reviewed starter state. A changed template is rejected instead
# of silently contaminating a later cold attempt.
EXPECTED_HASHES = {
    "kata_01_dasher_pay/COLD_PROMPT.md":
        "05fcd81b48120ba758f8add88ef085e103d7a8f12c44532cc874e87ea5276341",
    "kata_01_dasher_pay/dasher_pay.py":
        "73059e0dc21845d039395a40877baf85315478d3428a6e2f092233a7bf9f8202",
    "kata_01_dasher_pay/test_dasher_pay.py":
        "118b6ea5d3f9b13507c0042f474df99af1a7c150141c0fbca62bf6047c9fb376",
    "kata_01_dasher_pay/interviewer_checks.py":
        "8d0488c12ac28caf361683adb1c4103d1e68dd9a47dcd35b50ff5d49469473bd",
    "kata_02_bootstrap/COLD_PROMPT.md":
        "35c7edfc99667c4c199edb32136912bc69c96305557931bedb2849f75383c654",
    "kata_02_bootstrap/bootstrap.py":
        "6a4761bc43178b89a396056bc4c1a478d17f71647f77b1e32c725addc08e24ea",
    "kata_02_bootstrap/test_bootstrap.py":
        "357215ff127cdf4e062d9adb2a4d531da6055ef313b99944bc8e8b11ba75c6ba",
    "kata_02_bootstrap/interviewer_checks.py":
        "18509777a0c6cf7c34cb9cd9980e120108daa0593b85c63b1d0614543b171d26",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a fresh DoorDash Code Craft practice attempt."
    )
    parser.add_argument("kata", choices=sorted(KATAS))
    parser.add_argument(
        "attempt_name",
        help="Unique folder name using letters, numbers, underscores, or hyphens.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the request and print the destination without writing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", args.attempt_name) is None:
        raise SystemExit(
            "attempt_name must be 1-64 characters and contain only letters, "
            "numbers, underscores, or hyphens"
        )

    source_dir_name, candidate_files = KATAS[args.kata]
    source_dir = PACK_ROOT / source_dir_name
    destination = ATTEMPTS_ROOT / args.attempt_name
    if destination.exists():
        raise SystemExit(
            f"refusing to overwrite existing attempt: {destination}"
        )

    files_to_copy = list(candidate_files) + ["interviewer_checks.py"]
    for filename in files_to_copy:
        source = source_dir / filename
        expected = EXPECTED_HASHES.get(f"{source_dir_name}/{filename}")
        if expected is None:
            raise SystemExit(f"missing trusted starter hash for {source}")
        actual = sha256(source)
        if actual != expected:
            raise SystemExit(
                f"starter template changed; refusing to create an attempt: {source}"
            )

    if args.dry_run:
        print(f"validated fresh attempt: {destination}")
        return 0

    destination.mkdir(parents=True)
    for filename in files_to_copy:
        shutil.copy2(source_dir / filename, destination / filename)
    shutil.copy2(PACK_ROOT / "RUN_LOG_TEMPLATE.md", destination / "RUN_LOG.md")
    shutil.copy2(PACK_ROOT / "SCORECARD.md", destination / "SCORECARD.md")

    print(f"created: {destination}")
    print(f"next: cd {shlex.quote(str(destination))}")
    print("then: python3 -m unittest -v")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

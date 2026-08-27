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
        (
            "COLD_PROMPT.md",
            "dasher_pay.py",
            "test_dasher_pay.py",
            "run_tests.py",
        ),
    ),
    "bootstrap": (
        "kata_02_bootstrap",
        ("COLD_PROMPT.md", "bootstrap.py", "test_bootstrap.py"),
    ),
    "validate-cart": (
        "kata_03_validate_cart",
        (
            "COLD_PROMPT.md",
            "validate_cart.py",
            "test_validate_cart.py",
            "run_tests.py",
        ),
    ),
}

# Filled from the reviewed starter state. A changed template is rejected instead
# of silently contaminating a later cold attempt.
EXPECTED_HASHES = {
    "kata_01_dasher_pay/COLD_PROMPT.md":
        "e0d1d26d802c9fc46ea191079556a7850c992754abee82e71d4d8fde498ce556",
    "kata_01_dasher_pay/dasher_pay.py":
        "e1afe0f4fccb88e99aa918a16438110e3faa9807407281d6a468519b19dca544",
    "kata_01_dasher_pay/test_dasher_pay.py":
        "118b6ea5d3f9b13507c0042f474df99af1a7c150141c0fbca62bf6047c9fb376",
    "kata_01_dasher_pay/interviewer_checks.py":
        "8d0488c12ac28caf361683adb1c4103d1e68dd9a47dcd35b50ff5d49469473bd",
    "kata_01_dasher_pay/run_tests.py":
        "8ae53f8451b14d6fe06be7a483032c9d0fb2899b4f91bf36d0e0bd0e953f7a1c",
    "kata_02_bootstrap/COLD_PROMPT.md":
        "535dce154858fb7bcfa2982becca09357af0093025f4b48698c371281811174e",
    "kata_02_bootstrap/bootstrap.py":
        "eddd248bde0c05fbf6a5842a9f4fbf842d1ca9293b8c77948d236d15637ab846",
    "kata_02_bootstrap/test_bootstrap.py":
        "357215ff127cdf4e062d9adb2a4d531da6055ef313b99944bc8e8b11ba75c6ba",
    "kata_02_bootstrap/interviewer_checks.py":
        "ad728977b1aa04355d437b4a6c4d55f8bc432029fc929c588422f8e601cc4905",
    "kata_03_validate_cart/COLD_PROMPT.md":
        "bdd0ec3d40a26cf939f36c552ae8d3ded30c91b535a6a90e7d9bf4729facd0bf",
    "kata_03_validate_cart/validate_cart.py":
        "71197522bf4103d1396c18df59cc865f9abd3ed53bf4ff5d51976958e7d49a42",
    "kata_03_validate_cart/test_validate_cart.py":
        "8664d53ec671498acde18bbd808305c84ba2506590f3f5d01c1388dc2e0f7046",
    "kata_03_validate_cart/run_tests.py":
        "f58479d040eb78e127de4ca7928dab883504d2390a93f7590bc8ef20d0760c8e",
    "kata_03_validate_cart/interviewer_checks.py":
        "8845835aca1e11e4a627c944a0f935a396169e413e33fb1ee574452740e38351",
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
    if args.kata == "dasher-pay":
        print("then: python3 run_tests.py visible")
    elif args.kata == "validate-cart":
        print("then: python3 run_tests.py")
    else:
        print("then: python3 -m unittest -v")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

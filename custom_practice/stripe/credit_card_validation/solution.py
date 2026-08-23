from typing import List


class CardValidator:
    """Validate and reconstruct card numbers under the practice contract."""

    def classify(self, number: str) -> str:
        raise NotImplementedError("Implement classify in solution.py")

    def count_redacted(self, pattern: str) -> int:
        raise NotImplementedError("Implement count_redacted in solution.py")

    def repair_one_digit(self, number: str) -> List[str]:
        raise NotImplementedError("Implement repair_one_digit in solution.py")

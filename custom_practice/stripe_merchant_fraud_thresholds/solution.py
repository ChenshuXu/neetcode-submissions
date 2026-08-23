from typing import List, Sequence


def fraudulent_merchants(
    merchant_config: Sequence[str],
    fraudulent_codes: Sequence[str],
    non_fraudulent_codes: Sequence[str],
    events: Sequence[str],
) -> List[str]:
    """Return merchants flagged after all charge and dispute events."""

    raise NotImplementedError("Implement fraudulent_merchants in solution.py")

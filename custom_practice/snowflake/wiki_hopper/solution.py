from collections.abc import Callable, Iterable


def find_shortest_path(
    start_page: str,
    target_page: str,
    get_linked_pages: Callable[[str], Iterable[str]],
) -> list[str]:
    """Return one shortest directed path from start_page to target_page."""

    raise NotImplementedError("Implement find_shortest_path")

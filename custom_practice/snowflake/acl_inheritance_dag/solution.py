from collections.abc import Iterable, Mapping, Sequence


def resolve_all_acls(
    node_count: int,
    edges: Sequence[tuple[int, int]],
    local_allow: Mapping[int, Iterable[str]],
    local_deny: Mapping[int, Iterable[str]],
) -> list[list[str]]:
    """Return each node's sorted effective permissions under deny-wins inheritance."""

    raise NotImplementedError("Implement resolve_all_acls")

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Node:
    val: int
    children: List["Node"] = field(default_factory=list)


TreeSpec = Tuple[int, Tuple["TreeSpec", ...]]
ForestSpec = Tuple[TreeSpec, ...]


def t(value: int, *children: TreeSpec) -> TreeSpec:
    """Create a compact, immutable tree specification for a visible test."""

    return value, tuple(children)


def build_tree(spec: Optional[TreeSpec]) -> Optional[Node]:
    if spec is None:
        return None
    value, children = spec
    return Node(value, [build_tree(child) for child in children])  # type: ignore[list-item]


def forest_to_spec(forest: List[Node]) -> ForestSpec:
    def encode(node: Node) -> TreeSpec:
        return node.val, tuple(encode(child) for child in node.children)

    return tuple(encode(root) for root in forest)


def format_tree(spec: Optional[TreeSpec]) -> str:
    if spec is None:
        return "None"
    value, children = spec
    if not children:
        return str(value)
    return f"{value}[{', '.join(format_tree(child) for child in children)}]"


def format_forest(forest: ForestSpec) -> str:
    return "[" + ", ".join(format_tree(root) for root in forest) + "]"

"""Simple lineage DAG. Node = table/feature, edge = derivation.

Phase 2 will auto-build this from OpenLineage events — the in-memory
graph here keeps the core concept easy to follow.
"""
from datetime import datetime


class LineageGraph:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.parents: dict[str, list[str]] = {}

    def add_source(self, name, last_updated: str, quality_status: str = "OK"):
        self.nodes[name] = {"type": "source_table", "last_updated": last_updated,
                            "quality_status": quality_status}

    def add_feature(self, name, derived_from: list[str], transform: str):
        self.nodes[name] = {"type": "feature", "transform": transform}
        self.parents[name] = derived_from

    def trace_to_sources(self, feature: str) -> list[dict]:
        """DFS from a feature up to its source tables."""
        out, stack, seen = [], [feature], set()
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            meta = self.nodes.get(node, {})
            if meta.get("type") == "source_table":
                out.append({"source": node, **meta})
            stack.extend(self.parents.get(node, []))
        return out

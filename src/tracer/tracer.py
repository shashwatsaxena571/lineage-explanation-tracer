"""Joining feature attributions with data lineage — the core idea of this project."""


class ExplanationTracer:
    def __init__(self, lineage_graph):
        self.graph = lineage_graph

    def root_cause_report(self, attributions: list[dict], top_k: int = 3) -> list[dict]:
        """attributions: [{feature, attribution}] sorted desc.

        For each top feature: its upstream sources plus their quality/freshness flags.
        """
        report = []
        for a in sorted(attributions, key=lambda x: -x["attribution"])[:top_k]:
            sources = self.graph.trace_to_sources(a["feature"])
            suspicious = [s for s in sources if s.get("quality_status") != "OK"]
            report.append({
                "feature": a["feature"],
                "attribution": a["attribution"],
                "upstream_sources": [s["source"] for s in sources],
                "suspicious_sources": suspicious,
                "flag": "INVESTIGATE" if suspicious else "clean",
            })
        return report

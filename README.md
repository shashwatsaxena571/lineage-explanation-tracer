# 🔍 Lineage-to-Explanation Tracer

**"Why was this prediction wrong?" → "Feature X drove it, X comes from table Y, and Y failed its quality check yesterday."**

XAI tells you *which feature* mattered. Data lineage tells you *where the feature came from*. This project joins the two — turning a model explanation into a **data-level root-cause report, in seconds**.

## The problem

When a production model misbehaves, the debugging conversation jumps between two disconnected worlds:

- **ML team:** "SHAP says `debt_ratio` drove the prediction."
- **Data team:** "Which of our 400 tables feeds `debt_ratio`? Was any of them broken?"

Nobody has a tool that answers both questions in one query — even though that's the *actual* question every incident review asks.

## The idea

```
[Prediction] → [Attribution] → [Feature] → [Lineage DAG] → [Source tables + freshness + quality flags]
```

Join the model's top attributions with a lineage graph, and flag any upstream source that failed quality checks:

```json
{
  "feature": "debt_ratio",
  "attribution": 0.61,
  "upstream_sources": ["customers_raw", "transactions_raw"],
  "suspicious_sources": [
    {
      "source": "transactions_raw",
      "last_updated": "2026-07-25",
      "quality_status": "FAILED: 34% nulls in amount"
    }
  ],
  "flag": "INVESTIGATE"
}
```

The story is clear: `debt_ratio` drove the bad prediction, and its upstream table was corrupt. End-to-end root cause — no labels, no war room.

## Quick start

```bash
pip install -r requirements.txt
python demo.py          # loan-model scenario with a corrupted upstream table
python -m pytest tests/ -v
```

## Components

| File | What it does |
|------|--------------|
| `src/tracer/lineage.py` | Lineage DAG — source → transform → feature, with freshness & quality metadata |
| `src/tracer/tracer.py` | The join: top attributions × lineage → root-cause report |
| `demo.py` | End-to-end scenario: wrong loan prediction traced to a corrupt table |

## Roadmap

- [x] Phase 1 — in-memory lineage DAG + tracer + demo scenario
- [ ] Phase 2 — ingest [OpenLineage](https://openlineage.io/) events (auto-build the DAG from Airflow/Spark)
- [ ] Phase 3 — [Great Expectations](https://greatexpectations.io/) quality flags integration
- [ ] Phase 4 — lineage graph visualization (mermaid / graphviz export)

## Why this exists

I'm a **Data Engineer at IBM** and a **PhD scholar in Trustworthy & Explainable AI** — this project sits exactly at that intersection. My core thesis: *you can't explain a model if you can't trace your data. Explainability starts in the pipeline, not the model.*

📰 I write about this weekly in [**Explainable Pipelines**](https://www.linkedin.com/newsletters/7488207829871304704/) · 💼 [LinkedIn](https://www.linkedin.com/in/saxena-shashwat/) · 🌐 [Portfolio](https://shashwatsaxena571.github.io/)

## License

MIT

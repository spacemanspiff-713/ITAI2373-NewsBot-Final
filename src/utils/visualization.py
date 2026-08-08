"""Accessible static charts used by notebooks, reports, and validation runs."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns


def _save(path: str | Path) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(); plt.savefig(target, dpi=150, bbox_inches="tight"); plt.close()
    return target


def category_distribution(frame: pd.DataFrame, path: str | Path) -> Path:
    counts = frame["category"].value_counts().sort_index(); plt.figure(figsize=(9, 5)); sns.barplot(x=counts.index, y=counts.values, hue=counts.index, legend=False); plt.title("HuffPost Sample: Category Distribution"); plt.xlabel("Category"); plt.ylabel("Article count"); plt.xticks(rotation=25); return _save(path)


def date_distribution(frame: pd.DataFrame, path: str | Path) -> Path:
    years = pd.to_datetime(frame["date"], errors="coerce").dt.year.dropna(); plt.figure(figsize=(10, 5)); sns.histplot(years, discrete=True, color="#3b82a0"); plt.title("HuffPost Sample: Article Date Distribution"); plt.xlabel("Year"); plt.ylabel("Article count"); return _save(path)


def model_comparison(rows: list[dict], path: str | Path) -> Path:
    data = pd.DataFrame(rows); plt.figure(figsize=(10, 5)); sns.barplot(data=data, x="macro_f1", y="model", color="#2a9d8f"); plt.xlim(0, 1); plt.title("Classifier Comparison: Macro F1"); plt.xlabel("Macro F1"); plt.ylabel(""); return _save(path)


def confusion(labels: list[str], values: list[list[float]], path: str | Path) -> Path:
    plt.figure(figsize=(8, 6)); sns.heatmap(values, annot=True, fmt=".0f", cmap="Blues", xticklabels=labels, yticklabels=labels); plt.title("Classification Confusion Matrix"); plt.xlabel("Predicted category"); plt.ylabel("Actual category"); return _save(path)


def topic_words(engine, model: str, path: str | Path) -> Path:
    rows = [{"topic": f"Topic {topic}", "word": word["word"], "weight": word["weight"]} for topic in range(engine.n_topics) for word in engine.get_topic_words(topic, 5, model)]
    data = pd.DataFrame(rows); plt.figure(figsize=(11, max(6, engine.n_topics * 1.1))); sns.barplot(data=data, x="weight", y="word", hue="topic", dodge=False); plt.title(f"{model.upper()} Topic Words"); plt.xlabel("Model weight"); plt.ylabel("Term"); return _save(path)


def topic_evolution(timeline: pd.DataFrame, path: str | Path) -> Path:
    plt.figure(figsize=(11, 6)); [plt.plot(timeline["period"], timeline[column], marker="o", label=column.replace("_", " ").title()) for column in timeline.columns if column.startswith("topic_")]; plt.title("Topic Prevalence Over Time"); plt.xlabel("Year"); plt.ylabel("Mean topic probability"); plt.legend(ncol=2, fontsize=8); plt.xticks(rotation=30); return _save(path)


def sentiment_timeline(timeline: pd.DataFrame, path: str | Path) -> Path:
    plt.figure(figsize=(11, 6)); hue = "category" if "category" in timeline else None; sns.lineplot(data=timeline, x="period", y="mean_compound", hue=hue, marker="o"); plt.axhline(0, color="black", linewidth=.8); plt.title("Average VADER Sentiment Over Time"); plt.xlabel("Year"); plt.ylabel("Mean compound sentiment"); plt.xticks(rotation=30); return _save(path)


def sentiment_by_category(frame: pd.DataFrame, path: str | Path) -> Path:
    data = frame.groupby("category", as_index=False)["compound"].mean(); plt.figure(figsize=(9, 5)); sns.barplot(data=data, x="category", y="compound", hue="category", legend=False); plt.axhline(0, color="black", linewidth=.8); plt.title("Average VADER Sentiment by Category"); plt.xlabel("Category"); plt.ylabel("Mean compound sentiment"); plt.xticks(rotation=25); return _save(path)


def entity_chart(entities: list[dict], path: str | Path) -> Path:
    data = pd.Series([item["label"] for item in entities]).value_counts(); plt.figure(figsize=(8, 5)); sns.barplot(x=data.index, y=data.values, hue=data.index, legend=False); plt.title("Named Entity Type Distribution"); plt.xlabel("Entity label"); plt.ylabel("Count"); return _save(path)


def entity_graph(graph: nx.Graph, path: str | Path, max_nodes: int = 40) -> Path:
    selected = sorted(graph.nodes, key=lambda node: graph.nodes[node].get("frequency", 0), reverse=True)[:max_nodes]; subgraph = graph.subgraph(selected).copy(); plt.figure(figsize=(12, 9)); positions = nx.spring_layout(subgraph, seed=42, k=0.75); sizes = [300 + 100 * subgraph.nodes[node].get("frequency", 1) for node in subgraph]; nx.draw_networkx(subgraph, positions, with_labels=True, node_size=sizes, font_size=7, node_color="#8ecae6", edge_color="#6c757d", width=[subgraph[left][right].get("weight", 1) for left,right in subgraph.edges]); plt.title("Entity Co-occurrence Graph (Corpus Evidence Only)"); plt.axis("off"); return _save(path)


def semantic_clusters(clusters: list[dict], path: str | Path) -> Path:
    data = pd.DataFrame(clusters); plt.figure(figsize=(9, 5)); sns.countplot(data=data, x="cluster", hue="cluster", legend=False, palette="colorblind"); plt.title("Semantic Content Clusters"); plt.xlabel("Cluster"); plt.ylabel("Article count"); return _save(path)

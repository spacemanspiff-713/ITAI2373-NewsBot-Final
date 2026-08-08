"""spaCy entity extraction and transparent relationship/graph construction."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable

import networkx as nx

ENTITY_LABELS = {"PERSON", "ORG", "GPE", "LOC", "DATE", "MONEY", "NORP", "EVENT", "PRODUCT"}


class EntityRelationshipMapper:
    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        self.model_name = model_name
        self._nlp = None

    @property
    def nlp(self):
        if self._nlp is None:
            import spacy
            try:
                self._nlp = spacy.load(self.model_name)
            except OSError:
                self._nlp = spacy.blank("en")
                self._nlp.add_pipe("sentencizer")
        return self._nlp

    def extract_entities(self, text: object) -> list[dict]:
        doc = self.nlp("" if text is None else str(text))
        return [{"text": ent.text, "label": ent.label_, "start": int(ent.start_char), "end": int(ent.end_char), "sentence": ent.sent.text} for ent in doc.ents if ent.label_ in ENTITY_LABELS]

    def extract_relationships(self, text: object) -> list[dict]:
        doc = self.nlp("" if text is None else str(text))
        relationships: list[dict] = []
        for sentence in doc.sents:
            ents = [ent for ent in sentence.ents if ent.label_ in ENTITY_LABELS]
            for index, left in enumerate(ents):
                for right in ents[index + 1:]:
                    relationships.append({"source": left.text, "target": right.text, "relation": "co_occurs", "sentence": sentence.text})
            for token in sentence:
                if token.dep_ in {"nsubj", "nsubjpass", "obj", "dobj"} and token.ent_type_ in ENTITY_LABELS and token.head.pos_ in {"VERB", "AUX"}:
                    relationships.append({"source": token.text, "target": token.head.text, "relation": "subject_of" if "subj" in token.dep_ else "object_of", "sentence": sentence.text})
        return relationships

    def build_knowledge_graph(self, articles: Iterable[dict]) -> nx.Graph:
        graph = nx.Graph()
        for article in articles:
            text = article.get("full_text") or article.get("text") or ""
            article_id = str(article.get("article_id", "unknown"))
            for entity in self.extract_entities(text):
                node = entity["text"].strip()
                if not node:
                    continue
                if node not in graph:
                    graph.add_node(node, entity_type=entity["label"], frequency=0)
                graph.nodes[node]["frequency"] += 1
            for relation in self.extract_relationships(text):
                source, target = relation["source"].strip(), relation["target"].strip()
                if not source or not target or source == target:
                    continue
                if graph.has_edge(source, target):
                    graph[source][target]["weight"] += 1
                    graph[source][target]["source_article_ids"].add(article_id)
                else:
                    graph.add_edge(source, target, relation=relation["relation"], weight=1, source_article_ids={article_id})
        return graph

    @staticmethod
    def find_entity_connections(graph: nx.Graph, entity1: str, entity2: str) -> dict:
        if entity1 not in graph or entity2 not in graph:
            return {"connected": False, "path": [], "reason": "One or both entities were not found."}
        try:
            return {"connected": True, "path": nx.shortest_path(graph, entity1, entity2)}
        except nx.NetworkXNoPath:
            return {"connected": False, "path": [], "reason": "No corpus co-occurrence path found."}

    @staticmethod
    def export_graph(graph: nx.Graph, path: str | Path) -> None:
        export = graph.copy()
        for _, _, data in export.edges(data=True):
            if isinstance(data.get("source_article_ids"), set):
                data["source_article_ids"] = ",".join(sorted(data["source_article_ids"]))
        nx.write_graphml(export, Path(path))

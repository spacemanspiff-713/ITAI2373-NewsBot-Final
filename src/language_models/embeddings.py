"""Multilingual embedding retrieval with a deterministic no-download fallback."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearchEngine:
    """Small-corpus semantic retrieval using embeddings when available.

    The sentence-transformer model is lazy and optional so tests and a CPU-only
    classroom setup remain dependable. The returned backend always tells the
    user whether a semantic embedding or lexical fallback produced a result.
    """

    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", use_transformer=False):
        self.model_name = model_name
        self.use_transformer = use_transformer
        self.model = None
        self.vectorizer = None
        self.documents, self.metadata, self.vectors = [], [], None
        self.backend = "tfidf"
        self.warning = None

    def _encode(self, texts):
        values = [str(text or "") for text in texts]
        if self.use_transformer:
            try:
                if self.model is None:
                    from sentence_transformers import SentenceTransformer

                    self.model = SentenceTransformer(self.model_name)
                self.backend = "sentence_transformer"
                return self.model.encode(values, normalize_embeddings=True)
            except Exception as exc:  # Model downloads are optional and never break the core app.
                self.model = None
                self.backend = "tfidf"
                self.warning = f"Sentence-transformer unavailable; TF-IDF fallback used ({type(exc).__name__})."
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        if hasattr(self.vectorizer, "vocabulary_"):
            return self.vectorizer.transform(values).toarray()
        try:
            return self.vectorizer.fit_transform(values).toarray()
        except ValueError:
            # Preserve a meaningful deterministic result for extremely short or
            # stopword-only inputs rather than failing a whole analysis.
            self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)
            return self.vectorizer.fit_transform(values).toarray()

    def encode_documents(self, documents):
        return self._encode(documents)

    def build_index(self, documents, metadata=None):
        self.documents = [str(document or "") for document in documents]
        self.metadata = list(metadata or [{} for _ in self.documents])
        self.vectorizer = None if self.use_transformer else TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        self.vectors = self._encode(self.documents)
        return self

    def semantic_search(self, query, top_k=5, filters=None):
        if self.vectors is None:
            raise RuntimeError("Build the index before searching.")
        query_vector = self._encode([query])[0]
        scores = cosine_similarity([query_vector], self.vectors)[0]
        pairs = []
        for index, score in enumerate(scores):
            metadata = self.metadata[index] or {}
            if filters and any(str(metadata.get(key, "")).upper() != str(value).upper() for key, value in filters.items()):
                continue
            pairs.append({**metadata, "text": self.documents[index], "score": float(score), "index": index, "retrieval_backend": self.backend})
        return sorted(pairs, key=lambda row: row["score"], reverse=True)[:top_k]

    def find_similar_articles(self, article_text, top_k=5):
        return self.semantic_search(article_text, top_k + 1)[:top_k]

    def cluster_similar_content(self, n_clusters=6):
        if self.vectors is None:
            raise RuntimeError("Build the index before clustering.")
        n_clusters = min(n_clusters, len(self.documents))
        labels = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit_predict(self.vectors)
        return [{**(self.metadata[index] or {}), "index": index, "cluster": int(label)} for index, label in enumerate(labels)]

    def expand_query(self, query, top_results=None):
        results = top_results or self.semantic_search(query, 3)
        words = []
        for row in results:
            words.extend(str(row["text"]).split())
        candidates = [word.lower().strip(".,;:!?()") for word in words if len(word) > 4]
        return " ".join(dict.fromkeys([query, *candidates[:8]]))

    def backend_status(self):
        return {
            "backend": self.backend,
            "model": self.model_name if self.backend == "sentence_transformer" else None,
            "transformer_requested": self.use_transformer,
            "warning": self.warning,
        }

    def save_cache(self, directory):
        """Persist run evidence; always rebuild the index from source before use."""
        if self.vectors is None:
            raise RuntimeError("Build the index before saving a cache.")
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        vectors = directory / "news_embeddings.npy"
        metadata = directory / "news_metadata.json"
        np.save(vectors, np.asarray(self.vectors))
        metadata.write_text(json.dumps(self.metadata, default=str, indent=2), encoding="utf-8")
        (directory / "README.txt").write_text(
            "Generated local retrieval cache. Rebuild it with scripts/run_phase2.py after changing the corpus or embedding model.\n",
            encoding="utf-8",
        )
        return {"vectors": str(vectors), "metadata": str(metadata), "backend": self.backend}

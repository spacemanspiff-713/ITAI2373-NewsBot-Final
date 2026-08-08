"""Multilingual embedding interface with a no-download TF-IDF fallback."""
from __future__ import annotations
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

class SemanticSearchEngine:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", use_transformer=False):
        self.model_name,self.use_transformer,self.model,self.vectorizer,self.documents,self.metadata,self.vectors=model_name,use_transformer,None,None,[],[],None
    def _encode(self,texts):
        values=[str(t or "") for t in texts]
        if self.use_transformer:
            try:
                if self.model is None:
                    from sentence_transformers import SentenceTransformer; self.model=SentenceTransformer(self.model_name)
                return self.model.encode(values,normalize_embeddings=True)
            except Exception: self.model=None
        if self.vectorizer is None: self.vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),min_df=1)
        return self.vectorizer.fit_transform(values).toarray() if not hasattr(self.vectorizer,"vocabulary_") else self.vectorizer.transform(values).toarray()
    def encode_documents(self,documents): return self._encode(documents)
    def build_index(self,documents,metadata=None):
        self.documents=[str(x or "") for x in documents]; self.metadata=list(metadata or [{} for _ in self.documents]); self.vectorizer=None if self.use_transformer else TfidfVectorizer(stop_words="english",ngram_range=(1,2),min_df=1); self.vectors=self._encode(self.documents); return self
    def semantic_search(self,query,top_k=5,filters=None):
        if self.vectors is None: raise RuntimeError("Build the index before searching.")
        q=self._encode([query])[0]; scores=cosine_similarity([q],self.vectors)[0]; pairs=[]
        for i,score in enumerate(scores):
            meta=self.metadata[i] or {}
            if filters and any(str(meta.get(k," ")).upper()!=str(v).upper() for k,v in filters.items()): continue
            pairs.append({**meta,"text":self.documents[i],"score":float(score),"index":i})
        return sorted(pairs,key=lambda row:row["score"],reverse=True)[:top_k]
    def find_similar_articles(self,article_text,top_k=5): return self.semantic_search(article_text,top_k+1)[:top_k]
    def cluster_similar_content(self,n_clusters=6):
        if self.vectors is None: raise RuntimeError("Build the index before clustering.")
        n=min(n_clusters,len(self.documents)); labels=KMeans(n_clusters=n,random_state=42,n_init=10).fit_predict(self.vectors); return [{**(self.metadata[i] or {}),"index":i,"cluster":int(label)} for i,label in enumerate(labels)]
    def expand_query(self,query,top_results=None):
        results=top_results or self.semantic_search(query,3); words=[]
        for row in results: words.extend(str(row["text"]).split())
        common=[w.lower().strip(".,;:!?()") for w in words if len(w)>4]; return " ".join(dict.fromkeys([query,*common[:8]]))

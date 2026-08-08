"""Conservative coverage comparison using translations and shared analysis outputs."""
from __future__ import annotations
from src.multilingual.translator import Translator
class CrossLingualAnalyzer:
    def __init__(self,search_engine=None,translator=None): self.search_engine=search_engine; self.translator=translator or Translator()
    def cross_lingual_similarity(self,text_a,text_b):
        if self.search_engine:
            self.search_engine.build_index([text_a,text_b]); return float(self.search_engine.semantic_search(text_a,2)[1]["score"])
        return 0.0
    def compare_entities(self,entities_a,entities_b):
        a={str(x["text"]).lower() for x in entities_a}; b={str(x["text"]).lower() for x in entities_b}; return {"overlapping_entities":sorted(a&b),"overlap_count":len(a&b)}
    def compare_sentiment(self,a,b): return {"compound_difference":float(a.get("compound",0)-b.get("compound",0)),"labels":[a.get("label"),b.get("label")]}
    def compare_coverage(self,articles_by_language):
        counts={language:len(items) for language,items in articles_by_language.items()}; return {"coverage_depth":counts,"language_specific_framing_signal":"Descriptive comparison only; this does not establish cultural conclusions."}

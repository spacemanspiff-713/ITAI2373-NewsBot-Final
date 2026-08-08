"""Lazy transformer summarization with a deterministic extractive fallback."""
from __future__ import annotations
import re
from collections import Counter

class IntelligentSummarizer:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6", use_transformer=False):
        self.model_name, self.use_transformer, self._pipeline, self.warning = model_name, use_transformer, None, None
    def _load(self):
        if not self.use_transformer: return None
        if self._pipeline is None:
            try:
                import torch
                from transformers import pipeline
                self._pipeline = pipeline("summarization", model=self.model_name, device=0 if torch.cuda.is_available() else -1)
            except Exception as exc: self.warning = f"Transformer unavailable; extractive fallback used ({type(exc).__name__})."
        return self._pipeline
    @staticmethod
    def _sentences(text): return [s.strip() for s in re.split(r"(?<=[.!?])\s+", str(text or "")) if s.strip()]
    def _extractive(self, text, max_words):
        sentences=self._sentences(text); words=re.findall(r"[A-Za-z']+", str(text).lower()); freq=Counter(word for word in words if len(word)>2)
        ranked=sorted(enumerate(sentences), key=lambda x: sum(freq[w.lower()] for w in re.findall(r"[A-Za-z']+",x[1]))/(len(x[1].split())+1), reverse=True)
        chosen=[]; count=0
        for _, sentence in sorted(ranked[:max(1,min(3,len(ranked)))]) :
            if count+len(sentence.split())<=max_words or not chosen: chosen.append(sentence); count+=len(sentence.split())
        return " ".join(chosen)
    def summarize_article(self, text, summary_type="balanced"):
        limits={"brief":45,"balanced":80,"detailed":120}; max_words=limits.get(summary_type,80); value=str(text or "").strip()
        if not value: return ""
        pipe=self._load()
        if pipe and len(value.split())>40:
            try: return pipe(value[:12000], max_length=max_words, min_length=min(25,max_words//2), do_sample=False)[0]["summary_text"]
            except Exception as exc: self.warning=f"Transformer summarization failed; extractive fallback used ({type(exc).__name__})."
        return self._extractive(value,max_words)
    def summarize_multiple_articles(self, articles, focus_topic=None):
        selected=[str(a.get("full_text") or a.get("text") or a) for a in articles]
        if focus_topic: selected=[t for t in selected if focus_topic.lower() in t.lower()] or selected
        return self.summarize_article(" ".join(selected),"detailed")
    def generate_headline(self,text):
        summary=self.summarize_article(text,"brief"); return " ".join(summary.split()[:14]).rstrip(".,;:") or "News analysis summary"
    def assess_summary_quality(self,original_text,summary,reference=None):
        original_words=max(len(str(original_text).split()),1); summary_words=len(str(summary).split()); result={"compression_ratio":summary_words/original_words,"summary_words":summary_words,"length_within_target":25<=summary_words<=120,"entity_preservation_proxy":sum(token.lower() in str(summary).lower() for token in re.findall(r"\b[A-Z][A-Za-z]+\b",str(original_text))) / max(len(re.findall(r"\b[A-Z][A-Za-z]+\b",str(original_text))),1)}
        if reference:
            try:
                from rouge_score import rouge_scorer; result["rougeL"]=rouge_scorer.RougeScorer(["rougeL"],use_stemmer=True).score(str(reference),str(summary))["rougeL"].fmeasure
            except Exception: pass
        return result

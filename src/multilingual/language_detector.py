"""Deterministic language detection with an uncertainty-aware short-text rule."""
from __future__ import annotations
from langdetect import DetectorFactory, detect_langs
DetectorFactory.seed=42
LANGUAGE_NAMES={"en":"English","es":"Spanish","fr":"French","de":"German"}
class LanguageDetector:
    def detect_language(self,text):
        value=str(text or "").strip()
        if len(value)<12: return {"language":"unknown","language_name":"Unknown","confidence":0.0,"is_supported":False,"warning":"Text is too short for reliable detection."}
        try:
            candidate=detect_langs(value)[0]; code=candidate.lang; confidence=float(candidate.prob)
            return {"language":code,"language_name":LANGUAGE_NAMES.get(code,code),"confidence":confidence,"is_supported":code in LANGUAGE_NAMES,"warning":None if confidence>=.70 else "Low-confidence language estimate."}
        except Exception: return {"language":"unknown","language_name":"Unknown","confidence":0.0,"is_supported":False,"warning":"Language could not be determined."}

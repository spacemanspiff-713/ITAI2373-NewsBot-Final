"""Lazy, no-key translation adapter with explicit availability and provenance."""

from __future__ import annotations

from functools import lru_cache


DEMO_TRANSLATIONS = {
    "La empresa tecnológica anunció una nueva herramienta de inteligencia artificial para pequeñas empresas.": "The technology company announced a new artificial intelligence tool for small businesses.",
    "La ciudad anunció nuevas medidas de salud pública después de una ola de calor.": "The city announced new public health measures after a heat wave.",
    "L'entreprise technologique a annoncé un nouvel outil d'intelligence artificielle pour les petites entreprises.": "The technology company announced a new artificial intelligence tool for small businesses.",
    "La ville a annoncé de nouvelles mesures de santé publique après une vague de chaleur.": "The city announced new public health measures after a heat wave.",
}


class Translator:
    """Support Spanish/French-to-English demos without a required paid API.

    ``auto`` uses the authored paired demonstrations first, then a locally
    cached MarianMT model if available, then the optional network translator.
    ``marian`` explicitly permits a first-run model download; it is never the
    default because the core project must work without a network connection.
    """

    MARIAN_MODELS = {
        ("es", "en"): "Helsinki-NLP/opus-mt-es-en",
        ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    }

    def __init__(self, backend="auto"):
        self.backend = backend

    @staticmethod
    @lru_cache(maxsize=2)
    def _load_marian(model_name, local_files_only):
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

        tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=local_files_only)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, local_files_only=local_files_only)
        return pipeline("translation", model=model, tokenizer=tokenizer)

    def _marian_translate(self, value, source_language, target_language, allow_download):
        model = self.MARIAN_MODELS.get((source_language, target_language))
        if not model:
            return None
        try:
            pipe = self._load_marian(model, not allow_download)
            return {
                "translation": pipe(value, max_length=256)[0]["translation_text"],
                "available": True,
                "backend": "marianmt",
                "warning": "Machine translation can lose nuance; verify sensitive or high-stakes text.",
            }
        except Exception:
            return None

    def translate_text(self, text, target_language="en", source_language=None):
        value = str(text or "")
        if target_language == source_language:
            return {"translation": value, "available": True, "backend": "identity", "warning": None}
        if value in DEMO_TRANSLATIONS and target_language == "en":
            return {"translation": DEMO_TRANSLATIONS[value], "available": True, "backend": "authored_demo", "warning": None}
        if self.backend in {"auto", "marian_local", "marian"}:
            translated = self._marian_translate(value, source_language, target_language, self.backend == "marian")
            if translated:
                return translated
        if self.backend in {"auto", "deep_translator"}:
            try:
                from deep_translator import GoogleTranslator

                return {
                    "translation": GoogleTranslator(source=source_language or "auto", target=target_language).translate(value),
                    "available": True,
                    "backend": "deep_translator",
                    "warning": "Network translation; verify sensitive or high-stakes text.",
                }
            except Exception:
                pass
        return {
            "translation": None,
            "available": False,
            "backend": "unavailable",
            "warning": "Translation is unavailable locally for this text. Use an authored demo, a cached MarianMT model, explicit NEWSBOT_TRANSLATION_BACKEND=marian, or the optional network backend.",
        }

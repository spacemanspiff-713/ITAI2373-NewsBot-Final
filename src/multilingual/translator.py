"""Optional translation adapter; core operation never needs a paid service."""
from __future__ import annotations
DEMO_TRANSLATIONS={
"La empresa tecnológica anunció una nueva herramienta de inteligencia artificial para pequeñas empresas.":"The technology company announced a new artificial intelligence tool for small businesses.",
"La ciudad anunció nuevas medidas de salud pública después de una ola de calor.":"The city announced new public health measures after a heat wave.",
"L'entreprise technologique a annoncé un nouvel outil d'intelligence artificielle pour les petites entreprises.":"The technology company announced a new artificial intelligence tool for small businesses.",
"La ville a annoncé de nouvelles mesures de santé publique après une vague de chaleur.":"The city announced new public health measures after a heat wave."}
class Translator:
    def __init__(self,backend="auto"): self.backend=backend
    def translate_text(self,text,target_language="en",source_language=None):
        value=str(text or "")
        if target_language==source_language: return {"translation":value,"available":True,"backend":"identity","warning":None}
        if value in DEMO_TRANSLATIONS and target_language=="en": return {"translation":DEMO_TRANSLATIONS[value],"available":True,"backend":"authored_demo","warning":None}
        if self.backend in {"auto","deep_translator"}:
            try:
                from deep_translator import GoogleTranslator
                return {"translation":GoogleTranslator(source=source_language or "auto",target=target_language).translate(value),"available":True,"backend":"deep_translator","warning":"Network translation; verify sensitive or high-stakes text."}
            except Exception: pass
        return {"translation":None,"available":False,"backend":"unavailable","warning":"Translation is unavailable locally for this text."}

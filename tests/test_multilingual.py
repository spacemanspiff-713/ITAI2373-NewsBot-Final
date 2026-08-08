from src.multilingual.language_detector import LanguageDetector
from src.multilingual.translator import Translator
from src.multilingual.cross_lingual_analyzer import CrossLingualAnalyzer
from src.language_models.embeddings import SemanticSearchEngine

def test_language_detection_and_demo_translation():
 detector=LanguageDetector(); assert detector.detect_language("This is a clear English news sentence with enough words.")["language"]=="en"; assert detector.detect_language("La empresa tecnológica anunció una nueva herramienta de inteligencia artificial para pequeñas empresas.")["language"]=="es"; assert detector.detect_language("bonjour")["confidence"]==0.0
 result=Translator().translate_text("La empresa tecnológica anunció una nueva herramienta de inteligencia artificial para pequeñas empresas.","en","es"); assert result["available"] and "technology company" in result["translation"].lower()

def test_cross_language_comparison_is_careful():
 analyzer=CrossLingualAnalyzer(SemanticSearchEngine()); assert "coverage_depth" in analyzer.compare_coverage({"en":["a"],"es":["b"]})

def test_cross_language_similarity_preserves_translation_provenance():
 analyzer=CrossLingualAnalyzer(SemanticSearchEngine())
 result=analyzer.cross_lingual_similarity("La empresa tecnológica anunció una nueva herramienta de inteligencia artificial para pequeñas empresas.","The technology company announced a new artificial intelligence tool for small businesses.")
 assert result["similarity"] >= 0 and result["left_translation"]["available"]

from src.language_models.embeddings import SemanticSearchEngine
from src.language_models.summarizer import IntelligentSummarizer

def test_extractive_summary_and_quality_metrics():
 text="The company announced a product launch. Investors welcomed the new software platform. The launch begins next week."; summary=IntelligentSummarizer().summarize_article(text); assert summary; assert "compression_ratio" in IntelligentSummarizer().assess_summary_quality(text,summary)

def test_semantic_search_fallback_returns_ranked_results():
 engine=SemanticSearchEngine().build_index(["artificial intelligence software", "football team championship"],[{"article_id":1},{"article_id":2}]); assert engine.semantic_search("software intelligence",1)[0]["article_id"]==1

def test_semantic_search_handles_very_short_input_without_crashing():
 engine=SemanticSearchEngine().build_index(["a", "b"],[{"article_id":1},{"article_id":2}])
 assert len(engine.semantic_search("a", 2))==2

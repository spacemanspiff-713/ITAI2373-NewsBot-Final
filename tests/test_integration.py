from config import NewsBot2Config
from src.system import NewsBot2IntegratedSystem

def test_comprehensive_analysis_has_required_keys_and_batch_limit():
 system=NewsBot2IntegratedSystem(NewsBot2Config(max_batch_size=2)).fit()
 result=system.comprehensive_analysis("Apple announced a new artificial intelligence product for software developers in California.")
 assert {"classification","sentiment","entities","relationships","topics","summary","semantic_neighbors","enhancements","language","translation","statistics"}.issubset(result)
 assert len(system.batch_analysis(["A technology article."]))==1
 try: system.batch_analysis(["one","two","three"])
 except ValueError: pass
 else: raise AssertionError("Batch limit should be enforced")

def test_component_failure_is_isolated():
 system=NewsBot2IntegratedSystem().fit(); system.summarizer.summarize_article=lambda _: (_ for _ in ()).throw(RuntimeError("simulated")); result=system.comprehensive_analysis("A software company released a product."); assert result["classification"] is not None and result["summary"] is None and result["warnings"]

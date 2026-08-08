"""Evidence-grounded, non-fact-checking content enhancement."""
from __future__ import annotations
from collections import Counter

class ContentEnhancer:
    def __init__(self, search_engine=None): self.search_engine=search_engine
    def enhance(self,analysis):
        entities=analysis.get("entities",[]); names=[item["text"] for item in entities]; neighbors=analysis.get("semantic_neighbors",[])
        return {"key_entities":names[:10],"related_articles":[{"article_id":row.get("article_id"),"title":row.get("title",row.get("text","")[:80]),"score":row.get("score")} for row in neighbors[:5]],"topic_context":analysis.get("topics",[])[:3],"trend_context":analysis.get("trend_context",{}),"coverage_gaps":["Compare language coverage and source diversity before drawing conclusions."],"corroboration":self.cross_reference_facts(analysis.get("text",""),neighbors)}
    def cross_reference_facts(self,text,neighbors=None):
        snippets=[str(item.get("text","") or item.get("full_text","") )[:180] for item in (neighbors or [])]
        return {"signal":"Internal corpus corroboration only; this is not an independent fact-check.","matching_articles":len(snippets),"snippets":snippets[:3]}
    def generate_insights(self,articles):
        categories=Counter(str(a.get("category","Unknown")) for a in articles); return {"article_count":len(articles),"category_distribution":dict(categories),"note":"Descriptive corpus insight; not causal evidence."}

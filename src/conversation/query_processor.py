from __future__ import annotations
import re
from src.conversation.intent_classifier import IntentClassifier
CATEGORIES={"politics":"POLITICS","entertainment":"ENTERTAINMENT","business":"BUSINESS","sports":"SPORTS","tech":"TECH","technology":"TECH","wellness":"WELLNESS"}
class QueryProcessor:
 def __init__(self,intent_classifier=None): self.intent_classifier=intent_classifier or IntentClassifier()
 def parse(self,query,dataset_max_date=None,context=None):
  value=str(query); low=value.lower(); intent=self.intent_classifier.classify_intent(value); params={}
  for word,category in CATEGORIES.items():
   if re.search(r"\b"+re.escape(word)+r"\b",low): params["category"]=category; break
  for sentiment in ("positive","negative","neutral"):
   if sentiment in low: params["sentiment"]=sentiment
  count=re.search(r"\b(\d+)\b",low)
  if count: params["count"]=min(int(count.group(1)),20)
  if "this week" in low and dataset_max_date is not None: params["timeframe_note"]=f"'this week' is resolved relative to the dataset maximum date ({dataset_max_date})."
  entities=re.findall(r"\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\b",value); params["entities"]=entities
  if context and not params.get("category") and context.get("last_filters",{}).get("category"): params["category"]=context["last_filters"]["category"]; params["inherited_category"]=True
  return {**intent,"parameters":params}

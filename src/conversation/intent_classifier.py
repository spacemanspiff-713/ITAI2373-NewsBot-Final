from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
EXAMPLES={"search":["show tech news","find articles about apple","recent business coverage"],"summarize":["summarize politics coverage","give me a summary","what happened in sports"],"sentiment":["show negative news","what is the sentiment","positive technology stories"],"topic_trend":["how has technology changed over time","topic trends","emerging topics"],"entity_lookup":["find articles about Google","who is mentioned","look up Apple"],"compare":["compare Apple and Google coverage","compare tech and business","difference between categories"],"similar_articles":["find similar articles","articles like this paragraph","related stories"],"help":["help","what can you do","how does this work"]}
class IntentClassifier:
 def __init__(self):
  x=[text for intent,texts in EXAMPLES.items() for text in texts]; y=[intent for intent,texts in EXAMPLES.items() for _ in texts]; self.model=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2))), ("classifier",LogisticRegression(max_iter=1000,random_state=42))]).fit(x,y)
 def classify_intent(self,query):
  probs=self.model.predict_proba([str(query)])[0]; index=probs.argmax(); return {"intent":self.model.classes_[index],"confidence":float(probs[index]),"fallback":bool(probs[index]<.35)}

from __future__ import annotations
class ResponseGenerator:
 def respond(self,query_data,dataframe,search_engine=None):
  params=query_data["parameters"]; filtered=dataframe.copy()
  if params.get("category"): filtered=filtered[filtered["category"]==params["category"]]
  if params.get("entities"):
   pattern="|".join(params["entities"]); filtered=filtered[filtered["full_text"].str.contains(pattern,case=False,na=False)]
  rows=filtered.sort_values("date",ascending=False).head(params.get("count",5)); titles=[{"article_id":int(row.article_id),"title":row.title,"category":row.category} for row in rows.itertuples()]
  excluded={"entities","count","inherited_category"}; applied=", ".join(f"{k}={v}" for k,v in params.items() if k not in excluded) or "no filters"; return {"response":f"Found {len(filtered)} matching historical articles with {applied}.","results":titles,"applied_filters":params,"next_actions":["Ask for a summary, sentiment, trend, or related articles."]}

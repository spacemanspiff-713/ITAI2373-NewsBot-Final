from __future__ import annotations
import os
from flask import Flask, jsonify, render_template, request
from src.system import NewsBot2IntegratedSystem
_system=None
def get_system():
 global _system
 if _system is None: _system=NewsBot2IntegratedSystem().fit()
 return _system
def create_app():
 app=Flask(__name__); app.config.update(SECRET_KEY=os.getenv("NEWSBOT_SECRET_KEY","development-only-change-me"),MAX_CONTENT_LENGTH=200_000)
 @app.get("/")
 def dashboard(): return render_template("dashboard.html")
 @app.post("/analyze")
 @app.post("/api/analyze")
 def analyze():
  text=(request.get_json(silent=True) or request.form).get("text","")
  if not 20<=len(text)<=20000: return jsonify({"error":"Provide 20–20,000 characters."}),400
  return jsonify(get_system().comprehensive_analysis(text))
 @app.get("/query")
 @app.post("/api/query")
 def query():
  value=(request.get_json(silent=True) or request.values).get("query","")
  if not value: return jsonify({"error":"Provide a query."}),400
  return jsonify(get_system().query_interface(value))
 @app.post("/batch")
 def batch(): return jsonify(get_system().batch_analysis((request.get_json(silent=True) or {}).get("articles",[])))
 @app.get("/health")
 def health(): return jsonify({"status":"ok","service":"NewsBot Intelligence System 2.0"})
 return app

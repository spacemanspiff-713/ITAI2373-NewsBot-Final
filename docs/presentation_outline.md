# NewsBot 2.0 Presentation Outline and Speaker Notes

Target length: 15 minutes plus Q&A. The generated presentation uses these 18 slides and keeps the live demo focused on reproducible evidence.

1. **Title — NewsBot Intelligence System 2.0**
   Introduce the independently completed capstone, course, and Jason Trimble.
2. **The research problem**
   Historical news coverage is hard to triage quickly; automated output must not be mistaken for truth.
3. **Midterm → final evolution**
   Show the preserved midterm foundation and the final modules added around it.
4. **System architecture**
   Walk through local data, modular NLP, integrated system, evidence artifacts, and UI.
5. **Dataset and responsible scope**
   1,800 balanced HuffPost records, six categories, historical headline/description text, separate multilingual demo.
6. **Advanced classification**
   Explain baseline versus enhanced candidates, probabilities, alternatives, macro F1, and calibration.
7. **Topic discovery and evolution**
   Show LDA/NMF figures; explain that NMF was selected by lexical distinctiveness, not a human-truth score.
8. **Sentiment and entity graph**
   Explain VADER trend output and why co-occurrence edges do not prove real relationships.
9. **Language understanding**
   Demonstrate extractive fallback and opt-in DistilBART path; distinguish a generated summary from verified reporting.
10. **Semantic retrieval and enhancement**
    Explain related local records, query expansion, internal corroboration guardrail, and retrieval evaluation.
11. **Multilingual demonstration**
    Show Spanish/French pairs, language detection, translation provenance, and careful framing language.
12. **Conversational interface**
    Show intent/slot evaluation, historical time interpretation, and follow-up category context.
13. **Live demo: article analysis**
    Paste a fresh short article in Streamlit and narrate classification, sentiment, entities, summary, and warnings.
14. **Live demo: query the corpus**
    Query “Show me tech news,” then “What about negative ones?” Show cited local records.
15. **Evaluation results**
    Report 0.714 accuracy / 0.712 macro F1, topic diagnostics, retrieval, multilingual demo, and conversation results with their sample sizes.
16. **Business value and ROI assumptions**
    Explain first-pass research value and the transparent time-saved formula; emphasize no audited savings claim.
17. **Limitations and ethics**
    Historical/source bias, model error, translation loss, privacy, confidence ≠ truth, similarity ≠ fact checking.
18. **Contribution summary, future work, and Q&A**
    Summarize Jason’s documented work and invite questions about reproducibility or limits.

## Demo script

Before presenting, run tests and the Phase 2 evaluation script, start Streamlit, and have the Command Center open. Begin with the measured corpus context. Use a newly written technology article rather than a training record. Then query the corpus and run the follow-up. Avoid claims of live coverage or factual verification. If the network/model path is unavailable, show the runtime backend status and explain the tested fallback—do not hide it.

## Speaker-note guidance

Use about 35–45 seconds per content slide and roughly 2–3 minutes for the live demo. Point to artifact filenames and metric sample sizes. The strongest answer to a technical question is a reproducible command, a cited local result, or an explicit limitation. Do not claim that a multilingual pair proves cultural understanding, that a graph edge proves a relationship, or that a model score determines article truth.

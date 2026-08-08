# User Guide — NewsBot Intelligence System 2.0

## Start the dashboard

From the repository root, install requirements and run:

```bash
./.venv/bin/streamlit run streamlit_app.py
```

Open the local address shown by Streamlit. The Command Center describes the corpus and measured results. The application works from a historical local dataset; it does not search live news.

## Analyze one article

Open **Article Intelligence**, paste at least 20 characters, and choose **Analyze article**. The result includes:

- a likely category and confidence score;
- sentiment and named entities;
- topic words, heuristic relationships, and similar local records;
- a summary and evidence-grounded enhancement;
- language/translation availability and component warnings.

Confidence is a routing estimate, not a truth score. A low-confidence prediction deserves human review. Entity relationships describe local text patterns and do not establish a real relationship.

## Query the corpus

Open **Query the Corpus** and try:

```text
Show me tech news
Summarize politics coverage
Show negative technology stories
How have topic trends changed?
Compare tech and business
Find articles about Apple
```

The system cites matching local titles and IDs. Try a follow-up such as “What about negative ones?” after a category search; it carries the previous category only when you do not provide a new one. Phrases such as “this week” mean the last week relative to the dataset’s most recent historical date, which is stated in the response.

## Batch, visual, and source views

Use **Batch Studio** to separate short pieces with a blank line. The configured cap protects responsiveness. Download result JSON when you need to cite the exact output. **Visual Evidence** shows reproducible figures from the evaluation script. **Data Explorer** lets you filter the underlying records before interpreting a pattern.

## Multilingual demonstration

The main corpus is English. Spanish and French examples are authored paired demonstrations. A translation result states its backend: authored demo, MarianMT, optional network translator, or unavailable. Translation and cross-language similarity are aids to exploration, not a claim of equivalent cultural meaning or factual agreement.

## Troubleshooting and FAQ

**The app says a component is unavailable.** Read the warning; the remaining components should still work. Install requirements and the spaCy model, then retry.

**Why is the summary extractive?** The default is reliable without downloading a large model. Set `NEWSBOT_ENABLE_TRANSFORMERS=1` to permit the lazy pretrained paths. The runtime output identifies the active backend.

**Why did a query return no records?** Broaden the category, remove a named entity, or use fewer keywords. The application searches only the preserved historical sample.

**Can I use the result as fact-checking?** No. Read cited articles and use independent reporting or trusted verification sources.

"""Presentation-ready Streamlit frontend for NewsBot Intelligence System 2.0."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_processing.data_validator import load_news_dataset
from src.system import NewsBot2IntegratedSystem


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "data" / "results"
NAVIGATION = ["Command Center", "Article Intelligence", "Query the Corpus", "Batch Studio", "Visual Evidence", "Data Explorer", "Project Brief"]

st.set_page_config(
    page_title="NewsBot 2.0 | Intelligence System",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """<style>
        :root {--ink:#101828;--muted:#667085;--canvas:#f7f8fc;--panel:#ffffff;--line:#e5e9f0;--violet:#6d4aff;--cyan:#0bb6c9;--lime:#b7e553;--navy:#152238;}
        .stApp {background:radial-gradient(circle at 92% -10%,#e8e0ff 0,transparent 31%),radial-gradient(circle at 3% 17%,#dff9f4 0,transparent 24%),var(--canvas);color:var(--ink)}
        [data-testid="stHeader"]{background:transparent}.block-container{max-width:1400px;padding-top:1.25rem;padding-bottom:3rem}
        [data-testid="stSidebar"]{background:linear-gradient(180deg,#121d31 0%,#192b46 100%)}
        [data-testid="stSidebar"] *{color:#edf2f8!important}[data-testid="stSidebar"] .stRadio label{padding:.25rem .35rem;border-radius:8px;margin:.08rem 0}
        [data-testid="stSidebar"] .stRadio label:hover{background:rgba(255,255,255,.08)}
        h1{font-size:2.75rem!important;letter-spacing:-.055em!important;line-height:1.02!important;margin-bottom:.6rem!important}h2{letter-spacing:-.035em!important}
        .eyebrow{font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#635bff;margin-bottom:.65rem}.lede{font-size:1.05rem;line-height:1.65;color:#566174;max-width:48rem}.hero{border:1px solid rgba(103,84,255,.13);border-radius:28px;padding:2.5rem 2.65rem;background:linear-gradient(120deg,rgba(255,255,255,.96),rgba(248,246,255,.9));box-shadow:0 24px 60px rgba(31,42,68,.09);position:relative;overflow:hidden}.hero:after{content:"";position:absolute;right:-6rem;top:-9rem;width:25rem;height:25rem;border-radius:50%;border:46px solid rgba(11,182,201,.10)}
        .metric-card{background:rgba(255,255,255,.82);border:1px solid var(--line);border-radius:18px;padding:1.15rem 1.2rem;min-height:120px;box-shadow:0 8px 24px rgba(15,23,42,.035)}.metric-label{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:#687386;font-weight:800}.metric-value{font-size:1.75rem;font-weight:800;letter-spacing:-.04em;margin:.35rem 0;color:#16233a}.metric-note{font-size:.78rem;color:#7a8494}
        .section-kicker{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#0b8795}.panel-note{border-left:3px solid var(--violet);background:#f7f5ff;border-radius:0 12px 12px 0;padding:.85rem 1rem;color:#4d4b63;font-size:.9rem}.chip{display:inline-block;padding:.32rem .55rem;margin:0 .35rem .35rem 0;border-radius:999px;background:#edf9fa;color:#087d88;font-size:.75rem;font-weight:700}.story-card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:1rem 1.1rem;margin-bottom:.65rem;box-shadow:0 4px 14px rgba(15,23,42,.025)}
        .stButton>button{border:0!important;border-radius:10px!important;background:linear-gradient(110deg,#6d4aff,#4c7cff)!important;color:white!important;font-weight:750!important;padding:.55rem 1rem!important;box-shadow:0 7px 16px rgba(91,75,255,.25)}.stDownloadButton>button{border-radius:10px!important}.stTextArea textarea,.stTextInput input{border-radius:12px!important;border-color:#d8dee9!important;background:#fff!important}.stTabs [data-baseweb="tab"]{font-weight:700}.stTabs [aria-selected="true"]{color:#5d45e8!important}.stDataFrame{border-radius:12px;overflow:hidden;border:1px solid var(--line)}
        </style>""",
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner="Preparing the intelligence engine…")
def get_system() -> NewsBot2IntegratedSystem:
    return NewsBot2IntegratedSystem().fit()


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    return load_news_dataset(ROOT / "data" / "processed" / "newsbot_dataset_sample.csv")


@st.cache_data(show_spinner=False)
def get_metrics() -> dict:
    path = RESULTS / "metrics" / "evaluation_summary.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def page_intro(eyebrow: str, title: str, copy: str) -> None:
    st.markdown(f'<div class="section-kicker">{eyebrow}</div><h2>{title}</h2><p class="lede">{copy}</p>', unsafe_allow_html=True)


def metric_card(column, label: str, value: str, note: str) -> None:
    column.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)


def command_center() -> None:
    metrics, dataframe = get_metrics(), get_data()
    classification = metrics.get("classification", {})
    topic = metrics.get("topic_model", {})
    st.markdown("""<div class="hero"><div class="eyebrow">ITAI 2373 · FINAL PROJECT</div><h1>The Signal Desk</h1><p class="lede">NewsBot Intelligence System 2.0 turns a completed midterm classifier into a transparent, evidence-led research workspace for historical news coverage.</p><div><span class="chip">6 coverage domains</span><span class="chip">topic evolution</span><span class="chip">multilingual demo</span><span class="chip">grounded query interface</span></div></div>""", unsafe_allow_html=True)
    st.write("")
    columns = st.columns(4)
    metric_card(columns[0], "Historical corpus", f"{len(dataframe):,}", "Balanced HuffPost records")
    metric_card(columns[1], "Routing quality", f"{classification.get('macro_f1', 0):.3f}", "Held-out macro F1")
    metric_card(columns[2], "Discovery model", topic.get("selected", "N/A").upper(), "Selected topic approach")
    metric_card(columns[3], "Search evaluation", f"{metrics.get('semantic_search', {}).get('precision_at_1', 0):.0%}", "Authored Precision@1 set")
    overview, evolution = st.tabs(["Coverage overview", "From midterm to final"])
    with overview:
        left, right = st.columns([1.1, .9])
        with left:
            counts = dataframe["category"].value_counts().sort_values()
            figure = px.bar(x=counts.values, y=counts.index, orientation="h", text=counts.values, color=counts.index, color_discrete_sequence=["#6d4aff", "#0bb6c9", "#b7e553", "#ffb04f", "#ff7676", "#7795f8"])
            figure.update_layout(title="Balanced coverage by category", showlegend=False, height=350, margin=dict(l=0, r=0, t=50, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Articles", yaxis_title="")
            st.plotly_chart(figure, use_container_width=True)
        with right:
            st.markdown("<div class='panel-note'><b>Research guardrail.</b><br>Every output is based on a historical local corpus. Confidence supports routing; it does not establish truth, factuality, or causation.</div>", unsafe_allow_html=True)
            st.write("")
            st.markdown("#### Evidence at a glance")
            st.write(f"• **{topic.get('selected', 'NMF').upper()}** was selected for topic distinctiveness.\n• Entity links represent **same-sentence corpus co-occurrence**.\n• Semantic search supports related-item discovery, not fact verification.")
    with evolution:
        st.markdown("### A deliberate evolution, not a replacement")
        left, right = st.columns(2)
        with left:
            st.markdown("**Midterm foundation**\n\nTF-IDF classification · VADER sentiment · spaCy NER · saved evaluation visuals · Streamlit dashboard")
        with right:
            st.markdown("**2.0 extension**\n\nLDA/NMF trends · entity graph · semantic retrieval · summarization fallback · multilingual demo · conversational context")


def article_intelligence() -> None:
    page_intro("Live analysis", "Put a fresh article under the lens", "Run the integrated pipeline against new text. Each panel shows its own evidence and warnings so a single unavailable component does not hide the rest of the analysis.")
    text = st.text_area("Article text", value="A technology company announced a new artificial intelligence product for small businesses in California. Executives said the release will support safer software development and new hiring.", height=180, max_chars=20_000, label_visibility="collapsed")
    if st.button("Analyze article ✦", type="primary"):
        if len(text.strip()) < 20:
            st.error("Please provide at least 20 characters for a meaningful analysis.")
            return
        with st.spinner("Tracing topics, entities, tone, and related coverage…"):
            result = get_system().comprehensive_analysis(text)
        classification, sentiment = result.get("classification") or {}, result.get("sentiment") or {}
        columns = st.columns(4)
        metric_card(columns[0], "Primary route", classification.get("primary_category", "N/A"), classification.get("content_family", ""))
        metric_card(columns[1], "Confidence", f"{classification.get('confidence', 0):.1%}", "Manual review below threshold")
        metric_card(columns[2], "Coverage tone", sentiment.get("label", "N/A").title(), f"VADER {sentiment.get('compound', 0):+.2f}")
        metric_card(columns[3], "Processing time", f"{result['statistics']['processing_seconds']:.2f}s", f"{result['statistics']['word_count']} words")
        summary, evidence, context = st.tabs(["Executive readout", "Entities & relationships", "Topic & related context"])
        with summary:
            st.markdown("### Summary")
            st.write(result.get("summary") or "No summary was returned.")
            st.markdown("### Grounded enhancement")
            st.json(result.get("enhancements", {}), expanded=False)
        with evidence:
            entities = pd.DataFrame(result.get("entities") or [])
            st.dataframe(entities if not entities.empty else pd.DataFrame({"Notice": ["No supported entities were detected."]}), use_container_width=True, hide_index=True)
            if result.get("relationships"):
                st.caption("Relationship labels are transparent heuristics; co-occurrence is not a proven real-world relationship.")
                st.dataframe(pd.DataFrame(result["relationships"]), use_container_width=True, hide_index=True)
        with context:
            st.dataframe(pd.DataFrame(result.get("topics") or []), use_container_width=True, hide_index=True)
            neighbors = pd.DataFrame(result.get("semantic_neighbors") or [])
            if not neighbors.empty:
                st.markdown("### Related local coverage")
                st.dataframe(neighbors[[column for column in ["article_id", "title", "category", "score"] if column in neighbors]], use_container_width=True, hide_index=True)
        if result.get("warnings"):
            st.warning(" · ".join(result["warnings"]))
        st.download_button("Download analysis JSON", json.dumps(result, indent=2), "newsbot_analysis.json", "application/json")


def query_corpus() -> None:
    page_intro("Conversational research", "Ask the corpus a question", "Explore historical coverage in plain language. Try “Show me tech news,” then ask “What about negative ones?” to demonstrate follow-up context.")
    query = st.text_input("Query", value="Show me tech news", label_visibility="collapsed")
    if st.button("Search the corpus", type="primary"):
        result = get_system().query_interface(query)
        st.markdown(f"<div class='panel-note'>{result['response']}</div>", unsafe_allow_html=True)
        note = result["intent"]["parameters"].get("timeframe_note")
        if note: st.caption(note)
        records = result.get("results", [])
        if records:
            for item in records:
                st.markdown(f"<div class='story-card'><b>{item['title']}</b><br><span class='caption'>#{item['article_id']} · {item['category']}</span></div>", unsafe_allow_html=True)
        else:
            st.info("No matching local records were found. Try a broader category or keyword.")


def batch_studio() -> None:
    page_intro("Batch studio", "Compare several pieces at once", "Separate articles with a blank line. The local batch cap protects responsiveness and makes each result easy to inspect.")
    raw = st.text_area("Articles", placeholder="Article one…\n\nArticle two…", height=240, label_visibility="collapsed")
    if st.button("Run batch analysis"):
        items = [item.strip() for item in raw.split("\n\n") if item.strip()]
        try:
            results = get_system().batch_analysis(items)
            table = pd.DataFrame([{"Category": (item.get("classification") or {}).get("primary_category"), "Confidence": (item.get("classification") or {}).get("confidence"), "Sentiment": (item.get("sentiment") or {}).get("label"), "Words": item["statistics"]["word_count"]} for item in results])
            st.dataframe(table.style.format({"Confidence": "{:.1%}"}), use_container_width=True, hide_index=True)
            st.download_button("Download batch JSON", json.dumps(results, indent=2), "newsbot_batch.json", "application/json")
        except ValueError as exc:
            st.error(str(exc))


def visual_evidence() -> None:
    page_intro("Research outputs", "Visual evidence, not decoration", "Every image below is generated by the reproducible evaluation pipeline and can be used in notebooks, the technical report, and your presentation.")
    figures = sorted((RESULTS / "figures").glob("*.png"))
    selected = st.selectbox("Featured visualization", figures, format_func=lambda path: path.stem.replace("_", " ").title())
    st.image(str(selected), use_container_width=True)
    with st.expander("Browse the full visual library"):
        columns = st.columns(3)
        for index, path in enumerate(figures):
            columns[index % 3].image(str(path), caption=path.stem.replace("_", " ").title(), use_container_width=True)


def explorer() -> None:
    page_intro("Source transparency", "Inspect the records behind the metrics", "Filter the exact historical sample used for the final system. This is an important safeguard against presenting model output without its source context.")
    frame = get_data()
    first, second, third = st.columns([1.2, 1, 1])
    with first: categories = st.multiselect("Categories", sorted(frame.category.unique()), default=sorted(frame.category.unique()))
    with second: years = st.slider("Date range", int(frame.date.dt.year.min()), int(frame.date.dt.year.max()), (int(frame.date.dt.year.min()), int(frame.date.dt.year.max())))
    with third: keyword = st.text_input("Keyword")
    shown = frame[frame.category.isin(categories) & frame.date.dt.year.between(*years)]
    if keyword: shown = shown[shown.full_text.str.contains(keyword, case=False, na=False)]
    st.caption(f"{len(shown):,} matching records")
    st.dataframe(shown[["date", "category", "title", "authors", "link"]].sort_values("date", ascending=False), use_container_width=True, hide_index=True)


def project_brief() -> None:
    page_intro("Presentation notes", "What makes this a credible final project", "The interface supports the capstone story; the reusable modules, notebooks, tests, outputs, and documentation remain the assessed core.")
    st.markdown("### Demonstration sequence")
    st.markdown("1. Start at **Command Center** to establish the data and measured results.\n2. Analyze a new article to show the components working together.\n3. Query the historical corpus and demonstrate a follow-up.\n4. Open **Visual Evidence** for evaluation-backed charts.\n5. End with the limitations and ethics discussion.")
    st.markdown("### Essential limitations")
    st.warning("Historical English-dominant dataset · headline/description records rather than full articles · confidence is not truth · sentiment and NER can be wrong · semantic similarity is not factual agreement · internal corroboration is not fact-checking.")


def main() -> None:
    inject_styles()
    st.sidebar.markdown("## ✦ NewsBot 2.0\n**INTELLIGENCE SYSTEM**\n\nA polished continuation of the midterm dashboard.")
    page = st.sidebar.radio("Workspace", NAVIGATION, label_visibility="collapsed")
    st.sidebar.markdown("---\n**Historical corpus**\n1,800 balanced HuffPost records\n\n**Built for**\nITAI 2373 Final Project")
    pages = {"Command Center": command_center, "Article Intelligence": article_intelligence, "Query the Corpus": query_corpus, "Batch Studio": batch_studio, "Visual Evidence": visual_evidence, "Data Explorer": explorer, "Project Brief": project_brief}
    pages[page]()


if __name__ == "__main__":
    main()

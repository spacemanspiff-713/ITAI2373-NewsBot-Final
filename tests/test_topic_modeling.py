import numpy as np

from src.analysis.topic_modeler import TopicDiscoveryEngine


def test_lda_and_nmf_fit_and_article_distribution_is_valid() -> None:
    documents = [
        "technology software computer data", "technology artificial intelligence computer",
        "sports team game score", "sports player team match",
        "health wellness doctor sleep", "health exercise wellness doctor",
    ]
    engine = TopicDiscoveryEngine(n_topics=2).fit_topics(documents, ["2022-01-01"] * 6)
    assert engine.get_topic_words(0)
    topics = engine.get_article_topics("technology software and computer")
    assert len(topics) == 2
    assert np.isclose(sum(item["probability"] for item in topics), 1.0)
    assert {row["model"] for row in engine.compare_models()} == {"lda", "nmf"}

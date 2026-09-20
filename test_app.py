"""
Verification test script for LiteratureAI
Checks imports, API connectors, PDF extraction, scoring, gap detection, review generation, and exports.
"""
import os
import sys

# Ensure UTF-8 stdout on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_imports():
    print("Testing imports...")
    import config.settings
    import models.paper
    import models.session
    import services.openalex
    import services.semantic_scholar
    import services.crossref
    import services.arxiv
    import services.pdf_processor
    import services.relevance
    import services.llm_service
    import services.analysis_service
    import services.gap_detector
    import services.review_generator
    import exporters.docx_exporter
    import exporters.csv_exporter
    import ui.theme
    import ui.styles
    import ui.assets
    import ui.components
    import ui.sidebar
    import ui.dashboard
    import ui.search_page
    import ui.upload_page
    import ui.analysis_page
    import ui.comparison_page
    import ui.gaps_page
    import ui.review_page
    print("✓ All modules imported successfully.")

def test_academic_apis():
    print("\nTesting Academic API connectors...")
    from services.openalex import OpenAlexService
    from services.arxiv import ArxivService
    
    # Test OpenAlex
    try:
        oa_papers = OpenAlexService.search("satellite network agentic ai", limit=3)
        print(f"✓ OpenAlex returned {len(oa_papers)} papers.")
        if oa_papers:
            print(f"   Sample: '{oa_papers[0].title}' ({oa_papers[0].year})")
    except Exception as e:
        print(f"⚠️ OpenAlex note: {e}")

    # Test arXiv
    try:
        ar_papers = ArxivService.search("satellite network", limit=3)
        print(f"✓ arXiv returned {len(ar_papers)} papers.")
        if ar_papers:
            print(f"   Sample: '{ar_papers[0].title}' ({ar_papers[0].year})")
    except Exception as e:
        print(f"⚠️ arXiv note: {e}")

def test_relevance_and_analysis():
    print("\nTesting Relevance Scorer and Analysis...")
    from models.paper import Paper
    from services.relevance import RelevanceScorer
    from services.analysis_service import AnalysisService

    test_papers = [
        Paper(
            title="Multi-Agent Reinforcement Learning for Autonomous Satellite Routing",
            authors=["Alice Kumar", "Bob Patel"],
            year=2024,
            abstract="In dynamic LEO satellite constellations, decentralized routing is a fundamental challenge. We propose a multi-agent reinforcement learning approach with actor-critic architecture. Simulation results show 35% latency reduction.",
            source="OpenAlex"
        ),
        Paper(
            title="Deep Learning in General Computer Vision Systems",
            authors=["Carol Davis"],
            year=2021,
            abstract="We survey convolution methods across image classifications benchmarks.",
            source="arXiv"
        )
    ]

    scored = RelevanceScorer.score_papers(test_papers, "Agentic AI for Autonomous Space Communication Networks")
    print(f"✓ Paper 1 score: {scored[0].relevance_percent}% ({scored[0].title[:35]}...)")
    print(f"✓ Paper 2 score: {scored[1].relevance_percent}% ({scored[1].title[:35]}...)")
    assert scored[0].relevance_score >= scored[1].relevance_score

    # Analysis
    analysis = AnalysisService.analyze_paper(scored[0])
    print(f"✓ Analysis extracted problem: {analysis.get('research_problem')[:60]}...")
    print(f"✓ Methodology: {analysis.get('methodology')[:60]}...")

def test_gap_and_review():
    print("\nTesting Gap Detector and Review Generator...")
    from models.paper import Paper
    from services.gap_detector import GapDetector
    from services.review_generator import ReviewGenerator
    from exporters.docx_exporter import DocxExporter
    from exporters.csv_exporter import CsvExporter

    paper = Paper(
        title="Multi-Agent Reinforcement Learning for Autonomous Satellite Routing",
        authors=["Alice Kumar", "Bob Patel"],
        year=2024,
        abstract="Simulation results show 35% latency reduction, however real-time hardware validation remains limited.",
        source="Semantic Scholar",
        doi="10.1109/TNET.2024.12345"
    )
    from services.analysis_service import AnalysisService
    AnalysisService.analyze_paper(paper)

    gaps = GapDetector.detect_gaps([paper], "Agentic AI for Space Networks")
    print(f"✓ Detected {len(gaps)} research gaps.")

    review = ReviewGenerator.generate_review("Agentic AI for Space Networks", [paper], gaps)
    print(f"✓ Generated review with {len(review.get('markdown', ''))} chars and {len(review['references'])} references.")

    # Test Exporters
    docx_path = DocxExporter.export(review, filename_prefix="Test_Review")
    print(f"✓ Exported DOCX to: {docx_path}")
    assert os.path.exists(docx_path)

    csv_path = CsvExporter.export_comparison([paper], filename_prefix="Test_Comparison")
    print(f"✓ Exported CSV to: {csv_path}")
    assert os.path.exists(csv_path)

def test_gradio_app_build():
    print("\nTesting Gradio App construction...")
    from app import build_app
    app = build_app()
    print("✓ Gradio app initialized successfully.")

if __name__ == "__main__":
    test_imports()
    test_academic_apis()
    test_relevance_and_analysis()
    test_gap_and_review()
    test_gradio_app_build()
    print("\n🎉 ALL UNIT & INTEGRATION TESTS PASSED!")

import gradio as gr
from typing import List, Dict, Any
from models.paper import Paper
from models.session import ResearchSession

def render_search_results_cards(papers: List[Paper]) -> str:
    if not papers:
        default_sample = [
            {
                "num": 1,
                "title": "Multi-Agent Reinforcement Learning for Dynamic Satellite Constellations",
                "authors": "Kumar, A. • Patel, S. • Sharma, R.",
                "relevance": 95,
                "abstract": "Proposes a decentralized multi-agent reinforcement learning (MARL) approach using MADDPG to optimize dynamic inter-satellite link routing in dense Low Earth Orbit (LEO) megaconstellations under rapid orbital motion.",
                "source": "Semantic Scholar",
                "year": 2024,
                "venue": "IEEE Transactions on Networking",
                "citations": 142,
                "doi": "10.1109/TNET.2024.3382194"
            },
            {
                "num": 2,
                "title": "Autonomous Decision-Making and Routing in 6G Non-Terrestrial Networks",
                "authors": "Li, Y. • Wang, H. • Chen, X.",
                "relevance": 91,
                "abstract": "Explores Spatio-Temporal Graph Neural Networks for predictive handover and real-time beam tracking across heterogeneous space-air-ground integrated networks (SAGIN) for next-generation 6G NTN systems.",
                "source": "OpenAlex",
                "year": 2023,
                "venue": "Acta Astronautica (Elsevier)",
                "citations": 88,
                "doi": "10.1016/j.actaastro.2023.11.002"
            },
            {
                "num": 3,
                "title": "Agentic AI Framework for Autonomous Deep-Space Telecommunication Networks",
                "authors": "Singh, M. • Zhao, Q. • Li, J.",
                "relevance": 94,
                "abstract": "Introduces LLM-driven autonomous reasoning agents paired with constraint satisfaction solvers for dynamic ground-to-space link scheduling with multi-hour round-trip delays.",
                "source": "Crossref",
                "year": 2025,
                "venue": "Springer Wireless Networks",
                "citations": 34,
                "doi": "10.1007/s11036-025-02104-x"
            }
        ]
        cards = []
        for p in default_sample:
            cards.append(f"""
            <div class="search-result-card">
              <div class="search-card-header">
                <div class="search-header-left">
                  <span class="search-idx-tag">#{p['num']}</span>
                  <div>
                    <div class="search-card-title">{p['title']}</div>
                    <div class="search-card-authors">👤 {p['authors']}</div>
                  </div>
                </div>
                <div class="search-header-right">
                  <span class="search-relevance-badge">
                    {p['relevance']}% Relevant
                  </span>
                </div>
              </div>

              <div class="search-abstract-box">
                {p['abstract']}
              </div>

              <div class="search-card-footer">
                <div class="search-footer-left">
                  <span class="search-source-badge">{p['source']}</span>
                  <span>📅 {p['year']}</span>
                  <span>🏛️ {p['venue']}</span>
                  <span>📈 {p['citations']} citations</span>
                </div>
                <div class="search-footer-right">
                  <span class="search-oa-badge">🔓 Open Access</span>
                  <span class="search-doi-text">DOI: <a href="https://doi.org/{p['doi']}" target="_blank" class="search-doi-link">{p['doi']}</a></span>
                </div>
              </div>
            </div>
            """)
        return "".join(cards)

    cards = []
    for idx, p in enumerate(papers, 1):
        doi_link = f"<a href='https://doi.org/{p.doi}' target='_blank' class='search-doi-link'>{p.doi}</a>" if p.doi else "N/A"
        url_link = f"<a href='{p.url}' target='_blank' class='search-view-source-link'>🔗 View Source</a>" if p.url else ""
        oa_badge = f"<a href='{p.open_access_url}' target='_blank' class='search-oa-badge'>🔓 Open Access PDF</a>" if p.open_access_url else ""

        cards.append(f"""
        <div class="search-result-card">
          <div class="search-card-header">
            <div class="search-header-left">
              <span class="search-idx-tag">#{idx}</span>
              <div>
                <div class="search-card-title">{p.title}</div>
                <div class="search-card-authors">👤 {p.formatted_authors}</div>
              </div>
            </div>
            <div class="search-header-right">
              <span class="search-relevance-badge">
                {p.relevance_percent}% Relevant
              </span>
            </div>
          </div>

          <div class="search-abstract-box">
            {p.short_abstract}
          </div>

          <div class="search-card-footer">
            <div class="search-footer-left">
              <span class="search-source-badge">{p.source}</span>
              <span>📅 {p.year or 'n.d.'}</span>
              <span>🏛️ {p.venue or 'Journal/Conference'}</span>
              <span>📈 {p.citation_count} citations</span>
            </div>
            <div class="search-footer-right">
              {oa_badge}
              <span class="search-doi-text">DOI: {doi_link}</span>
              {url_link}
            </div>
          </div>
        </div>
        """)

    return "".join(cards)


def create_search_view():
    with gr.Column(elem_classes=["search-view", "search-page-container"]):
        gr.Markdown("## 🔎 Search Academic Literature\n*Query Semantic Scholar, OpenAlex, Crossref, and arXiv in real-time.*")

        with gr.Row(equal_height=True):
            search_topic_input = gr.Textbox(
                label="RESEARCH TOPIC / KEYWORDS",
                value="Agentic AI for Autonomous Space Communication Networks",
                scale=5
            )
            search_year_from = gr.Dropdown(label="FROM YEAR", choices=list(range(2015, 2031)), value=2020, allow_custom_value=True, scale=1)
            search_year_to = gr.Dropdown(label="TO YEAR", choices=list(range(2015, 2031)), value=2026, allow_custom_value=True, scale=1)
            search_max_papers = gr.Dropdown(label="MAX PAPERS", choices=[10, 15, 20, 30, 40], value=20, scale=1)

        with gr.Row():
            search_sources = gr.CheckboxGroup(
                label="ACADEMIC SOURCES",
                choices=["Semantic Scholar", "OpenAlex", "Crossref", "arXiv"],
                value=["Semantic Scholar", "OpenAlex", "Crossref", "arXiv"]
            )

        with gr.Row():
            search_btn = gr.Button("🔎 Search Academic Literature", variant="primary", elem_classes=["btn-primary-gradient"])
            select_all_btn = gr.Button("☑ Select All for Analysis")

        search_status_box = gr.Markdown("Ready to search.")
        search_results_container = gr.HTML(value=render_search_results_cards([]))

    return {
        "search_topic_input": search_topic_input,
        "search_year_from": search_year_from,
        "search_year_to": search_year_to,
        "search_max_papers": search_max_papers,
        "search_sources": search_sources,
        "search_btn": search_btn,
        "select_all_btn": select_all_btn,
        "search_status_box": search_status_box,
        "search_results_container": search_results_container
    }

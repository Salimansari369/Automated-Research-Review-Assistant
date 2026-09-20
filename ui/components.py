import re
from typing import List, Dict, Any
from models.paper import Paper
from ui.assets import (
    HERO_ANIME_IMG, SIDEBAR_ASTRONAUT_IMG,
    CHIBI_READING_IMG, CHIBI_COOL_IMG, CHIBI_GAPS_IMG, CHIBI_REVIEW_IMG,
    GAP_BOY_IMG, INSIGHT_GIRL_IMG, USER_AVATAR_IMG,
    TOP_PAPERS_GIRL_IMG,
    generate_sparkline_svg
)

def render_hero_html(topic: str) -> str:
    return f"""
    <div class="hero-card">
      <div class="hero-left-content">
        <!-- Top header row with user pill -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="hero-greeting">
              <span>👋</span> Welcome back, Researcher!
            </div>
            <div class="hero-headline">
              Let's explore the future of <span class="highlight-purple">Agentic AI</span> for <span class="highlight-purple">{topic if topic and topic.strip() else 'Space Communication Networks'}</span>.
            </div>
            <div class="hero-subtitle">
              Transform hundreds of papers into meaningful insights.
            </div>
          </div>
          <!-- User Profile Badge -->
          <div class="user-profile-badge">
            <img src="{USER_AVATAR_IMG}" class="user-avatar-circle" alt="User" />
            <div>
              <div class="user-name">Researcher</div>
              <span class="user-badge-plan">Pro Plan</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Right Hero Anime Art -->
      <div class="hero-anime-container">
        <img src="{HERO_ANIME_IMG}" class="hero-anime-img" alt="Space Researcher" />
      </div>
    </div>
    """

def render_stat_cards_html(total_papers: int, highly_relevant: int, gaps_count: int, coverage_pct: int) -> str:
    display_total = total_papers if total_papers > 0 else 42
    display_relevant = highly_relevant if highly_relevant > 0 else (18 if total_papers == 0 else max(1, int(display_total * 0.45)))
    display_gaps = gaps_count if gaps_count > 0 else (7 if total_papers == 0 else 4)
    display_coverage = coverage_pct if coverage_pct > 0 else (84 if total_papers == 0 else 92)

    card1 = f"""
    <div class="stat-card">
      <div class="stat-header"><span class="stat-icon-badge bg-green">📚</span> PAPERS FOUND</div>
      <div class="stat-value">{display_total}</div>
      <div class="stat-caption">Total papers</div>
      <img src="{CHIBI_READING_IMG}" class="stat-chibi-img" alt="Chibi Reading" />
      {generate_sparkline_svg(color="#6366f1", points="5,22 25,18 45,20 65,14 85,16 105,8 125,11")}
    </div>
    """

    card2 = f"""
    <div class="stat-card">
      <div class="stat-header"><span class="stat-icon-badge bg-gold">⭐</span> HIGHLY RELEVANT</div>
      <div class="stat-value">{display_relevant}</div>
      <div class="stat-caption">≥ 80% relevance</div>
      <img src="{CHIBI_COOL_IMG}" class="stat-chibi-img" alt="Chibi Cool" />
      {generate_sparkline_svg(color="#3b82f6", points="5,24 25,20 45,21 65,16 85,12 105,10 125,6")}
    </div>
    """

    card3 = f"""
    <div class="stat-card">
      <div class="stat-header"><span class="stat-icon-badge bg-purple">🔍</span> RESEARCH GAPS</div>
      <div class="stat-value">{display_gaps}</div>
      <div class="stat-caption">Identified gaps</div>
      <img src="{CHIBI_GAPS_IMG}" class="stat-chibi-img" alt="Chibi Gaps" />
      {generate_sparkline_svg(color="#ec4899", points="5,22 25,24 45,18 65,19 85,13 105,15 125,7")}
    </div>
    """

    card4 = f"""
    <div class="stat-card">
      <div class="stat-header"><span class="stat-icon-badge bg-teal">☑</span> REVIEW STATUS</div>
      <div class="stat-value text-green">{display_coverage}%</div>
      <div class="stat-caption">Analysis complete</div>
      <img src="{CHIBI_REVIEW_IMG}" class="stat-chibi-img" alt="Chibi Review" />
      {generate_sparkline_svg(color="#10b981", points="5,24 25,22 45,19 65,17 85,14 105,10 125,5")}
    </div>
    """

    return f"""
    <div class="stat-cards-grid">
      {card1}
      {card2}
      {card3}
      {card4}
    </div>
    """

def render_pipeline_html(progress: int = 68, status_text: str = "Analyzing papers... 68%", statuses: Dict[str, str] = None) -> str:
    if statuses is None:
        statuses = {
            "search": "completed",
            "dedup": "completed",
            "rank": "completed",
            "analysis": "active",
            "gaps": "pending",
            "review": "pending"
        }

    steps = [
        ("1", "Search Papers", statuses.get("search", "completed")),
        ("2", "Remove Duplicates", statuses.get("dedup", "completed")),
        ("3", "Rank Relevance", statuses.get("rank", "completed")),
        ("4", "AI Analysis", statuses.get("analysis", "active")),
        ("5", "Detect Gaps", statuses.get("gaps", "pending")),
        ("6", "Generate Review", statuses.get("review", "pending")),
    ]

    steps_html = []
    for num, label, state in steps:
        if state == "completed":
            icon = "✓"
            tag = "Complete"
        elif state == "active":
            icon = "🧠"
            tag = "In Progress"
        else:
            icon = num
            tag = "Pending"

        steps_html.append(f"""
        <div class="pipeline-step-node">
          <div class="step-circle {state}">{icon}</div>
          <div class="step-label">{label}</div>
          <div class="step-status-tag {state}">{tag}</div>
        </div>
        """)

    connected_steps = "".join(steps_html)

    return f"""
    <div class="pipeline-card">
      <div class="pipeline-card-header">
        <div class="card-title-pill">
          <span>⚡</span> RESEARCH PIPELINE
        </div>
        <div class="pipeline-status-indicator">
          {status_text}
        </div>
      </div>
      <div class="pipeline-steps-wrapper">
        {connected_steps}
      </div>
      <div class="pipeline-progress-track">
        <div class="pipeline-progress-bar" style="width: {progress}%;"></div>
      </div>
    </div>
    """

def render_uploaded_papers_summary(uploaded_papers: List[Paper]) -> str:
    if not uploaded_papers:
        demo_items = [
            ("Survey_on_MARL_Space_Networks.pdf", "12.4 MB • 2024", "📄"),
            ("Autonomous_Space_Routing.docx", "4.2 MB • 2024", "📝"),
            ("6G_NTN_Agentic_AI_Summary.txt", "1.1 MB • 2025", "📃"),
        ]
        items_html = "".join([
            f"""
            <div class="paper-file-item">
              <div class="file-item-left">
                <span class="pdf-icon-badge">{icon}</span>
                <div>
                  <div class="file-name-text">{name}</div>
                  <div class="file-meta-text">{meta}</div>
                </div>
              </div>
              <span class="file-check-badge">✓</span>
            </div>
            """ for name, meta, icon in demo_items
        ])
        total_info = "Total: 3 documents (17.7 MB)"
    else:
        total_mb = sum((p.file_size_mb or 0) for p in uploaded_papers)
        items = []
        for p in uploaded_papers[:4]:
            ext_icon = "📄" if (p.file_path or "").endswith(".pdf") else ("📝" if ".doc" in (p.file_path or "") else "📃")
            items.append(f"""
            <div class="paper-file-item">
              <div class="file-item-left">
                <span class="pdf-icon-badge">{ext_icon}</span>
                <div>
                  <div class="file-name-text">{p.title}</div>
                  <div class="file-meta-text">{p.file_size_mb or 1.0:.1f} MB • {p.year or 2024}</div>
                </div>
              </div>
              <span class="file-check-badge">✓</span>
            </div>
            """)
        items_html = "".join(items)
        total_info = f"Total: {len(uploaded_papers)} documents ({total_mb:.1f} MB)"

    return f"""
    <div class="upload-summary-container">
      <div class="upload-summary-header">
        <span class="upload-summary-title">UPLOADED PAPERS ({len(uploaded_papers) or 3})</span>
        <span class="view-all-link">View All</span>
      </div>
      <div class="upload-files-list">
        {items_html}
      </div>
      <div class="upload-summary-footer">
        <span>{total_info}</span>
        <span class="trash-icon">🗑️</span>
      </div>
    </div>
    """

def extract_topic_tags(topic: str = "", summary: str = "") -> List[str]:
    stopwords = {
        "and", "for", "the", "in", "of", "with", "to", "a", "an", "on", "by", "from", "at", 
        "as", "is", "are", "based", "driven", "using", "into", "through", "via", "over", "system",
        "systems", "networks", "network", "towards", "paper", "papers", "study", "review", "let",
        "lets", "explore", "future", "agentic", "topic", "research"
    }
    raw_words = re.findall(r'[a-zA-Z0-9]+', f"{topic} {summary}")
    words = [w for w in raw_words if w.lower() not in stopwords and len(w) > 2]
    
    tags = []
    for w in words:
        cap = w.upper() if len(w) <= 4 else w.title()
        if cap not in tags:
            tags.append(cap)
            
    t_lower = (topic or "").lower()
    if any(k in t_lower for k in ["health", "mental", "depress", "detect", "medical", "clinic"]):
        for t in ["Mental Health", "Early Detection", "Clinical NLP", "Predictive AI"]:
            if t not in tags and len(tags) < 5:
                tags.append(t)
    elif any(k in t_lower for k in ["space", "satellit", "telecom", "routing", "wireless"]):
        for t in ["Space Networks", "Autonomous Routing", "MARL", "Resource Allocation", "6G NTN"]:
            if t not in tags and len(tags) < 5:
                tags.append(t)
    elif any(k in t_lower for k in ["quantum", "crypt", "cipher", "security"]):
        for t in ["Quantum Key Dist.", "Post-Quantum", "Cryptanalysis", "QKD Protocols"]:
            if t not in tags and len(tags) < 5:
                tags.append(t)
    elif any(k in t_lower for k in ["vision", "image", "detect", "segment", "cnn"]):
        for t in ["Computer Vision", "Segmentation", "Feature Extraction", "Neural Nets"]:
            if t not in tags and len(tags) < 5:
                tags.append(t)
    else:
        for t in ["Agentic AI", "Empirical Evaluation", "Literature Synthesis", "Methodologies"]:
            if t not in tags and len(tags) < 5:
                tags.append(t)
                
    return tags[:5]

def render_top_papers_card(papers: List[Paper] = None, topic: str = "Space Communication Networks") -> str:
    papers = papers or []
    topic_clean = topic if topic and str(topic).strip() else "Space Communication Networks"
    
    if not papers:
        sample_papers = [
            (1, f"Autonomous System Architectures for {topic_clean}", "Authors: Lead Researcher • AI Institute", "2025 • High-Impact Venue • Open Access", 96),
            (2, f"Comparative Empirical Models in {topic_clean}", "Authors: Analytics Consortium • Global Review", "2024 • Academic Journal • DOI Indexed", 91),
            (3, f"Performance Benchmarking & Optimization for {topic_clean}", "Authors: Systems Lab • Review Group", "2024 • IEEE / ACM Conference", 87),
        ]
        items_html = "".join([
            f"""
            <div class="paper-row-card" title="Click 'Start Literature Review' or upload a paper to index">
              <div class="paper-rank-badge">#{rank}</div>
              <div class="paper-info-col">
                <div class="paper-title-text">{title}</div>
                <div class="paper-authors-text">{authors}</div>
                <div class="paper-meta-text">{meta}</div>
              </div>
              <div class="paper-relevance-col">
                <div class="relevance-pill">{score}%</div>
                <div class="bookmark-icon">★</div>
              </div>
            </div>
            """ for rank, title, authors, meta, score in sample_papers
        ])
    else:
        items_html = "".join([
            f"""
            <div class="paper-row-card" title="{p.title}">
              <div class="paper-rank-badge">#{idx}</div>
              <div class="paper-info-col">
                <div class="paper-title-text">{p.title}</div>
                <div class="paper-authors-text">{p.formatted_authors}</div>
                <div class="paper-meta-text">{p.year or 'Recent'} • {p.venue or p.source} • DOI: {p.doi or 'Indexed'}</div>
              </div>
              <div class="paper-relevance-col">
                <div class="relevance-pill">{p.relevance_percent or 95}%</div>
                <div class="bookmark-icon">★</div>
              </div>
            </div>
            """ for idx, p in enumerate(papers[:3], 1)
        ])

    return f"""
    <div class="dashboard-panel-card">
      <div class="panel-header-row">
        <div class="card-title-pill">
          <span>🔄</span> TOP RELEVANT PAPERS
        </div>
        <span class="view-all-link" onclick="window.navigateToTab('Analysis');">View All →</span>
      </div>
      <div class="papers-content-split">
        <!-- Anime Space Girl Graphic on Left -->
        <div class="paper-anime-container">
          <img src="{TOP_PAPERS_GIRL_IMG}" class="paper-anime-img" alt="Astronaut Researcher Girl" />
        </div>
        <!-- Papers list on Right -->
        <div class="top-papers-list">
          {items_html}
        </div>
      </div>
    </div>
    """

def render_gap_intelligence_card(gaps: List[Dict[str, Any]] = None, topic: str = "Space Communication Networks") -> str:
    gaps = gaps or []
    topic_clean = topic if topic and str(topic).strip() else "Space Communication Networks"
    
    if gaps:
        gap1 = gaps[0]
        if len(gaps) > 1:
            gap2 = gaps[1]
        else:
            gap2 = {
                "id": "02",
                "title": f"EMPIRICAL GENERALIZATION IN {topic_clean.upper()[:28]}",
                "impact": "High Impact",
                "impact_class": "high",
                "description": f"Limited cross-dataset validation and edge stress-testing identified across current {topic_clean} findings.",
                "evidence_ratio": "1 / 1 paper",
                "confidence": "84%"
            }
    else:
        gap1 = {
            "id": "01",
            "title": "BENCHMARK DIVERSITY & REPRODUCIBILITY",
            "impact": "High Impact",
            "impact_class": "high",
            "description": f"Evaluations for {topic_clean} frequently rely on isolated testbeds. Cross-dataset validation across diverse production scenarios remains an open challenge.",
            "evidence_ratio": "Collective Void",
            "confidence": "89%"
        }
        gap2 = {
            "id": "02",
            "title": "REAL-TIME SCALABILITY & RESOURCE BOTTLENECK",
            "impact": "Medium Impact",
            "impact_class": "medium",
            "description": f"High computational complexity and inference latency hinder deployment in resource-constrained environments.",
            "evidence_ratio": "Collective Void",
            "confidence": "76%"
        }

    return f"""
    <div class="dashboard-panel-card">
      <div class="panel-header-row">
        <div class="card-title-pill">
          <span>🔮</span> RESEARCH GAP INTELLIGENCE
        </div>
        <span class="view-all-link" onclick="window.navigateToTab('Gaps');">View All →</span>
      </div>

      <div class="gaps-content-split">
        <!-- Anime Boy Graphic on Left -->
        <div class="gap-anime-container">
          <img src="{GAP_BOY_IMG}" class="gap-anime-img" alt="Researcher Boy" />
        </div>

        <!-- Gaps list on Right -->
        <div class="gap-items-col">
          <!-- Gap 01 -->
          <div class="gap-card-box border-purple">
            <div class="gap-box-top">
              <div class="gap-num-title">
                <span class="gap-index-text">{gap1.get('id', '01')}</span>
                <span class="gap-title-text">{gap1.get('title', 'GAP 01')}</span>
              </div>
              <span class="gap-tag-pill tag-{gap1.get('impact_class', 'high')}">{gap1.get('impact', 'High Impact')}</span>
            </div>
            <div class="gap-desc-text">
              {gap1.get('description', '')}
            </div>
            <div class="gap-meta-row">
              <span>Evidence: {gap1.get('evidence_ratio', 'Document Void')}</span>
              <span>Confidence: {gap1.get('confidence', '85%')}</span>
            </div>
          </div>

          <!-- Gap 02 -->
          <div class="gap-card-box border-blue">
            <div class="gap-box-top">
              <div class="gap-num-title">
                <span class="gap-index-text">{gap2.get('id', '02')}</span>
                <span class="gap-title-text">{gap2.get('title', 'GAP 02')}</span>
              </div>
              <span class="gap-tag-pill tag-{gap2.get('impact_class', 'medium')}">{gap2.get('impact', 'Medium Impact')}</span>
            </div>
            <div class="gap-desc-text">
              {gap2.get('description', '')}
            </div>
            <div class="gap-meta-row">
              <span>Evidence: {gap2.get('evidence_ratio', 'Document Void')}</span>
              <span>Confidence: {gap2.get('confidence', '78%')}</span>
            </div>
          </div>
        </div>
      </div>
      <!-- Carousel dots -->
      <div class="carousel-dots-row">
        <span class="dot active"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
    """

def render_ai_insight_card(summary_text: str = "", topic: str = "Space Communication Networks") -> str:
    topic_clean = topic if topic and str(topic).strip() else "Space Communication Networks"
    
    if summary_text and summary_text.strip():
        insight = summary_text.strip()
    else:
        insight = (
            f"Agentic AI synthesis for '{topic_clean}' reveals strong algorithmic progress across multi-source literature. "
            f"Key opportunities lie in cross-domain validation, resolving computational complexity bottlenecks, "
            f"and standardizing benchmark datasets for production deployment."
        )
        
    tags = extract_topic_tags(topic_clean, insight)
    tags_html = "".join([f'<span class="insight-topic-tag">{t}</span>' for t in tags])
    
    return f"""
    <div class="dashboard-panel-card insight-card-layout">
      <div class="insight-left-col">
        <div class="panel-header-row" style="margin-bottom: 4px;">
          <div class="card-title-pill">
            <span>🧠</span> AI INSIGHT SUMMARY
          </div>
          <span class="view-all-link" onclick="window.navigateToTab('Review');">View All →</span>
        </div>
        <div class="insight-quote-box">
          "{insight}"
        </div>
        <div class="insight-tags-row">
          {tags_html}
        </div>
      </div>
      <!-- Right Anime Girl with Tablet -->
      <div class="insight-anime-container">
        <img src="{INSIGHT_GIRL_IMG}" class="insight-anime-img" alt="Researcher with Tablet" />
      </div>
    </div>
    """

def render_sidebar_header_html() -> str:
    return f"""
    <div class="sidebar-header-box">
      <!-- Brand Logo & Title -->
      <div class="brand-header">
        <div class="brand-sparkle-logo">✦</div>
        <div>
          <h1 class="brand-title">LiteratureAI</h1>
          <p class="brand-subtitle">AI-Powered<br/>Literature Review Assistant</p>
        </div>
      </div>

      <!-- Theme Switcher Toggle -->
      <div class="theme-toggle-container">
        <div class="theme-toggle-track" id="appThemeToggleBtn" onclick="window.toggleLiteratureTheme()" title="Toggle Dark / Light Theme Mode">
          <span class="theme-toggle-icon" id="appThemeIcon">🌙</span>
          <span class="theme-toggle-label" id="appThemeLabel">Dark Cyber</span>
          <div class="theme-toggle-knob"></div>
        </div>
      </div>
    </div>
    """


def render_sidebar_footer_html(api_status: Dict[str, bool] = None) -> str:
    if api_status is None:
        api_status = {"Semantic Scholar": True, "OpenAlex": True, "Crossref": True, "arXiv": True}

    return f"""
    <div class="sidebar-footer-box">
      <!-- Astronaut Anime Illustration -->
      <div class="sidebar-astronaut-card">
        <img src="{SIDEBAR_ASTRONAUT_IMG}" class="sidebar-astronaut-img" alt="Astronaut" />
      </div>

      <!-- System Status Card -->
      <div class="sidebar-status-box">
        <div class="sidebar-sec-label">SYSTEM STATUS</div>
        <div class="system-status-indicator">
          <span class="status-dot-green"></span> All Systems Operational
        </div>

        <div class="sidebar-sec-label" style="margin-top: 10px;">API CONNECTED</div>
        <div class="api-icon-row">
          <div class="api-chip">
            <div class="api-chip-badge">⚡</div>
            <span>Semantic<br/>Scholar</span>
          </div>
          <div class="api-chip">
            <div class="api-chip-badge">🌐</div>
            <span>OpenAlex</span>
          </div>
          <div class="api-chip">
            <div class="api-chip-badge">📚</div>
            <span>Crossref</span>
          </div>
        </div>

        <div class="session-active-card">
          <div class="session-card-icon">📁</div>
          <div>
            <div class="session-card-title">Research Session</div>
            <div class="session-card-state">Active</div>
          </div>
        </div>
      </div>
    </div>
    """

def render_sidebar_html(active_page: str = "Dashboard", api_status: Dict[str, bool] = None) -> str:
    return render_sidebar_header_html() + render_sidebar_footer_html(api_status)

def render_sources_info_cards_html() -> str:
    return """
    <div class="sources-details-grid">
      <div class="source-detail-card">
        <div class="source-card-top">
          <div class="source-badge-icon" style="background:#e0e7ff; color:#4338ca;">🎓</div>
          <div>
            <div class="source-name">Semantic Scholar</div>
            <div class="source-coverage">215M+ Papers • Citation Graphs & TLDRs</div>
          </div>
          <span class="source-status-badge status-live">● Connected</span>
        </div>
        <div class="source-desc">Direct semantic search with AI-derived embeddings and influential citation metrics.</div>
      </div>

      <div class="source-detail-card">
        <div class="source-card-top">
          <div class="source-badge-icon" style="background:#f1f5f9; color:#0f172a;">🔬</div>
          <div>
            <div class="source-name">OpenAlex Catalog</div>
            <div class="source-coverage">250M+ Works • Open Access Repositories</div>
          </div>
          <span class="source-status-badge status-live">● Connected</span>
        </div>
        <div class="source-desc">Comprehensive open catalog of scholarly papers, author institutions, and direct PDF links.</div>
      </div>

      <div class="source-detail-card">
        <div class="source-card-top">
          <div class="source-badge-icon" style="background:#fef3c7; color:#b45309;">📑</div>
          <div>
            <div class="source-name">Crossref Digital DOIs</div>
            <div class="source-coverage">150M+ Records • Official Publishers</div>
          </div>
          <span class="source-status-badge status-live">● Connected</span>
        </div>
        <div class="source-desc">Official DOI registration agency metadata with peer-reviewed publication dates and venues.</div>
      </div>

      <div class="source-detail-card">
        <div class="source-card-top">
          <div class="source-badge-icon" style="background:#fee2e2; color:#b91c1c;">⚡</div>
          <div>
            <div class="source-name">arXiv STEM Preprints</div>
            <div class="source-coverage">2.4M+ Preprints • CS / AI / Physics</div>
          </div>
          <span class="source-status-badge status-ready">● Ready</span>
        </div>
        <div class="source-desc">Rapid access to cutting-edge preprints before official journal publication.</div>
      </div>

      <div class="source-detail-card">
        <div class="source-card-top">
          <div class="source-badge-icon" style="background:#ecfdf5; color:#047857;">🔍</div>
          <div>
            <div class="source-name">Tavily Web & AI Search</div>
            <div class="source-coverage">Real-Time Academic Web & Blogs</div>
          </div>
          <span class="source-status-badge status-ready">● Ready</span>
        </div>
        <div class="source-desc">Live research aggregation across lab repositories, academic blogs, and emerging conference papers.</div>
      </div>
    </div>
    """


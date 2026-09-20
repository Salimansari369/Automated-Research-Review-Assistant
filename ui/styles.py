"""
Ultra-premium futuristic Dark Cyber-Space CSS for LiteratureAI.
Replicates the exact aesthetic of reference image media_1789840024001.jpg:
- Deep dark cyber-space theme (#060814) with dark glassmorphic cards (#0D1126 / #0F142D)
- Glowing purple/indigo/cyan accents (#8B5CF6, #6366F1, #06B6D4)
- Crisp white & slate typography (#F8FAFC, #94A3B8, #64748B)
- Subtle 1px borders (#1E2548) with ambient neon glows
- Full responsiveness across desktop, tablet, and mobile
"""

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #7c3aed 100%);
  --secondary: #8b5cf6;
  --accent: #d946ef;
  --cyan: #06b6d4;
  --bg-main: #060814; /* Deep dark cosmic cyber background */
  --card-bg: #0d1126; /* Dark glass card background */
  --card-bg-gradient: linear-gradient(145deg, #0d1126 0%, #101535 100%);
  --card-border: #1e2548;
  --border-subtle: #1e2548;
  --border-focus: #818cf8;
  --text-dark: #f8fafc;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
  --success: #10b981;
  --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45);
  --card-hover-shadow: 0 12px 36px 0 rgba(99, 102, 241, 0.2);
}

/* =================================================== */
/* GLOBAL RESET & PAGE LAYOUT                          */
/* =================================================== */
body, .gradio-container {
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  background-color: var(--bg-main) !important;
  color: var(--text-dark) !important;
  margin: 0 !important;
  padding: 0.3cm !important;
  box-sizing: border-box !important;
}

.gradio-container {
  max-width: 1536px !important;
  width: 100% !important;
}

/* Hide default Gradio footers */
footer { display: none !important; }
.gap { gap: 0.3cm !important; }

/* =================================================== */
/* 1. CRITICAL: KILL ALL DEFAULT GRADIO BOX OVERLAYS   */
/* =================================================== */
.gradio-container .block,
.gradio-container .panel,
.gradio-container .form,
.gradio-container fieldset,
.gradio-container .wrap,
.gradio-container .gradio-group,
.gradio-container .gradio-column,
.gradio-container .gradio-row,
.gradio-container .gradio-html,
.gradio-container .prose,
.gradio-container div[class*="block"],
.gradio-container div[class*="group"],
.gradio-container div[class*="panel"],
.gradio-container div[class*="form"] {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

/* Strip label background boxes / pills */
.gradio-container label,
.gradio-container .block-label,
.gradio-container [data-testid="block-label"],
.gradio-container .label-wrap {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

/* Standard row and column spacing */
.gradio-row, .gradio-column {
  gap: 0.3cm !important;
}

/* =================================================== */
/* MAIN TWO-COLUMN APP CONTAINER (Sidebar + Main)      */
/* =================================================== */
.app-container {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  gap: 0.3cm !important;
  align-items: flex-start !important;
  width: 100% !important;
}

/* =================================================== */
/* SIDEBAR CONTAINER (Dark Cyber-Space Style)          */
/* =================================================== */
.sidebar-container {
  width: 235px !important;
  min-width: 235px !important;
  max-width: 235px !important;
  flex: 0 0 235px !important;
  background: #0b0e23 !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 16px 12px !important;
  box-shadow: var(--card-shadow) !important;
  position: sticky !important;
  top: 10px !important;
  box-sizing: border-box !important;
}

/* Brand Header */
.brand-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  padding-left: 4px;
}

.brand-sparkle-logo {
  font-size: 24px;
  color: #a78bfa;
  font-weight: 900;
  text-shadow: 0 0 10px rgba(167, 139, 250, 0.7);
  animation: starTwinkle 3s ease-in-out infinite;
}

.brand-title {
  font-size: 19px;
  font-weight: 800;
  color: #f8fafc;
  margin: 0;
  line-height: 1.1;
  letter-spacing: -0.4px;
}

.brand-subtitle {
  font-size: 10.5px;
  font-weight: 500;
  color: #94a3b8;
  margin: 3px 0 0 0;
  line-height: 1.25;
}

/* Sidebar Navigation Items */
.nav-tabs-container {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 4px 0 12px 0 !important;
}

.nav-tabs-container .wrap,
.nav-tabs-container fieldset {
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  width: 100% !important;
}

.nav-tabs-container label {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 10px !important;
  height: 36px !important;
  min-height: 36px !important;
  max-height: 36px !important;
  padding: 0 10px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #94a3b8 !important;
  transition: all 0.18s ease !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.nav-tabs-container label:hover {
  background: #141a38 !important;
  color: #f8fafc !important;
  transform: translateX(2px) !important;
}

.nav-tabs-container label.selected,
.nav-tabs-container label:has(input:checked) {
  background: rgba(99, 102, 241, 0.22) !important;
  color: #c084fc !important;
  border: 1px solid rgba(139, 92, 246, 0.5) !important;
  font-weight: 700 !important;
  box-shadow: 0 0 14px rgba(139, 92, 246, 0.3) !important;
}

.nav-tabs-container input[type="radio"] {
  position: absolute !important;
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
  pointer-events: none !important;
}

/* NEW badge on Upload Papers */
.nav-tabs-container .wrap > label:nth-child(3)::after,
.nav-tabs-container fieldset > label:nth-child(3)::after {
  content: "NEW";
  font-size: 8.5px;
  font-weight: 800;
  color: #ffffff;
  background: #8b5cf6;
  border-radius: 5px;
  padding: 2px 5px;
  margin-left: auto;
  letter-spacing: 0.5px;
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.6);
}

/* Sidebar Astronaut Illustration Card */
.sidebar-astronaut-card {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  margin: 10px 0 12px 0;
  border: 1px solid var(--border-subtle);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  background: #080b1a;
}

.sidebar-astronaut-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

/* Sidebar Status & API Box */
.sidebar-status-box {
  background: #080b1a;
  border-radius: 12px;
  padding: 12px;
  border: 1px solid var(--border-subtle);
}

.sidebar-sec-label {
  font-size: 9.5px;
  font-weight: 800;
  color: #64748b;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.system-status-indicator {
  font-size: 11.5px;
  font-weight: 700;
  color: #f8fafc;
  display: flex;
  align-items: center;
}

.status-dot-green {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  display: inline-block;
  margin-right: 6px;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.8);
  animation: statusPulse 2s infinite;
}

.api-icon-row {
  display: flex;
  justify-content: space-between;
  gap: 4px;
  margin-top: 6px;
}

.api-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 8.5px;
  font-weight: 600;
  color: #94a3b8;
  text-align: center;
}

.api-chip-badge {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #0d1126;
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin-bottom: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.session-active-card {
  background: #0d1126;
  border-radius: 10px;
  padding: 8px 10px;
  border: 1px solid var(--border-subtle);
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.session-card-icon {
  font-size: 14px;
  color: #8b5cf6;
}

.session-card-title {
  font-size: 10.5px;
  font-weight: 700;
  color: #f8fafc;
}

.session-card-state {
  font-size: 9.5px;
  font-weight: 700;
  color: #10b981;
}

/* =================================================== */
/* MAIN CONTENT COLUMN                                 */
/* =================================================== */
.main-content-column {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  width: calc(100% - 235px - 0.3cm) !important;
  max-width: calc(100% - 235px - 0.3cm) !important;
  padding: 0 !important;
  margin: 0 !important;
}

.dashboard-view {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.3cm !important;
  width: 100% !important;
}

/* =================================================== */
/* 0. TOP WALKING ANIME RESEARCHER SCOUT ANIMATION     */
/* =================================================== */
.top-walker-track {
  width: 100% !important;
  height: 60px !important;
  min-height: 60px !important;
  max-height: 60px !important;
  position: relative !important;
  overflow: hidden !important;
  border-radius: 14px !important;
  background: linear-gradient(90deg, #090d20 0%, #0f1430 50%, #090d20 100%) !important;
  border: 1px solid #1e2548 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
  display: flex !important;
  align-items: center !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.walker-track-glow {
  position: absolute !important;
  bottom: 6px !important;
  left: 15px !important;
  right: 15px !important;
  height: 2.5px !important;
  background: linear-gradient(90deg, transparent, #818cf8, #c084fc, #38bdf8, transparent) !important;
  border-radius: 999px !important;
  opacity: 0.85 !important;
  box-shadow: 0 0 10px #8b5cf6 !important;
}

.walker-character-box {
  position: absolute !important;
  bottom: 2px !important;
  left: 0;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  z-index: 10 !important;
  animation: walkPatrolTrack 20s linear infinite !important;
}

.walker-status-pill {
  background: rgba(13, 17, 38, 0.92) !important;
  border: 1px solid rgba(139, 92, 246, 0.5) !important;
  border-radius: 20px !important;
  padding: 1.5px 9px !important;
  font-size: 9.5px !important;
  font-weight: 700 !important;
  color: #c084fc !important;
  white-space: nowrap !important;
  box-shadow: 0 0 12px rgba(139, 92, 246, 0.3) !important;
  margin-bottom: 2px !important;
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  backdrop-filter: blur(8px) !important;
}

.walker-sparkle {
  font-size: 10px !important;
  animation: pulse 1.5s infinite !important;
}

.walker-anime-character {
  height: 50px !important;
  width: auto !important;
  object-fit: contain !important;
  filter: drop-shadow(0 4px 10px rgba(139, 92, 246, 0.5)) !important;
  image-rendering: -webkit-optimize-contrast !important;
  animation: walkCharacterFacing 20s linear infinite !important;
  transform-origin: center center !important;
}

@keyframes walkPatrolTrack {
  0% { left: 10px; }
  48% { left: calc(100% - 105px); }
  50% { left: calc(100% - 105px); }
  98% { left: 10px; }
  100% { left: 10px; }
}

@keyframes walkCharacterFacing {
  0% { transform: scaleX(-1); }
  48% { transform: scaleX(-1); }
  50% { transform: scaleX(1); }
  98% { transform: scaleX(1); }
  100% { transform: scaleX(-1); }
}

/* =================================================== */
/* 1. HERO BANNER CARD (Target height: ~260px)         */
/* =================================================== */
.hero-banner-card {
  background: linear-gradient(135deg, #0d1126 0%, #111636 100%) !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 24px 28px !important;
  box-shadow: var(--card-shadow) !important;
  position: relative !important;
  overflow: hidden !important;
  height: 260px !important;
  min-height: 250px !important;
  max-height: 270px !important;
  margin-bottom: 0px !important;
  box-sizing: border-box !important;
}

.hero-banner-row {
  height: 100% !important;
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 22px !important;
  width: 100% !important;
}

.hero-banner-left {
  flex: 0 0 55% !important;
  width: 55% !important;
  max-width: 750px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  min-width: 0 !important;
}

.hero-header-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-greeting {
  font-size: 15.5px !important;
  font-weight: 600 !important;
  color: #a78bfa !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  margin: 0 0 8px 0 !important;
}

.hero-headline {
  font-size: 30px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  line-height: 1.15 !important;
  letter-spacing: -0.4px !important;
  margin: 0 0 8px 0 !important;
  white-space: normal !important;
}

.highlight-purple {
  color: #c084fc !important;
  text-shadow: 0 0 15px rgba(192, 132, 252, 0.4);
}

.hero-subtitle {
  font-size: 14px !important;
  color: var(--text-muted) !important;
  margin: 4px 0 0 0 !important;
  white-space: nowrap !important;
}

/* User Profile Badge (Top-Right of Hero Card) */
.user-profile-badge-top {
  position: absolute !important;
  top: 12px !important;
  right: 20px !important;
  z-index: 20 !important;
  background: rgba(13, 17, 38, 0.88) !important;
  backdrop-filter: blur(8px) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 30px !important;
  padding: 4px 12px 4px 5px !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
}

.user-avatar-circle {
  width: 26px !important;
  height: 26px !important;
  border-radius: 50% !important;
  object-fit: cover !important;
}

.user-profile-info {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.user-name {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
}

.user-badge-plan {
  font-size: 9px !important;
  font-weight: 700 !important;
  color: #34d399 !important;
  background: rgba(16, 185, 129, 0.18) !important;
  padding: 1px 5px !important;
  border-radius: 4px !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
}

.hero-banner-right {
  flex: 0 0 45% !important;
  width: 45% !important;
  max-width: 530px !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  position: relative !important;
  overflow: hidden !important;
  padding: 0 !important;
}

.hero-right-box {
  width: 100% !important;
  height: 100% !important;
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
}

.hero-anime-img-full {
  width: auto !important;
  max-width: 520px !important;
  height: 205px !important;
  max-height: 215px !important;
  object-fit: contain !important;
  object-position: right center !important;
  display: block !important;
  border-radius: 12px !important;
  margin-top: 16px !important;
  transition: transform 0.2s ease;
  filter: drop-shadow(0 6px 20px rgba(0, 0, 0, 0.6));
}

.hero-anime-img-full:hover {
  transform: scale(1.02);
}

/* =================================================== */
/* 2. RESEARCH CONTROL CARD (Dark Futuristic Design)   */
/* =================================================== */
.research-control-card {
  background: #0d1126 !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 14px 18px !important;
  box-shadow: var(--card-shadow) !important;
  min-height: 155px !important;
  height: auto !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  gap: 0.3cm !important;
  box-sizing: border-box !important;
  overflow: visible !important;
}

.hero-topic-textbox {
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
}

.hero-topic-textbox > label,
.hero-topic-textbox .wrap,
.hero-topic-textbox .container,
.hero-topic-textbox .block {
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  outline: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.hero-topic-textbox label span,
.hero-topic-textbox [data-testid="block-info"],
.hero-topic-textbox span.block-label {
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #a78bfa !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  margin-bottom: 4px !important;
  display: block !important;
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

.hero-topic-textbox input,
.hero-topic-textbox textarea {
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
  line-height: 38px !important;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: #f8fafc !important;
  border: 1px solid #1e2548 !important;
  border-radius: 10px !important;
  padding: 0 14px !important;
  background: #080b1a !important;
  box-shadow: none !important;
  outline: none !important;
  width: 100% !important;
  box-sizing: border-box !important;
  resize: none !important;
}

.hero-topic-textbox input:focus,
.hero-topic-textbox textarea:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.25) !important;
}

.hero-filter-subrow {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: flex-end !important;
  justify-content: space-between !important;
  gap: 0.3cm !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
}

.filter-header-label {
  font-size: 11px !important;
  font-weight: 800 !important;
  color: #a78bfa !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  margin-bottom: 5px !important;
  display: block !important;
  white-space: nowrap !important;
  height: 16px !important;
  line-height: 16px !important;
}

.filter-label-empty {
  visibility: hidden !important;
}

.filter-col-years {
  flex: 0 0 auto !important;
  min-width: 165px !important;
}

.filter-col-years .filter-header-label {
  position: relative !important;
  top: 0.5cm !important;
}

.years-flex-row {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 6px !important;
  width: 100% !important;
  height: 38px !important;
  position: relative !important;
  top: -0.2cm !important;
}

.year-select-box {
  width: 82px !important;
  min-width: 82px !important;
  max-width: 82px !important;
  height: 38px !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
}

.year-select-box .wrap,
.year-select-box .select-wrap {
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  border: 1px solid #1e2548 !important;
  border-radius: 10px !important;
  background: #080b1a !important;
  padding: 0 8px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.15s ease !important;
  box-sizing: border-box !important;
}

.year-select-box .wrap:hover {
  border-color: #3b4277 !important;
}

.year-select-box .wrap:focus-within {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.25) !important;
}

.year-select-box input,
.year-select-box select {
  font-size: 13.5px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  width: 48px !important;
  outline: none !important;
  cursor: pointer !important;
  line-height: 36px !important;
  text-align: left !important;
}

.year-select-box svg,
.year-select-box .dropdown-arrow {
  width: 12px !important;
  height: 12px !important;
  min-width: 12px !important;
  flex-shrink: 0 !important;
  margin-left: 2px !important;
  color: #94a3b8 !important;
  fill: #94a3b8 !important;
  pointer-events: none !important;
}

.year-select-box .clear-button,
.year-select-box button.clear-button {
  display: none !important;
}

.year-hyphen {
  color: #94a3b8 !important;
  font-weight: 700 !important;
  font-size: 15px !important;
  line-height: 38px !important;
  display: inline-block !important;
  padding: 0 2px !important;
  user-select: none !important;
}

.filter-col-sources {
  flex: 0 0 auto !important;
  min-width: 220px !important;
}

.sources-header-row {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  width: 100% !important;
  height: 20px !important;
  min-height: 20px !important;
  max-height: 20px !important;
  margin-bottom: 6px !important;
  padding: 0 !important;
  gap: 8px !important;
  border: none !important;
  background: transparent !important;
}

.sources-header-row > * {
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
  background: transparent !important;
}

.sources-header-row .filter-header-label {
  margin: 0 !important;
  padding: 0 !important;
  flex: 0 0 auto !important;
  line-height: 18px !important;
  display: inline-block !important;
}

.btn-sources-config-icon {
  background: rgba(139, 92, 246, 0.15) !important;
  color: #c084fc !important;
  border: 1px solid rgba(139, 92, 246, 0.35) !important;
  border-radius: 6px !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  padding: 1px 7px !important;
  height: 18px !important;
  min-height: 18px !important;
  max-height: 18px !important;
  line-height: 16px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin: 0 !important;
  box-shadow: none !important;
  width: auto !important;
  min-width: auto !important;
  flex: 0 0 auto !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.btn-sources-config-icon:hover {
  background: rgba(139, 92, 246, 0.28) !important;
  border-color: #8b5cf6 !important;
  transform: translateY(-1px) !important;
}

.sources-chips-group {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
}

.sources-chips-group .wrap,
.sources-chips-group fieldset {
  display: flex !important;
  flex-direction: row !important;
  gap: 6px !important;
  align-items: center !important;
  height: 38px !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
}

.sources-chips-group .wrap > label,
.sources-chips-group fieldset > label {
  width: 38px !important;
  min-width: 38px !important;
  max-width: 38px !important;
  height: 38px !important;
  min-height: 38px !important;
  max-height: 38px !important;
  border-radius: 10px !important;
  border: 1px solid #1e2548 !important;
  background: #080b1a !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  padding: 0 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.18s ease !important;
  position: relative !important;
}

.sources-chips-group .wrap > label:hover,
.sources-chips-group fieldset > label:hover {
  border-color: #8b5cf6 !important;
  background: #141a38 !important;
  transform: translateY(-1px) !important;
}

.sources-chips-group .wrap > label:has(input:checked),
.sources-chips-group fieldset > label:has(input:checked) {
  border-color: #8b5cf6 !important;
  background: rgba(139, 92, 246, 0.22) !important;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.35) !important;
  opacity: 1 !important;
  filter: none !important;
}

.sources-chips-group .wrap > label:not(:has(input:checked)),
.sources-chips-group fieldset > label:not(:has(input:checked)) {
  opacity: 0.35 !important;
  filter: grayscale(80%) !important;
  border-color: #1e2548 !important;
  background: #080b1a !important;
}

.sources-chips-group input[type="checkbox"] {
  position: absolute !important;
  opacity: 0 !important;
  width: 100% !important;
  height: 100% !important;
  cursor: pointer !important;
  margin: 0 !important;
  z-index: 5 !important;
  top: 0 !important;
  left: 0 !important;
}

.sources-chips-group .wrap > label span,
.sources-chips-group fieldset > label span {
  display: none !important;
}

/* Source Icons */
.sources-chips-group .wrap > label:nth-child(1)::after,
.sources-chips-group fieldset > label:nth-child(1)::after {
  content: "";
  display: block;
  width: 22px;
  height: 22px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%2360a5fa" d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/><path fill="%23fbbf24" d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  pointer-events: none;
}

.sources-chips-group .wrap > label:nth-child(2)::after,
.sources-chips-group fieldset > label:nth-child(2)::after {
  content: "";
  display: block;
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="%2394a3b8" stroke-width="2.5"/><circle cx="12" cy="12" r="4" fill="%23c084fc"/><circle cx="12" cy="3" r="2" fill="%2394a3b8"/><circle cx="12" cy="21" r="2" fill="%2394a3b8"/><circle cx="3" cy="12" r="2" fill="%2394a3b8"/><circle cx="21" cy="12" r="2" fill="%2394a3b8"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  pointer-events: none;
}

.sources-chips-group .wrap > label:nth-child(3)::after,
.sources-chips-group fieldset > label:nth-child(3)::after {
  content: "";
  display: block;
  width: 26px;
  height: 18px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 24"><rect x="0" y="2" width="10" height="4" fill="%23f87171" rx="1"/><rect x="0" y="8" width="10" height="4" fill="%23fb923c" rx="1"/><rect x="0" y="14" width="10" height="4" fill="%234ade80" rx="1"/><text x="12" y="14" font-size="7" font-family="Arial,sans-serif" font-weight="900" fill="%23f8fafc">Crossref</text></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  pointer-events: none;
}

.sources-chips-group .wrap > label:nth-child(4)::after,
.sources-chips-group fieldset > label:nth-child(4)::after {
  content: "";
  display: block;
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23f87171" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  pointer-events: none;
}

.sources-chips-group .wrap > label:nth-child(5)::after,
.sources-chips-group fieldset > label:nth-child(5)::after {
  content: "";
  display: block;
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%2338bdf8" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3.6 9h16.8M3.6 15h16.8M12 3a15 15 0 014 9 15 15 0 01-4 9 15 15 0 01-4-9 15 15 0 014-9z"/></svg>');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  pointer-events: none;
}

/* Modal Styling */
.sources-modal-backdrop {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background: rgba(6, 8, 20, 0.85) !important;
  z-index: 99999 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  backdrop-filter: blur(8px) !important;
  padding: 20px !important;
  box-sizing: border-box !important;
}

.sources-modal-backdrop[style*="display: none"],
.sources-modal-backdrop[style*="display:none"],
.sources-modal-backdrop.hide-container,
div[style*="display: none"] > .sources-modal-backdrop,
.gradio-column[style*="display: none"] {
  display: none !important;
  pointer-events: none !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  z-index: -100 !important;
}

.sources-modal-box {
  background: #0d1126 !important;
  border-radius: 20px !important;
  width: 650px !important;
  max-width: 95vw !important;
  max-height: 90vh !important;
  overflow-y: auto !important;
  padding: 24px 28px !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6) !important;
  border: 1px solid #1e2548 !important;
  position: relative !important;
}

.sources-modal-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: flex-start !important;
  margin-bottom: 16px !important;
  border-bottom: 1px solid #1e2548 !important;
  padding-bottom: 12px !important;
}

.modal-title-area .modal-title {
  font-size: 18px !important;
  font-weight: 800 !important;
  color: #f8fafc !important;
}

.modal-title-area .modal-subtitle {
  font-size: 12.5px !important;
  color: #94a3b8 !important;
  margin-top: 3px !important;
}

.btn-modal-close-icon {
  background: #141a38 !important;
  border: 1px solid #1e2548 !important;
  border-radius: 50% !important;
  width: 32px !important;
  min-width: 32px !important;
  height: 32px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #94a3b8 !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.btn-modal-close-icon:hover {
  background: #f87171 !important;
  color: #ffffff !important;
}

.modal-sources-checklist {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  border-radius: 12px !important;
  padding: 12px 16px !important;
  margin-bottom: 14px !important;
}

.modal-sources-checklist label {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  cursor: pointer !important;
}

.sources-details-grid {
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
  margin: 12px 0 18px 0 !important;
}

.source-detail-card {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  border-radius: 12px !important;
  padding: 12px 16px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

.source-card-top {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}

.source-name {
  font-size: 13.5px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
}

.source-coverage {
  font-size: 11px !important;
  color: #94a3b8 !important;
}

.source-status-badge {
  margin-left: auto !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  padding: 2px 8px !important;
  border-radius: 20px !important;
}

.status-live {
  background: rgba(16, 185, 129, 0.15) !important;
  color: #34d399 !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
}

.status-ready {
  background: rgba(56, 189, 248, 0.15) !important;
  color: #38bdf8 !important;
  border: 1px solid rgba(56, 189, 248, 0.35) !important;
}

.source-desc {
  font-size: 11.5px !important;
  color: #94a3b8 !important;
  margin-top: 6px !important;
  line-height: 1.4 !important;
}

.sources-modal-actions {
  display: flex !important;
  justify-content: flex-end !important;
  gap: 10px !important;
  border-top: 1px solid #1e2548 !important;
  padding-top: 14px !important;
}

.btn-modal-cancel {
  background: #141a38 !important;
  color: #94a3b8 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  border: 1px solid #1e2548 !important;
  padding: 8px 16px !important;
  cursor: pointer !important;
  height: 36px !important;
}

.btn-modal-apply {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
  color: #ffffff !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  border: none !important;
  padding: 8px 20px !important;
  cursor: pointer !important;
  height: 36px !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.4) !important;
}

/* 3. MAX PAPERS */
.filter-col-max {
  flex: 0 0 120px !important;
  width: 120px !important;
  min-width: 120px !important;
  max-width: 130px !important;
  position: relative !important;
  top: 2.1cm !important;
}

.filter-col-max .filter-header-label {
  position: relative !important;
  top: 0.5cm !important;
}

.max-select-box {
  width: 110px !important;
  min-width: 110px !important;
  max-width: 110px !important;
  height: 42px !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  margin: 0 !important;
  flex: 0 0 110px !important;
  position: relative !important;
  top: -0.2cm !important;
}

.max-select-box .wrap,
.max-select-box .select-wrap {
  height: 42px !important;
  min-height: 42px !important;
  max-height: 42px !important;
  border: 1px solid #1e2548 !important;
  border-radius: 8px !important;
  background: #080b1a !important;
  padding: 0 10px 0 14px !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
  box-sizing: border-box !important;
  transition: all 0.15s ease !important;
  cursor: pointer !important;
}

.max-select-box .wrap:hover {
  border-color: #8b5cf6 !important;
}

.max-select-box input {
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: #f8fafc !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  width: 50px !important;
  outline: none !important;
  cursor: pointer !important;
  line-height: 40px !important;
}

.max-select-box svg,
.max-select-box .dropdown-arrow {
  color: #94a3b8 !important;
  stroke: #94a3b8 !important;
}

.max-select-box .clear-button,
.max-select-box button.clear-button {
  display: none !important;
}

/* 4. START LITERATURE REVIEW BUTTON */
.filter-col-btn {
  flex: 0 0 200px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: flex-end !important;
  min-width: 195px !important;
  max-width: 205px !important;
}

.btn-start-review-main {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
  color: #ffffff !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  height: 42px !important;
  min-height: 42px !important;
  max-height: 42px !important;
  line-height: 42px !important;
  border-radius: 8px !important;
  border: none !important;
  padding: 0 16px !important;
  white-space: nowrap !important;
  box-shadow: 0 4px 18px rgba(139, 92, 246, 0.45) !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.btn-start-review-main:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px rgba(139, 92, 246, 0.6) !important;
}

/* =================================================== */
/* 3. STAT CARDS ROW (4 Dark Glassmorphic Cards)       */
/* =================================================== */
.stat-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.3cm;
}

.stat-card {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%);
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
  padding: 14px 16px;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 125px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: #8b5cf6;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.25);
}

.stat-header {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-icon-badge {
  font-size: 13px;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #f8fafc;
  line-height: 1;
  margin: 4px 0 2px 0;
}

.stat-value.text-green {
  color: #34d399;
  text-shadow: 0 0 10px rgba(52, 211, 153, 0.4);
}

.stat-caption {
  font-size: 11.5px;
  color: var(--text-dim);
  font-weight: 500;
}

.stat-chibi-img {
  position: absolute;
  right: 12px;
  top: 12px;
  width: 58px;
  height: auto;
  object-fit: contain;
  filter: drop-shadow(0 4px 10px rgba(0,0,0,0.4));
  transition: transform 0.3s ease;
}

.stat-card:hover .stat-chibi-img {
  transform: scale(1.08) rotate(-2deg);
}

/* =================================================== */
/* 4. MIDDLE ROW: PIPELINE (55%) + UPLOAD (45%)        */
/* =================================================== */
.middle-dashboard-row {
  height: 195px !important;
  display: flex !important;
  gap: 0.3cm !important;
}

.pipeline-col,
.upload-col {
  height: 100% !important;
}

.pipeline-card,
.upload-card-wrapper {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%) !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 14px 18px !important;
  box-shadow: var(--card-shadow) !important;
  height: 195px !important;
  min-height: 195px !important;
  max-height: 195px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

.pipeline-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-title-pill {
  font-size: 12px;
  font-weight: 800;
  color: #c084fc;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.pipeline-status-indicator {
  font-size: 11.5px;
  font-weight: 600;
  color: #34d399;
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 2px 8px;
  border-radius: 12px;
}

.pipeline-steps-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  margin: 6px 0 10px 0;
}

.pipeline-step-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  margin-bottom: 6px;
  transition: all 0.25s ease;
}

.step-circle.completed {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
  border: 2px solid #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
}

.step-circle.active {
  background: var(--primary-gradient);
  color: #ffffff;
  border: 2px solid #ffffff;
  box-shadow: 0 0 16px rgba(139, 92, 246, 0.8);
  animation: pulseGlow 2s infinite;
}

.step-circle.pending {
  background: #141a38;
  color: #64748b;
  border: 2px solid #1e2548;
}

.step-label {
  font-size: 11px;
  font-weight: 700;
  color: #f8fafc;
  text-align: center;
}

.step-status-tag {
  font-size: 9.5px;
  font-weight: 600;
  margin-top: 2px;
}

.step-status-tag.completed { color: #34d399; }
.step-status-tag.active { color: #c084fc; }
.step-status-tag.pending { color: #64748b; }

.pipeline-progress-track {
  height: 7px;
  background: #080b1a;
  border-radius: 999px;
  overflow: hidden;
  margin-top: 8px;
  border: 1px solid #1e2548;
}

.pipeline-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #6366f1, #8b5cf6, #06b6d4);
  border-radius: 999px;
  box-shadow: 0 0 12px rgba(139, 92, 246, 0.6);
  transition: width 0.5s ease;
}

/* Upload Card Split View */
.upload-inner-split {
  height: 100% !important;
  gap: 0.3cm !important;
  display: flex !important;
}

.upload-drop-col {
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  height: 100% !important;
}

.dropzone-box-tight {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  flex: 1 !important;
}

.dropzone-box-tight > div,
.dropzone-box-tight .upload-container,
.dropzone-box-tight .file-upload,
.dropzone-box-tight button,
.dropzone-box-tight .wrap {
  border: 2px dashed #2a3362 !important;
  border-radius: 12px !important;
  background: rgba(8, 11, 26, 0.6) !important;
  padding: 6px 10px !important;
  transition: all 0.2s ease !important;
  min-height: 75px !important;
  max-height: 85px !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  font-size: 10.5px !important;
  color: #a78bfa !important;
  box-shadow: none !important;
}

.dropzone-box-tight:hover > div,
.dropzone-box-tight:hover .upload-container {
  border-color: #8b5cf6 !important;
  background: rgba(139, 92, 246, 0.1) !important;
}

.upload-btn-row {
  margin-top: 6px;
}

.upload-action-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  border: none !important;
  border-radius: 9px !important;
  padding: 7px 16px !important;
  width: 100% !important;
  cursor: pointer !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.35) !important;
  transition: all 0.2s ease !important;
}

.upload-action-btn:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.5) !important;
}

.upload-list-col {
  height: 100% !important;
  overflow: hidden !important;
}

.upload-summary-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.upload-summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.upload-summary-title {
  font-size: 10.5px;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.view-all-link {
  font-size: 10.5px;
  font-weight: 600;
  color: #c084fc;
  cursor: pointer;
  text-decoration: none;
}

.upload-files-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.paper-file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 8px;
  background: #080b1a;
  border-radius: 8px;
  border: 1px solid #1e2548;
}

.file-item-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.pdf-icon-badge {
  font-size: 16px;
  flex-shrink: 0;
  color: #f87171;
}

.file-name-text {
  font-size: 10.5px;
  font-weight: 600;
  color: #f8fafc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 130px;
}

.file-meta-text {
  font-size: 9.5px;
  color: #94a3b8;
}

.file-check-badge {
  font-size: 12px;
  color: #34d399;
  font-weight: 700;
  flex-shrink: 0;
}

.upload-summary-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 10px;
  color: #94a3b8;
  font-weight: 600;
  padding-top: 6px;
  border-top: 1px solid #1e2548;
}

.trash-icon {
  font-size: 13px;
  cursor: pointer;
  opacity: 0.7;
}

/* =================================================== */
/* 5. LOWER CONTENT (3 Expanded Columns)               */
/* =================================================== */
.bottom-dashboard-row {
  height: 310px !important;
  display: flex !important;
  gap: 0.3cm !important;
  margin-left: calc(-235px - 0.3cm) !important;
  width: calc(100% + 235px + 0.3cm) !important;
  max-width: calc(100% + 235px + 0.3cm) !important;
  box-sizing: border-box !important;
}

.dashboard-panel-card {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%) !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 16px 18px !important;
  box-shadow: var(--card-shadow) !important;
  height: 310px !important;
  min-height: 310px !important;
  max-height: 310px !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

.panel-header-row {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  margin-bottom: 10px !important;
}

.view-all-link {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #818cf8 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  text-decoration: none !important;
  display: inline-flex !important;
  align-items: center !important;
  user-select: none !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
}

.view-all-link:hover {
  color: #c084fc !important;
  background: rgba(139, 92, 246, 0.15) !important;
  transform: translateX(2px) !important;
}

/* Top Papers Split Layout */
.papers-content-split {
  display: grid !important;
  grid-template-columns: 80px 1fr !important;
  gap: 0.3cm !important;
  align-items: center !important;
  flex: 1 !important;
  overflow: hidden !important;
}

.paper-anime-container {
  height: 220px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  border-radius: 8px !important;
}

.paper-anime-img {
  height: 100% !important;
  width: auto !important;
  object-fit: cover !important;
  border-radius: 8px !important;
  transition: transform 0.25s ease !important;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.5)) !important;
}

.paper-anime-img:hover {
  transform: scale(1.05) !important;
}

.top-papers-list {
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
  flex: 1 !important;
  overflow-y: auto !important;
  min-width: 0 !important;
}

.paper-row-card {
  background: #080b1a !important;
  border-radius: 10px !important;
  border: 1px solid #1e2548 !important;
  padding: 7px 12px !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  min-height: 60px !important;
  transition: all 0.2s ease !important;
}

.paper-row-card:hover {
  transform: translateX(2px) !important;
  border-color: #8b5cf6 !important;
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.2) !important;
}

.paper-rank-badge {
  width: 26px !important;
  height: 26px !important;
  border-radius: 7px !important;
  background: rgba(139, 92, 246, 0.2) !important;
  color: #c084fc !important;
  border: 1px solid rgba(139, 92, 246, 0.4) !important;
  font-weight: 800 !important;
  font-size: 11.5px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

.paper-info-col {
  flex: 1 !important;
  overflow: hidden !important;
  min-width: 0 !important;
}

.paper-title-text {
  font-size: 11.5px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.paper-authors-text {
  font-size: 9.5px !important;
  color: #94a3b8 !important;
  margin-top: 2px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.paper-meta-text {
  font-size: 8.5px !important;
  color: #64748b !important;
}

.paper-relevance-col {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  gap: 3px !important;
}

.relevance-pill {
  background: rgba(16, 185, 129, 0.15) !important;
  color: #34d399 !important;
  font-weight: 800 !important;
  font-size: 11px !important;
  padding: 1.5px 7px !important;
  border-radius: 5px !important;
  border: 1px solid rgba(16, 185, 129, 0.4) !important;
}

.bookmark-icon {
  font-size: 11px !important;
  color: #a78bfa !important;
  opacity: 0.8 !important;
}

/* Research Gap Split Layout */
.gaps-content-split {
  display: grid !important;
  grid-template-columns: 80px 1fr !important;
  gap: 0.3cm !important;
  align-items: center !important;
  flex: 1 !important;
  overflow: hidden !important;
}

.gap-anime-container {
  height: 220px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  border-radius: 10px !important;
}

.gap-anime-img {
  height: 100% !important;
  width: auto !important;
  object-fit: cover !important;
  border-radius: 8px !important;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.5)) !important;
}

.gap-items-col {
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
}

.gap-card-box {
  border-radius: 10px !important;
  padding: 8px 10px !important;
}

.gap-card-box.border-purple {
  background: rgba(139, 92, 246, 0.1) !important;
  border: 1px solid rgba(139, 92, 246, 0.35) !important;
}

.gap-card-box.border-blue {
  background: rgba(6, 182, 212, 0.1) !important;
  border: 1px solid rgba(6, 182, 212, 0.35) !important;
}

.gap-box-top {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  margin-bottom: 3px !important;
}

.gap-num-title {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.gap-index-text {
  font-size: 10.5px !important;
  font-weight: 800 !important;
  color: #c084fc !important;
}

.gap-title-text {
  font-size: 10.5px !important;
  font-weight: 800 !important;
  color: #f8fafc !important;
}

.gap-tag-pill {
  font-size: 8.5px !important;
  font-weight: 700 !important;
  padding: 1.5px 6px !important;
  border-radius: 4px !important;
}

.gap-tag-pill.tag-high {
  background: rgba(239, 68, 68, 0.2) !important;
  color: #f87171 !important;
  border: 1px solid rgba(239, 68, 68, 0.4) !important;
}

.gap-tag-pill.tag-medium {
  background: rgba(245, 158, 11, 0.2) !important;
  color: #fbbf24 !important;
  border: 1px solid rgba(245, 158, 11, 0.4) !important;
}

.gap-desc-text {
  font-size: 9.5px !important;
  color: #94a3b8 !important;
  line-height: 1.35 !important;
  margin-bottom: 4px !important;
}

.gap-meta-row {
  display: flex !important;
  justify-content: space-between !important;
  font-size: 8.5px !important;
  font-weight: 700 !important;
  color: #a78bfa !important;
}

.carousel-dots-row {
  display: flex !important;
  justify-content: center !important;
  gap: 5px !important;
  margin-top: 6px !important;
}

.dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #1e2548;
  display: inline-block;
}

.dot.active {
  background: #8b5cf6;
  box-shadow: 0 0 6px #8b5cf6;
}

/* AI Insight Card */
.insight-card-layout {
  display: grid !important;
  grid-template-columns: 1.35fr 0.65fr !important;
  gap: 0.3cm !important;
  align-items: center !important;
  height: 310px !important;
}

.insight-left-col {
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  height: 100% !important;
  padding: 2px 0 !important;
}

.insight-quote-box {
  font-size: 11px !important;
  line-height: 1.45 !important;
  color: #e2e8f0 !important;
  font-style: italic !important;
  margin: 6px 0 !important;
  max-height: 165px !important;
  overflow-y: auto !important;
  background: rgba(8, 11, 26, 0.6) !important;
  border-left: 3px solid #8b5cf6 !important;
  padding: 8px 10px !important;
  border-radius: 0 8px 8px 0 !important;
}

.insight-tags-row {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 5px !important;
}

.insight-topic-tag {
  background: rgba(139, 92, 246, 0.15) !important;
  color: #c084fc !important;
  border: 1px solid rgba(139, 92, 246, 0.35) !important;
  font-size: 9px !important;
  font-weight: 700 !important;
  padding: 2.5px 7px !important;
  border-radius: 5px !important;
}

.insight-anime-container {
  height: 245px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  border-radius: 10px !important;
}

.insight-anime-img {
  height: 100% !important;
  width: auto !important;
  object-fit: contain !important;
  filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.5)) !important;
}

/* =================================================== */
/* 6. FOOTER CTA BANNER & BUTTON                       */
/* =================================================== */
.footer-cta-row {
  background: linear-gradient(135deg, #0d1126 0%, #151b3d 100%) !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 12px 20px !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  box-shadow: var(--card-shadow) !important;
  height: 52px !important;
  box-sizing: border-box !important;
  margin-left: calc(-235px - 0.3cm) !important;
  width: calc(100% + 235px + 0.3cm) !important;
  max-width: calc(100% + 235px + 0.3cm) !important;
}

.footer-cta-left {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  font-size: 13px !important;
  color: #e2e8f0 !important;
}

.footer-sparkle {
  font-size: 18px !important;
  color: #a78bfa !important;
}

.btn-footer-cta {
  width: 340px !important;
  min-width: 330px !important;
  max-width: 360px !important;
  height: 44px !important;
  font-size: 13.5px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.btn-primary-gradient {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  border-radius: 11px !important;
  border: none !important;
  padding: 9px 18px !important;
  box-shadow: 0 4px 18px rgba(139, 92, 246, 0.45) !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
  white-space: nowrap !important;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px rgba(139, 92, 246, 0.6) !important;
}

/* =================================================== */
/* 7. CHAT WITH LITERATURE - ARIA ANIME ASSISTANT UI   */
/* =================================================== */
.chat-view-container {
  background: #0d1126 !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 20px 24px !important;
  box-shadow: var(--card-shadow) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 16px !important;
  box-sizing: border-box !important;
  width: 100% !important;
}

.chat-header-banner {
  background: #080b1a !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  padding: 14px 18px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
  position: relative !important;
}

.chat-header-left {
  display: flex !important;
  align-items: center !important;
  gap: 14px !important;
}

.chat-avatar-frame {
  position: relative !important;
  width: 50px !important;
  height: 50px !important;
  min-width: 50px !important;
  border-radius: 50% !important;
  padding: 2px !important;
  background: #141a38 !important;
  border: 1px solid #8b5cf6 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.4) !important;
}

.chat-assistant-hero-img {
  width: 100% !important;
  height: 100% !important;
  border-radius: 50% !important;
  object-fit: cover !important;
  background: #0d1126 !important;
}

.chat-online-dot {
  position: absolute !important;
  bottom: 0px !important;
  right: 0px !important;
  width: 12px !important;
  height: 12px !important;
  background: #10b981 !important;
  border: 2px solid #080b1a !important;
  border-radius: 50% !important;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.8) !important;
}

.chat-header-info {
  display: flex !important;
  flex-direction: column !important;
  gap: 3px !important;
}

.chat-assistant-name {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.chat-title-separator {
  color: #64748b !important;
  font-weight: 400 !important;
}

.chat-assistant-role {
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: #a78bfa !important;
}

.chat-badge-status {
  font-size: 10px !important;
  font-weight: 700 !important;
  color: #34d399 !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  padding: 1px 6px !important;
  border-radius: 10px !important;
  margin-left: 4px !important;
}

.chat-assistant-desc {
  font-size: 12px !important;
  color: #94a3b8 !important;
  line-height: 1.4 !important;
}

.chat-stats-pill {
  background: #080b1a !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 20px !important;
  padding: 4px 12px !important;
  display: flex !important;
  align-items: center !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

.chat-stat-text {
  font-size: 11px !important;
  color: #94a3b8 !important;
}

.chat-stat-text strong {
  color: #f8fafc !important;
  font-weight: 600 !important;
}

.chat-main-row {
  display: flex !important;
  flex-direction: row !important;
  gap: 0.3cm !important;
  width: 100% !important;
  align-items: stretch !important;
}

.chat-left-sidebar {
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  flex: 0 0 30% !important;
  max-width: 320px !important;
  box-sizing: border-box !important;
}

.chat-right-area {
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
  flex: 1 1 70% !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
}

.ren-agent-card {
  background: #080b1a !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  padding: 14px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 12px !important;
}

.ren-card-header {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  text-align: center !important;
  gap: 8px !important;
}

.ren-portrait-box {
  width: 90px !important;
  height: 90px !important;
  border-radius: 14px !important;
  padding: 2px !important;
  background: #0d1126 !important;
  border: 1px solid var(--border-subtle) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
  overflow: hidden !important;
}

.ren-full-portrait-img {
  width: 100% !important;
  height: 100% !important;
  border-radius: 12px !important;
  object-fit: cover !important;
}

.ren-name-title {
  font-size: 14.5px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
}

.ren-subtitle {
  font-size: 11px !important;
  color: #94a3b8 !important;
}

.ren-session-summary-box {
  background: #0d1126 !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  padding: 10px 12px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}

.ren-summary-row {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  font-size: 11px !important;
}

.summary-label {
  color: #94a3b8 !important;
  font-weight: 500 !important;
}

.summary-val {
  color: #f8fafc !important;
  font-weight: 600 !important;
}

.summary-val.highlight-val {
  color: #c084fc !important;
  font-weight: 700 !important;
}

.quick-actions-title {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #a78bfa !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
  margin-top: 2px !important;
  margin-bottom: 2px !important;
}

.quick-buttons-col {
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}

.btn-quick-action {
  background: #0d1126 !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important;
  color: #e2e8f0 !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  padding: 8px 12px !important;
  text-align: left !important;
  justify-content: flex-start !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  border-left: 3px solid #8b5cf6 !important;
  line-height: 1.3 !important;
}

.btn-quick-action:hover {
  background: #141a38 !important;
  border-color: #8b5cf6 !important;
  color: #ffffff !important;
}

/* Chatbot container & message bubbles */
.literature-chatbot-box {
  background: #080b1a !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 14px !important;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.4) !important;
  padding: 12px !important;
}

.literature-chatbot-box .message-wrap {
  gap: 14px !important;
}

.literature-chatbot-box .message.user {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
  color: #ffffff !important;
  border-radius: 16px 16px 4px 16px !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
  border: none !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  padding: 12px 16px !important;
}

.literature-chatbot-box .message.user p {
  color: #ffffff !important;
  margin: 0 !important;
}

.literature-chatbot-box .message.bot {
  background: #0d1126 !important;
  color: #f8fafc !important;
  border: 1px solid #1e2548 !important;
  border-radius: 16px 16px 16px 4px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
  font-size: 13.5px !important;
  line-height: 1.55 !important;
  padding: 14px 18px !important;
}

.literature-chatbot-box .message.bot h1,
.literature-chatbot-box .message.bot h2,
.literature-chatbot-box .message.bot h3 {
  color: #c084fc !important;
  font-weight: 800 !important;
  margin-top: 10px !important;
  margin-bottom: 4px !important;
}

.literature-chatbot-box .message.bot strong {
  color: #a78bfa !important;
  font-weight: 700 !important;
}

.literature-chatbot-box .avatar-container {
  width: 38px !important;
  height: 38px !important;
  min-width: 38px !important;
  border-radius: 50% !important;
  overflow: hidden !important;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.4) !important;
  border: 1.5px solid #8b5cf6 !important;
}

/* Chat Input Controls */
.chat-input-row {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 10px !important;
  margin-top: 6px !important;
}

.chat-textbox-input input,
.chat-textbox-input textarea {
  height: 44px !important;
  min-height: 44px !important;
  max-height: 44px !important;
  line-height: 42px !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  border-radius: 12px !important;
  border: 1px solid #1e2548 !important;
  padding: 0 16px !important;
  background: #080b1a !important;
  color: #f8fafc !important;
  transition: all 0.2s ease !important;
}

.chat-textbox-input input:focus,
.chat-textbox-input textarea:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25) !important;
}

.btn-chat-send {
  height: 44px !important;
  min-height: 44px !important;
  border-radius: 12px !important;
  font-size: 13.5px !important;
}

.btn-chat-clear {
  height: 44px !important;
  min-height: 44px !important;
  border-radius: 12px !important;
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  color: #94a3b8 !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  transition: all 0.15s ease !important;
}

.btn-chat-mic {
  height: 44px !important;
  min-height: 44px !important;
  width: 44px !important;
  min-width: 44px !important;
  border-radius: 12px !important;
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  color: #a78bfa !important;
  font-size: 18px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
}

.btn-chat-mic:hover {
  background: #141a38 !important;
  border-color: #8b5cf6 !important;
  color: #c084fc !important;
  transform: translateY(-1px) !important;
}

.btn-chat-mic.recording-pulse {
  background: rgba(239, 68, 68, 0.2) !important;
  border-color: #ef4444 !important;
  color: #f87171 !important;
  animation: micPulseGlow 1.2s infinite ease-in-out !important;
}

@keyframes micPulseGlow {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); transform: scale(1); }
  50% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); transform: scale(1.05); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); transform: scale(1); }
}

.chat-voice-row {
  margin-top: 6px !important;
  padding: 8px 12px !important;
  background: #080b1a !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
}

.voice-status-pill {
  display: inline-flex !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 5px 14px !important;
  margin-bottom: 6px !important;
  border-radius: 20px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
}

.voice-status-active {
  background: rgba(239, 68, 68, 0.2) !important;
  border: 1px solid #f87171 !important;
  color: #f87171 !important;
}

.voice-status-error {
  background: rgba(245, 158, 11, 0.2) !important;
  border: 1px solid #fbbf24 !important;
  color: #fbbf24 !important;
}

.voice-pulse-dot {
  width: 9px !important;
  height: 9px !important;
  background: #ef4444 !important;
  border-radius: 50% !important;
  display: inline-block !important;
  animation: pulseMicDot 1s infinite alternate ease-in-out !important;
}

@keyframes pulseMicDot {
  from { opacity: 0.3; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1.3); }
}

.chat-view-container .gr-sample-pill {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  border-radius: 20px !important;
  padding: 6px 14px !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  color: #e2e8f0 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}

.chat-view-container .gr-sample-pill:hover {
  background: #141a38 !important;
  border-color: #8b5cf6 !important;
  color: #c084fc !important;
  transform: translateY(-1px) !important;
}

/* =================================================== */
/* 8. GENERAL STYLES FOR SUBPAGES                      */
/* =================================================== */
.search-page-container,
.upload-page-container,
.analysis-page-container,
.comparison-page-container,
.gaps-page-container,
.review-page-container {
  background: #0d1126 !important;
  border-radius: 16px !important;
  border: 1px solid var(--border-subtle) !important;
  padding: 20px 24px !important;
  box-shadow: var(--card-shadow) !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 16px !important;
  box-sizing: border-box !important;
  width: 100% !important;
}

/* Dataframe and Tables dark styling */
.gradio-dataframe,
table, thead, tbody, th, td {
  background-color: #080b1a !important;
  color: #f8fafc !important;
  border-color: #1e2548 !important;
}

th {
  background-color: #0d1126 !important;
  color: #c084fc !important;
  font-weight: 700 !important;
}

/* Accordions */
.gradio-accordion {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  border-radius: 12px !important;
}

/* Markdown prose */
.prose {
  color: #f8fafc !important;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
  color: #c084fc !important;
}

.prose p, .prose li {
  color: #e2e8f0 !important;
}

.prose strong {
  color: #a78bfa !important;
}

/* =================================================== */
/* ANIMATIONS                                          */
/* =================================================== */
@keyframes starTwinkle {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.15); }
}

@keyframes pulseGlow {
  0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.6); }
  70% { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
}

@keyframes statusPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
}

/* =================================================== */
/* 9. PLOTLY CHARTS & COMPARISON ANALYTICS             */
/* =================================================== */
.comparison-view .gr-plot,
.comparison-page-container .gr-plot,
div[data-testid="plot"],
.js-plotly-plot,
.plotly,
.plot-container {
  background: #0d1126 !important;
  border-radius: 14px !important;
  border: 1px solid #1e2548 !important;
  box-shadow: var(--card-shadow) !important;
  overflow: hidden !important;
}

.js-plotly-plot .plotly .main-svg {
  border-radius: 14px !important;
}

.modebar-container {
  background: rgba(8, 11, 26, 0.8) !important;
  border-radius: 8px !important;
  border: 1px solid #1e2548 !important;
}

.modebar-btn {
  color: #94a3b8 !important;
}

.modebar-btn:hover {
  color: #c084fc !important;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition-duration: 0.01ms !important;
  }
}

/* =================================================== */
/* THEME SWITCHER TOGGLE PILL                          */
/* =================================================== */
.theme-toggle-container {
  width: 100% !important;
  margin: 10px 0 14px 0 !important;
}

.theme-toggle-track {
  width: 100% !important;
  height: 36px !important;
  border-radius: 18px !important;
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0 12px !important;
  cursor: pointer !important;
  position: relative !important;
  user-select: none !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
  box-sizing: border-box !important;
}

.theme-toggle-track:hover {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.25) !important;
}

.theme-toggle-icon {
  font-size: 14px !important;
  transition: transform 0.3s ease !important;
}

.theme-toggle-label {
  font-size: 11px !important;
  font-weight: 700 !important;
  color: #c084fc !important;
  letter-spacing: 0.3px !important;
  text-transform: uppercase !important;
}

.theme-toggle-knob {
  width: 16px !important;
  height: 16px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%) !important;
  box-shadow: 0 0 10px rgba(167, 139, 250, 0.8) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.theme-toggle-track.active-light {
  background: #e2e8f0 !important;
  border-color: #cbd5e1 !important;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.theme-toggle-track.active-light .theme-toggle-label {
  color: #4338ca !important;
}

.theme-toggle-track.active-light .theme-toggle-knob {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.8) !important;
}

/* =================================================== */
/* LIGHT ACADEMIC THEME (EXACT MATCH TO SCREENSHOT 1)  */
/* =================================================== */
body.light-theme,
.gradio-container.light-theme,
html.light-theme,
.light-theme {
  --bg-main: #f8fafc !important;
  --card-bg: #ffffff !important;
  --card-bg-gradient: linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%) !important;
  --card-border: #e2e8f0 !important;
  --border-subtle: #e2e8f0 !important;
  --border-focus: #6366f1 !important;
  --text-dark: #0f172a !important;
  --text-main: #0f172a !important;
  --text-muted: #475569 !important;
  --text-dim: #64748b !important;
  --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
  --card-hover-shadow: 0 10px 25px rgba(99, 102, 241, 0.12) !important;
  background-color: #f8fafc !important;
  color: #0f172a !important;
}

/* 1. Sidebar in Light Theme */
.light-theme .sidebar-container {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .brand-title {
  color: #0f172a !important;
}

.light-theme .brand-subtitle {
  color: #64748b !important;
}

.light-theme .brand-sparkle-logo {
  color: #6366f1 !important;
  text-shadow: none !important;
}

.light-theme .nav-tabs-container label {
  background: transparent !important;
  color: #475569 !important;
  border-color: transparent !important;
}

.light-theme .nav-tabs-container label:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

.light-theme .nav-tabs-container label.selected,
.light-theme .nav-tabs-container label:has(input:checked) {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  border: 1px solid #c7d2fe !important;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1) !important;
  font-weight: 700 !important;
}

.light-theme .sidebar-astronaut-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .sidebar-status-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .sidebar-sec-label {
  color: #64748b !important;
}

.light-theme .system-status-indicator {
  color: #0f172a !important;
}

.light-theme .api-chip {
  color: #64748b !important;
}

.light-theme .api-chip-badge {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  color: #6366f1 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

.light-theme .session-active-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
}

.light-theme .session-card-title {
  color: #0f172a !important;
}

.light-theme .session-card-state {
  color: #10b981 !important;
}

/* 2. Top Walker Scout Track */
.light-theme .top-walker-track {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .walker-status-pill {
  background: #eef2ff !important;
  border: 1px solid #c7d2fe !important;
  color: #4338ca !important;
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.1) !important;
}

.light-theme .walker-track-glow {
  background: linear-gradient(90deg, transparent, #818cf8, #c084fc, transparent) !important;
  opacity: 0.3 !important;
}

/* 3. Hero Banner Card */
.light-theme .hero-banner-card,
.light-theme .hero-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .hero-greeting {
  color: #475569 !important;
}

.light-theme .hero-headline {
  color: #0f172a !important;
}

.light-theme .highlight-purple {
  color: #6366f1 !important;
  text-shadow: none !important;
  font-weight: 800 !important;
}

.light-theme .hero-subtitle {
  color: #64748b !important;
}

.light-theme .user-profile-badge-top,
.light-theme .user-profile-badge {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .user-name {
  color: #0f172a !important;
}

.light-theme .user-badge-plan {
  color: #059669 !important;
  background: #ecfdf5 !important;
  border: 1px solid #a7f3d0 !important;
}

/* 4. Research Control Card & Filters */
.light-theme .research-control-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .filter-header-label,
.light-theme .hero-topic-textbox label span,
.light-theme .hero-topic-textbox span.block-label {
  color: #4338ca !important;
  font-weight: 800 !important;
}

.light-theme .hero-topic-textbox input,
.light-theme .hero-topic-textbox textarea {
  background: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  color: #0f172a !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .hero-topic-textbox input:focus,
.light-theme .hero-topic-textbox textarea:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

.light-theme .year-select-box .wrap,
.light-theme .year-select-box .select-wrap,
.light-theme .max-select-box .wrap,
.light-theme .max-select-box .select-wrap {
  background: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .year-select-box input,
.light-theme .year-select-box select,
.light-theme .max-select-box input {
  color: #0f172a !important;
}

.light-theme .year-hyphen {
  color: #64748b !important;
}

.light-theme .btn-sources-config-icon {
  background: #eef2ff !important;
  color: #4338ca !important;
  border: 1px solid #c7d2fe !important;
}

.light-theme .sources-chips-group label {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  color: #334155 !important;
}

.light-theme .sources-chips-group label:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

.light-theme .sources-chips-group label.selected,
.light-theme .sources-chips-group label:has(input:checked) {
  background: #eef2ff !important;
  color: #4338ca !important;
  border: 1px solid #818cf8 !important;
}

.light-theme .btn-start-review-main {
  background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
}

/* 5. Stat Cards */
.light-theme .stat-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .stat-header {
  color: #64748b !important;
}

.light-theme .stat-value {
  color: #0f172a !important;
}

.light-theme .stat-value.text-green {
  color: #059669 !important;
  text-shadow: none !important;
}

.light-theme .stat-caption {
  color: #94a3b8 !important;
}

/* 6. Pipeline Card */
.light-theme .pipeline-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .card-title-pill {
  color: #4338ca !important;
}

.light-theme .pipeline-status-indicator {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 1px solid #a7f3d0 !important;
}

.light-theme .step-circle.completed {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 2px solid #10b981 !important;
  box-shadow: none !important;
}

.light-theme .step-circle.active {
  background: #6366f1 !important;
  color: #ffffff !important;
  border: 2px solid #4f46e5 !important;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.4) !important;
}

.light-theme .step-circle.pending {
  background: #f1f5f9 !important;
  color: #94a3b8 !important;
  border: 2px solid #e2e8f0 !important;
}

.light-theme .step-label {
  color: #0f172a !important;
}

.light-theme .pipeline-progress-track {
  background: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .pipeline-progress-bar {
  background: linear-gradient(90deg, #10b981, #6366f1, #8b5cf6) !important;
}

/* 7. Upload Card & Summary */
.light-theme .upload-card-wrapper,
.light-theme .upload-col {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .dropzone-box-tight > div,
.light-theme .dropzone-box-tight .upload-container,
.light-theme .dropzone-box-tight .file-upload,
.light-theme .dropzone-box-tight button,
.light-theme .dropzone-box-tight .wrap {
  background: #f8fafc !important;
  border: 2px dashed #cbd5e1 !important;
  color: #4338ca !important;
}

.light-theme .dropzone-box-tight:hover > div,
.light-theme .dropzone-box-tight:hover .upload-container {
  border-color: #6366f1 !important;
  background: #eef2ff !important;
}

.light-theme .upload-action-btn {
  background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
  color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3) !important;
}

.light-theme .upload-summary-title {
  color: #64748b !important;
}

.light-theme .view-all-link {
  color: #6366f1 !important;
}

.light-theme .paper-file-item {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .file-name-text {
  color: #0f172a !important;
}

.light-theme .file-meta-text {
  color: #64748b !important;
}

.light-theme .pdf-icon-badge {
  color: #ef4444 !important;
}

.light-theme .file-check-badge {
  color: #10b981 !important;
}

.light-theme .upload-summary-footer {
  color: #64748b !important;
  border-top: 1px solid #e2e8f0 !important;
}

/* 8. Bottom 3 Panels (Top Papers, Gaps, AI Insight) */
.light-theme .dashboard-panel-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .view-all-link {
  color: #4f46e5 !important;
}

.light-theme .view-all-link:hover {
  color: #4338ca !important;
  background: #eef2ff !important;
}

.light-theme .paper-row-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .paper-row-card:hover {
  border-color: #6366f1 !important;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1) !important;
}

.light-theme .paper-rank-badge {
  background: #eef2ff !important;
  color: #4338ca !important;
  border: 1px solid #c7d2fe !important;
}

.light-theme .paper-title-text {
  color: #0f172a !important;
}

.light-theme .paper-authors-text {
  color: #475569 !important;
}

.light-theme .paper-meta-text {
  color: #64748b !important;
}

.light-theme .relevance-pill {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 1px solid #a7f3d0 !important;
}

.light-theme .bookmark-icon {
  color: #6366f1 !important;
}

.light-theme .gap-card-box.border-purple {
  background: #f5f3ff !important;
  border: 1px solid #ddd6fe !important;
}

.light-theme .gap-card-box.border-blue {
  background: #f0f9ff !important;
  border: 1px solid #bae6fd !important;
}

.light-theme .gap-index-text {
  color: #6366f1 !important;
}

.light-theme .gap-title-text {
  color: #0f172a !important;
}

.light-theme .gap-tag-pill.tag-high {
  background: #fee2e2 !important;
  color: #dc2626 !important;
  border: 1px solid #fecaca !important;
}

.light-theme .gap-tag-pill.tag-medium {
  background: #fef3c7 !important;
  color: #d97706 !important;
  border: 1px solid #fde68a !important;
}

.light-theme .gap-desc-text {
  color: #334155 !important;
}

.light-theme .gap-meta-row {
  color: #6366f1 !important;
}

.light-theme .dot {
  background: #e2e8f0 !important;
}

.light-theme .dot.active {
  background: #6366f1 !important;
  box-shadow: 0 0 6px rgba(99, 102, 241, 0.4) !important;
}

.light-theme .insight-quote-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-left: 3px solid #6366f1 !important;
  color: #334155 !important;
}

.light-theme .insight-topic-tag {
  background: #eef2ff !important;
  color: #4338ca !important;
  border: 1px solid #c7d2fe !important;
}

/* 9. Footer CTA Banner */
.light-theme .footer-cta-row {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .footer-cta-left {
  color: #0f172a !important;
}

.light-theme .footer-sparkle {
  color: #6366f1 !important;
}

.light-theme .btn-footer-cta,
.light-theme .btn-primary-gradient {
  background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
}

/* 10. Sources Modal in Light Theme */
.light-theme .sources-modal-box {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
}

.light-theme .modal-title {
  color: #0f172a !important;
}

.light-theme .modal-subtitle {
  color: #64748b !important;
}

.light-theme .btn-modal-close-icon {
  background: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
  color: #64748b !important;
}

.light-theme .modal-sources-checklist {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .modal-sources-checklist label {
  color: #0f172a !important;
}

.light-theme .source-detail-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .source-name {
  color: #0f172a !important;
}

.light-theme .source-coverage,
.light-theme .source-desc {
  color: #64748b !important;
}

.light-theme .btn-modal-cancel {
  background: #f1f5f9 !important;
  color: #64748b !important;
  border: 1px solid #e2e8f0 !important;
}

/* 11. Chat Assistant View in Light Theme */
.light-theme .chat-view-container {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .chat-header-banner {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .chat-avatar-frame {
  background: #eef2ff !important;
  border-color: #c7d2fe !important;
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.2) !important;
}

.light-theme .chat-assistant-name {
  color: #0f172a !important;
}

.light-theme .chat-assistant-role {
  color: #6366f1 !important;
}

.light-theme .chat-assistant-desc {
  color: #475569 !important;
}

.light-theme .chat-stats-pill {
  background: #f1f5f9 !important;
  border: 1px solid #cbd5e1 !important;
}

.light-theme .chat-stat-text {
  color: #475569 !important;
}

.light-theme .chat-stat-text strong {
  color: #0f172a !important;
}

/* Salim Ren Agent Card in Light Theme */
.light-theme .ren-agent-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .ren-portrait-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
}

.light-theme .ren-name-title {
  color: #0f172a !important;
}

.light-theme .ren-subtitle {
  color: #64748b !important;
}

.light-theme .ren-session-summary-box {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .summary-label {
  color: #64748b !important;
}

.light-theme .summary-val {
  color: #0f172a !important;
}

.light-theme .summary-val.highlight-val {
  color: #6366f1 !important;
}

.light-theme .quick-actions-title {
  color: #4338ca !important;
}

.light-theme .btn-quick-action {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  border-left: 3px solid #6366f1 !important;
  color: #334155 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .btn-quick-action:hover {
  background: #eef2ff !important;
  border-color: #818cf8 !important;
  color: #4338ca !important;
}

/* Chatbot Messages in Light Theme */
.light-theme .literature-chatbot-box {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.03) !important;
}

.light-theme .literature-chatbot-box .message.bot {
  background: #f8fafc !important;
  color: #0f172a !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .literature-chatbot-box .message.bot h1,
.light-theme .literature-chatbot-box .message.bot h2,
.light-theme .literature-chatbot-box .message.bot h3 {
  color: #4338ca !important;
}

.light-theme .literature-chatbot-box .message.bot strong {
  color: #4338ca !important;
}

.light-theme .literature-chatbot-box .message.bot p,
.light-theme .literature-chatbot-box .message.bot li {
  color: #334155 !important;
}

.light-theme .literature-chatbot-box .message.user {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
}

.light-theme .literature-chatbot-box .message.user p {
  color: #ffffff !important;
}

.light-theme .literature-chatbot-box .avatar-container {
  border-color: #818cf8 !important;
  box-shadow: 0 0 8px rgba(99, 102, 241, 0.2) !important;
}

.light-theme .chat-textbox-input input,
.light-theme .chat-textbox-input textarea {
  background: #ffffff !important;
  border: 1px solid #cbd5e1 !important;
  color: #0f172a !important;
}

.light-theme .chat-textbox-input input:focus,
.light-theme .chat-textbox-input textarea:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

.light-theme .btn-chat-mic {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  color: #6366f1 !important;
}

.light-theme .btn-chat-clear {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  color: #64748b !important;
}

.light-theme .btn-whisper-toggle {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  color: #475569 !important;
}

.light-theme .chat-view-container .gr-sample-pill {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  color: #334155 !important;
}

.light-theme .chat-view-container .gr-sample-pill:hover {
  background: #eef2ff !important;
  border-color: #818cf8 !important;
  color: #4338ca !important;
}

.light-theme .chat-voice-row {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

/* 12. Subpages (Search, Upload, Analysis, Comparison, Gaps, Review) */
.light-theme .search-page-container,
.light-theme .upload-page-container,
.light-theme .analysis-page-container,
.light-theme .comparison-page-container,
.light-theme .gaps-page-container,
.light-theme .review-page-container {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04) !important;
  color: #0f172a !important;
}

.light-theme .search-page-container input,
.light-theme .search-page-container textarea,
.light-theme .search-page-container .wrap,
.light-theme .search-page-container .select-wrap,
.light-theme .analysis-page-container input,
.light-theme .analysis-page-container textarea,
.light-theme .analysis-page-container .wrap,
.light-theme .gaps-page-container input,
.light-theme .gaps-page-container textarea,
.light-theme .gaps-page-container .wrap,
.light-theme .comparison-page-container input,
.light-theme .comparison-page-container textarea,
.light-theme .comparison-page-container .wrap {
  background-color: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #0f172a !important;
}

.light-theme .search-page-container label,
.light-theme .analysis-page-container label,
.light-theme .gaps-page-container label,
.light-theme .comparison-page-container label {
  color: #475569 !important;
}

.light-theme .search-page-container .checkbox-label,
.light-theme .search-page-container label span,
.light-theme .analysis-page-container label span,
.light-theme .gaps-page-container label span,
.light-theme .comparison-page-container label span {
  color: #334155 !important;
  font-weight: 600 !important;
}

.light-theme .search-page-container button:not(.btn-primary-gradient),
.light-theme .analysis-page-container button:not(.btn-primary-gradient),
.light-theme .gaps-page-container button:not(.btn-primary-gradient),
.light-theme .comparison-page-container button:not(.btn-primary-gradient) {
  background: #f8fafc !important;
  border: 1px solid #cbd5e1 !important;
  color: #334155 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .search-page-container button:not(.btn-primary-gradient):hover,
.light-theme .analysis-page-container button:not(.btn-primary-gradient):hover,
.light-theme .gaps-page-container button:not(.btn-primary-gradient):hover,
.light-theme .comparison-page-container button:not(.btn-primary-gradient):hover {
  background: #eef2ff !important;
  border-color: #818cf8 !important;
  color: #4338ca !important;
}

.light-theme .gradio-dataframe,
.light-theme table,
.light-theme tbody,
.light-theme td {
  background-color: #ffffff !important;
  color: #0f172a !important;
  border-color: #e2e8f0 !important;
}

.light-theme th {
  background-color: #f1f5f9 !important;
  color: #4338ca !important;
  border-color: #e2e8f0 !important;
  font-weight: 700 !important;
}

.light-theme .gradio-accordion {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}

.light-theme .prose {
  color: #0f172a !important;
}

.light-theme .prose h1,
.light-theme .prose h2,
.light-theme .prose h3,
.light-theme .prose h4 {
  color: #4338ca !important;
}

.light-theme .prose p,
.light-theme .prose li {
  color: #334155 !important;
}

.light-theme .prose strong {
  color: #0f172a !important;
}

.light-theme h1, .light-theme h2, .light-theme h3, .light-theme h4, .light-theme h5 {
  color: #0f172a !important;
}

.light-theme p, .light-theme td {
  color: #334155 !important;
}

.light-theme strong {
  color: #0f172a !important;
}

.light-theme textarea,
.light-theme input {
  color: #0f172a !important;
}

.light-theme .comparison-view .gr-plot,
.light-theme .comparison-page-container .gr-plot,
.light-theme div[data-testid="plot"],
.light-theme .js-plotly-plot,
.light-theme .plotly,
.light-theme .plot-container,
.light-theme .plotly-chart-container {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

/* =================================================== */
/* DARK THEME SPECIFIC (body:not(.light-theme))         */
/* =================================================== */
body:not(.light-theme),
html:not(.light-theme),
.gradio-container:not(.light-theme) {
  background-color: #060814 !important;
  color: #f8fafc !important;
}

body:not(.light-theme) .sidebar-container {
  background: #0b0e23 !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .hero-banner-card,
body:not(.light-theme) .hero-card {
  background: linear-gradient(135deg, #0d1126 0%, #111636 100%) !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .research-control-card {
  background: #0d1126 !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .hero-topic-textbox input,
body:not(.light-theme) .hero-topic-textbox textarea {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  color: #f8fafc !important;
}

body:not(.light-theme) .year-select-box .wrap,
body:not(.light-theme) .year-select-box .select-wrap,
body:not(.light-theme) .max-select-box .wrap,
body:not(.light-theme) .max-select-box .select-wrap {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  color: #f8fafc !important;
}

body:not(.light-theme) .year-select-box input,
body:not(.light-theme) .max-select-box input {
  color: #f8fafc !important;
}

body:not(.light-theme) .stat-card {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%) !important;
  border: 1px solid #1e2548 !important;
  color: #f8fafc !important;
}

body:not(.light-theme) .stat-value {
  color: #f8fafc !important;
}

body:not(.light-theme) .stat-caption {
  color: #64748b !important;
}

body:not(.light-theme) .pipeline-card,
body:not(.light-theme) .upload-card-wrapper {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%) !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .dashboard-panel-card {
  background: linear-gradient(145deg, #0d1126 0%, #101535 100%) !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .paper-row-card {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .paper-title-text {
  color: #f8fafc !important;
}

body:not(.light-theme) .footer-cta-row {
  background: linear-gradient(135deg, #0d1126 0%, #151b3d 100%) !important;
  border: 1px solid #1e2548 !important;
  color: #e2e8f0 !important;
}

body:not(.light-theme) .footer-cta-left {
  color: #e2e8f0 !important;
}

/* Dark Theme Chat Specifics */
body:not(.light-theme) .chat-view-container {
  background: #0d1126 !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .chat-header-banner {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .ren-agent-card {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .ren-portrait-box {
  background: #0d1126 !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .ren-name-title {
  color: #f8fafc !important;
}

body:not(.light-theme) .ren-subtitle {
  color: #94a3b8 !important;
}

body:not(.light-theme) .ren-session-summary-box {
  background: #0d1126 !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .summary-label {
  color: #94a3b8 !important;
}

body:not(.light-theme) .summary-val {
  color: #f8fafc !important;
}

body:not(.light-theme) .btn-quick-action {
  background: #0d1126 !important;
  border: 1px solid #1e2548 !important;
  color: #e2e8f0 !important;
}

body:not(.light-theme) .literature-chatbot-box {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .literature-chatbot-box .message.bot {
  background: #0d1126 !important;
  color: #f8fafc !important;
  border: 1px solid #1e2548 !important;
}

body:not(.light-theme) .chat-textbox-input input,
body:not(.light-theme) .chat-textbox-input textarea {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
  color: #f8fafc !important;
}

body:not(.light-theme) .btn-chat-mic,
body:not(.light-theme) .btn-chat-clear {
  background: #080b1a !important;
  border: 1px solid #1e2548 !important;
}

/* =================================================== */
/* SUBPAGES: SEARCH, ANALYSIS, GAPS, COMPARISON (DARK) */
/* =================================================== */

/* 1. Search Cards */
.search-result-card {
  background: #0d1126;
  border-radius: 16px;
  border: 1px solid #1e2548;
  padding: 20px;
  margin-bottom: 14px;
  box-shadow: var(--card-shadow);
  transition: all 0.2s ease;
}
.search-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}
.search-header-left {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.search-idx-tag {
  background: rgba(139, 92, 246, 0.25);
  color: #c084fc;
  font-weight: 800;
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid rgba(139, 92, 246, 0.4);
}
.search-card-title {
  font-size: 15px;
  font-weight: 700;
  color: #f8fafc;
  line-height: 1.3;
}
.search-card-authors {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}
.search-relevance-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  font-weight: 800;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid rgba(16, 185, 129, 0.4);
}
.search-abstract-box {
  font-size: 12.5px;
  color: #cbd5e1;
  line-height: 1.5;
  margin: 12px 0;
  background: #080b1a;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #1e2548;
}
.search-card-footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #94a3b8;
  border-top: 1px solid #1e2548;
  padding-top: 10px;
}
.search-footer-left {
  display: flex;
  gap: 12px;
  align-items: center;
}
.search-source-badge {
  background: #141a38;
  color: #a78bfa;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid #1e2548;
}
.search-footer-right {
  display: flex;
  gap: 10px;
  align-items: center;
}
.search-oa-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 6px;
  border: 1px solid rgba(16, 185, 129, 0.3);
  text-decoration: none;
}
.search-doi-text {
  color: #64748b;
}
.search-doi-link {
  color: #8b5cf6;
  text-decoration: underline;
}
.search-view-source-link {
  color: #c084fc;
  font-weight: 600;
  text-decoration: none;
}

/* 2. Analysis Cards */
.analysis-result-card {
  background: #0d1126;
  border-radius: 18px;
  border: 1px solid #1e2548;
  padding: 22px;
  margin-bottom: 20px;
  box-shadow: var(--card-shadow);
}
.analysis-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}
.analysis-badge-row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 6px;
}
.analysis-idx-badge {
  background: rgba(139, 92, 246, 0.25);
  color: #c084fc;
  font-weight: 800;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(139, 92, 246, 0.4);
}
.analysis-domain-badge {
  background: #080b1a;
  color: #94a3b8;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid #1e2548;
}
.analysis-source-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.analysis-card-title {
  font-size: 16px;
  font-weight: 800;
  color: #f8fafc;
  margin: 0;
}
.analysis-card-meta {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}
.analysis-synthesis-box {
  background: #080b1a;
  border-left: 4px solid #8b5cf6;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
  font-size: 13px;
  color: #e2e8f0;
  margin-bottom: 18px;
  border-top: 1px solid #1e2548;
  border-right: 1px solid #1e2548;
  border-bottom: 1px solid #1e2548;
}
.analysis-synthesis-label {
  color: #c084fc;
}
.analysis-grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 16px;
}
.analysis-grid-card {
  background: #080b1a;
  border: 1px solid #1e2548;
  border-radius: 12px;
  padding: 14px;
}
.analysis-grid-card-title {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.analysis-title-problem { color: #f87171; }
.analysis-title-methodology { color: #38bdf8; }
.analysis-title-dataset { color: #fbbf24; }
.analysis-title-findings { color: #34d399; }
.analysis-title-limitations { color: #f43f5e; }
.analysis-title-future { color: #a78bfa; }

.analysis-grid-card-desc {
  font-size: 12px;
  color: #cbd5e1;
  line-height: 1.4;
}
.analysis-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #1e2548;
  padding-top: 10px;
}
.analysis-kw-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.analysis-kw-tag {
  background: rgba(139, 92, 246, 0.2);
  color: #c084fc;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  border: 1px solid rgba(139, 92, 246, 0.4);
}
.analysis-trace-text {
  font-size: 10.5px;
  color: #64748b;
}

/* 3. Gaps Cards */
.gap-result-card {
  background: #0d1126;
  border-radius: 18px;
  border: 1px solid #1e2548;
  padding: 22px;
  margin-bottom: 20px;
  box-shadow: var(--card-shadow);
}
.gap-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.gap-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.gap-id-badge {
  background: rgba(139, 92, 246, 0.25);
  color: #c084fc;
  font-weight: 800;
  font-size: 13px;
  padding: 4px 10px;
  border-radius: 8px;
  border: 1px solid rgba(139, 92, 246, 0.4);
}
.gap-card-title {
  font-size: 16.5px;
  font-weight: 800;
  color: #f8fafc;
  margin: 0;
}
.gap-impact-badge {
  font-weight: 800;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 8px;
}
.gap-impact-badge.impact-high {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}
.gap-impact-badge.impact-medium {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.4);
}
.gap-metrics-row {
  display: flex;
  gap: 20px;
  font-size: 12px;
  font-weight: 700;
  color: #a78bfa;
  margin-bottom: 12px;
}
.gap-void-box {
  background: #080b1a;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #cbd5e1;
  line-height: 1.5;
  border: 1px solid #1e2548;
}
.gap-void-label {
  color: #f87171;
}
.gap-direction-box {
  background: rgba(6, 182, 212, 0.1);
  border-left: 4px solid #06b6d4;
  padding: 12px 16px;
  border-radius: 0 8px 8px 0;
  margin-bottom: 14px;
  font-size: 13px;
  color: #38bdf8;
  border-top: 1px solid rgba(6, 182, 212, 0.25);
  border-right: 1px solid rgba(6, 182, 212, 0.25);
  border-bottom: 1px solid rgba(6, 182, 212, 0.25);
}
.gap-direction-label {
  color: #67e8f9;
}
.gap-details-accordion {
  font-size: 12px;
  color: #94a3b8;
}
.gap-summary-btn {
  cursor: pointer;
  font-weight: 700;
  color: #c084fc;
}
.gap-supporting-list {
  margin-top: 8px;
  padding-left: 20px;
}
.gap-supporting-item {
  margin-bottom: 4px;
  color: #cbd5e1;
}
.gap-supporting-title {
  color: #f8fafc;
}
.gap-supporting-meta {
  color: #94a3b8;
}

/* 4. Comparison Table */
.comparison-table-wrapper {
  background: #0d1126;
  border-radius: 16px;
  border: 1px solid #1e2548;
  overflow-x: auto;
  box-shadow: var(--card-shadow);
  margin-top: 16px;
}
.comparison-matrix-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  min-width: 1000px;
}
.comparison-matrix-thead {
  background: #080b1a;
  border-bottom: 2px solid #1e2548;
  font-size: 11px;
  font-weight: 800;
  color: #a78bfa;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.comparison-matrix-thead th {
  padding: 14px 12px;
}
.comparison-matrix-row {
  border-bottom: 1px solid #1e2548;
  vertical-align: top;
}
.comparison-matrix-row.comparison-row-odd {
  background: #080b1a;
}
.comparison-matrix-row.comparison-row-even {
  background: #0d1126;
}
.comparison-cell-source {
  padding: 12px;
  font-weight: 700;
  color: #a78bfa;
}
.comparison-source-tag {
  font-size: 10px;
  color: #64748b;
  margin-top: 2px;
}
.comparison-cell-title {
  padding: 12px;
  max-width: 200px;
}
.comparison-paper-title {
  font-weight: 700;
  font-size: 12px;
  color: #f8fafc;
}
.comparison-paper-meta {
  font-size: 10.5px;
  color: #34d399;
  margin-top: 3px;
}
.comparison-cell-domain {
  padding: 12px;
  font-size: 11.5px;
  color: #cbd5e1;
  max-width: 170px;
}
.comparison-cell-methodology {
  padding: 12px;
  font-size: 11.5px;
  color: #c084fc;
  max-width: 170px;
}
.comparison-cell-dataset {
  padding: 12px;
  font-size: 11.5px;
  color: #38bdf8;
  max-width: 150px;
}
.comparison-cell-findings {
  padding: 12px;
  font-size: 11.5px;
  color: #34d399;
  max-width: 180px;
}
.comparison-cell-limitations {
  padding: 12px;
  font-size: 11.5px;
  color: #f87171;
  max-width: 160px;
}

/* =================================================== */
/* LIGHT THEME OVERRIDES FOR 4 SUBPAGES                */
/* =================================================== */

/* 1. Search Cards (Light) */
.light-theme .search-result-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
}
.light-theme .search-idx-tag {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  border: 1px solid #c7d2fe !important;
}
.light-theme .search-card-title {
  color: #0f172a !important;
}
.light-theme .search-card-authors {
  color: #64748b !important;
}
.light-theme .search-relevance-badge {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 1px solid #a7f3d0 !important;
}
.light-theme .search-abstract-box {
  background: #f8fafc !important;
  color: #334155 !important;
  border: 1px solid #e2e8f0 !important;
}
.light-theme .search-card-footer {
  border-top: 1px solid #e2e8f0 !important;
  color: #64748b !important;
}
.light-theme .search-source-badge {
  background: #f1f5f9 !important;
  color: #4f46e5 !important;
  border: 1px solid #cbd5e1 !important;
}
.light-theme .search-oa-badge {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 1px solid #a7f3d0 !important;
}
.light-theme .search-doi-text {
  color: #64748b !important;
}
.light-theme .search-doi-link {
  color: #4f46e5 !important;
}
.light-theme .search-view-source-link {
  color: #6366f1 !important;
}

/* 2. Analysis Cards (Light) */
.light-theme .analysis-result-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
}
.light-theme .analysis-idx-badge {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  border: 1px solid #c7d2fe !important;
}
.light-theme .analysis-domain-badge {
  background: #f8fafc !important;
  color: #475569 !important;
  border: 1px solid #e2e8f0 !important;
}
.light-theme .analysis-source-badge {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border: 1px solid #a7f3d0 !important;
}
.light-theme .analysis-card-title {
  color: #0f172a !important;
}
.light-theme .analysis-card-meta {
  color: #64748b !important;
}
.light-theme .analysis-synthesis-box {
  background: #f8fafc !important;
  border-left: 4px solid #6366f1 !important;
  border-top: 1px solid #e2e8f0 !important;
  border-right: 1px solid #e2e8f0 !important;
  border-bottom: 1px solid #e2e8f0 !important;
  color: #1e293b !important;
}
.light-theme .analysis-synthesis-label {
  color: #4338ca !important;
}
.light-theme .analysis-grid-card {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
}
.light-theme .analysis-grid-card-desc {
  color: #334155 !important;
}
.light-theme .analysis-title-problem { color: #dc2626 !important; }
.light-theme .analysis-title-methodology { color: #0284c7 !important; }
.light-theme .analysis-title-dataset { color: #d97706 !important; }
.light-theme .analysis-title-findings { color: #059669 !important; }
.light-theme .analysis-title-limitations { color: #e11d48 !important; }
.light-theme .analysis-title-future { color: #7c3aed !important; }

.light-theme .analysis-card-footer {
  border-top: 1px solid #e2e8f0 !important;
}
.light-theme .analysis-kw-tag {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  border: 1px solid #c7d2fe !important;
}
.light-theme .analysis-trace-text {
  color: #94a3b8 !important;
}

/* 3. Gaps Cards (Light) */
.light-theme .gap-result-card {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
}
.light-theme .gap-id-badge {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  border: 1px solid #c7d2fe !important;
}
.light-theme .gap-card-title {
  color: #0f172a !important;
}
.light-theme .gap-impact-badge.impact-high {
  background: #fef2f2 !important;
  color: #dc2626 !important;
  border: 1px solid #fecaca !important;
}
.light-theme .gap-impact-badge.impact-medium {
  background: #fffbeb !important;
  color: #d97706 !important;
  border: 1px solid #fde68a !important;
}
.light-theme .gap-metrics-row {
  color: #4f46e5 !important;
}
.light-theme .gap-void-box {
  background: #fff5f5 !important;
  border: 1px solid #fed7d7 !important;
  color: #2d3748 !important;
}
.light-theme .gap-void-label {
  color: #dc2626 !important;
}
.light-theme .gap-direction-box {
  background: #f0fdfa !important;
  border-left: 4px solid #0d9488 !important;
  border-top: 1px solid #ccfbf1 !important;
  border-right: 1px solid #ccfbf1 !important;
  border-bottom: 1px solid #ccfbf1 !important;
  color: #0f766e !important;
}
.light-theme .gap-direction-label {
  color: #0d9488 !important;
}
.light-theme .gap-details-accordion {
  color: #64748b !important;
}
.light-theme .gap-summary-btn {
  color: #4f46e5 !important;
}
.light-theme .gap-supporting-item {
  color: #334155 !important;
}
.light-theme .gap-supporting-title {
  color: #0f172a !important;
}
.light-theme .gap-supporting-meta {
  color: #64748b !important;
}

/* 4. Comparison Table (Light) */
.light-theme .comparison-table-wrapper {
  background: #ffffff !important;
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
}
.light-theme .comparison-matrix-thead {
  background: #f1f5f9 !important;
  border-bottom: 2px solid #cbd5e1 !important;
  color: #4338ca !important;
}
.light-theme .comparison-matrix-row {
  border-bottom: 1px solid #e2e8f0 !important;
}
.light-theme .comparison-matrix-row.comparison-row-odd {
  background: #f8fafc !important;
}
.light-theme .comparison-matrix-row.comparison-row-even {
  background: #ffffff !important;
}
.light-theme .comparison-cell-source {
  color: #4f46e5 !important;
}
.light-theme .comparison-source-tag {
  color: #64748b !important;
}
.light-theme .comparison-paper-title {
  color: #0f172a !important;
}
.light-theme .comparison-paper-meta {
  color: #059669 !important;
}
.light-theme .comparison-cell-domain {
  color: #334155 !important;
}
.light-theme .comparison-cell-methodology {
  color: #6366f1 !important;
}
.light-theme .comparison-cell-dataset {
  color: #0284c7 !important;
}
.light-theme .comparison-cell-findings {
  color: #059669 !important;
}
.light-theme .comparison-cell-limitations {
  color: #dc2626 !important;
}

/* Plotly Light Mode SVG Overrides */
.light-theme .js-plotly-plot .main-svg:first-child {
  background: transparent !important;
}
.light-theme .js-plotly-plot .bg {
  fill: #ffffff !important;
  fill-opacity: 1 !important;
}
.light-theme .js-plotly-plot .g-gtitle text {
  fill: #4338ca !important;
  font-weight: 700 !important;
}
.light-theme .js-plotly-plot .g-xtitle text,
.light-theme .js-plotly-plot .g-ytitle text {
  fill: #475569 !important;
  font-weight: 600 !important;
}
.light-theme .js-plotly-plot .xtick text,
.light-theme .js-plotly-plot .ytick text {
  fill: #64748b !important;
}
.light-theme .js-plotly-plot .gridlayer path {
  stroke: #e2e8f0 !important;
}
.light-theme .js-plotly-plot .zerolinelayer path {
  stroke: #cbd5e1 !important;
}
.light-theme .js-plotly-plot .legend .bg {
  fill: #f8fafc !important;
  stroke: #e2e8f0 !important;
}
.light-theme .js-plotly-plot .legend text {
  fill: #0f172a !important;
}

/* =================================================== */
/* MOBILE & TOUCH RESPONSIVE STYLES                    */
/* =================================================== */
@media (max-width: 900px) {
  .app-container {
    flex-direction: column !important;
    flex-wrap: wrap !important;
  }
  .sidebar-container {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    position: static !important;
    flex: 1 1 auto !important;
    margin-bottom: 12px !important;
  }
  .main-content-column {
    width: 100% !important;
    min-width: 100% !important;
  }
  .hero-banner-row {
    flex-direction: column !important;
  }
  .hero-banner-left {
    width: 100% !important;
    flex: 1 1 100% !important;
  }
  .hero-banner-right {
    display: none !important;
  }
  .hero-filter-subrow {
    flex-direction: column !important;
    gap: 12px !important;
  }
  .filter-col-years, .filter-col-sources, .filter-col-max, .filter-col-btn {
    width: 100% !important;
    min-width: 100% !important;
    flex: 1 1 100% !important;
  }

  /* Grid & Columns responsiveness on mobile */
  .stat-cards-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 10px !important;
  }
  .middle-dashboard-row, .bottom-dashboard-row, .footer-cta-row {
    flex-direction: column !important;
    gap: 14px !important;
  }
  .pipeline-col, .upload-col {
    width: 100% !important;
    max-width: 100% !important;
    flex: 1 1 100% !important;
  }
  .upload-inner-split {
    flex-direction: column !important;
    gap: 10px !important;
  }
  .upload-drop-col, .upload-list-col {
    width: 100% !important;
    max-width: 100% !important;
    flex: 1 1 100% !important;
  }
  .paper-anime-container, .gap-anime-container {
    display: none !important;
  }
  .papers-content-split, .gaps-content-split {
    flex-direction: column !important;
  }
  .top-papers-list, .gap-items-col {
    width: 100% !important;
    max-width: 100% !important;
  }
  .table-responsive, table {
    display: block !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .gradio-container {
    padding: 8px !important;
  }
}

@media (max-width: 540px) {
  .stat-cards-grid {
    grid-template-columns: 1fr !important;
  }
  .hero-headline {
    font-size: 18px !important;
    line-height: 1.3 !important;
  }
  .hero-greeting {
    font-size: 13px !important;
  }
  .card-title-pill, .stat-header {
    font-size: 11px !important;
  }
  .btn-start-review-main, .upload-action-btn {
    padding: 12px 14px !important;
    font-size: 13px !important;
  }
}

/* ========================================================= */
/* 3D EARTH KNOWLEDGE SPHERE & SEE BEYOND HERO STYLES        */
/* ========================================================= */
.earth-hero-row {
  background: radial-gradient(circle at 75% 40%, rgba(0, 160, 255, 0.12) 0%, rgba(6, 12, 28, 0.95) 70%);
  border: 1px solid rgba(0, 220, 255, 0.2);
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 22px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  align-items: center !important;
}

.see-beyond-container {
  margin-bottom: 20px;
}

.agentic-pill-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: 100px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #34d399;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.pulse-emerald-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
  animation: pulseEmerald 1.8s infinite;
}

@keyframes pulseEmerald {
  0% { transform: scale(0.95); opacity: 0.7; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.7; }
}

.see-beyond-title {
  font-size: 38px !important;
  font-weight: 900 !important;
  line-height: 1.15 !important;
  color: #ffffff !important;
  letter-spacing: -0.5px;
  margin: 0 0 10px 0 !important;
}

.text-cyan-glow {
  color: #00f0ff !important;
  text-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
  font-style: italic;
}

.see-beyond-subtitle {
  font-size: 15px;
  color: #94a3b8;
  margin-bottom: 20px;
  line-height: 1.5;
}

.investigate-input-group {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  padding: 14px !important;
}

.investigate-label {
  font-size: 11px;
  letter-spacing: 1.2px;
  color: #64748b;
  margin-bottom: 6px;
}

.investigate-search-box textarea, .investigate-search-box input {
  background: rgba(2, 6, 23, 0.8) !important;
  border: 1px solid rgba(0, 220, 255, 0.3) !important;
  border-radius: 8px !important;
  color: #f8fafc !important;
  font-size: 14px !important;
}

.btn-investigate-cta {
  background: linear-gradient(135deg, #0284c7 0%, #06b6d4 50%, #0d9488 100%) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  border: none !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4) !important;
  transition: all 0.25s ease !important;
}

.btn-investigate-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(6, 182, 212, 0.6) !important;
}

/* Earth Canvas & HUD */
.earth-globe-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.earth-hud-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(0, 220, 255, 0.1);
  border: 1px solid rgba(0, 220, 255, 0.3);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #38bdf8;
  margin-bottom: 8px;
}

.hud-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #38bdf8;
  box-shadow: 0 0 8px #38bdf8;
}

.earth-canvas {
  width: 100%;
  max-width: 480px;
  height: auto;
  cursor: grab;
  touch-action: none;
}

.earth-canvas:active {
  cursor: grabbing;
}

.earth-controls-hint {
  font-size: 11px;
  color: #64748b;
  margin-top: 6px;
}

/* Gap Survival Result Card */
.gap-survival-result-box {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(8, 14, 28, 0.98) 100%);
  border: 1px solid rgba(16, 185, 129, 0.4);
  border-radius: 14px;
  padding: 22px;
  margin-bottom: 22px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16, 185, 129, 0.12);
  width: 100%;
}

.survival-result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.survival-tag-eyebrow {
  font-size: 10px;
  letter-spacing: 1.5px;
  font-weight: 800;
  color: #34d399;
  text-transform: uppercase;
}

.survival-target-title {
  font-size: 20px !important;
  font-weight: 800 !important;
  color: #f8fafc !important;
  margin: 4px 0 0 0 !important;
}

.survival-badge-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.survival-status-pill {
  font-size: 12px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 100px;
  letter-spacing: 0.5px;
}

.survival-conf-pill {
  font-size: 11px;
  font-weight: 700;
  color: #cbd5e1;
  background: rgba(255, 255, 255, 0.08);
  padding: 6px 10px;
  border-radius: 100px;
}

.survival-verdict-banner {
  display: flex;
  gap: 14px;
  background: rgba(16, 185, 129, 0.08);
  border-left: 4px solid #10b981;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 16px;
  align-items: center;
}

.verdict-banner-icon {
  font-size: 24px;
}

.verdict-banner-content strong {
  color: #34d399;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.verdict-banner-content p {
  color: #e2e8f0;
  margin: 4px 0 0 0;
  font-size: 14px;
  line-height: 1.5;
}

.survival-engine-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 18px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 12px;
}

.survival-refs-heading {
  font-size: 14px !important;
  color: #38bdf8 !important;
  font-weight: 700 !important;
  margin: 0 0 12px 0 !important;
}

.survival-refs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
}

.verdict-ref-card {
  background: rgba(2, 6, 23, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 12px 14px;
  transition: border-color 0.2s;
}

.verdict-ref-card:hover {
  border-color: rgba(56, 189, 248, 0.4);
}

.verdict-ref-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}

.verdict-ref-title {
  color: #38bdf8 !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-decoration: none !important;
  line-height: 1.3;
}

.verdict-ref-title:hover {
  text-decoration: underline !important;
}

.verdict-ref-score {
  font-size: 10px;
  font-weight: 700;
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.verdict-ref-snippet {
  font-size: 12px;
  color: #94a3b8;
  line-height: 1.4;
  margin: 0;
}

.survival-empty-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px dashed rgba(0, 220, 255, 0.25);
  border-radius: 12px;
  padding: 16px 20px;
  width: 100%;
}

.survival-empty-icon {
  font-size: 32px;
}

.survival-empty-text strong {
  color: #e2e8f0;
  font-size: 14px;
}

.survival-empty-text p {
  color: #64748b;
  font-size: 12px;
  margin: 2px 0 0 0;
}
"""





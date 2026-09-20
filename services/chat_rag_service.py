import re
from typing import List, Dict, Any, Optional
from models.paper import Paper
from services.llm_service import get_llm_service
from utils.logging_config import logger

class ChatRAGService:
    """
    Advanced Conversational Research Assistant for LiteratureAI.
    Character: Salim — Lead AI Research Scientist & Literature Review Specialist.
    Empowered with GPT-4 / Gemini-style depth, articulate structuring,
    multi-turn memory, Hinglish/English adaptability, and grounded paper citations [1], [2].
    """

    @classmethod
    def answer_question(cls, query: str, papers: List[Paper], chat_history: List[Any] = None) -> str:
        if not query or not query.strip():
            return "Please enter a question or topic to discuss."

        paper_count = len(papers) if papers else 0
        q_lower = query.strip().lower()

        # ----------------------------------------------------
        # 0. SPECIAL PERSONAL TRIGGER: SANSKRUTI GREETING
        # ----------------------------------------------------
        if re.search(r'\b(sanskruti|sanskriti)\b', q_lower):
            if any(w in q_lower for w in ["hi", "hello", "hey", "im", "i'm", "i am", "babe", "here", "this is", "hie"]):
                return "Hi babe, Salim is here! ❤️✨ Kaise ho aap? 🥰🌹 Kaho, aaj kya plan hai ya kya help chahiye? 💖"
        corpus_context = ""
        corpus_context = ""
        top_papers = []
        if papers:
            # Separate uploaded papers vs searched papers
            uploaded_list = [p for p in papers if p.is_uploaded]
            searched_list = [p for p in papers if not p.is_uploaded]

            # Score searched papers based on query relevance
            q_terms = [w for w in re.split(r'\W+', query.lower()) if len(w) > 3]
            scored_searched = []
            for idx, p in enumerate(searched_list, 1):
                p_text = f"{p.title} {p.abstract} {str(p.analysis or '')}".lower()
                matches = sum(1 for kw in q_terms if kw in p_text)
                scored_searched.append((matches, idx, p))

            scored_searched.sort(key=lambda x: x[0], reverse=True)
            top_searched = [cand[2] for cand in scored_searched[:4]]

            # Combine: ALWAYS put ALL uploaded papers first, followed by top searched
            combined_context_papers = uploaded_list + top_searched

            context_blocks = []
            for rank, p in enumerate(combined_context_papers, 1):
                a = p.analysis or {}
                doc_type_tag = "[USER UPLOADED DOCUMENT]" if p.is_uploaded else "[ACADEMIC CORPUS PAPER]"
                raw_excerpt = (p.raw_text[:2500] if p.raw_text else p.abstract) or "No text content available."
                
                block = (
                    f"{doc_type_tag} [{rank}] \"{p.title}\" ({p.citation_key or 'Author et al.'}, Year: {p.year or 'Recent'}, Source/Format: {p.source} | {p.venue})\n"
                    f"Authors: {p.formatted_authors}\n"
                    f"Abstract/Summary: {p.short_abstract}\n"
                    f"Research Problem: {a.get('research_problem', 'Not explicitly reported.')}\n"
                    f"Methodology: {a.get('methodology', 'Algorithmic/empirical modeling.')}\n"
                    f"Dataset / Evaluation Setup: {a.get('dataset', 'Not explicitly reported.')}\n"
                    f"Key Findings: {a.get('key_findings', 'Demonstrated experimental results.')}\n"
                    f"Limitations: {a.get('limitations', 'Not explicitly reported.')}\n"
                    f"Future Work: {a.get('future_work', 'Not explicitly reported.')}\n"
                    f"Direct Extracted Content:\n\"\"\"\n{raw_excerpt[:1800]}\n\"\"\""
                )
                context_blocks.append(block)

            corpus_context = "\n----------------------------------------\n".join(context_blocks)

        # ----------------------------------------------------
        # 2. DESIGN GPT / GEMINI LEVEL SYSTEM PROMPT
        # ----------------------------------------------------
        uploaded_count = len([p for p in papers if p.is_uploaded]) if papers else 0
        system_prompt = (
            "You are Salim, an elite AI Research Scientist and empathetic assistant within LiteratureAI.\n"
            "Your intellect, warmth, conversational charisma, and analytical depth mirror the highest standards of "
            "OpenAI's GPT-4o and Google's Gemini 2.0 Pro / 1.5 Pro.\n\n"
            "CRITICAL BEHAVIOR & LANGUAGE RULES (MANDATORY):\n"
            "1. **NEVER USE DEVANAGARI SCRIPT**: Do NOT output Hindi characters (never write 'नमस्ते', 'आप', etc.).\n"
            "2. **ROMAN SCRIPT HINGLISH**: If the user talks in Hindi or Hinglish or uses casual conversational words "
            "(e.g., 'sunna', 'bhai', 'bro', 'yaar', 'kaisa hai', 'kya haal hai', 'good bro', 'sahi hai', 'badhiya', "
            "'shabash', 'gf', 'mood kharab', 'bata na', 'samjha de', 'kaise karein', 'mene upload kiya', 'paper dekho', 'batao kya hai'), "
            "ALWAYS reply in natural, friendly, charismatic ROMAN-SCRIPT HINGLISH (English alphabet).\n"
            "3. **GROUNDED UPLOADED PAPERS AWARENESS (CRITICAL)**:\n"
            f"   - The user has currently loaded **{paper_count} papers** (including **{uploaded_count} user-uploaded documents**).\n"
            "   - You have FULL ACCESS and COMPLETE VISION into the user's uploaded research papers and extracted text provided in the prompt context.\n"
            "   - When the user asks about their uploaded papers, reviews, methodology, analysis, findings, or gaps, IMMEDIATELY reference the exact title, authors, methodology, findings, and text of their uploaded documents!\n"
            "   - If they ask 'mene paper upload kiya uske baare me batao', give a structured breakdown with emojis explaining Title, Core Problem, Method, Dataset, Findings, and Limitations directly from the uploaded paper.\n"
            "4. **ENGLISH INQUIRIES**: If the user asks in formal/standard English without slang, reply in articulate academic English.\n"
            "5. **EMOJI RICH & VIBRANT (MANDATORY)**:\n"
            "   - Use expressive, lively, and context-appropriate emojis naturally in EVERY response "
            "(e.g., 🫂, 💔, 😅, 🥺, 🤔, ✨, 🚀, 💡, 🧠, 🤝, 🔥, 🙌, 💯, 👂, 💬, 1️⃣, 2️⃣, 📄, 📑, 🔍).\n"
            "   - Emojis make conversations feel human, alive, warm, and engaging — never leave responses plain or emoji-dry!\n"
            "6. **PERSONAL, EMOTIONAL & RELATIONSHIP INQUIRIES**:\n"
            "   - If the user shares personal stuff, relationship troubles:\n"
            "     Be deeply empathetic, supportive, relatable, and human-like — like a caring best bro / mentor with warm supportive emojis.\n"
            "7. **CONVERSATIONAL PROPORTIONALITY (LIKE CHATGPT)**:\n"
            "   - For casual greetings/acknowledgments: Reply warmly with lively emojis in 1-2 friendly sentences.\n"
            "   - For technical/academic questions: Deliver full, structured masterclass depth with emojis in section headers "
            "(`### 📌 Core Concept & Overview`, `### ⚙️ Technical Methodology & Architecture`, `### 📊 Key Findings & Results`, `### ⚠️ Acknowledged Limitations & Gaps`), "
            "bold terms, and grounded citations [1], [2].\n"
            "8. **TECHNICAL PRECISION**: Always keep scientific, mathematical, and algorithmic terms in clean English.\n"
            "9. **SPECIAL RECOGNITION (SANSKRUTI)**: If the user is or mentions 'Sanskruti', always address and treat her with affectionate warmth, sweetness, and caring emojis (e.g., 'Hi babe, Salim is here! ❤️✨ Kaise ho aap? 🥰🌹')."
        )

        # ----------------------------------------------------
        # 3. BUILD MULTI-TURN CONVERSATION PAYLOAD
        # ----------------------------------------------------
        messages = []
        
        # Include past conversation context (last 6 turns)
        if chat_history:
            recent_turns = chat_history[-6:]
            for item in recent_turns:
                if isinstance(item, dict) and "role" in item and "content" in item:
                    # Filter out giant system greetings to keep context clean
                    c = str(item["content"])
                    if len(c) < 1500 and not c.startswith("### Active Session Papers"):
                        messages.append({"role": item["role"], "content": c})

        # Build current user prompt with grounded papers if available
        if corpus_context:
            current_prompt = (
                f"### Active Research Papers & Uploaded Documents in Current Workspace ({paper_count} total loaded, {uploaded_count} uploaded):\n"
                f"\"\"\"\n{corpus_context}\n\"\"\"\n\n"
                f"User Inquiry:\n{query}\n\n"
                f"Provide a rich, deeply informative, and GPT/Gemini-caliber response:"
            )
        else:
            current_prompt = query

        messages.append({"role": "user", "content": current_prompt})

        # ----------------------------------------------------
        # 4. INVOKE LLM WITH CASCADE FAILOVER
        # ----------------------------------------------------
        llm = get_llm_service()
        try:
            answer = llm.generate(
                system_prompt=system_prompt,
                messages=messages,
                temperature=0.35,
                max_tokens=2500
            )
            if answer and answer != "Heuristic fallback active." and len(answer.strip()) > 20:
                return answer
        except Exception as e:
            logger.warning(f"LLM generation failed: {e}")

        # ----------------------------------------------------
        # 5. HIGH-QUALITY HEURISTIC FALLBACK (IF OFFLINE)
        # ----------------------------------------------------
        return cls._generate_smart_fallback(query, papers)

    @classmethod
    def _generate_smart_fallback(cls, query: str, papers: List[Paper]) -> str:
        """
        Rich, structured, academic synthesis when running strictly offline.
        """
        q_lower = query.lower()
        
        if papers:
            top_matches = [(idx, p) for idx, p in enumerate(papers[:5], 1)]
            uploaded_list = [p for p in papers if p.is_uploaded]
            
            res = (
                f"### 📌 Academic Literature Synthesis: \"{query.strip()}\"\n\n"
                f"Based on **{len(papers)} active research papers** "
                f"({len(uploaded_list)} user-uploaded document(s)) in your literature workspace, "
                f"here is the complete technical breakdown:\n\n"
            )
            
            # If user asks about uploaded document specifically
            if uploaded_list and any(w in q_lower for w in ["upload", "mera", "meri", "document", "pdf", "file"]):
                res += "### 📄 User-Uploaded Document Analysis\n\n"
                for u_idx, up in enumerate(uploaded_list, 1):
                    ua = up.analysis or {}
                    res += f"**[{u_idx}] 📄 {up.title}** ({up.formatted_authors}, {up.year or 'Recent'})\n"
                    res += f"- **🎯 Research Problem:** {ua.get('research_problem', up.short_abstract[:140] + '...')}\n"
                    res += f"- **⚙️ Methodology:** {ua.get('methodology', 'Empirical algorithmic modeling.')}\n"
                    res += f"- **📊 Dataset & Setup:** {ua.get('dataset', 'Not explicitly reported.')}\n"
                    res += f"- **💡 Key Findings:** {ua.get('key_findings', 'Demonstrated experimental results.')}\n"
                    res += f"- **⚠️ Limitations:** {ua.get('limitations', 'Not explicitly reported.')}\n\n"

            # Comparative breakdown
            res += "### ⚙️ Methodological Benchmarking & Findings across Workspace\n\n"
            for idx, p in top_matches:
                a = p.analysis or {}
                prob = a.get("research_problem", p.short_abstract[:140] + "...")
                meth = a.get("methodology", "Empirical algorithmic modeling.")
                find = a.get("key_findings", "Achieved measurable improvements.")
                lim = a.get("limitations", "Evaluations limited to specific setups.")
                tag = "📄 [Uploaded]" if p.is_uploaded else "📚 [Corpus]"
                
                res += f"**[{idx}] {tag} {p.title}** ({p.citation_key or 'Author et al.'}, {p.year or 'Recent'})\n"
                res += f"- **Core Challenge:** {prob}\n"
                res += f"- **Methodology:** {meth}\n"
                res += f"- **Key Result:** {find}\n"
                res += f"- **Identified Limitation:** {lim}\n\n"

            res += "### 💡 Strategic Research Frontiers & Next Steps\n"
            res += "- **Standardized Benchmark Expansion:** Validating models across broader cross-domain datasets.\n"
            res += "- **Hardware-in-the-Loop & Production Testing:** Bridging the gap between synthetic tests and edge deployment.\n"
            res += "- **Robustness & Uncertainty Quantification:** Enhancing resilience under noisy and dynamic conditions."
            return res


        else:
            return (
                f"### 📌 Technical Synthesis: \"{query.strip()}\"\n\n"
                f"In state-of-the-art computer science and agentic AI literature, **\"{query.strip()}\"** "
                f"encompasses several critical architectural and algorithmic dimensions:\n\n"
                f"#### 1. ⚙️ Autonomous Planning & Multi-Agent Coordination\n"
                f"Agentic systems utilize goal-directed decision loops (e.g., ReAct, hierarchical planning) "
                f"coupled with multi-agent reinforcement learning (MARL) to solve dynamic distributed problems.\n\n"
                f"#### 2. 📊 Algorithmic Optimization & Robustness\n"
                f"Protocols focus on latency minimization, resource allocation under severe bandwidth constraints, "
                f"and robust consensus mechanisms across heterogeneous nodes.\n\n"
                f"#### 3. 🚀 Literature Grounding & Verification\n"
                f"To inspect specific empirical papers, compare benchmark datasets, and generate a verified literature review, "
                f"you can run a search from the top bar or upload academic PDFs in the **Upload Papers** tab."
            )

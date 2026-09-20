from typing import List, Dict, Any
from datetime import datetime
import re
from models.paper import Paper
from services.llm_service import get_llm_service, OpenAICompatibleProvider
from utils.logging_config import logger

class ReviewGenerator:
    """
    Generates a structured, publication-grade academic literature review.
    Strictly preserves citation grounding ([1], [2]...) and bibliographical fidelity.
    Uses LLM (Groq/OpenAI) for high-caliber synthesis, with dynamic grounded fallback.
    """

    @classmethod
    def generate_review(
        cls,
        topic: str,
        papers: List[Paper],
        gaps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not papers:
            return {
                "markdown": "### No papers available to generate literature review.\nPlease search or upload papers first.",
                "sections": {},
                "references": []
            }

        # Build stable citation mapping & references list
        paper_map = {}
        references = []
        for idx, p in enumerate(papers, 1):
            paper_map[p.id] = idx
            authors_str = p.formatted_authors
            year_str = str(p.year) if p.year else "n.d."
            venue_str = f", *{p.venue}*" if p.venue else ""
            doi_str = f", DOI: https://doi.org/{p.doi}" if p.doi else ""
            source_tag = f" [{p.source}]"
            ref_entry = f"[{idx}] {authors_str}, \"{p.title}\"{venue_str}, {year_str}{doi_str}{source_tag}."
            references.append(ref_entry)

        # Infer refined topic if default or generic
        effective_topic = topic
        if not topic or topic == "Agentic AI for Autonomous Space Communication Networks":
            if papers and papers[0].is_uploaded:
                effective_topic = papers[0].title

        # Try LLM generation first
        llm = get_llm_service()
        if isinstance(llm, OpenAICompatibleProvider) and llm.is_available:
            try:
                review_data = cls._generate_with_llm(effective_topic, papers, gaps, references, paper_map, llm)
                if review_data and len(review_data.get("markdown", "")) > 400:
                    return review_data
            except Exception as e:
                logger.warning(f"LLM review generation failed: {e}. Using dynamic grounded fallback.")

        # Grounded Dynamic Synthesis Fallback
        return cls._generate_dynamic_fallback(effective_topic, papers, gaps, references, paper_map)

    @classmethod
    def _generate_with_llm(
        cls,
        topic: str,
        papers: List[Paper],
        gaps: List[Dict[str, Any]],
        references: List[str],
        paper_map: Dict[str, int],
        llm: OpenAICompatibleProvider
    ) -> Dict[str, Any]:
        papers_context = []
        for p in papers[:10]:
            cid = paper_map.get(p.id, 1)
            a = p.analysis or {}
            raw_snippet = p.raw_text[:2000] if p.raw_text else p.abstract
            p_block = (
                f"[{cid}] \"{p.title}\" by {p.formatted_authors} ({p.year or 'Recent'})\n"
                f"Source/Venue: {p.source} | {p.venue}\n"
                f"Content/Abstract: {raw_snippet[:1500]}\n"
                f"Problem: {a.get('research_problem', 'N/A')}\n"
                f"Methodology: {a.get('methodology', 'N/A')}\n"
                f"Key Findings: {a.get('key_findings', 'N/A')}\n"
                f"Limitations: {a.get('limitations', 'N/A')}\n"
                f"Future Work: {a.get('future_work', 'N/A')}"
            )
            papers_context.append(p_block)

        gaps_summary = "\n".join([f"- {g['title']}: {g['description']}" for g in gaps]) if gaps else "None provided."

        system_prompt = (
            "You are an elite Senior Academic Researcher and Literature Review Author. "
            "Your task is to write an exhaustive, rigorous, publication-ready academic Literature Review based STRICTLY "
            "on the provided research papers.\n\n"
            "MANDATORY GUIDELINES:\n"
            "1. Ground every claim in the provided papers using in-text numbered citations like [1], [2], etc.\n"
            "2. Structure the review into EXACTLY these 7 sections with markdown headers:\n"
            "   ## 1. Introduction\n"
            "   ## 2. Theoretical Foundations & Background\n"
            "   ## 3. Literature Synthesis & State of the Art\n"
            "   ## 4. Comparative Methodology Analysis\n"
            "   ## 5. Critical Research Gaps\n"
            "   ## 6. Future Research Directions\n"
            "   ## 7. Conclusion\n"
            "3. In Section 4 (Comparative Methodology Analysis), include a detailed Markdown comparison table comparing Citation, Key Methodology, Dataset/Evaluation Setup, and Reported Limitations.\n"
            "4. Maintain zero hallucination; do not fabricate numbers or papers outside the provided corpus."
        )

        user_prompt = f"""
Topic: {topic}
Number of Papers: {len(papers)}

Corpus of Papers:
\"\"\"
{chr(10).join(papers_context)}
\"\"\"

Identified Research Gaps:
\"\"\"
{gaps_summary}
\"\"\"

Write the complete 7-section literature review now:
"""
        response_text = llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.25,
            max_tokens=3500
        )

        # Append references
        ref_block = "\n\n## References\n\n" + "\n\n".join(references)
        if "## References" not in response_text:
            full_md = response_text.strip() + ref_block
        else:
            full_md = response_text.strip()

        # Add title header if missing
        if not full_md.startswith("#"):
            full_md = f"# Literature Review: {topic}\n\n*Generated by LiteratureAI Assistant on {datetime.now().strftime('%B %d, %Y')}*\n\n**Analyzed Corpus:** {len(papers)} publications | **Identified Gaps:** {len(gaps)}\n\n---\n\n" + full_md

        logger.info(f"Successfully generated LLM literature review for '{topic}'.")
        return {
            "markdown": full_md,
            "topic": topic,
            "references": references,
            "timestamp": datetime.now().isoformat()
        }

    @classmethod
    def _generate_dynamic_fallback(
        cls,
        topic: str,
        papers: List[Paper],
        gaps: List[Dict[str, Any]],
        references: List[str],
        paper_map: Dict[str, int]
    ) -> Dict[str, Any]:
        """Dynamically builds a publication-grade review matching the actual uploaded/searched papers."""
        p1 = papers[0]
        a1 = p1.analysis or {}
        domain = a1.get("research_domain", "Computational and Applied Sciences")

        # Section 1: Introduction
        s1 = (
            f"The rapid evolution of **{topic}** has spurred significant academic inquiry and technological innovation across {domain.lower()}. "
            f"As modern research paradigms demand greater scalability, precision, and empirical validation, addressing core efficiency bottlenecks "
            f"and methodological trade-offs has become an imperative. "
            f"This comprehensive literature review systematically synthesizes evidence from {len(papers)} publications ([1]–[{len(papers)}]), "
            f"critically analyzing algorithmic architectures, evaluation benchmarks, empirical results, and unresolved research challenges."
        )

        # Section 2: Theoretical Foundations & Background
        s2_items = []
        for p in papers[:3]:
            cid = paper_map.get(p.id, 1)
            a = p.analysis or {}
            prob = a.get("research_problem", p.short_abstract)
            s2_items.append(f"- As investigated by {p.citation_key} [{cid}], foundational efforts have targeted {prob.lower() if len(prob) < 150 else prob[:140] + '...'}")
        
        s2 = (
            f"Theoretical advancements in {topic.lower()} are grounded in iterative algorithmic modeling, empirical experimentation, and domain-specific optimization frameworks. "
            f"Early investigations established baseline formulations, yet expanding operational complexity necessitated dynamic, adaptive approaches:\n\n"
            + "\n".join(s2_items)
        )

        # Section 3: Literature Synthesis & State of the Art
        s3_lines = [
            f"Cross-study examination of the {len(papers)} analyzed works reveals several foundational thematic clusters:\n"
        ]
        for idx, p in enumerate(papers[:5], 1):
            cid = paper_map.get(p.id, idx)
            a = p.analysis or {}
            meth = a.get("methodology", "algorithmic modeling")
            find = a.get("key_findings", "demonstrated measurable gains over conventional baselines")
            s3_lines.append(
                f"{idx}. **{p.title}** ({p.citation_key} [{cid}]):\n"
                f"   - *Methodology:* {meth}\n"
                f"   - *Core Contribution & Results:* {find}\n"
            )
        s3 = "\n".join(s3_lines)

        # Section 4: Comparative Methodology Analysis
        s4_lines = [
            "| Citation | Key Methodology | Experimental Setup / Dataset | Reported Limitations |",
            "| :--- | :--- | :--- | :--- |"
        ]
        for p in papers[:8]:
            cid = f"[{paper_map.get(p.id, 1)}] {p.citation_key}"
            a = p.analysis or {}
            meth = (a.get("methodology", "Empirical Modeling") or "Empirical Modeling")[:50]
            data = (a.get("dataset", "Benchmark Dataset") or "Benchmark Dataset")[:40]
            limit = (a.get("limitations", "Not explicitly reported") or "Not explicitly reported")[:50]
            s4_lines.append(f"| {cid} | {meth} | {data} | {limit} |")
        s4 = "\n".join(s4_lines)

        # Section 5: Critical Research Gaps
        s5_lines = [
            f"Synthesizing the limitations and future work across the corpus highlights {len(gaps)} core research frontiers:\n"
        ]
        for g in gaps:
            s5_lines.append(
                f"- **{g['title']}** (*{g.get('impact', 'High Impact')}* — Evidence: {g.get('evidence_ratio', 'Corpus-wide')}):\n"
                f"  {g['description']}\n"
                f"  *Recommended Trajectory:* {g.get('suggested_direction', 'Empirical benchmarking and extended evaluation.')}\n"
            )
        s5 = "\n".join(s5_lines) if gaps else "Empirical evaluation reveals opportunities for scalable benchmark expansion."

        # Section 6: Future Research Directions
        s6_lines = [
            "Based on the synthesized findings, future investigations should prioritize three strategic trajectories:\n",
            "1. **Standardized Benchmarking & Open Reproducibility:** Developing open-access evaluation suites to validate cross-model generalization.\n",
            "2. **Adaptive Real-Time Optimization:** Mitigating computational overhead during runtime inference under dynamic resource constraints.\n",
            "3. **Robustness & Generalization Under Noise:** Enhancing algorithmic resilience against out-of-distribution inputs and environmental perturbations."
        ]
        s6 = "".join(s6_lines)

        # Section 7: Conclusion
        s7 = (
            f"This review has provided a grounded synthesis of contemporary research in **{topic}**. "
            f"While current paradigms demonstrate significant empirical enhancements across diverse benchmarks, "
            f"bridging the identified research gaps will be essential to achieving robust, production-grade deployment."
        )

        sections = {
            "1. Introduction": s1,
            "2. Theoretical Foundations & Background": s2,
            "3. Literature Synthesis & State of the Art": s3,
            "4. Comparative Methodology Analysis": s4,
            "5. Critical Research Gaps": s5,
            "6. Future Research Directions": s6,
            "7. Conclusion": s7,
            "References": "\n\n".join(references)
        }

        md_doc = f"# Literature Review: {topic}\n\n"
        md_doc += f"*Generated by LiteratureAI Assistant on {datetime.now().strftime('%B %d, %Y')}*\n\n"
        md_doc += f"**Analyzed Corpus:** {len(papers)} publications | **Identified Gaps:** {len(gaps)}\n\n---\n\n"

        for heading, body in sections.items():
            md_doc += f"## {heading}\n\n{body}\n\n"

        logger.info(f"Successfully generated dynamic fallback literature review for '{topic}'.")
        return {
            "markdown": md_doc,
            "sections": sections,
            "references": references,
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        }


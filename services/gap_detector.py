from typing import List, Dict, Any
from models.paper import Paper
from utils.logging_config import logger

class GapDetector:
    """
    Synthesizes collective paper analyses to identify empirical,
    methodological, and theoretical research gaps with evidence traceability.
    Dynamically extracts gaps directly from analyzed paper limitations and future work.
    """

    @classmethod
    def detect_gaps(cls, papers: List[Paper], topic: str) -> List[Dict[str, Any]]:
        if not papers:
            return []

        analyzed_count = len(papers)
        detected_gaps = []

        # 1. First, check if papers contain specific extracted limitations/future work
        extracted_limitations = []
        for p in papers:
            if p.analysis:
                lim = p.analysis.get("limitations", "").strip()
                fw = p.analysis.get("future_work", "").strip()
                if lim and "not explicitly reported" not in lim.lower():
                    extracted_limitations.append((p, lim, fw))

        gap_counter = 1

        # If papers have specific grounded limitations, build dynamic gaps from them
        if extracted_limitations:
            for p, lim, fw in extracted_limitations[:4]:
                p_title_short = (p.title[:50] + "...") if len(p.title) > 50 else p.title
                title = f"LIMITATION IN {p_title_short.upper()}"
                desc = f"Acknowledged experimental/architectural bottleneck in [{p.citation_key}]: \"{lim}\""
                direction = fw if (fw and "not explicitly reported" not in fw.lower()) else f"Extended empirical evaluation, cross-dataset generalization, and hardware validation for {p.citation_key}."

                detected_gaps.append({
                    "id": f"{gap_counter:02d}",
                    "title": title,
                    "impact": "High Impact",
                    "impact_class": "high",
                    "evidence_ratio": f"1 / {analyzed_count} papers",
                    "evidence_count": 1,
                    "confidence": "88%",
                    "description": desc,
                    "suggested_direction": direction,
                    "supporting_papers": [{
                        "id": p.id,
                        "title": p.title,
                        "year": p.year or "Recent",
                        "authors": p.citation_key,
                        "doi": p.doi
                    }]
                })
                gap_counter += 1

        # 2. Add domain-wide candidate gap patterns
        candidate_patterns = [
            {
                "title": "BENCHMARK DIVERSITY & REPRODUCIBILITY",
                "impact": "High Impact",
                "impact_class": "high",
                "base_confidence": 85,
                "keywords": ["benchmark", "dataset", "evaluation", "baseline", "simulation", "synthetic", "testbed", "reproducib"],
                "description": "Studies frequently rely on synthetic test environments or narrow evaluation benchmarks. Cross-dataset validation across diverse production scenarios remains an open challenge.",
                "suggested_direction": "Establishing open-source standardized benchmarking pipelines and multi-environment empirical stress-testing."
            },
            {
                "title": "SCALABILITY & COMPUTATIONAL OVERHEAD",
                "impact": "Medium Impact",
                "impact_class": "medium",
                "base_confidence": 78,
                "keywords": ["complexity", "overhead", "comput", "scale", "scalability", "memory", "latency", "real-time"],
                "description": "High algorithmic computational complexity and memory footprints hinder real-time deployment on constrained edge hardware.",
                "suggested_direction": "Model compression, asynchronous distributed inference, and lightweight quantization frameworks."
            },
            {
                "title": "ROBUSTNESS & ADVERSARIAL RESILIENCE",
                "impact": "High Impact",
                "impact_class": "high",
                "base_confidence": 82,
                "keywords": ["noise", "adversar", "robust", "resilien", "safety", "uncertainty", "fault", "security"],
                "description": "Decision models often assume near-ideal inputs, showing vulnerability to out-of-distribution shifts, sensor noise, or adversarial perturbations.",
                "suggested_direction": "Formal verification methods, uncertainty quantification, and defensive regularization schemes."
            }
        ]

        for cand in candidate_patterns:
            supporting = []
            for p in papers:
                search_scope = f"{p.title} {p.abstract} {p.raw_text[:2000]}".lower()
                if p.analysis:
                    search_scope += f" {p.analysis.get('limitations', '')} {p.analysis.get('future_work', '')}".lower()
                
                if any(kw in search_scope for kw in cand["keywords"]):
                    supporting.append({
                        "id": p.id,
                        "title": p.title,
                        "year": p.year or "n.d.",
                        "authors": p.citation_key,
                        "doi": p.doi
                    })

            evidence_count = len(supporting)
            if evidence_count > 0 and len(detected_gaps) < 4:
                confidence = min(95, max(65, int(cand["base_confidence"] * (0.75 + 0.25 * (evidence_count / analyzed_count)))))
                detected_gaps.append({
                    "id": f"{gap_counter:02d}",
                    "title": cand["title"],
                    "impact": cand["impact"],
                    "impact_class": cand["impact_class"],
                    "evidence_ratio": f"{evidence_count} / {analyzed_count} papers",
                    "evidence_count": evidence_count,
                    "confidence": f"{confidence}%",
                    "description": cand["description"],
                    "suggested_direction": cand["suggested_direction"],
                    "supporting_papers": supporting
                })
                gap_counter += 1

        logger.info(f"Identified {len(detected_gaps)} grounded research gaps.")
        return detected_gaps


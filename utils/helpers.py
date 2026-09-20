from typing import List, Dict, Any, Optional

def reconstruct_openalex_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """
    OpenAlex provides abstracts as inverted index: {"word": [0, 4], "another": [1]}
    Reconstructs this into readable continuous prose.
    """
    if not inverted_index:
        return ""
    try:
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(word for _, word in word_positions)
    except Exception:
        return ""

def chunk_text(text: str, max_chars: int = 4000, overlap: int = 400) -> List[str]:
    """Splits long texts into overlapping chunks suitable for LLM processing."""
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_chars - overlap
    return chunks

def format_file_size(size_bytes: int) -> str:
    """Formats bytes into human-readable MB / KB string."""
    size_mb = size_bytes / (1024 * 1024)
    if size_mb >= 1.0:
        return f"{size_mb:.1f} MB"
    size_kb = size_bytes / 1024
    return f"{size_kb:.0f} KB"

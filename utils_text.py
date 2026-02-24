import re


# ======================================
# TEXT NORMALIZATION (robust for PDFs)
# ======================================
def normalize_question_text(text: str) -> str:
    """
    Aggressively normalizes question text so that
    Master QP and Response PDF versions match.

    Designed specifically for exam PDFs.
    """
    if not text:
        return ""

    # ---- lowercase ----
    text = text.lower()

    # ---- remove common PDF noise ----
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # ---- normalize unicode dashes/quotes ----
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'")

    # ---- collapse whitespace ----
    text = re.sub(r"\s+", " ", text)

    # ---- remove most punctuation but keep math symbols ----
    text = re.sub(r"[^\w\s\.\:\-\+\*/=<>\(\)]", "", text)

    return text.strip()


# ======================================
# QUESTION FINGERPRINT
# ======================================
def fingerprint(text: str, n: int = 160) -> str:
    """
    Creates a stable fingerprint for question matching.

    Why 160 chars?
    - 120 sometimes too short for long GATE questions
    - still very fast
    - low collision risk

    Returns normalized prefix.
    """
    norm = normalize_question_text(text)
    return norm[:n]
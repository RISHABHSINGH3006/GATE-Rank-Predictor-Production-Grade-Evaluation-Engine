import pdfplumber
import pandas as pd
import re

from utils_text import fingerprint


# ======================================
# MARKS RULE (same as answer key)
# ======================================
def assign_marks(qno: int) -> int:
    if 1 <= qno <= 5:
        return 1
    elif 6 <= qno <= 10:
        return 2
    elif 11 <= qno <= 35:
        return 1
    elif 36 <= qno <= 65:
        return 2
    else:
        raise ValueError(f"Invalid question number: {qno}")


# ======================================
# CLEAN QUESTION TEXT (remove options)
# ======================================
def clean_question_block(block: str) -> str:
    """
    Removes options and metadata from question block,
    leaving only the question stem.
    """

    if not block:
        return ""

    # cut before options start
    block = re.split(r"\(\s*A\s*\)", block)[0]

    # remove extra whitespace
    block = re.sub(r"\s+", " ", block)

    return block.strip()


# ======================================
# MAIN PARSER
# ======================================
def parse_master_qp(pdf_path: str) -> pd.DataFrame:
    records = []

    # ---- extract full text ----
    with pdfplumber.open("C:\\Users\\dell\\OneDrive\\Desktop\\gate rank predictor 2026\\questionPaper.pdf") as pdf:
        full_text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                full_text += extracted + "\n"

    # ---- split by question ----
    blocks = re.split(r"\bQ\.\s*\d+\b", full_text)
    qnos = re.findall(r"\bQ\.\s*(\d+)\b", full_text)

    for qno, block in zip(qnos, blocks[1:]):
        try:
            qno_int = int(qno)

            # ---------- clean question text ----------
            question_text = clean_question_block(block)

            # ---------- build fingerprint ----------
            fp = fingerprint(question_text)

            records.append({
                "question_id_master": qno_int,
                "question_text": question_text,
                "fingerprint": fp,
                "marks": assign_marks(qno_int)
            })

        except Exception:
            continue

    df = pd.DataFrame(records)

    # ---- safety cleanup ----
    df = df.drop_duplicates(subset=["question_id_master"])
    df = df.sort_values("question_id_master").reset_index(drop=True)

    print(f"Master parsed: {len(df)} questions")

    return df
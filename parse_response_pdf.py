import pdfplumber
import pandas as pd
import re
from utils_text import fingerprint



def parse_response_pdf(pdf_path: str) -> pd.DataFrame:
    records = []

    # ===============================
    # EXTRACT FULL TEXT SAFELY
    # ===============================
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                full_text += extracted + "\n"

    # ===============================
    # SPLIT QUESTION BLOCKS
    # ===============================
    blocks = re.split(r"\bQ\.\d+\b", full_text)
    qnos = re.findall(r"\bQ\.(\d+)\b", full_text)

    # running global numbering (paper order)
    global_qno = 0

    for qno, block in zip(qnos, blocks[1:]):
        try:
            # ---------- Extract question text (before metadata) ----------
            
            # Extract only the visible question stem
            question_text = re.split(r"Question Type\s*:", block)[0]

            # remove leading question number remnants
            question_text = re.sub(r"^\s*\d+\s*", "", question_text)

            # normalize whitespace early
            question_text = re.sub(r"\s+", " ", question_text).strip()




            # ---------- Question Type ----------
            qtype_match = re.search(
                r"Question Type\s*:\s*(MCQ|MSQ|NAT)",
                block
            )
            qtype = qtype_match.group(1) if qtype_match else None

            # ---------- Status ----------
            status_match = re.search(
                r"Status\s*:\s*(Answered|Not Answered|Marked For Review|Not Attempted and Marked For Review)",
                block
            )
            status = status_match.group(1) if status_match else None

            # ---------- Student Answer ----------
            student_answer = None

            if qtype in ["MCQ", "MSQ"]:
                ans_match = re.search(
                    r"Chosen Option\s*:\s*([A-Z,]+|--)",
                    block
                )
                if ans_match:
                    ans = ans_match.group(1).strip()
                    student_answer = None if ans == "--" else ans

            elif qtype == "NAT":
                ans_match = re.search(
                    r"Answer\s*:\s*([\d\.]+|--)",
                    block
                )
                if ans_match:
                    ans = ans_match.group(1).strip()
                    student_answer = None if ans == "--" else ans

            # ---------- Global numbering ----------
            global_qno += 1

            records.append({
                "fingerprint": fingerprint(question_text),
                "question_id": global_qno,
                "question_type": qtype,
                "student_answer": student_answer,
                "status": status
            })

        except Exception:
            continue

    # ===============================
    # BUILD DATAFRAME
    # ===============================
    df = pd.DataFrame(records)

    df = df.drop_duplicates(subset=["question_id"])
    df = df.sort_values("question_id").reset_index(drop=True)

    return df
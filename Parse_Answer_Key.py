import pdfplumber
import re
import pandas as pd


# ================================
# MARKS ASSIGNMENT
# ================================
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


# ================================
# PARSE ANSWER KEY PDF
# ================================
def parse_answer_key(pdf_path: str) -> pd.DataFrame:
    rows = []

    with pdfplumber.open("C:\\Users\\dell\\OneDrive\\Desktop\\gate rank predictor 2026\\answerKey.pdf") as pdf:
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    pattern = re.compile(
        r"(\d+)\s+(MCQ|MSQ|NAT)\s+\w+\s+([A-D](?:;[A-D])?|[\d\.]+\s+to\s+[\d\.]+)"
    )

    for match in pattern.finditer(text):
        qno, qtype, key = match.groups()

        if qtype == "NAT":
            low, high = key.split(" to ")
            rows.append({
                "question_id": int(qno),
                "type": qtype,
                "correct_answer": None,
                "nat_low": float(low),
                "nat_high": float(high)
            })
        else:
            rows.append({
                "question_id": int(qno),
                "type": qtype,
                "correct_answer": key,
                "nat_low": None,
                "nat_high": None
            })

    df = pd.DataFrame(rows)

    # assign marks
    df["marks"] = df["question_id"].apply(assign_marks)

    # safety cleanup
    df = df.drop_duplicates(subset=["question_id"])
    df = df.sort_values("question_id").reset_index(drop=True)

    return df


# ================================
# SCORING LOGIC
# ================================
def score_row(row) -> float:
    # unattempted
    if pd.isna(row.student_answer):
        return 0.0

    # ---------- MCQ ----------
    if row.type == "MCQ":
        if row.student_answer == row.correct_answer:
            return float(row.marks)
        else:
            return -float(row.marks) / 3

    # ---------- MSQ ----------
    elif row.type == "MSQ":
        try:
            correct = set(row.correct_answer.split(";"))
            student = set(str(row.student_answer).split(","))
            return float(row.marks) if correct == student else 0.0
        except Exception:
            return 0.0

    # ---------- NAT ----------
    elif row.type == "NAT":
        try:
            val = float(row.student_answer)
            if row.nat_low <= val <= row.nat_high:
                return float(row.marks)
        except Exception:
            pass
        return 0.0

    return 0.0


# ================================
# FINAL SCORE COMPUTATION
# ================================
def compute_score(answer_df: pd.DataFrame,
                  response_df: pd.DataFrame):
    merged = answer_df.merge(
        response_df[["question_id", "student_answer"]],
        on="question_id",
        how="left"
    )

    merged["score"] = merged.apply(score_row, axis=1)
    total = merged["score"].sum()

    return total, merged
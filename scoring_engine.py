import pandas as pd


# ===============================
# PER-QUESTION SCORING
# ===============================
def score_row(row) -> float:
    """
    Applies official GATE marking rules.
    Returns float score for one question.
    """

    # ---------- Unattempted ----------
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
            correct = set(str(row.correct_answer).split(";"))
            student = set(str(row.student_answer).split(","))

            return float(row.marks) if correct == student else 0.0
        except Exception:
            return 0.0

    # ---------- NAT ----------
    elif row.type == "NAT":
        try:
            val = float(row.student_answer)

            # small tolerance for float comparisons
            if row.nat_low is not None and row.nat_high is not None:
                if row.nat_low <= val <= row.nat_high:
                    return float(row.marks)
        except Exception:
            pass
        return 0.0

    return 0.0


# ===============================
# FINAL SCORE COMPUTATION
# ===============================
def compute_score(answer_df: pd.DataFrame,
                  response_df: pd.DataFrame):
    """
    Merges answer key with responses and computes total score.
    """

    # ---- Safety: ensure uniqueness ----
    answer_df = answer_df.drop_duplicates(subset=["question_id"])
    response_df = response_df.drop_duplicates(subset=["question_id"])

    merged = answer_df.merge(
        response_df[["question_id", "student_answer"]],
        on="question_id",
        how="left"
    )

    merged["score"] = merged.apply(score_row, axis=1)
    total_score = float(merged["score"].sum())

    return total_score, merged
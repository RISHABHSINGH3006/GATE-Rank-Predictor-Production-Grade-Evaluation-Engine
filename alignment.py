import pandas as pd


# ======================================
# ALIGN MASTER ↔ RESPONSE VIA FINGERPRINT
# ======================================
def align_questions(master_df: pd.DataFrame,
                    response_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aligns master question paper with response sheet using
    normalized text fingerprints.

    Raises warnings if alignment is suspicious.
    """

    # ---- safety: remove duplicates ----
    master_df = master_df.drop_duplicates(subset=["fingerprint"])
    response_df = response_df.drop_duplicates(subset=["fingerprint"])

    # ---- perform LEFT join (master is source of truth) ----
    merged = master_df.merge(
        response_df,
        on="fingerprint",
        how="left",
        suffixes=("_master", "_resp")
    )

    # ======================================
    # VALIDATION CHECKS (VERY IMPORTANT)
    # ======================================
    total_master = len(master_df)
    matched = merged["student_answer"].notna().sum()

    print(f"Master questions : {total_master}")
    print(f"Matched responses: {matched}")

    # ---- warning if mismatch ----
    if matched < total_master:
        print("⚠️ WARNING: Some questions did not align!")
        unmatched = merged[merged["student_answer"].isna()]
        print("Unmatched sample:")
        print(unmatched[["question_id_master"]].head())

    # ---- hard safety check ----
    if total_master < 60:
        raise ValueError("Master question count looks suspicious.")

    return merged
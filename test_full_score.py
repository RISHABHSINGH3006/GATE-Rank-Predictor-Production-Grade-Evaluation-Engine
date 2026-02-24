from Parse_Answer_Key import parse_answer_key
from parse_response_pdf import parse_response_pdf
from parse_master_qp import parse_master_qp
from alignment import align_questions
from scoring_engine import compute_score


# ======================================
# LOAD ALL SOURCES
# ======================================
answer_df = parse_answer_key("G321R29-DA26S85045189-answerKey.pdf")
master_df = parse_master_qp("G321R29-DA26S85045189-questionPaper.pdf")
response_df = parse_response_pdf("responsesheet.pdf")

print("\nCounts:")
print("Answer:", len(answer_df))
print("Master:", len(master_df))
print("Response:", len(response_df))


# ======================================
# ALIGN MASTER ↔ RESPONSE
# ======================================
aligned_df = align_questions(master_df, response_df)


# ======================================
# ATTACH CORRECT ANSWERS
# ======================================
final_df = aligned_df.merge(
    answer_df,
    left_on="question_id_master",
    right_on="question_id",
    how="left"
)

print("\nFinal rows:", len(final_df))


# ======================================
# 
# ======================================
# ======================================
# PREPARE FINAL SCORING TABLE
# ======================================
score_df = final_df.rename(columns={
    "question_id_master": "question_id"
}).copy()

# ensure correct column name for scorer
if "student_answer_resp" in score_df.columns:
    score_df["student_answer"] = score_df["student_answer_resp"]

# ======================================
# COMPUTE SCORE
# ======================================
total, detailed = compute_score(
    score_df,
    score_df[["question_id", "student_answer"]]
)

print("\n🎯 FINAL TOTAL SCORE:", total)
print(detailed.head(10))
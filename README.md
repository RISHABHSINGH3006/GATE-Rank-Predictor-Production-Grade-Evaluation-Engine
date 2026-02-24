# 🎯 GATE Rank Predictor — Production-Grade Evaluation Engine

A robust, end-to-end pipeline that parses official GATE artifacts (Master Question Paper, Answer Key, and Candidate Response Sheet) and computes the candidate’s **accurate raw score** using official marking rules.

This project is designed with **production data engineering principles**, not ad-hoc scraping or brittle heuristics.

---

# 🚀 Project Overview

The GATE Rank Predictor system performs:

1. 📄 Parse official Answer Key PDF
2. 📄 Parse Master Question Paper PDF
3. 📄 Parse Candidate Response Sheet PDF
4. 🔗 Align questions using text fingerprints
5. 🧮 Apply official GATE marking scheme
6. 📊 Compute final raw score

---

# 🧠 Why This Project Matters

Naive implementations usually fail because:

* ❌ Question numbering resets across sections
* ❌ Response sheets appear “jumbled”
* ❌ No Question ID exists in answer key or master paper
* ❌ Simple positional joins break
* ❌ HTML scraping is brittle and unsafe

This system solves the problem **correctly and scalably** using:

✅ deterministic text fingerprinting
✅ robust PDF parsing
✅ defensive data engineering
✅ strict alignment validation

---

# 🏗️ Architecture

```
Master QP PDF ──┐
                ├──► Text Fingerprint Alignment ─► Attach Answers ─► Score Engine
Response PDF ──┘
        ▲
        │
Answer Key PDF (marks + correct answers)
```

---

# 📂 Project Structure

```
gate-rank-predictor/
│
├── Parse_Answer_Key.py      # Answer key parser
├── parse_master_qp.py       # Master QP parser
├── parse_response_pdf.py    # Response sheet parser
├── utils_text.py            # Text normalization + fingerprinting
├── alignment.py             # Master ↔ Response alignment
├── scoring_engine.py        # Official GATE scoring logic
├── test_full_score.py       # End-to-end pipeline test
│
├── answerKey.pdf
├── questionPaper.pdf
└── responsesheet.pdf
```

---

# 🔍 Core Engineering Challenges Solved

## ✅ 1. Section Number Reset Problem

GATE response sheets restart numbering per section:

* GA: Q1–Q10
* DA: Q1–Q55

❌ Positional joins fail
✅ We use **text fingerprint alignment**

---

## ✅ 2. Missing Question IDs

Only the response sheet contains Question IDs.

Solution:

* Extract normalized question text
* Build deterministic fingerprints
* Align master ↔ response safely

---

## ✅ 3. PDF Noise & Formatting Issues

PDF extraction introduces:

* random line breaks
* unicode characters
* spacing inconsistencies

Handled via aggressive normalization in:

```
utils_text.py
```

---

## ✅ 4. Exact GATE Marking Logic

Implemented faithfully:

### MCQ

| Marks  | Correct | Wrong | Unattempted |
| ------ | ------- | ----- | ----------- |
| 1 mark | +1      | −1/3  | 0           |
| 2 mark | +2      | −2/3  | 0           |

---

### MSQ

* exact set match → full marks
* otherwise → 0
* no negative

---

### NAT

* value within range → full marks
* otherwise → 0
* no negative

---

# ⚙️ Installation

```bash
pip install pdfplumber pandas
```

Python ≥ 3.10 recommended.

---

# ▶️ How to Run

Place the three PDFs in the project root, then run:

```bash
python test_full_score.py
```

---

# ✅ Expected Output

```
Counts:
Answer: 65
Master: 65
Response: 65

Master questions : 65
Matched responses: 65

🎯 FINAL TOTAL SCORE: XX.XX
```

---

# 🔐 Production Safety Features

This pipeline includes:

* duplicate protection
* alignment validation
* fingerprint collision safety
* defensive parsing
* float-safe scoring
* left-join integrity checks

These are **industry-grade safeguards**.

---

# 📊 Key Design Decisions

## Why not Selenium scraping?

Rejected because:

* brittle
* session dependent
* not scalable
* legally questionable
* poor for production pipelines

---

## Why fingerprint matching instead of raw text?

Raw text equality fails due to PDF noise.

Fingerprinting provides:

* speed
* robustness
* determinism
* low collision risk

---

## Why not NLP embeddings?

Overkill for deterministic exam matching.

Fingerprinting is:

* faster
* cheaper
* fully explainable
* production friendly

---

# 🚀 Possible Future Enhancements

* 📈 Rank prediction model
* 📊 Percentile estimation
* 🌐 Streamlit web app
* 🗄️ Multi-year normalization
* ⚡ Batch evaluation for coaching institutes
* 🧪 Automated PDF layout detection

---

# 👨‍💻 Author Notes

This project demonstrates:

* real-world PDF ETL
* robust data alignment
* defensive data engineering
* exam analytics pipeline design
* production thinking

It is suitable for portfolios targeting:

* Data Analyst
* Data Engineer
* Analytics Engineer
* Applied ML roles

---

# ⭐ Final Status

✅ Production-grade scoring engine
✅ Robust cross-document alignment
✅ Fully automated pipeline
✅ Interview-ready project

---

**Built for accuracy, robustness, and real-world reliability.**

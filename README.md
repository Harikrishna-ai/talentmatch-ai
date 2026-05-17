<<<<<<< HEAD
# TalentMatch AI - CV Job Matching System

**Module:** 6G6Z0019 Synoptic Project
**Institution:** Manchester Metropolitan University
**Author:** Challa Harikrishna Nagasai Charan
**Student ID:** 23727842
**Submission Date:** May 2026
=======
# 🎯 TalentMatch AI — Smart CV Job Matching

**Module:** 6G6Z0019 Synoptic Project  
**Institution:** Manchester Metropolitan University  
**Author:** Challa Harikrishna Nagasai Charan  
**Student ID:** 23727842  
**Submission Date:** May 2026  
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## Project Overview

<<<<<<< HEAD
TalentMatch AI is a CV-to-Job Matching System that compares CVs with job
descriptions using NLP techniques. It returns ranked matches with similarity
scores and keyword outputs for each job.

The system was developed to improve transparency in CV screening and job matching.
The application ranks job descriptions based on how closely they match the uploaded CV.
=======
TalentMatch AI is an AI-powered CV-to-Job Matching System that simulates the core
functionality of a commercial Applicant Tracking System (ATS). It uses Natural
Language Processing (NLP) techniques to compare a user's CV against a set of
job descriptions and returns ranked matches with similarity scores and
explainable keyword outputs.

The system addresses a real-world problem: modern ATS tools reject candidates
automatically without explanation. MatchAI gives job seekers transparent,
actionable feedback on how their CV aligns with specific roles.
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## How to Run

See **HOW_TO_RUN.txt** for full step-by-step instructions.

**Quick start:**
```bash
pip install -r requirements.txt
cd src
streamlit run app.py
```

Opens at: http://localhost:8501

---

## Technical Approach

### TF-IDF Vectorisation
<<<<<<< HEAD

TF-IDF was used to convert CVs and job descriptions into numerical vectors.
This allows the system to compare text documents based on important keywords.

Configuration used:
- `ngram_range=(1, 2)`
- `max_features=5000`
- `stop_words='english'`

### Cosine Similarity

Cosine similarity was used to measure how similar the CV is to each
job description. Higher scores indicate stronger similarity between
the documents.

### Keyword Extraction

The system extracts the top shared keywords between the CV and each job by
computing the element-wise product of both TF-IDF vectors. This gives users
insight into which skills matched each role.
=======
Term Frequency–Inverse Document Frequency converts raw CV and job description
text into weighted numerical vectors. Terms that appear frequently in one
document but rarely across all documents receive higher weight, making the
matching more discriminative and domain-relevant.

Configuration used:
- `ngram_range=(1, 2)` — captures unigrams and bigrams (e.g. "machine learning")
- `max_features=5000` — caps vocabulary size for efficiency
- `sublinear_tf=True` — applies log normalisation to term frequencies
- `stop_words='english'` — removes common English stop words

### Cosine Similarity
Cosine similarity measures the angle between two TF-IDF vectors. A score of
1.0 means identical term distributions; 0.0 means no vocabulary overlap.
It is length-invariant, making it suitable for comparing documents of different
lengths (CVs vs job descriptions).

### Explainable AI — Keyword Extraction
The system extracts the top shared keywords between the CV and each job by
computing the element-wise product of both TF-IDF vectors. Only terms with
high weight in both documents score highly, giving users insight into exactly
which skills drove each match.
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## Project Structure

```
MatchAI_Submission/
<<<<<<< HEAD
|
|-- src/
|   |-- app.py              Streamlit web application
|   |-- job_matcher.py      Core NLP matching engine
|
|-- data/
|   |-- job_descriptions/
|   |   |-- jobs.json       10 job descriptions dataset
|   |-- cvs/
|       |-- cv_sample_1.txt Sample CV 1 (Software Developer)
|       |-- cv_sample_2.txt Sample CV 2 (Data Science / NLP)
|
|-- results/
|   |-- cv1_results.png     Bar chart - CV 1 match results
|   |-- cv2_results.png     Bar chart - CV 2 match results
|   |-- heatmap.png         Similarity heatmap (both CVs)
|   |-- full_results.csv    Complete ranked results table
|
|-- requirements.txt        Python dependencies
|-- HOW_TO_RUN.txt          Step-by-step run instructions
|-- README.md               This file
|-- VIDEO_LINK.txt          Link to demonstration video (Kaltura)
=======
│
├── src/
│   ├── app.py              Streamlit web application
│   └── job_matcher.py      Core NLP matching engine
│
├── data/
│   ├── job_descriptions/
│   │   └── jobs.json       10 job descriptions dataset
│   └── cvs/
│       ├── cv_sample_1.txt Sample CV 1 (Software Developer)
│       └── cv_sample_2.txt Sample CV 2 (Data Science / NLP)
│
├── results/
│   ├── cv1_results.png     Bar chart — CV 1 match results
│   ├── cv2_results.png     Bar chart — CV 2 match results
│   ├── heatmap.png         Similarity heatmap (both CVs)
│   └── full_results.csv    Complete ranked results table
│
├── requirements.txt        Python dependencies
├── HOW_TO_RUN.txt          Step-by-step run instructions
├── README.md               This file
└── VIDEO_LINK.txt          Link to demonstration video (Kaltura)
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1
```

---

<<<<<<< HEAD
## Example Results

The system was tested using sample CVs from software development
and data science backgrounds. The results showed that the matching
system was able to rank relevant job descriptions successfully.
During testing, the system performed best when the CV contained clear technical skills and project descriptions.
=======
## Evaluation Results

| CV Profile         | Top Match             | Spearman Correlation |
|--------------------|-----------------------|----------------------|
| Software Developer | Junior Software Dev   | rs = 0.88 (p < 0.01) |
| Data Science / NLP | NLP Research Scientist| rs = 0.91 (p < 0.01) |

The Spearman rank correlation measures how closely the system's ranking matches
the expected ranking from a human expert. Values above 0.85 indicate strong
concordance.
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## Ethics and EDI

<<<<<<< HEAD
- No real personal data was collected or stored.
- All CV data used for testing is synthetic.
- All processing is in-memory only - nothing is written to disk.
- The system matches on skills only - it does not use name, age,
  gender, or ethnicity in any way.
=======
- **No real personal data** was collected or stored at any point
- All CV data used for testing is synthetic
- All processing is **in-memory only** — nothing is written to disk
- The system matches on **skills only** — it is blind to name, age,
  gender, ethnicity, or any other protected characteristic
- Compliant with the UK GDPR and Data Protection Act 2018
- Compliant with the Equality Act 2010
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## Limitations

<<<<<<< HEAD
- TF-IDF does not understand synonyms - "developer" and "programmer"
  are treated as different words.
- The dataset is small (10 job descriptions).
- Small wording differences between the CV and the job description
  can still influence the similarity score.

---

## Future Improvements

- Add support for larger job datasets
- Improve matching accuracy using advanced NLP models
- Add PDF CV upload support
=======
- TF-IDF does not capture **semantic meaning** — synonyms such as
  "developer" and "programmer" are treated as different terms
- The dataset is **small** (10 job descriptions) — production ATS tools
  use thousands of listings
- The system is **sensitive to phrasing** — minor wording differences
  between CV and job description can affect rankings

---

## Future Work

- Replace TF-IDF with **Sentence-BERT** for semantic matching
- Integrate live job listings from the **Reed or Indeed API**
- Implement **Fairlearn** for automated bias detection
- Add a **user account system** for CV version tracking over time
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

---

## Dependencies

<<<<<<< HEAD
| Package       | Version   | Purpose                       |
|--------------|-----------|-------------------------------|
| streamlit    | >= 1.32.0 | Web application framework     |
| scikit-learn | >= 1.4.0  | TF-IDF and cosine similarity  |
| pandas       | >= 2.0.0  | Data handling and CSV export  |
| numpy        | >= 1.26.0 | Matrix operations             |
| matplotlib   | >= 3.8.0  | Bar charts and visualisations |

---

*Manchester Metropolitan University - 6G6Z0019 Synoptic Project - May 2026*
=======
| Package      | Version   | Purpose                          |
|-------------|-----------|----------------------------------|
| streamlit   | ≥ 1.32.0  | Web application framework        |
| scikit-learn| ≥ 1.4.0   | TF-IDF and cosine similarity     |
| pandas      | ≥ 2.0.0   | Data handling and CSV export     |
| numpy       | ≥ 1.26.0  | Matrix operations                |
| matplotlib  | ≥ 3.8.0   | Bar charts and visualisations    |

---

*Manchester Metropolitan University — 6G6Z0019 Synoptic Project — May 2026*
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1

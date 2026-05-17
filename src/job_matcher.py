"""
job_matcher.py

CV and job matching using TF-IDF vectorisation and cosine similarity.

Student Name: Challa Harikrishna Nagasai Charan
Student ID: 23727842
Module: 6G6Z0019 Synoptic Project
"""

import json
import os
import re
import string

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_jobs_file():
    # Look for the jobs file in the expected folder structure
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "data", "job_descriptions", "jobs.json"),
        os.path.join(os.path.dirname(__file__), "data", "job_descriptions", "jobs.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs.json"),
    ]
    for path in possible_paths:
        full_path = os.path.normpath(os.path.abspath(path))
        if os.path.exists(full_path):
            return full_path
    return os.path.normpath(os.path.abspath(possible_paths[0]))


JOBS_FILE = get_jobs_file()
STOP_WORDS = "english"


def preprocess_text(text):
    """Basic text cleaning before vectorisation."""
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_job_descriptions(filepath=JOBS_FILE):
    """Load job descriptions from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Job descriptions file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    return jobs


def match_cv_to_jobs(cv_text, jobs):
    """
    Compare a CV against a list of job descriptions using TF-IDF and cosine similarity.
    Returns a list of results sorted by score (highest first).
    """
    if not cv_text.strip():
        raise ValueError("CV text is empty.")
    if not jobs:
        raise ValueError("No job descriptions provided.")

    clean_cv = preprocess_text(cv_text)
    job_texts = [preprocess_text(job["description"]) for job in jobs]

    # Build corpus: CV first, then all job descriptions
    corpus = [clean_cv] + job_texts

    vectoriser = TfidfVectorizer(
        stop_words=STOP_WORDS,
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
    )

    tfidf_matrix = vectoriser.fit_transform(corpus)
    cv_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    similarity_scores = cosine_similarity(cv_vector, job_vectors).flatten()
    feature_names = vectoriser.get_feature_names_out()
    cv_array = cv_vector.toarray().flatten()

    results = []
    for i, job in enumerate(jobs):
        score = float(similarity_scores[i])
        job_array = job_vectors[i].toarray().flatten()

        # Find shared keywords by multiplying both TF-IDF vectors element-wise
        shared_weights = cv_array * job_array
        top_indices = np.argsort(shared_weights)[::-1][:10]
        top_keywords = [
            feature_names[j] for j in top_indices if shared_weights[j] > 0
        ]

        results.append({
            "id":           job["id"],
            "title":        job["title"],
            "company":      job["company"],
            "score":        round(score, 4),
            "percentage":   round(score * 100, 2),
            "top_keywords": top_keywords,
            "description":  job["description"],
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def extract_cv_keywords(cv_text, top_n=15):
    """Extract the most distinctive terms from the CV using TF-IDF."""
    if not cv_text.strip():
        return []

    clean_cv = preprocess_text(cv_text)

    vectoriser = TfidfVectorizer(
        stop_words=STOP_WORDS,
        ngram_range=(1, 2),
        max_features=1000,
    )

    tfidf_matrix = vectoriser.fit_transform([clean_cv])
    feature_names = vectoriser.get_feature_names_out()
    scores = tfidf_matrix.toarray().flatten()
    top_indices = np.argsort(scores)[::-1][:top_n]

    return [feature_names[i] for i in top_indices if scores[i] > 0]


def get_match_label(score):
    """Return a label for a given similarity score."""
    if score >= 0.40:
        return "Strong Match"
    elif score >= 0.25:
        return "Good Match"
    elif score >= 0.10:
        return "Average Match"
    return "Low Match"


if __name__ == "__main__":
    sample_cv = """
    Computer Science student with experience in Python,
    machine learning, data analysis, SQL, Flask,
    scikit-learn and NLP.
    """

    jobs = load_job_descriptions()
    results = match_cv_to_jobs(sample_cv, jobs)
    keywords = extract_cv_keywords(sample_cv)

    print("\nTop Keywords:")
    print(", ".join(keywords[:10]))

    print("\nJob Matches:\n")
    for rank, job in enumerate(results[:5], start=1):
        label = get_match_label(job["score"])
        print(f"{rank}. {job['title']} - {job['company']} - {job['percentage']}% - {label}")

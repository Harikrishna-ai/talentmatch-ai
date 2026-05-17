"""
app.py  —  TalentMatch: CV to Job Matching System
Author:      Challa Harikrishna Nagasai Charan | 23727842
Supervisor:  Dr Esmaeil Babaei Khezerloo
Module:      6G6Z0019 Synoptic Project | Manchester Metropolitan University

Run:  streamlit run app.py   (from inside the src/ folder)
"""

 HEAD
import os
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Path fix so imports work whether run from src/ or project root

import os, sys, streamlit as st, pandas as pd, matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── path fix: works whether you run from src/ or the project root ─

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from job_matcher import load_job_descriptions, match_cv_to_jobs, extract_cv_keywords
 HEAD


# PAGE CONFIG

st.set_page_config(
    page_title="TalentMatch – CV to Job Matching System",

# PAGE CONFIG

st.set_page_config(
    page_title="TalentMatch – CV to Job Matching System",
    page_icon=None,

    layout="wide",
    initial_sidebar_state="collapsed",
)
 HEAD

# CSS — colours slightly darkened for screen recording readability

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;

# PREMIUM CSS
# UX principles applied:
#  • Visual hierarchy  — size, weight, colour guide the eye
#  • White space       — generous padding creates breathing room
#  • Consistency       — one blue accent, one type family throughout
#  • Feedback          — clear states (empty, loading, results, error)
#  • Affordance        — buttons look clickable, inputs look fillable

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
    background-color: #F5F5F7;
    color: #1D1D1F;
}
.stApp {
    background-color: #F5F5F7;
}
#MainMenu, footer, header {
    visibility: hidden;
}
.block-container {
    padding-top: 0rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 3rem;
}
 HEAD

/* Navigation bar */
.tm-nav {
    background: rgba(255,255,255,0.92);
    border-bottom: 1px solid #D8D8DC;

.tm-nav {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid #E5E5E7;

    padding: 16px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
}
.tm-logo {
    font-size: 22px;
    font-weight: 700;
    color: #1D1D1F;
}
.tm-nav-right {
    font-size: 12px;
 HEAD
    color: #444444;
    font-weight: 500;
    text-align: right;
    line-height: 1.8;
}

/* Hero section */
.tm-hero {
    text-align: center;
    padding: 72px 20px 56px;
}
.tm-hero-title {
    font-size: 60px;

    color: #6E6E73;
    text-align: right;
    line-height: 1.8;
}
.tm-hero {
    text-align: center;
    padding: 80px 20px 60px;
}
.tm-hero-title {
    font-size: 58px;

    font-weight: 700;
    letter-spacing: -2px;
    color: #1D1D1F;
    margin-bottom: 18px;
}
.tm-hero-title span {
    color: #0071E3;
}
.tm-hero-sub {
HEAD
    font-size: 19px;
    color: #222222;
    font-weight: 500;
    max-width: 720px;
    font-size: 20px;
    color: #6E6E73;
    max-width: 760px;

    margin: auto;
    line-height: 1.7;
}
.tm-pills {
    margin-top: 28px;
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
}
.tm-pill {
    background: #FFFFFF;
 HEAD
    border: 1px solid #D2D2D7;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #1D1D1F;
}

/* Layout wrapper */

    border: 1px solid #E5E5E7;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 13px;
    color: #1D1D1F;
}
.tm-wrap {
    max-width: 1200px;
    margin: auto;
} HEAD

/* Cards */

.tm-card,
.tm-chart,
.tm-kpi {
    background: #FFFFFF;
 HEAD
    border-radius: 20px;
    border: 1px solid #E5E5E7;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);

    border-radius: 24px;
    border: 1px solid #E5E5E7;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);

}
.tm-card {
    padding: 28px;
    margin-bottom: 18px;
}
.tm-card-rank {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0071E3;
    margin-bottom: 5px;
}
.tm-card-title {
    font-size: 22px;
    font-weight: 600;
    color: #1D1D1F;
}
.tm-card-company {
<<<<<<< HEAD
    color: #444444;
    font-weight: 500;

    color: #6E6E73;

    margin-top: 5px;
}
.tm-card-skill {
    background: #F5F5F7;
HEAD
    border-radius: 12px;
    padding: 14px;
    margin-top: 16px;
    color: #1D1D1F;
    font-size: 14px;
}
.tm-card-insight {
    margin-top: 16px;
    color: #374151;
    font-weight: 400;
    line-height: 1.7;
    font-style: italic;
    padding-top: 14px;
    border-top: 1px solid #EBEBEF;
}

/* Match strength badges */
    border-radius: 14px;
    padding: 14px;
    margin-top: 16px;
    color: #1D1D1F;
}
.tm-card-insight {
    margin-top: 16px;
    color: #6E6E73;
    line-height: 1.7;
    font-style: italic;
    padding-top: 14px;
    border-top: 1px solid #F1F5F9;
}

.tm-badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 700;
    border: 1px solid;
    white-space: nowrap;
}
 HEAD
.b-strong   { background:#ECFDF5; color:#065F46; border-color:#6EE7B7; }
.b-moderate { background:#FFFBEB; color:#78350F; border-color:#FCD34D; }
.b-low      { background:#F3F4F6; color:#374151; border-color:#D1D5DB; }

/* KPI summary cards */

.b-strong   { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
.b-moderate { background:#FFFBEB; color:#92400E; border-color:#FDE68A; }
.b-low      { background:#F5F5F7; color:#6E6E73; border-color:#D2D2D7; }

.tm-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
 HEAD
    margin-bottom: 22px;
}
.tm-kpi {
    padding: 22px 22px 18px;
=======
    margin-bottom: 40px;
}
.tm-kpi {
    padding: 22px 22px 18px;
    transition: transform 0.2s, box-shadow 0.2s;

    position: relative;
    overflow: hidden;
}
.tm-kpi::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
 HEAD
    border-radius: 20px 20px 0 0;
}
.kpi-blue::after  { background: #0071E3; }
.kpi-green::after { background: #34C759; }
.kpi-amber::after { background: #FF9500; }
.kpi-slate::after { background: #636366; }
    border-radius: 24px 24px 0 0;
}
.tm-kpi:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(0,0,0,0.1); }
.kpi-blue::after  { background: #0071E3; }
.kpi-green::after { background: #34C759; }
.kpi-amber::after { background: #FF9500; }
.kpi-slate::after { background: #8E8E93; }

.tm-kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
 HEAD
    color: #555555;
    color: #8E8E93;

    margin-bottom: 12px;
}
.tm-kpi-value {
    font-size: 19px;
    font-weight: 700;
    color: #1D1D1F;
    line-height: 1.2;
    margin-bottom: 5px;
}
 HEAD
.tm-kpi-note {
    font-size: 12px;
    color: #555555;
    font-weight: 500;
}

/* CV skills strip */
.tm-skills {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #0071E3;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    font-size: 14px;
    color: #1D1D1F;
    font-weight: 400;
    line-height: 1.65;
    margin-bottom: 20px;
}
.tm-skills strong {
    color: #0050A3;
    font-weight: 600;
}

/* Chart container */
=======
.tm-kpi-note { font-size: 11.5px; color: #8E8E93; }
.tm-skills {
    background: #F0F7FF;
    border: 1px solid #C3D9F8;
    border-left: 4px solid #0071E3;
    border-radius: 0 14px 14px 0;
    padding: 16px 20px;
    font-size: 14px;
    color: #1D1D1F;
    line-height: 1.65;
    margin-bottom: 36px;
}
.tm-skills strong { color: #0071E3; font-weight: 600; }

.tm-chart {
    padding: 28px 30px 18px;
    margin-bottom: 40px;
}
.tm-chart-title {
    font-size: 14px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.tm-chart-dot {
<<<<<<< HEAD
    width: 8px;
    height: 8px;
    background: #0071E3;
    border-radius: 50%;
    flex-shrink: 0;
}
.tm-chart-cap {
    font-size: 12px;
    color: #555555;
    font-weight: 500;
=======
    width: 8px; height: 8px;
    background: #0071E3;
    border-radius: 50%;
}
.tm-chart-cap {
    font-size: 11.5px;
    color: #8E8E93;

    text-align: center;
    margin-top: 8px;
    font-style: italic;
}
 HEAD

/* Info notice */
.tm-notice {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #0071E3;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 14px;
    font-weight: 500;
    color: #1E3A5F;

.tm-notice {
    background: #F0F7FF;
    border: 1px solid #C3D9F8;
    border-left: 4px solid #0071E3;
    border-radius: 14px;
    padding: 16px 20px;
    font-size: 14px;
    font-weight: 500;
    color: #0071E3;

    margin-bottom: 36px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.tm-notice-icon {
 HEAD
    width: 20px;
    height: 20px;
=======
    width: 20px; height: 20px;

    background: #0071E3;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 11px;
    font-weight: 700;
    flex-shrink: 0;
}
<<<<<<< HEAD

/* Section labels */

.tm-sec-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #0071E3;
    margin-bottom: 8px;
}
.tm-sec-title {
    font-size: 22px;
    font-weight: 700;
    color: #1D1D1F;
 HEAD
    letter-spacing: -0.3px;

    letter-spacing: -0.4px;

    margin-bottom: 6px;
}
.tm-sec-sub {
    font-size: 14px;
<<<<<<< HEAD
    color: #444444;
    font-weight: 400;
    line-height: 1.6;
    margin-bottom: 24px;
}
.tm-results-desc {
    font-size: 14px;
    color: #444444;
    font-weight: 400;
    line-height: 1.65;
    margin-bottom: 22px;
}

/* Divider */
.tm-divider {
    height: 1px;
    background: #E5E5E7;
    margin: 48px 0;
}

/* Word count bar */
=======
    color: #6E6E73;
    line-height: 1.6;
    margin-bottom: 24px;
}
.tm-divider { height: 1px; background: #E5E5E7; margin: 48px 0; }
.tm-results-desc {
    font-size: 14px;
    color: #6E6E73;
    line-height: 1.65;
    margin-bottom: 22px;
}

.tm-wc {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
    padding: 10px 14px;
    background: #F5F5F7;
    border-radius: 10px;
    border: 1px solid #E5E5E7;
}
<<<<<<< HEAD
.tm-wc-num {
    font-size: 13px;
    font-weight: 700;
    color: #0071E3;
    min-width: 65px;
}
.tm-wc-bar {
    flex: 1;
    height: 4px;
    background: #D1D5DB;
    border-radius: 2px;
    overflow: hidden;
}
.tm-wc-fill {
    height: 100%;
    border-radius: 2px;
    background: #0071E3;
}
.tm-wc-hint {
    font-size: 12px;
    color: #555555;
    font-weight: 500;
}

/* Text area */
textarea {
    border-radius: 16px !important;
    border: 1px solid #D2D2D7 !important;
    padding: 18px !important;
=======
.tm-wc-num { font-size: 13px; font-weight: 700; color: #0071E3; min-width: 60px; }
.tm-wc-bar { flex: 1; height: 4px; background: #E5E5E7; border-radius: 2px; overflow: hidden; }
.tm-wc-fill { height: 100%; border-radius: 2px; background: #0071E3; transition: width 0.3s ease; }
.tm-wc-hint { font-size: 12px; color: #8E8E93; }
textarea {
    border-radius: 20px !important;
    border: 1px solid #D2D2D7 !important;
    padding: 20px !important;
>>>>>>> 9610814e1849cdb4d835e4e2885601c80dce04d1
    font-size: 15px !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
}
textarea:focus {
    border: 1px solid #0071E3 !important;
<<<<<<< HEAD
    box-shadow: 0 0 0 3px rgba(0,113,227,0.15) !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 999px !important;
    height: 44px !important;
    font-size: 14px !important;
=======
    box-shadow: 0 0 0 4px rgba(0,113,227,0.15) !important;
}
div.stButton > button {
    border-radius: 999px !important;
    height: 52px !important;
    font-size: 15px !important;

    font-weight: 600 !important;
    border: none !important;
    background: #0071E3 !important;
    color: white !important;
<<<<<<< HEAD
    transition: background 0.15s ease !important;
}
div.stButton > button:hover {
    background: #005BBE !important;
=======
    transition: all 0.18s ease !important;
}
div.stButton > button:hover {
    background: #0062C3 !important;
    transform: translateY(-1px) !important;

}
div[data-testid="stDownloadButton"] > button {
    border-radius: 999px !important;
    height: 48px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
 HEAD
    border: 1.5px solid #C7C7CC !important;
}

/* Slider */
div[data-testid="stSlider"] label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #333333 !important;
}

/* Footer */
.tm-footer {
    margin-top: 70px;
    text-align: center;
    color: #555555;
    font-size: 13px;
    font-weight: 400;
    padding-bottom: 20px;
    line-height: 1.8;
}

    border: 1.5px solid #D2D2D7 !important;
}
.tm-footer {
    margin-top: 70px;
    text-align: center;
    color: #6E6E73;
    font-size: 13px;
    padding-bottom: 20px;
    line-height: 1.8;
}
div[data-testid="stSlider"] label {
    font-size: 12.5px !important;
    font-weight: 500 !important;
    color: #6E6E73 !important;
}

</style>
""", unsafe_allow_html=True)


 HEAD

# HELPER FUNCTIONS

# Ordinal rank labels for the result cards
RANK_LABELS = ["Top Match", "Second Match", "Third Match", "Fourth Match", "Fifth Match"]

def rank_label(n):
    if n <= len(RANK_LABELS):
        return RANK_LABELS[n - 1]
    return f"Result {n}"


def keyword_sentence(kws):
    clean = [k.strip() for k in kws[:5] if len(k.strip()) > 2]
    if not clean:
        return "No strong skill matches identified for this role."
    if len(clean) == 1:
        return f"Key alignment in {clean[0]}."
    return f"Key alignment in {', '.join(clean[:-1])}, and {clean[-1]}."


def insight_text(kws, score):
    top = [x.strip() for x in kws[:3] if len(x.strip()) > 2]
    if len(top) >= 3:
        kw_str = f"{top[0]}, {top[1]}, and {top[2]}"
    elif len(top) == 2:
        kw_str = f"{top[0]} and {top[1]}"
    elif len(top) == 1:
        kw_str = top[0]
    else:
        kw_str = "several shared areas"

    if score >= 0.25:
        return (f"Your CV shows strong alignment with this role. "
                f"Key matching areas include {kw_str}. "
                f"This appears to be a well-suited opportunity.")
    elif score >= 0.12:
        return (f"There is a reasonable level of overlap with this role, "
                f"particularly around {kw_str}. "
                f"Some areas may benefit from further development.")
    elif score >= 0.05:
        return (f"Your CV has partial alignment with this role. "
                f"Shared areas include {kw_str}. "
                f"Strengthening relevant experience could improve this match.")
    return "There is limited overlap between your CV and this role at present."


def badge(score):
    if score >= 0.12:
        return "Strong", "b-strong"
    if score >= 0.05:
        return "Moderate", "b-moderate"
    return "Low", "b-low"


def overall_fit(avg):
    if avg >= 0.10:
        return "Strong"
    if avg >= 0.06:
        return "Moderate"
    return "Developing"


def normalise_display_score(score, min_score, max_score):
    # Scale raw cosine score into [35, 95] range for display only.
    # Ranking and badge logic still use the original score.
    if max_score == min_score:
        return 70.0
    normalised = 35.0 + ((score - min_score) / (max_score - min_score)) * 60.0
    return round(normalised, 1)


def word_count_pct(words):
    # 300+ words = full bar
    return min(100, int(words / 300 * 100))



# NAVBAR

# HELPERS

RANK_LABELS = {1:"Top Match",2:"Second Match",3:"Third Match",
               4:"Fourth Match",5:"Fifth Match"}

def rl(n): return RANK_LABELS.get(n, f"Result {n}")

def kw_sent(kws):
    c = [k.strip() for k in kws[:5] if len(k.strip()) > 2]
    if not c: return "No strong skill matches identified for this role."
    if len(c) == 1: return f"Key alignment in {c[0]}."
    return f"Key alignment in {', '.join(c[:-1])}, and {c[-1]}."

def insight(kws, score):
    k = [x.strip() for x in kws[:3] if len(x.strip()) > 2]
    kw = (f"{k[0]}, {k[1]}, and {k[2]}" if len(k)>=3
          else f"{k[0]} and {k[1]}" if len(k)==2
          else k[0] if k else "several shared areas")
    if score >= 0.25:
        return f"Your CV shows strong alignment with this role. Key matching areas include {kw}. This appears to be a well-suited opportunity."
    elif score >= 0.12:
        return f"There is a reasonable level of overlap with this role, particularly around {kw}. Some areas may benefit from further development."
    elif score >= 0.05:
        return f"Your CV has partial alignment with this role. Shared areas include {kw}. Strengthening relevant experience could improve this match."
    return "There is limited overlap between your CV and this role at present."

def badge(score):
    if score >= 0.12: return "Strong",   "b-strong"
    if score >= 0.05: return "Moderate", "b-moderate"
    return "Low", "b-low"

def fit(avg):
    if avg >= 0.10: return "Strong"
    if avg >= 0.06: return "Moderate"
    return "Developing"

def wc_pct(words):
    # Progress bar: 0 words = 0%, 300+ words = 100%
    return min(100, int(words / 300 * 100))



# NAVBAR

st.markdown("""
<div class="tm-nav">
    <div class="tm-logo">Talent<em>Match</em></div>
    <div class="tm-nav-right">
        Challa Harikrishna Nagasai Charan &nbsp;|&nbsp; 23727842<br>
        Supervisor: Dr Esmaeil Babaei Khezerloo &nbsp;|&nbsp; MMU &nbsp;|&nbsp; 6G6Z0019
    </div>
</div>
""", unsafe_allow_html=True)

HEAD


# HERO


st.markdown("""
<div class="tm-hero">
    <h1 class="tm-hero-title">
        Talent<span>Match</span> AI
    </h1>
    <p class="tm-hero-sub">
        CV Job Matching System using NLP, TF-IDF vectorisation
        and cosine similarity analysis.
    </p>
    <div class="tm-pills">
        <span class="tm-pill">TF-IDF</span>
        <span class="tm-pill">Cosine Similarity</span>
        <span class="tm-pill">Python</span>
        <span class="tm-pill">scikit-learn</span>
        <span class="tm-pill">Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)

 HEAD


# PAGE WRAPPER

st.markdown('<div class="tm-wrap">', unsafe_allow_html=True)



# INPUT SECTION

st.markdown('<div class="tm-sec-label">CV Input</div>', unsafe_allow_html=True)

# PAGE WRAPPER OPEN

st.markdown('<div class="tm-wrap">', unsafe_allow_html=True)


# SAMPLE CV — find it wherever it may be

def _find_sample():
    candidates = [
        os.path.join(_HERE, "..", "data", "cvs", "cv_sample_1.txt"),
        os.path.join(_HERE, "data", "cvs", "cv_sample_1.txt"),
        os.path.join(_HERE, "cv_sample_1.txt"),
    ]
    for c in candidates:
        p = os.path.normpath(os.path.abspath(c))
        if os.path.exists(p):
            with open(p) as f:
                return f.read()
    return ""

sample_cv = _find_sample()


# INPUT SECTION

st.markdown('<div class="tm-sec-label">Step 1</div>', unsafe_allow_html=True)

st.markdown('<div class="tm-sec-title">Paste Your CV</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tm-sec-sub">Include your skills, work experience, '
    'qualifications, and education. The more detail you provide, '
    'the more accurate the results.</div>',
 HEAD
    unsafe_allow_html=True,

    unsafe_allow_html=True

)

col_cv, col_right = st.columns([3, 1], gap="large")

with col_cv:
HEAD
    # Decorative header bar above the text area
    st.markdown("""
    <div style="background:#F8FBFF;border:1px solid #D8E4F4;border-bottom:none;
                border-radius:12px 12px 0 0;padding:10px 16px;
                display:flex;align-items:center;gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#FF5F57;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#FFBD2E;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#28CA41;"></div>
        <span style="font-size:12px;font-weight:500;color:#555555;margin-left:8px;">

    # ── decorative input card header 
    st.markdown("""
    <div style="background:#F8FBFF;border:1px solid #DDE5F0;border-bottom:none;
                border-radius:14px 14px 0 0;padding:12px 18px;
                display:flex;align-items:center;gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#FF5F57"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#FFBD2E"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#28CA41"></div>
        <span style="font-size:12px;font-weight:500;color:#94A3B8;margin-left:8px;">

            curriculum_vitae.txt
        </span>
    </div>
    """, unsafe_allow_html=True)

    cv_input = st.text_area(
        label="cv_paste",
        placeholder=(
            "Paste your full CV here...\n\n"
            "Include:\n"
            "  - Technical skills (Python, SQL, TensorFlow...)\n"
            "  - Work experience with responsibilities\n"
            "  - Education and qualifications\n"
            "  - Projects and achievements"
        ),
        height=320,
        label_visibility="collapsed",
    )

 HEAD
    words = len(cv_input.split()) if cv_input.strip() else 0
    pct = word_count_pct(words)
    hint = ("Ready to compare." if words >= 80
            else f"Add {max(0, 80 - words)} more words for better accuracy.")

    # Word count bar
    words = len(cv_input.split()) if cv_input.strip() else 0
    pct   = wc_pct(words)
    hint  = ("Ready to compare." if words >= 80
             else f"Add {max(0,80-words)} more words for better accuracy.")


    st.markdown(f"""
    <div class="tm-wc">
        <span class="tm-wc-num">{words} words</span>
        <div class="tm-wc-bar">
 HEAD
            <div class="tm-wc-fill" style="width:{pct}%;"></div>

            <div class="tm-wc-fill" style="width:{pct}%"></div>

        </div>
        <span class="tm-wc-hint">{hint}</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
 HEAD
    st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)

    run_btn = st.button("Compare CV", type="primary", use_container_width=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:12px;font-weight:700;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#444444;margin-bottom:10px;">Options</p>',
        unsafe_allow_html=True,
    )

    num_res = st.slider("Results to show", 3, 10, 5, label_visibility="visible")



# SESSION STATE

if run_btn:
    if cv_input.strip():
        st.session_state["cv"] = cv_input
=======
    st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

    run_btn = st.button("Compare CV", type="primary", use_container_width=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    smp_btn = st.button("Load Sample CV", use_container_width=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:11px;font-weight:700;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#94A3B8;margin-bottom:10px;">Optio

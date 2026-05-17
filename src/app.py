"""
app.py  —  TalentMatch: CV to Job Matching System
Author:      Challa Harikrishna Nagasai Charan | 23727842
Supervisor:  Dr Esmaeil Babaei Khezerloo
Module:      6G6Z0019 Synoptic Project | Manchester Metropolitan University

Run:  streamlit run app.py   (from inside the src/ folder)
"""

import os
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Path fix so imports work whether run from src/ or project root
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from job_matcher import load_job_descriptions, match_cv_to_jobs, extract_cv_keywords


# -----------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="TalentMatch – CV to Job Matching System",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------
# CSS — colours slightly darkened for screen recording readability
# -----------------------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
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

/* Navigation bar */
.tm-nav {
    background: rgba(255,255,255,0.92);
    border-bottom: 1px solid #D8D8DC;
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
    font-weight: 700;
    letter-spacing: -2px;
    color: #1D1D1F;
    margin-bottom: 18px;
}
.tm-hero-title span {
    color: #0071E3;
}
.tm-hero-sub {
    font-size: 19px;
    color: #222222;
    font-weight: 500;
    max-width: 720px;
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
    border: 1px solid #D2D2D7;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #1D1D1F;
}

/* Layout wrapper */
.tm-wrap {
    max-width: 1200px;
    margin: auto;
}

/* Cards */
.tm-card,
.tm-chart,
.tm-kpi {
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid #E5E5E7;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
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
    color: #444444;
    font-weight: 500;
    margin-top: 5px;
}
.tm-card-skill {
    background: #F5F5F7;
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
.b-strong   { background:#ECFDF5; color:#065F46; border-color:#6EE7B7; }
.b-moderate { background:#FFFBEB; color:#78350F; border-color:#FCD34D; }
.b-low      { background:#F3F4F6; color:#374151; border-color:#D1D5DB; }

/* KPI summary cards */
.tm-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 22px;
}
.tm-kpi {
    padding: 22px 22px 18px;
    position: relative;
    overflow: hidden;
}
.tm-kpi::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 20px 20px 0 0;
}
.kpi-blue::after  { background: #0071E3; }
.kpi-green::after { background: #34C759; }
.kpi-amber::after { background: #FF9500; }
.kpi-slate::after { background: #636366; }
.tm-kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #555555;
    margin-bottom: 12px;
}
.tm-kpi-value {
    font-size: 19px;
    font-weight: 700;
    color: #1D1D1F;
    line-height: 1.2;
    margin-bottom: 5px;
}
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
    text-align: center;
    margin-top: 8px;
    font-style: italic;
}

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
    margin-bottom: 36px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.tm-notice-icon {
    width: 20px;
    height: 20px;
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
    letter-spacing: -0.3px;
    margin-bottom: 6px;
}
.tm-sec-sub {
    font-size: 14px;
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
    font-size: 15px !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
}
textarea:focus {
    border: 1px solid #0071E3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.15) !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 999px !important;
    height: 44px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border: none !important;
    background: #0071E3 !important;
    color: white !important;
    transition: background 0.15s ease !important;
}
div.stButton > button:hover {
    background: #005BBE !important;
}
div[data-testid="stDownloadButton"] > button {
    border-radius: 999px !important;
    height: 48px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
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
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------

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


# -----------------------------------------------------------------------
# NAVBAR
# -----------------------------------------------------------------------
st.markdown("""
<div class="tm-nav">
    <div class="tm-logo">Talent<em>Match</em></div>
    <div class="tm-nav-right">
        Challa Harikrishna Nagasai Charan &nbsp;|&nbsp; 23727842<br>
        Supervisor: Dr Esmaeil Babaei Khezerloo &nbsp;|&nbsp; MMU &nbsp;|&nbsp; 6G6Z0019
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------
# HERO
# -----------------------------------------------------------------------
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


# -----------------------------------------------------------------------
# PAGE WRAPPER
# -----------------------------------------------------------------------
st.markdown('<div class="tm-wrap">', unsafe_allow_html=True)


# -----------------------------------------------------------------------
# INPUT SECTION
# -----------------------------------------------------------------------
st.markdown('<div class="tm-sec-label">CV Input</div>', unsafe_allow_html=True)
st.markdown('<div class="tm-sec-title">Paste Your CV</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tm-sec-sub">Include your skills, work experience, '
    'qualifications, and education. The more detail you provide, '
    'the more accurate the results.</div>',
    unsafe_allow_html=True,
)

col_cv, col_right = st.columns([3, 1], gap="large")

with col_cv:
    # Decorative header bar above the text area
    st.markdown("""
    <div style="background:#F8FBFF;border:1px solid #D8E4F4;border-bottom:none;
                border-radius:12px 12px 0 0;padding:10px 16px;
                display:flex;align-items:center;gap:8px;">
        <div style="width:10px;height:10px;border-radius:50%;background:#FF5F57;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#FFBD2E;"></div>
        <div style="width:10px;height:10px;border-radius:50%;background:#28CA41;"></div>
        <span style="font-size:12px;font-weight:500;color:#555555;margin-left:8px;">
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

    words = len(cv_input.split()) if cv_input.strip() else 0
    pct = word_count_pct(words)
    hint = ("Ready to compare." if words >= 80
            else f"Add {max(0, 80 - words)} more words for better accuracy.")

    st.markdown(f"""
    <div class="tm-wc">
        <span class="tm-wc-num">{words} words</span>
        <div class="tm-wc-bar">
            <div class="tm-wc-fill" style="width:{pct}%;"></div>
        </div>
        <span class="tm-wc-hint">{hint}</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='height:52px'></div>", unsafe_allow_html=True)

    run_btn = st.button("Compare CV", type="primary", use_container_width=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:12px;font-weight:700;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#444444;margin-bottom:10px;">Options</p>',
        unsafe_allow_html=True,
    )

    num_res = st.slider("Results to show", 3, 10, 5, label_visibility="visible")


# -----------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------
if run_btn:
    if cv_input.strip():
        st.session_state["cv"] = cv_input
        st.session_state["run"] = True
    else:
        st.warning("Please paste your CV text before clicking Compare CV.")

active_cv = st.session_state.get("cv", cv_input)
run_now = st.session_state.get("run", False)


# -----------------------------------------------------------------------
# RESULTS
# -----------------------------------------------------------------------
st.markdown('<div class="tm-divider"></div>', unsafe_allow_html=True)

if run_now and active_cv.strip():
    st.session_state["run"] = False

    with st.spinner("Analysing your CV against available roles..."):
        try:
            jobs = load_job_descriptions()
            results = match_cv_to_jobs(active_cv, jobs)
            cv_kws = extract_cv_keywords(active_cv)
        except FileNotFoundError as e:
            st.error(
                f"Could not find the jobs data file.\n\n"
                f"Make sure your folder structure is correct:\n"
                f"```\n"
                f"TalentMatch_Project/\n"
                f"├── src/\n"
                f"│   ├── app.py\n"
                f"│   └── job_matcher.py\n"
                f"└── data/\n"
                f"    └── job_descriptions/\n"
                f"        └── jobs.json\n"
                f"```\n"
                f"Detail: {e}"
            )
            st.stop()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

    # Compute display percentages — raw scores used for all ranking/badge logic
    raw_scores = [r["score"] for r in results]
    min_raw = min(raw_scores)
    max_raw = max(raw_scores)
    for r in results:
        r["display_pct"] = normalise_display_score(r["score"], min_raw, max_raw)

    st.markdown(
        '<div class="tm-notice">'
        '<div class="tm-notice-icon">i</div>'
        'Your CV has been compared with selected roles. '
        'Results are ranked below based on skill relevance.'
        '</div>',
        unsafe_allow_html=True,
    )

    # KPI summary cards
    st.markdown('<div class="tm-sec-label">Overview</div>', unsafe_allow_html=True)

    top = results[0]
    avg_sc = sum(r["score"] for r in results) / len(results)
    fit = overall_fit(avg_sc)
    st_area = ", ".join(cv_kws[:3]).title() if cv_kws else "Not detected"
    im_area = results[-1]["title"].split()[0] + " roles"

    st.markdown(f"""
    <div class="tm-kpi-grid">
        <div class="tm-kpi kpi-blue">
            <div class="tm-kpi-label">Best Matching Role</div>
            <div class="tm-kpi-value">{top["title"]}</div>
            <div class="tm-kpi-note">{top["company"]}</div>
        </div>
        <div class="tm-kpi kpi-green">
            <div class="tm-kpi-label">Overall Alignment</div>
            <div class="tm-kpi-value">{fit}</div>
            <div class="tm-kpi-note">{len(results)} roles reviewed</div>
        </div>
        <div class="tm-kpi kpi-amber">
            <div class="tm-kpi-label">Strength Area</div>
            <div class="tm-kpi-value" style="font-size:15px;">{st_area}</div>
            <div class="tm-kpi-note">Key skills from your CV</div>
        </div>
        <div class="tm-kpi kpi-slate">
            <div class="tm-kpi-label">Area to Develop</div>
            <div class="tm-kpi-value" style="font-size:15px;">{im_area}</div>
            <div class="tm-kpi-note">Based on lowest match</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CV keywords strip
    if cv_kws:
        st.markdown(
            f'<div class="tm-skills">'
            f'<strong>Skills identified from your CV:</strong> '
            f'{keyword_sentence(cv_kws[:8])}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Bar chart
    st.markdown('<div class="tm-sec-label">Results Overview</div>', unsafe_allow_html=True)

    chart_results = results[:num_res]
    labels = [
        r["title"][:30] + "…" if len(r["title"]) > 30 else r["title"]
        for r in chart_results
    ]
    scores = [r["display_pct"] for r in chart_results]
    colours = [
        "#3B82F6" if r["score"] >= 0.10 else
        "#60A5FA" if r["score"] >= 0.05 else
        "#BFDBFE"
        for r in chart_results
    ]

    st.markdown('<div class="tm-chart">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tm-chart-title">'
        '<span class="tm-chart-dot"></span>'
        'Relevance Score by Role'
        '</div>',
        unsafe_allow_html=True,
    )

    fig, ax = plt.subplots(figsize=(9, max(3.0, len(chart_results) * 0.56)))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F8FAFF")

    bars = ax.barh(
        labels[::-1], scores[::-1],
        color=colours[::-1], height=0.54, edgecolor="none",
    )
    for bar, sc in zip(bars, scores[::-1]):
        ax.text(
            bar.get_width() + 0.12, bar.get_y() + bar.get_height() / 2,
            f"{sc:.1f}%", va="center", ha="left",
            color="#1F2937", fontsize=9.5, fontweight="600",
        )

    ax.set_xlabel("Relevance Score (%)", color="#374151", fontsize=9)
    ax.tick_params(colors="#374151", labelsize=9)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB")
    ax.spines["bottom"].set_color("#D1D5DB")
    ax.set_xlim(0, min(100, max(scores) * 1.18 + 2))
    plt.tight_layout(pad=1.2)
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown(
        '<p class="tm-chart-cap">Higher scores indicate stronger alignment '
        'between your CV and the role.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Result cards
    st.markdown('<div class="tm-sec-label">Detailed Results</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tm-results-desc">'
        'Each card shows how closely your CV aligns with the role. '
        'The skill line shows shared vocabulary and the insight explains the match quality.'
        '</p>',
        unsafe_allow_html=True,
    )

    for rank, job in enumerate(results[:num_res], 1):
        badge_text, badge_class = badge(job["score"])
        skill_s = keyword_sentence(job["top_keywords"])
        ins = insight_text(job["top_keywords"], job["score"])

        st.markdown(f"""
        <div class="tm-card">
            <div class="tm-card-rank">{rank_label(rank)}</div>
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:10px;">
                <div>
                    <div class="tm-card-title">{job["title"]}</div>
                    <div class="tm-card-company">{job["company"]}</div>
                </div>
                <span class="tm-badge {badge_class}">
                    {badge_text} &nbsp; {job["display_pct"]:.1f}%
                </span>
            </div>
            <div class="tm-card-skill">{skill_s}</div>
            <div class="tm-card-insight">{ins}</div>
        </div>
        """, unsafe_allow_html=True)

    # Export
    st.markdown('<div class="tm-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="tm-sec-label">Export</div>', unsafe_allow_html=True)
    st.markdown('<div class="tm-sec-title">Download Your Results</div>', unsafe_allow_html=True)

    rows = [{
        "Rank":              i + 1,
        "Role":              r["title"],
        "Company":           r["company"],
        "Score":             r["score"],
        "Match Strength":    f"{r['display_pct']:.1f}%",
        "Key Skill Matches": keyword_sentence(r["top_keywords"]),
        "Alignment Level":   badge(r["score"])[0],
    } for i, r in enumerate(results)]

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Results as CSV",
        data=df.to_csv(index=False),
        file_name="talentmatch_results.csv",
        mime="text/csv",
    )

else:
    st.markdown("""
    <div class="tm-card" style="text-align:center;padding:60px;">
        <h2 style="font-size:34px;margin-bottom:16px;color:#1D1D1F;">
            Ready to Compare Your CV
        </h2>
        <p style="font-size:16px;color:#444444;max-width:680px;
                  margin:auto;line-height:1.8;">
            Paste your CV above and click Compare CV to view matching
            job roles based on similarity scores and matching skills.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Close page wrapper
st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------
st.markdown("""
<div class="tm-footer">
    TalentMatch AI — University Project using Python, Streamlit and scikit-learn<br><br>
    Challa Harikrishna Nagasai Charan | 23727842<br>
    Manchester Metropolitan University | 6G6Z0019 Synoptic Project
</div>
""", unsafe_allow_html=True)

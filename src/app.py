"""
app.py  —  TalentMatch: CV to Job Matching System
Author:      Challa Harikrishna Nagasai Charan | 23727842
Supervisor:  Dr Esmaeil Babaei Khezerloo
Module:      6G6Z0019 Synoptic Project | Manchester Metropolitan University

Run:  streamlit run app.py   (from inside the src/ folder)
"""

import os, sys, streamlit as st, pandas as pd, matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── path fix: works whether you run from src/ or the project root ─
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from job_matcher import load_job_descriptions, match_cv_to_jobs, extract_cv_keywords

# ════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TalentMatch – CV to Job Matching System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════════
# PREMIUM CSS
# UX principles applied:
#  • Visual hierarchy  — size, weight, colour guide the eye
#  • White space       — generous padding creates breathing room
#  • Consistency       — one blue accent, one type family throughout
#  • Feedback          — clear states (empty, loading, results, error)
#  • Affordance        — buttons look clickable, inputs look fillable
# ════════════════════════════════════════════════════════════════════
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
    border: 1px solid #E5E5E7;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 13px;
    color: #1D1D1F;
}
.tm-wrap {
    max-width: 1200px;
    margin: auto;
}
.tm-card,
.tm-chart,
.tm-kpi {
    background: #FFFFFF;
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
    color: #6E6E73;
    margin-top: 5px;
}
.tm-card-skill {
    background: #F5F5F7;
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
.b-strong   { background:#ECFDF5; color:#065F46; border-color:#A7F3D0; }
.b-moderate { background:#FFFBEB; color:#92400E; border-color:#FDE68A; }
.b-low      { background:#F5F5F7; color:#6E6E73; border-color:#D2D2D7; }
.tm-kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
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
    letter-spacing: -0.4px;
    margin-bottom: 6px;
}
.tm-sec-sub {
    font-size: 14px;
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
.tm-wc-num { font-size: 13px; font-weight: 700; color: #0071E3; min-width: 60px; }
.tm-wc-bar { flex: 1; height: 4px; background: #E5E5E7; border-radius: 2px; overflow: hidden; }
.tm-wc-fill { height: 100%; border-radius: 2px; background: #0071E3; transition: width 0.3s ease; }
.tm-wc-hint { font-size: 12px; color: #8E8E93; }
textarea {
    border-radius: 20px !important;
    border: 1px solid #D2D2D7 !important;
    padding: 20px !important;
    font-size: 15px !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
}
textarea:focus {
    border: 1px solid #0071E3 !important;
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


# ════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════
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


# ════════════════════════════════════════════════════════════════════
# NAVBAR
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="tm-nav">
    <div class="tm-logo">Talent<em>Match</em></div>
    <div class="tm-nav-right">
        Challa Harikrishna Nagasai Charan &nbsp;|&nbsp; 23727842<br>
        Supervisor: Dr Esmaeil Babaei Khezerloo &nbsp;|&nbsp; MMU &nbsp;|&nbsp; 6G6Z0019
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════
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

# ════════════════════════════════════════════════════════════════════
# PAGE WRAPPER OPEN
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="tm-wrap">', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# SAMPLE CV — find it wherever it may be
# ════════════════════════════════════════════════════════════════════
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

# ════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="tm-sec-label">Step 1</div>', unsafe_allow_html=True)
st.markdown('<div class="tm-sec-title">Paste Your CV</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tm-sec-sub">Include your skills, work experience, '
    'qualifications, and education. The more detail you provide, '
    'the more accurate the results.</div>',
    unsafe_allow_html=True
)

col_cv, col_right = st.columns([3, 1], gap="large")

with col_cv:
    # ── decorative input card header ─────────────────────────────
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

    # Word count bar
    words = len(cv_input.split()) if cv_input.strip() else 0
    pct   = wc_pct(words)
    hint  = ("Ready to compare." if words >= 80
             else f"Add {max(0,80-words)} more words for better accuracy.")

    st.markdown(f"""
    <div class="tm-wc">
        <span class="tm-wc-num">{words} words</span>
        <div class="tm-wc-bar">
            <div class="tm-wc-fill" style="width:{pct}%"></div>
        </div>
        <span class="tm-wc-hint">{hint}</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

    run_btn = st.button("Compare CV", type="primary", use_container_width=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    smp_btn = st.button("Load Sample CV", use_container_width=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:11px;font-weight:700;letter-spacing:0.1em;'
        'text-transform:uppercase;color:#94A3B8;margin-bottom:10px;">Options</p>',
        unsafe_allow_html=True
    )
    num_res  = st.slider("Results to show", 3, 10, 5, label_visibility="visible")
    show_jd  = st.checkbox("Show full job description", value=False)

# ════════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════════
if smp_btn:
    if sample_cv:
        st.session_state["cv"]  = sample_cv
        st.session_state["run"] = False
        st.info("Sample CV loaded — click Compare CV to analyse it.")
    else:
        st.warning("Sample CV file not found. Please paste your own CV text.")

if run_btn:
    if cv_input.strip():
        st.session_state["cv"]  = cv_input
        st.session_state["run"] = True
    else:
        st.warning("Please paste your CV text before clicking Compare CV.")

active_cv = st.session_state.get("cv", cv_input)
run_now   = st.session_state.get("run", False)

# ════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="tm-divider"></div>', unsafe_allow_html=True)

if run_now and active_cv.strip():
    st.session_state["run"] = False

    with st.spinner("Analysing your CV against available roles..."):
        try:
            jobs    = load_job_descriptions()
            results = match_cv_to_jobs(active_cv, jobs)
            cv_kws  = extract_cv_keywords(active_cv)
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
                f"Technical detail: {e}"
            )
            st.stop()
        except Exception as e:
            st.error(f"An error occurred during comparison: {str(e)}")
            st.stop()

    # ── NOTICE ──────────────────────────────────────────────────────
    st.markdown(
        '<div class="tm-notice">'
        '<div class="tm-notice-icon">i</div>'
        'Your CV has been compared with selected roles. '
        'Results are ranked below based on skill relevance.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── KPI CARDS ───────────────────────────────────────────────────
    st.markdown('<div class="tm-sec-label">Overview</div>', unsafe_allow_html=True)

    top     = results[0]
    avg_sc  = sum(r["score"] for r in results) / len(results)
    fl      = fit(avg_sc)
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
            <div class="tm-kpi-value">{fl}</div>
            <div class="tm-kpi-note">{len(results)} roles reviewed</div>
        </div>
        <div class="tm-kpi kpi-amber">
            <div class="tm-kpi-label">Strength Area</div>
            <div class="tm-kpi-value" style="font-size:15px">{st_area}</div>
            <div class="tm-kpi-note">Key skills from your CV</div>
        </div>
        <div class="tm-kpi kpi-slate">
            <div class="tm-kpi-label">Area to Develop</div>
            <div class="tm-kpi-value" style="font-size:15px">{im_area}</div>
            <div class="tm-kpi-note">Based on lowest match</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SKILLS ──────────────────────────────────────────────────────
    if cv_kws:
        st.markdown(
            f'<div class="tm-skills">'
            f'<strong>Skills identified from your CV:</strong> '
            f'{kw_sent(cv_kws[:8])}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── CHART ───────────────────────────────────────────────────────
    st.markdown('<div class="tm-sec-label">Step 2</div>', unsafe_allow_html=True)

    cr      = results[:num_res]
    lbls    = [r["title"][:30]+"…" if len(r["title"])>30 else r["title"] for r in cr]
    scrs    = [r["percentage"] for r in cr]
    clrs    = ["#4F8EF7" if r["score"]>=0.10 else
               "#7ABAFF" if r["score"]>=0.05 else
               "#C3D7FF" for r in cr]

    st.markdown('<div class="tm-chart">', unsafe_allow_html=True)
    st.markdown(
        '<div class="tm-chart-title">'
        '<span class="tm-chart-dot"></span>'
        'Relevance Score by Role'
        '</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(9, max(3.0, len(cr)*0.56)))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#F7FAFF")

    bars = ax.barh(lbls[::-1], scrs[::-1],
                   color=clrs[::-1], height=0.54, edgecolor="none")
    for bar, sc in zip(bars, scrs[::-1]):
        ax.text(bar.get_width()+0.12, bar.get_y()+bar.get_height()/2,
                f"{sc:.2f}%", va="center", ha="left",
                color="#374151", fontsize=9.5, fontweight="600")

    ax.set_xlabel("Relevance Score (%)", color="#94A3B8", fontsize=9)
    ax.tick_params(colors="#64748B", labelsize=9)
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#E4EDF8")
    ax.spines["bottom"].set_color("#E4EDF8")
    ax.set_xlim(0, max(scrs)*1.32+1)
    plt.tight_layout(pad=1.2)
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown(
        '<p class="tm-chart-cap">Higher scores = stronger alignment between your CV and the role.</p>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── RESULT CARDS ────────────────────────────────────────────────
    st.markdown('<div class="tm-sec-label">Step 3 — Detailed Results</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="tm-results-desc">'
        'Each card shows how closely your CV aligns with the role. '
        'The skill line shows shared vocabulary and the insight explains the match quality.'
        '</p>',
        unsafe_allow_html=True,
    )

    for rank, job in enumerate(results[:num_res], 1):
        bt, bc    = badge(job["score"])
        skill_s   = kw_sent(job["top_keywords"])
        ins       = insight(job["top_keywords"], job["score"])

        jd_html = ""
        if show_jd:
            jd_html = (
                f'<div style="margin-top:14px;padding-top:14px;'
                f'border-top:1px solid #F1F5F9;font-size:13px;'
                f'color:#64748B;line-height:1.75;">'
                f'{job["description"]}</div>'
            )

        st.markdown(f"""
        <div class="tm-card">
            <div class="tm-card-rank">{rl(rank)}</div>
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:10px;">
                <div>
                    <div class="tm-card-title">{job["title"]}</div>
                    <div class="tm-card-company">{job["company"]}</div>
                </div>
                <span class="tm-badge {bc}">{bt} &nbsp; {job["percentage"]:.2f}%</span>
            </div>
            <div class="tm-card-skill">{skill_s}</div>
            <div class="tm-card-insight">{ins}</div>
            {jd_html}
        </div>
        """, unsafe_allow_html=True)

    # ── EXPORT ──────────────────────────────────────────────────────
    st.markdown('<div class="tm-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="tm-sec-label">Export</div>', unsafe_allow_html=True)
    st.markdown('<div class="tm-sec-title">Download Your Results</div>',
                unsafe_allow_html=True)

    rows = [{
        "Rank":             i+1,
        "Role":             r["title"],
        "Company":          r["company"],
        "Score":            r["score"],
        "Match Strength":   f"{r['percentage']:.2f}%",
        "Key Skill Matches": kw_sent(r["top_keywords"]),
        "Alignment Level":  badge(r["score"])[0],
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
    # ── EMPTY STATE ─────────────────────────────────────────────────
    st.markdown("""
<div class="tm-card" style="text-align:center;padding:60px;">
    <h2 style="font-size:36px;margin-bottom:18px;color:#1D1D1F;">
        Ready to Compare Your CV
    </h2>
    <p style="font-size:17px;color:#6E6E73;max-width:700px;margin:auto;line-height:1.8;">
        Paste your CV above and click Compare CV to view matching
        job roles based on similarity scores and matching skills.
    </p>
</div>
""", unsafe_allow_html=True)

# Close page wrapper
st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="tm-footer">
TalentMatch AI — University Project using Python, Streamlit and scikit-learn
<br><br>
Challa Harikrishna Nagasai Charan | 23727842
<br>
Manchester Metropolitan University | 6G6Z0019 Synoptic Project
</div>
""", unsafe_allow_html=True)

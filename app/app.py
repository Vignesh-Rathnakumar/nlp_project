import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title = "Clickbait Detector",
    page_icon  = "⚡",
    layout     = "centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0a0f;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Hero header */
.hero {
    padding: 3rem 0 2rem;
    text-align: center;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #f0c040;
    border: 1px solid #f0c04040;
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    color: #f5f5f0;
    line-height: 1.05;
    letter-spacing: -1px;
    margin: 0 0 0.8rem;
}
.hero-title span { color: #f0c040; }
.hero-sub {
    font-size: 15px;
    color: #888;
    font-weight: 300;
    margin: 0;
}

/* Input card */
.input-card {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 1.8rem;
    margin: 1.5rem 0;
}
.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.6rem;
}

/* Override streamlit textarea */
.stTextArea textarea {
    background: #0a0a0f !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 8px !important;
    color: #f5f5f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 14px !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #f0c040 !important;
    box-shadow: 0 0 0 2px #f0c04020 !important;
}
.stTextArea textarea::placeholder { color: #444 !important; }

/* Button */
.stButton > button {
    background: #f0c040 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    padding: 0.7rem 2.2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #f5d060 !important;
    transform: translateY(-1px) !important;
}

/* Result cards */
.result-clickbait {
    background: #1a0d0d;
    border: 1px solid #5a1a1a;
    border-left: 4px solid #e04040;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}
.result-clean {
    background: #0d1a0f;
    border: 1px solid #1a4a1a;
    border-left: 4px solid #40c060;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.result-label.bad  { color: #e04040; }
.result-label.good { color: #40c060; }
.result-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f5f5f0;
    margin: 0;
}
.conf-pill {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 999px;
    margin-left: 10px;
    vertical-align: middle;
}
.conf-pill.bad  { background: #e0404025; color: #e06060; border: 1px solid #e0404040; }
.conf-pill.good { background: #40c06025; color: #60e080; border: 1px solid #40c06040; }

/* Rewrite box */
.rewrite-box {
    background: #0f0f18;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}
.rewrite-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #f0c040;
    margin-bottom: 10px;
}
.rewrite-text {
    font-size: 17px;
    color: #f5f5f0;
    font-weight: 400;
    line-height: 1.5;
    margin: 0;
}

/* Model pills */
.model-row {
    display: flex;
    gap: 10px;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.model-pill {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 8px;
    padding: 10px 14px;
    flex: 1;
    min-width: 180px;
}
.model-pill-name {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 4px;
}
.model-pill-desc {
    font-size: 12px;
    color: #aaa;
    line-height: 1.4;
    margin: 0;
}

/* Sidebar */
.stSidebar {
    background: #0d0d14 !important;
    border-right: 1px solid #1a1a2a !important;
}
.stSidebar [data-testid="stSidebarContent"] {
    padding: 2rem 1.2rem;
}

/* Examples */
.example-btn {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 8px;
    padding: 10px 14px;
    cursor: pointer;
    margin-bottom: 8px;
    font-size: 13px;
    color: #aaa;
    width: 100%;
    text-align: left;
    transition: border-color 0.2s;
}
.example-btn:hover { border-color: #f0c040; color: #f5f5f0; }

/* Slider */
.stSlider [data-baseweb="slider"] { padding-top: 0.5rem; }

/* History item */
.history-item {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 13px;
    color: #aaa;
}
.history-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 1px;
    padding: 1px 7px;
    border-radius: 3px;
    margin-bottom: 5px;
    text-transform: uppercase;
}
.history-badge.cb  { background: #e0404025; color: #e06060; }
.history-badge.ok  { background: #40c06025; color: #60e080; }
.divider { border: none; border-top: 1px solid #1a1a2a; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Load models from Hugging Face
@st.cache_resource
def load_models():
    classifier = pipeline(
        "text-classification",
        model="vikirk/clickbait-bert"
    )
    
    rewriter = pipeline(
        "text2text-generation",
        model="vikirk/clickbait-t5"
    )
    
    return classifier, rewriter

classifier, rewriter = load_models()

def classify(headline):
    result = classifier(headline)[0]
    label = 1 if result["label"] == "LABEL_1" else 0
    confidence = result["score"]
    return label, confidence

def rewrite(headline):
    result = rewriter(headline)[0]
    return result["generated_text"]

# ── Session state ──
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:18px;font-weight:800;color:#f5f5f0;margin-bottom:1.5rem;">⚡ Settings</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:8px;">Confidence threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("", min_value=0.5, max_value=0.99, value=0.75, step=0.01, label_visibility="collapsed")
    st.caption(f"Headlines below {threshold*100:.0f}% confidence will show as uncertain")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:10px;">Try an example</div>', unsafe_allow_html=True)

    examples = [
        "You Won't Believe What This Student Did With AI!",
        "10 Shocking Reasons Why Your Diet Is Failing You",
        "Scientists Publish New Study on Climate Change",
        "This Simple Trick Will Change Your Life Forever",
        "Government Announces New Budget Allocations for 2026",
    ]
    for ex in examples:
        if st.button(ex[:52] + ("…" if len(ex) > 52 else ""), key=ex):
            st.session_state.selected_example = ex

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    auto_rewrite = st.toggle("Auto rewrite if clickbait", value=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:10px;">Model info</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#555;line-height:1.6;">Classifier — bert-base-uncased<br>Rewriter — T5 paraphrase model<br>Device — MPS (Apple M1)</div>', unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px;color:#666;text-transform:uppercase;margin-bottom:10px;">History</div>', unsafe_allow_html=True)
        for h in reversed(st.session_state.history[-5:]):
            badge = "cb" if h["label"] == 1 else "ok"
            badge_text = "clickbait" if h["label"] == 1 else "clean"
            st.markdown(f'''
            <div class="history-item">
                <div class="history-badge {badge}">{badge_text}</div>
                <div>{h["headline"][:60]}{"…" if len(h["headline"])>60 else ""}</div>
            </div>''', unsafe_allow_html=True)

        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()

# ── Main ──
st.html('''
<div class="hero">
    <div class="hero-tag">⚡ NLP Project — BERT + T5</div>
    <h1 class="hero-title">Clickbait<br><span>Detector</span> & Rewriter</h1>
    
    <p class="hero-sub">
        An AI-powered system that detects misleading or sensational headlines 
        using a fine-tuned BERT model and rewrites them into clear, factual statements 
        using a T5 transformer model.
    </p>

    <p style="font-size:13px;color:#666;margin-top:8px;">
        👉 Helps identify clickbait, improve content quality, and promote trustworthy information.
    </p>
</div>
''')

default_val = st.session_state.get("selected_example", "")

headline = st.text_area(
    "Headline input",
    value       = default_val,
    placeholder = "e.g. You Won't Believe What This Student Did With AI!",
    height      = 90,
    label_visibility = "collapsed"
)

analyse = st.button("⚡  Analyse Headline")

if analyse:
    if not headline.strip():
        st.warning("Please enter a headline first.")
    else:
        with st.spinner("Running BERT classifier..."):
            label_idx, confidence = classify(headline)

        st.session_state.history.append({
            "headline": headline,
            "label":    label_idx,
            "conf":     confidence
        })

        uncertain = confidence < threshold

        if label_idx == 1:
            conf_class = "bad"
            verdict    = "CLICKBAIT DETECTED"
            note       = "⚠ Uncertain prediction" if uncertain else ""
            st.markdown(f'''
            <div class="result-clickbait">
                <div class="result-label bad">Classification</div>
                <p class="result-value">{verdict}
                    <span class="conf-pill bad">{confidence*100:.1f}%</span>
                </p>
                <div style="font-size:13px;color:#e06060;margin-top:6px;">{note}</div>
            </div>''', unsafe_allow_html=True)

            if auto_rewrite:
                with st.spinner("T5 rewriting headline..."):
                    rewritten = rewrite(headline)

                st.markdown(f'''
                <div class="rewrite-box">
                    <div class="rewrite-label">Honest rewrite</div>
                    <p class="rewrite-text">{rewritten}</p>
                </div>''', unsafe_allow_html=True)

        else:
            st.markdown(f'''
            <div class="result-clean">
                <div class="result-label good">Classification</div>
                <p class="result-value">NOT CLICKBAIT
                    <span class="conf-pill good">{confidence*100:.1f}%</span>
                </p>
                <div style="font-size:13px;color:#60e080;margin-top:6px;">
                    This headline looks factual and informative.
                </div>
            </div>''', unsafe_allow_html=True)

        st.markdown('''
        <div class="model-row">
            <div class="model-pill">
                <div class="model-pill-name">BERT classifier</div>
                <p class="model-pill-desc">Fine-tuned bert-base-uncased on Clickbait-17 dataset for binary classification.</p>
            </div>
            <div class="model-pill">
                <div class="model-pill-name">T5 rewriter</div>
                <p class="model-pill-desc">Paraphrase model that neutralises sensationalist language into factual headlines.</p>
            </div>
        </div>''', unsafe_allow_html=True)
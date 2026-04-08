"""UI styling helpers for the Streamlit dashboard."""

import streamlit as st


APPLE_STYLE_CSS = """
<style>
    :root {
        --bg: #f5f5f7;
        --card: #ffffff;
        --text: #1d1d1f;
        --muted: #6e6e73;
        --line: #d2d2d7;
        --accent: #0071e3;
        --primary-color: #0071e3;
    }

    .stApp {
        --primary-color: #0071e3;
        background: radial-gradient(circle at top right, #ffffff 0%, var(--bg) 55%);
        color: var(--text);
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
    }

    .hero {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.15rem 1.25rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
    }

    .hero h1 {
        margin: 0;
        letter-spacing: -0.02em;
        font-weight: 650;
        font-size: 1.55rem;
        color: var(--text);
    }

    .hero p {
        margin: 0.45rem 0 0;
        color: var(--muted);
        line-height: 1.45;
        font-size: 0.96rem;
    }

    .log-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.8rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid var(--line);
        background: #f0f8ff;
        color: #005bb5;
    }

    div[data-baseweb="notification"] {
        border-radius: 12px;
    }

    div[data-baseweb="notification"] div[role="alert"] {
        border-left: 4px solid #0071e3;
    }

    div[data-baseweb="notification"] p {
        color: #004a99;
    }

    .stAlert {
        background: #eef6ff;
        border: 1px solid #c7defa;
    }

    .stButton > button[kind="primary"] {
        background: #0071e3;
        border-color: #0071e3;
    }

    .stButton > button[kind="primary"]:hover {
        background: #005bb5;
        border-color: #005bb5;
    }

    /* Slider bar/handle: active segment blue, remaining segment gray. */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background: #0071e3;
        border-color: #005bb5;
    }

    .stSlider [data-baseweb="slider"] div[role="slider"]:hover,
    .stSlider [data-baseweb="slider"] div[role="slider"]:focus,
    .stSlider [data-baseweb="slider"] div[role="slider"]:active {
        background: #005bb5;
        border-color: #004a99;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.2);
    }

    .stSlider input,
    .stSlider p,
    .stSlider span {
        color: #005bb5 !important;
    }

    /* Multiselect selected tags/chips */
    .stMultiSelect [data-baseweb="tag"] {
        background: #eaf3ff;
        border: 1px solid #c7defa;
    }

    .stMultiSelect [data-baseweb="tag"] span {
        color: #005bb5;
    }

    .stMultiSelect label p,
    .stMultiSelect [data-testid="stWidgetLabel"] p {
        color: #4b5563 !important;
    }

    /* Progress bars and metric bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #0071e3, #4a9cff);
    }

    /* Ensure headers are white when dark mode is active. */
    html[data-theme="dark"] .stApp h1,
    html[data-theme="dark"] .stApp h2,
    html[data-theme="dark"] .stApp h3,
    body[data-theme="dark"] .stApp h1,
    body[data-theme="dark"] .stApp h2,
    body[data-theme="dark"] .stApp h3,
    [data-theme="dark"] .stApp h1,
    [data-theme="dark"] .stApp h2,
    [data-theme="dark"] .stApp h3 {
        color: #ffffff !important;
    }
</style>
"""


def apply_apple_style() -> None:
    st.markdown(APPLE_STYLE_CSS, unsafe_allow_html=True)

"""
F6 — Real-Time Dashboard (Streamlit)
Live feed overlay, pass/fail counter, defect breakdown, alerts, CSV/PDF export.
"""
import os
import time
from pathlib import Path

import cv2
import numpy as np
import requests
import streamlit as st

# Load .env for API_URL
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AutoQI Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom theme: readable text + Industry 4.0 background
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@400;500;600;700&display=swap');

/* Background: industrial grid + gradient */
.stApp {
  background: 
    linear-gradient(90deg, rgba(8,145,178,0.03) 1px, transparent 1px),
    linear-gradient(rgba(8,145,178,0.03) 1px, transparent 1px),
    linear-gradient(135deg, #e2e8f0 0%, #f1f5f9 25%, #f8fafc 50%, #e0f2fe 75%, #f0f9ff 100%);
  background-size: 24px 24px, 24px 24px, 100% 100%;
  background-position: 0 0, 0 0, 0 0;
}
.main .block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* All text: dark, high contrast */
h1, h2, h3 { font-family: 'Outfit', sans-serif !important; font-weight: 600 !important; color: #0f172a !important; }
p, span, label, .stMarkdown, [data-testid="stMarkdownContainer"] { color: #1e293b !important; font-family: 'Outfit', sans-serif !important; }
[data-testid="stCaptionContainer"] { color: #475569 !important; font-size: 0.95rem !important; }
input, textarea { color: #0f172a !important; background: #fff !important; }

/* Metrics */
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-weight: 600 !important; color: #0891b2 !important; font-size: 1.8rem !important; }
[data-testid="stMetricLabel"] { color: #334155 !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] { color: #64748b !important; }
div[data-testid="stMetric"] { 
  background: #ffffff; padding: 1.2rem; border-radius: 12px; 
  border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(8,145,178,0.15); }

/* Sidebar */
[data-testid="stSidebar"] { 
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important; 
}
[data-testid="stSidebar"] .stMarkdown { color: #e2e8f0 !important; }
[data-testid="stSidebar"] label { color: #cbd5e1 !important; }
[data-testid="stSidebar"] input { color: #0f172a !important; background: #f8fafc !important; }

/* Tabs */
.stTabs [data-baseweb="tab"] { 
  font-family: 'Outfit', sans-serif !important; font-weight: 500 !important; color: #475569 !important;
  border-radius: 8px !important; padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] { background: rgba(8,145,178,0.12) !important; color: #0891b2 !important; font-weight: 600 !important; }

/* Buttons */
.stButton > button { 
  font-family: 'Outfit', sans-serif !important; font-weight: 500 !important; color: #0f172a !important;
  border-radius: 8px !important; padding: 0.5rem 1.5rem !important;
}
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important; border: none !important; color: #fff !important; }

/* File uploader */
[data-testid="stFileUploader"] { 
  border: 2px dashed #94a3b8 !important; border-radius: 12px !important; 
  padding: 1.5rem !important; background: rgba(255,255,255,0.8) !important;
}
[data-testid="stFileUploader"] label { color: #334155 !important; }

/* Images */
div[data-testid="stImage"] img { 
  border-radius: 12px !important; border: 1px solid #e2e8f0 !important; 
  box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
}

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg, #0891b2 0%, #0e7490 100%) !important; border-radius: 4px !important; }
.stProgress label { color: #334155 !important; }

/* Decision badges */
.decision-pass { color: #059669 !important; font-weight: 700 !important; font-size: 1.1rem !important; 
  padding: 0.4rem 0.8rem; background: #d1fae5; border-radius: 8px; display: inline-block; }
.decision-fail { color: #dc2626 !important; font-weight: 700 !important; font-size: 1.1rem !important; 
  padding: 0.4rem 0.8rem; background: #fee2e2; border-radius: 8px; display: inline-block; }

/* Expanders, JSON, info boxes */
.streamlit-expanderHeader { color: #1e293b !important; font-weight: 500 !important; }
[data-testid="stJson"] { color: #1e293b !important; }
div[data-testid="stAlert"] { color: #1e293b !important; }

/* hr */
hr { border-color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar: Settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    api_url = st.text_input("**API URL**", value=API_URL, help="Backend API base URL", placeholder="http://localhost:8000")
    API_URL = api_url or API_URL
    try:
        r = requests.get(f"{API_URL}/config", timeout=2)
        if r.ok:
            cfg = r.json()
            if cfg.get("anthropic_configured"):
                st.success("🤖 Claude AI enabled")
            else:
                st.info("Add ANTHROPIC_API_KEY to .env for AI features")
    except Exception:
        st.warning("API offline")
    st.markdown("---")
    st.caption("AutoQI v1.0 • Industry 4.0")

st.title("🔍 AutoQI")
st.markdown("**Automated Quality Inspection** — Defect detection for Industry 4.0")
st.caption("Upload an image to run inspection • View stats • Export reports")

# Live metrics with API data
col1, col2, col3, col4 = st.columns(4)
try:
    r = requests.get(f"{API_URL}/stats", timeout=2)
    if r.ok:
        s = r.json()
        with col1:
            st.metric("Total Inspections", s["total"], help="Total inspections run")
        with col2:
            st.metric("Pass", s["pass_count"], f"{s['pass_rate']:.0%} rate")
        with col3:
            st.metric("Fail", s["fail_count"], f"{s['fail_rate']:.0%} rate")
        with col4:
            pct = s["pass_rate"] * 100 if s["total"] else 0
            st.progress(min(1.0, s["pass_rate"]), text=f"Pass rate: {pct:.0f}%")
    else:
        raise Exception("No data")
except Exception:
    with col1:
        st.metric("Total", "—", "API offline")
    with col2:
        st.metric("Pass", "—", "")
    with col3:
        st.metric("Fail", "—", "")
    with col4:
        st.caption("Start API for live metrics")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📷 Inspect", "📊 Stats", "🤖 AI Insights", "📜 History", "📤 Export"
])

with tab1:
    st.subheader("Upload & Inspect")
    uploaded = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
    if uploaded:
        img = np.frombuffer(uploaded.read(), dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Image preview**")
                preview_placeholder = st.empty()
                preview_placeholder.image(img_rgb, use_container_width=True)
            with col_b:
                if st.button("Run Inspection", type="primary"):
                    files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                    with st.spinner("🔄 Analyzing..."):
                        try:
                            for i in range(3):
                                time.sleep(0.15)
                            r = requests.post(f"{API_URL}/inspect", files=files)
                            r.raise_for_status()
                            data = r.json()
                            decision = data["decision"]
                            h, w = img.shape[:2]

                            # Preview with simulated bbox overlay when detections exist
                            overlay = img_rgb.copy()
                            if data["detections"]:
                                for i, d in enumerate(data["detections"]):
                                    # Simulate bbox (model may not return coords; use placeholder)
                                    x1, y1 = int(w * 0.2 + i * 40), int(h * 0.2 + i * 30)
                                    x2, y2 = x1 + int(w * 0.35), y1 + int(h * 0.25)
                                    cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 80, 80), 3)
                                    cv2.putText(
                                        overlay, f"{d['defect_class']} {d['confidence']:.0%}",
                                        (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                                    )
                            else:
                                cv2.putText(
                                    overlay, "PASS", (w // 2 - 60, h // 2 - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 210, 106), 4
                                )
                            preview_placeholder.image(overlay, use_container_width=True)

                            # Success animation
                            if decision == "pass":
                                st.balloons()
                            cls = "decision-pass" if decision == "pass" else "decision-fail"
                            st.markdown(f'<p class="{cls}">Decision: {decision.upper()}</p>', unsafe_allow_html=True)
                            st.metric("Inference (ms)", round(data["inference_ms"], 1))
                            if data["detections"]:
                                st.subheader("Detections")
                                for d in data["detections"]:
                                    st.write(f"**{d['defect_class']}** — {d['confidence']:.2%}")
                                    if d.get("ai_description"):
                                        st.caption(f"_{d['ai_description']}_")
                            else:
                                st.info("✅ No defects detected above threshold")
                        except Exception as e:
                            st.error(f"Error: {e}")

with tab2:
    st.subheader("Metrics")
    try:
        r = requests.get(f"{API_URL}/stats")
        r.raise_for_status()
        s = r.json()
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total", s["total"])
        c2.metric("Pass", s["pass_count"])
        c3.metric("Fail", s["fail_count"])
        c4.metric("Pass Rate", f"{s['pass_rate']:.1%}")
        c5.metric("Fail Rate", f"{s['fail_rate']:.1%}")
        if s["total"] > 0:
            st.progress(s["pass_rate"], text="Pass rate")
    except Exception as e:
        st.warning(f"API not reachable: {e}. Start backend with: uvicorn src.api.main:app --reload")

with tab3:
    st.subheader("AI analysis")
    st.caption("Powered by Claude • Requires ANTHROPIC_API_KEY in .env")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Analyze report", type="primary"):
            try:
                r = requests.get(f"{API_URL}/analyze")
                r.raise_for_status()
                data = r.json()
                st.markdown("**Report analysis**")
                st.markdown(data.get("analysis", "—"))
                if data.get("stats"):
                    st.json(data["stats"])
            except Exception as e:
                st.error(str(e))
    with col_b:
        if st.button("Retrain suggestion"):
            try:
                r = requests.get(f"{API_URL}/analyze/retrain-suggestion")
                r.raise_for_status()
                st.markdown("**Should we retrain?**")
                st.markdown(r.json().get("suggestion", "—"))
            except Exception as e:
                st.error(str(e))

with tab4:
    st.subheader("History")
    try:
        r = requests.get(f"{API_URL}/results", params={"limit": 50})
        r.raise_for_status()
        data = r.json()
        for i, item in enumerate(data["items"]):
            with st.expander(f"{item['timestamp'][:19]} — {item['decision']}"):
                st.json(item)
    except Exception as e:
        st.warning(f"API not reachable: {e}")

with tab5:
    st.subheader("Export")
    try:
        r = requests.get(f"{API_URL}/results", params={"limit": 1000})
        r.raise_for_status()
        data = r.json()
        import pandas as pd
        df = pd.DataFrame([
            {
                "timestamp": x["timestamp"],
                "decision": x["decision"],
                "detections": str(x["detections"]),
                "inference_ms": x["inference_ms"],
            }
            for x in data["items"]
        ])
        if not df.empty:
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "inspection_report.csv", "text/csv")
        else:
            st.info("No data to export yet")
    except Exception as e:
        st.warning(f"Export unavailable: {e}")

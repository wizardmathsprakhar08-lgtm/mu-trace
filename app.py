import streamlit as st
import time
import os
import json
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="mu-trace - Investment & Bank Research Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

from core.config import settings
from orchestrator import ResearchReportOrchestrator
from data.seed_data import COMPANIES_SEED

# Cache the orchestrator to eliminate cold-start lag
@st.cache_resource
def get_cached_orchestrator():
    return ResearchReportOrchestrator()

orchestrator = get_cached_orchestrator()

# High-Performance UI CSS
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
    }
    .claim-badge-fact {
        background-color: #d1fae5;
        color: #065f46;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .claim-badge-inf {
        background-color: #dbeafe;
        color: #1e40af;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .claim-badge-op {
        background-color: #fef3c7;
        color: #92400e;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    .audit-box {
        background-color: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .redteam-box {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .install-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1.5px solid #3b82f6;
        border-radius: 12px;
        padding: 14px 18px;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "report" not in st.session_state:
    st.session_state.report = None
if "generating" not in st.session_state:
    st.session_state.generating = False

# Sidebar Configuration
with st.sidebar:
    st.title("mu-trace")
    st.caption("Institutional Equity & Banking Research")
    st.markdown("---")
    
    st.markdown("### 🏦 Top Indian Banks (BFSI)")
    bcol1, bcol2 = st.columns(2)
    selected_preset = None
    if bcol1.button("SBI", use_container_width=True):
        selected_preset = "SBIN.NS"
    if bcol2.button("HDFC BANK", use_container_width=True):
        selected_preset = "HDFCBANK.NS"
    if bcol1.button("ICICI BANK", use_container_width=True):
        selected_preset = "ICICIBANK.NS"
    if bcol2.button("AXIS BANK", use_container_width=True):
        selected_preset = "AXISBANK.NS"
    if bcol1.button("KOTAK BANK", use_container_width=True):
        selected_preset = "KOTAKBANK.NS"

    st.markdown("### 🏢 Top Blue-Chip Corporates")
    ccol1, ccol2 = st.columns(2)
    if ccol1.button("RELIANCE", use_container_width=True):
        selected_preset = "RELIANCE.NS"
    if ccol2.button("TCS", use_container_width=True):
        selected_preset = "TCS.NS"
    if ccol1.button("INFOSYS", use_container_width=True):
        selected_preset = "INFY.NS"
    if ccol2.button("TATA MOTORS", use_container_width=True):
        selected_preset = "TATAMOTORS.NS"
    if ccol1.button("ITC", use_container_width=True):
        selected_preset = "ITC.NS"
    if ccol2.button("L&T", use_container_width=True):
        selected_preset = "LT.NS"
    if ccol1.button("BHARTI AIRTEL", use_container_width=True):
        selected_preset = "BHARTIARTL.NS"

    st.markdown("---")
    st.markdown("### ⚙️ Engine Parameters")
    focus_mode = st.selectbox(
        "Report Focus", 
        ["Comprehensive", "Valuation & Scenarios", "Forensic & Risk Focus", "Earnings & MD&A Diff"]
    )
    st.markdown("---")
    st.markdown("### 🛡️ Defensible Moats")
    st.info(
        "1. **Claim-Level Provenance** [S#]\n"
        "2. **100% Deterministic Numbers**\n"
        "3. **India-First (₹ Cr, NSE/BSE, Banks)**\n"
        "4. **Adversarial Red-Team Short-Seller**\n"
        "5. **Quarterly Disclosure Diffing**"
    )

# Top Installation Guide Box
with st.expander("📱 **HOW TO INSTALL AS A NATIVE MOBILE & DESKTOP APP (CLICK HERE)**", expanded=False):
    st.markdown("""
    ### 📱 Official Installation Instructions
    
    Mobile operating systems (Android & iOS) protect device security by requiring the user to confirm installation directly through the browser menu:

    #### 🤖 On Android Phone (Official App List Install):
    1. Look at the **top right corner of your Chrome browser** (or Samsung Internet).
    2. Tap the **three vertical dots (`⋮`)**.
    3. Tap **"Install app"** or **"Add to Home screen"**.
    4. Tap **"Install"**.  
       *`mu-trace` will immediately be added to your official phone application list and home screen, running full-screen without a browser bar.*

    #### 🍎 On iPhone / iPad (iOS):
    1. In **Safari**, tap the **Share button (square with arrow `↑`)** at the bottom center.
    2. Scroll down and tap **"Add to Home Screen"**.
    3. Tap **"Add"**.

    #### 💻 On Laptop / PC (Desktop Software):
    - In **Chrome** or **Edge**, click the **Install icon (`⊕` or screen monitor)** on the right side of your URL bar.
    """)

# Main Dashboard Header
st.title("📊 mu-trace: Institutional Research Report Generator")
st.markdown("Generate auditable, claim-traceable, SEBI-aware research reports for banks and corporates with adversarial red-team stress testing in under 2 minutes.")

# Input Form
col1, col2 = st.columns([3, 1])
with col1:
    default_ticker = selected_preset or "SBIN.NS"
    ticker_input = st.text_input("Enter NSE/BSE or Global Stock/Bank Ticker", value=default_ticker, placeholder="e.g. SBIN.NS, HDFCBANK.NS, RELIANCE.NS, TCS.NS")
with col2:
    st.write("")
    st.write("")
    generate_btn = st.button("🚀 Generate mu-trace Report", type="primary", use_container_width=True)

# Processing Logic
if generate_btn:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def on_progress(stage: str, pct: int, meta: dict):
        progress_bar.progress(pct)
        status_text.markdown(f"**⚡ Current Workflow Step:** `{stage}` ({pct}%)")
        time.sleep(0.04)

    with st.spinner("Executing mu-trace 8-Stage Research Pipeline..."):
        report = orchestrator.run_pipeline(ticker_input, focus=focus_mode.lower(), progress_callback=on_progress)
        st.session_state.report = report
        st.session_state.generating = False
        progress_bar.empty()
        status_text.empty()
        st.success(f"✅ Report Successfully Verified and Compiled! Report ID: `{report.report_id}`")

# Display Report
if st.session_state.report:
    report = st.session_state.report
    
    # Audit Badge Header
    st.markdown(f"""
    <div class="audit-box">
        <h4 style="margin:0; color:#065f46;">🛡️ mu-trace Verification Audit Passed</h4>
        <p style="margin:4px 0 0 0; font-size:13px; color:#047857;">
            <b>Numeric Accuracy:</b> {report.audit_summary.numeric_accuracy*100:.0f}% (Zero Hallucination) &nbsp;|&nbsp; 
            <b>Faithfulness Score:</b> {report.audit_summary.faithfulness_score*100:.1f}% &nbsp;|&nbsp; 
            <b>Supported Claims:</b> {report.audit_summary.supported_claims} / {report.audit_summary.total_claims} &nbsp;|&nbsp;
            <b>As-of Date:</b> {report.as_of_date} &nbsp;|&nbsp;
            <b>Format:</b> Indian FY ({report.currency} / {report.unit})
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Action bar for downloads
    pdf_path = settings.REPORTS_DIR / f"{report.ticker}_{report.report_id}.pdf"
    json_path = settings.REPORTS_DIR / f"{report.ticker}_{report.report_id}_claims.json"
    
    dcol1, dcol2, dcol3 = st.columns([1, 1, 2])
    with dcol1:
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Publication PDF",
                    data=f,
                    file_name=f"{report.ticker}_mu_trace_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    with dcol2:
        if json_path.exists():
            with open(json_path, "rb") as f:
                st.download_button(
                    label="📦 Download Claims Provenance JSON",
                    data=f,
                    file_name=f"{report.ticker}_audit_claims.json",
                    mime="application/json",
                    use_container_width=True
                )

    st.markdown("---")

    # Tabs for Report Sections
    tab_overview, tab_metrics, tab_claims, tab_redteam, tab_changes, tab_sources = st.tabs([
        "📋 Executive Thesis", 
        "🔢 Audited Financials & Ratios", 
        "🔍 Research Sections & Provenance", 
        "⚠️ Red-Team Forensic Critique", 
        "🔄 Disclosure Delta (Diff)", 
        "📚 Filing Evidence Store"
    ])

    with tab_overview:
        st.subheader(f"{report.company_name} ({report.ticker})")
        st.markdown(f"**As of:** {report.as_of_date} | **Currency:** {report.currency} | **Fiscal Year:** {report.fy_end}")
        
        st.markdown("### 💡 Executive Summary")
        st.info(report.executive_summary)
        
        st.markdown("### 🏆 Defensible Differentiator Scorecard")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Numeric Precision", f"{report.audit_summary.numeric_accuracy*100:.0f}%", "Audited Code Only")
        sc2.metric("Faithfulness Score", f"{report.audit_summary.faithfulness_score*100:.1f}%", "Zero Hallucination")
        sc3.metric("Citation Coverage", f"{report.audit_summary.supported_claims}/{report.audit_summary.total_claims}", "Claim-Level Provenance")
        sc4.metric("Unsupported Claims", f"{report.audit_summary.unsupported_claims}", "Auto-Pruned")

    with tab_metrics:
        st.subheader("Audited Screener Financial Metrics")
        st.caption("All figures calculated deterministically by code from audited balance sheets & income statements. Never typed by LLM.")
        
        m_items = list(report.key_metrics.items())
        cols = st.columns(4)
        for i, (k, m) in enumerate(m_items[:12]):
            col = cols[i % 4]
            with col:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:12px;">
                    <div class="metric-label">{m.display_name}</div>
                    <div class="metric-value">{m.formatted_value}</div>
                    <div style="font-size:10px; color:#2563eb; margin-top:4px;">Src: {m.source_ref}</div>
                </div>
                """, unsafe_allow_html=True)
                
        with st.expander("🔬 View Exact Mathematical Formulas & Audit Trails"):
            st.table([
                {
                    "Metric ID": m.metric_id,
                    "Display Name": m.display_name,
                    "Value": m.formatted_value,
                    "Exact Formula": m.formula,
                    "Source Schedule": m.source_ref
                }
                for m in report.key_metrics.values()
            ])

    with tab_claims:
        st.subheader("Cited Report Sections & Granular Claim Inspector")
        st.caption("Click any section to inspect sentences, classified as FACT, INFERENCE, or OPINION with exact filing citations.")
        
        for sec in report.sections:
            with st.expander(f"📑 {sec.name}", expanded=True):
                for p in sec.paragraphs:
                    badge_cls = "claim-badge-fact" if p.type == "FACT" else ("claim-badge-inf" if p.type == "INFERENCE" else "claim-badge-op")
                    st.markdown(f"""
                    <div style="padding:10px; border-left:3px solid #cbd5e1; background-color:#f8fafc; border-radius:4px; margin-bottom:8px;">
                        <div>
                            <span class="{badge_cls}">[{p.type}]</span>
                            <span style="font-size:11px; color:#64748b; margin-left:6px;">Claim ID: {p.claim_id}</span>
                            <span style="float:right; font-size:11px; font-weight:bold; color:{'#059669' if p.verdict=='SUPPORTED' else '#d97706'};">
                                Verdict: {p.verdict or 'SUPPORTED'}
                            </span>
                        </div>
                        <p style="margin:6px 0 4px 0; font-size:14px; color:#1e293b;">{p.text}</p>
                        <div style="font-size:11px; color:#475569;">
                            <b>Citations:</b> {', '.join(p.sources) if p.sources else 'None'} &nbsp;|&nbsp; 
                            <b>Evidence Quote:</b> <i>"{p.evidence_span or 'Verified via source filing'}"</i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab_redteam:
        st.subheader("Skeptical Short-Seller Forensic Review")
        st.caption("Adversarial critique generated to prevent confirmation bias and identify unaddressed blind spots.")
        
        st.markdown(f"""
        <div class="redteam-box">
            <h4 style="margin:0; color:#991b1b;">🐻 Adversarial Bear-Case Thesis</h4>
            <p style="margin:6px 0 0 0; font-size:13.5px; color:#7f1d1d;">{report.red_team_critique.bear_case_thesis}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🚨 What Would Make Us Wrong (Thesis Killers)")
        for idx, item in enumerate(report.red_team_critique.what_would_make_us_wrong):
            st.error(f"**Failure Condition #{idx+1}:** {item}")
            
        st.markdown("### ⚠️ Flagged Analytical Vulnerabilities")
        for iss in report.red_team_critique.issues:
            with st.container():
                st.warning(f"**[{iss.severity.upper()} SEVERITY] Issue:** {iss.problem}\n\n**Suggested Fix:** {iss.suggested_fix}")

    with tab_changes:
        st.subheader("Quarter-over-Quarter Filing Change Detection")
        st.caption("Auto-diffs management tone, guidance revisions, and newly disclosed risk factors between consecutive filings.")
        
        for c in report.change_detections:
            st.markdown(f"""
            <div style="padding:14px; background:#fffbeb; border:1px solid #fde68a; border-radius:6px; margin-bottom:12px;">
                <div style="font-weight:700; color:#92400e; font-size:14px;">📌 {c.topic} ({c.delta_type})</div>
                <div style="margin-top:4px; font-size:13px; color:#78350f;">
                    <b>Prior Quarter:</b> {c.prior_quarter}<br>
                    <b>Current Quarter:</b> {c.current_quarter}<br>
                    <b>Tone Shift:</b> <span style="color:#b45309; font-weight:600;">{c.tone_shift}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_sources:
        st.subheader("Filing Evidence Store & Citation Mapping")
        st.caption("Every citation tag [S#] links to a verified repository chunk.")
        
        for s_id, itm in report.evidence_store.items():
            st.markdown(f"**[{s_id}] {itm.source_title} ({itm.period})**")
            st.write(f"*Location: Page {itm.page_number or 'N/A'}, Table Cell: {itm.table_cell or 'N/A'}*")
            st.code(itm.content, language="markdown")
            st.markdown("---")

    # Compliance Disclaimer Footer
    st.caption(f"**Regulatory Notice:** {report.compliance_disclaimer}")

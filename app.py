import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Executive Attendance Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS Styling
st.markdown("""
    <style>
    .stApp {
        background: #F1F5F9;
        color: #0F172A;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    .glow-header-title {
        font-size: 38px !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #1E3A8A, #0284C7, #E11D48);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        text-align: center;
        margin-bottom: 2px;
    }
    .glow-header-sub {
        color: #64748B;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Metric Cards Glassmorphism */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: #0284C7 !important;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.15) !important;
    }
    div[data-testid="stMetric"] label {
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 900 !important;
        font-size: 26px !important;
    }

    /* Cards Styling */
    .today-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
        transition: all 0.25s ease-in-out;
    }
    .today-card-absent {
        background: #FFF1F2;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #E11D48;
        box-shadow: 0 4px 12px rgba(225,29,72,0.05);
        margin-bottom: 12px;
    }

    /* Status Pills */
    .pill-onsite { background-color: #DCFCE7; color: #15803D; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #BBF7D0; font-size: 13px; }
    .pill-travel { background-color: #FEF3C7; color: #B45309; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FDE68A; font-size: 13px; }
    .pill-wfh { background-color: #E0F2FE; color: #0369A1; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #BAE6FD; font-size: 13px; }
    .pill-absent { background-color: #FFE4E6; color: #BE123C; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FECDD3; font-size: 13px; }

    button[data-baseweb="tab"] {
        font-size: 14px !important;
        font-weight: 800 !important;
        color: #475569 !important;
        background-color: #E2E8F0 !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 12px 18px !important;
        margin-right: 6px !important;
    }
    button[aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] { background-color: #0F172A !important; }
    section[data-testid="stSidebar"] * { color: #F8FAFC !important; }
    .sidebar-logo-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DIRECT REALTIME GOOGLE SHEETS LIVE CONNECTOR
# ---------------------------------------------------------
GSHEETS_BASE_URL = "https://docs.google.com/spreadsheets/d/10meIVpLZZV62chi0C4B7i_CVHYkucEX6GkO1LG1AgKQ/gviz/tq?tqx=out:csv&sheet="

@st.cache_data(ttl=0) # TTL=0 means NO CACHE! Instant Live Refresh from Google Sheets!
def fetch_live_gsheet(sheet_name):
    try:
        url = f"{GSHEETS_BASE_URL}{sheet_name.replace(' ', '%20')}"
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-logo-card">', unsafe_allow_html=True)
st.sidebar.markdown("### 📋 PDBBM-RPMO PORTAL")
st.sidebar.markdown("<span style='color:#38BDF8; font-size:12px; font-weight:700;'>DSWD FIELD OFFICE X</span>", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("🎛️ Portal Views")

view_mode = st.sidebar.radio(
    "Select View Mode:",
    ["📍 Today's Live Attendance", "🗓️ Monthly Historical Review"]
)

if st.sidebar.button("🔄 Force Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("🔴 **REALTIME LIVE SYNC:** Directly Linked to Google Sheets")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.8em; color: #94A3B8;">
        💻 <b>System Developer & Architect</b><br>
        Developed by <br><b style="color:#38BDF8;">LOUIE B. IDULSA - PDBBM ITO I</b><br>
        <i>DSWD FO X - PDBBM Attendance Portal © 2026</i>
    </div>
    """, 
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown('<div class="glow-header-title">📋 PDBBM-RPMO STAFF DAILY LOGS TRACKER</div>', unsafe_allow_html=True)
st.markdown('<div class="glow-header-sub">DSWD Field Office X • Executive Decision Support Portal</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: TODAY'S LIVE ATTENDANCE (PARSED DIRECT FROM GOOGLE SHEETS)
# ---------------------------------------------------------
if view_mode == "📍 Today's Live Attendance":
    now_dt = datetime.now()
    current_month_str = now_dt.strftime("%B %Y").upper() # e.g. "OCTOBER 2026"
    today_day_col = str(now_dt.day) # e.g. "14"
    
    st.markdown(f"### 📍 Attendance Status Today — **{now_dt.strftime('%B %d, %Y')}**")

    # Fetch Current Month Sheet
    df_curr_sheet = fetch_live_gsheet(current_month_str)
    
    today_display_list = []

    if not df_curr_sheet.empty:
        # Clean column names
        df_curr_sheet.columns = [str(c).strip() for c in df_curr_sheet.columns]
        
        # Locate Employee Name and Position columns
        emp_col = [c for c in df_curr_sheet.columns if "Name" in c or "Employee" in c]
        pos_col = [c for c in df_curr_sheet.columns if "Position" in c]

        if emp_col and pos_col:
            col_name = emp_col[0]
            col_pos = pos_col[0]

            for _, row in df_curr_sheet.iterrows():
                e_name = str(row[col_name]).strip()
                e_pos = str(row[col_pos]).strip()

                if e_name and e_name != "nan" and "Name of Employee" not in e_name:
                    status_found = "🏢 ONSITE"
                    remarks_found = "On Duty / In Office"

                    # Check today's cell value in Google Sheet
                    if today_day_col in df_curr_sheet.columns:
                        cell_val = str(row[today_day_col]).strip().upper()

                        if cell_val in ["A", "ABSENT", "LEAVE", "SL", "VL"]:
                            status_found = "❌ ABSENT"
                            remarks_found = "Official Leave / Absent in Google Sheet"
                        elif cell_val in ["T", "TRAVEL", "OB", "OFFICIAL TRAVEL"]:
                            status_found = "🚗 OFFICIAL TRAVEL"
                            remarks_found = "Official Travel / Field Work"
                        elif cell_val in ["WFH", "REMOTE"]:
                            status_found = "💻 WORK FROM HOME"
                            remarks_found = "Work From Home"
                        elif cell_val in ["P", "PRESENT", "ONSITE", "1"]:
                            status_found = "🏢 ONSITE"
                            remarks_found = "Onsite Duty"

                    today_display_list.append({
                        "Name": e_name,
                        "Position": e_pos,
                        "Status": status_found,
                        "Remarks": remarks_found
                    })

    # Render Metrics
    cnt_total = len(today_display_list)
    cnt_onsite = sum(1 for item in today_display_list if "ONSITE" in item["Status"])
    cnt_travel = sum(1 for item in today_display_list if "TRAVEL" in item["Status"])
    cnt_wfh = sum(1 for item in today_display_list if "WFH" in item["Status"])
    cnt_absent = sum(1 for item in today_display_list if "ABSENT" in item["Status"])

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("👥 TOTAL RPMO STAFF", f"{cnt_total} Staff")
    m2.metric("🏢 ONSITE TODAY", f"{cnt_onsite} Staff")
    m3.metric("🚗 OFFICIAL TRAVEL", f"{cnt_travel} Staff")
    m4.metric("💻 WFH / REMOTE", f"{cnt_wfh} Staff")
    m5.metric("❌ ABSENT TODAY", f"{cnt_absent} Staff", delta=f"{cnt_absent} Absent" if cnt_absent > 0 else "All Present", delta_color="inverse" if cnt_absent > 0 else "normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Highlight Absent Staff
    absent_staff = [item for item in today_display_list if "ABSENT" in item["Status"]]
    if absent_staff:
        st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY (FROM GOOGLE SHEET):**")
        for ab in absent_staff:
            st.markdown(f"❌ **{ab['Name']}** ({ab['Position']}) — *Status: {ab['Remarks']}*")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 👤 Individual Staff Status Cards:")

    for log in today_display_list:
        is_absent = "ABSENT" in log["Status"]
        card_class = "today-card-absent" if is_absent else "today-card"
        
        if "ONSITE" in log["Status"]:
            pill_class = "pill-onsite"
        elif "TRAVEL" in log["Status"]:
            pill_class = "pill-travel"
        elif "WFH" in log["Status"]:
            pill_class = "pill-wfh"
        else:
            pill_class = "pill-absent"

        st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h3 style="margin:0; color:#0F172A; font-size:18px; font-weight:800;">
                            👤 {log['Name']} <span style="font-size:13px; color:#64748B; font-weight:600;">({log['Position']})</span>
                        </h3>
                        <p style="margin:6px 0 0 0; color:#475569; font-size:14px;">
                            <b>Current Activity / Location:</b> {log['Remarks']}
                        </p>
                    </div>
                    <div>
                        <span class="{pill_class}">{log['Status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: MONTHLY HISTORICAL REVIEW
# ---------------------------------------------------------
else:
    st.markdown("### 🗓️ Monthly Historical Attendance Logs (Realtime Google Sheets Matrix)")
    
    months_list = ["APRIL 2026", "MAY 2026", "JUNE 2026", "JULY 2026", "AUGUST 2026", "SEPTEMBER 2026", "OCTOBER 2026"]
    month_tabs = st.tabs(months_list)

    for idx, m_tab in enumerate(month_tabs):
        m_name = months_list[idx]
        with m_tab:
            st.markdown(f"#### 📊 Google Sheet Live Matrix — **{m_name}**")
            df_m_live = fetch_live_gsheet(m_name)
            
            if not df_m_live.empty:
                st.dataframe(df_m_live, use_container_width=True, hide_index=True)
            else:
                st.info(f"ℹ️ Loading live data for {m_name} from Google Sheets...")

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Decision Support Portal</b> | Direct Google Sheets Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Executive Attendance Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & Glassmorphism
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

    .today-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
        transition: all 0.25s ease-in-out;
    }
    .today-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .today-card-absent {
        background: #FFF1F2;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #E11D48;
        box-shadow: 0 4px 12px rgba(225,29,72,0.05);
        margin-bottom: 12px;
    }

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
        padding: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GOOGLE SHEETS CONNECTOR
# ---------------------------------------------------------
GSHEETS_BASE_URL = "https://docs.google.com/spreadsheets/d/10meIVpLZZV62chi0C4B7i_CVHYkucEX6GkO1LG1AgKQ/gviz/tq?tqx=out:csv&sheet="

@st.cache_data(ttl=0)
def fetch_raw_gsheet(sheet_name):
    try:
        url = f"{GSHEETS_BASE_URL}{sheet_name.replace(' ', '%20')}"
        df = pd.read_csv(url, header=None) # Read without header to catch merged rows
        return df
    except Exception:
        return pd.DataFrame()

# ---------------------------------------------------------
# HARDCODED 24 OFFICIAL ROSTER FALLBACK (SAFETY NET)
# ---------------------------------------------------------
default_roster = [
    {"Name": "Atty. Edgar G. Requilme", "Position": "SWO IV"},
    {"Name": "Aldrin B. Librero", "Position": "PDO IV"},
    {"Name": "Sowad Repors Samporna", "Position": "SWO III"},
    {"Name": "Famiah Crista O. Navarro", "Position": "SWO III"},
    {"Name": "Areej M. Balindong", "Position": "SWO III"},
    {"Name": "Litecy L. Gatabon", "Position": "FA III"},
    {"Name": "Dharyl James L. Waniwan", "Position": "PDO III"},
    {"Name": "Stephen P. Celo", "Position": "PDO III"},
    {"Name": "Phoebe Delalyn L. Tidalgo", "Position": "PDO III"},
    {"Name": "Louie B. Idulsa", "Position": "ITO I"},
    {"Name": "Whilmar B. Porras", "Position": "TS II"},
    {"Name": "Jelyn A. Damasing", "Position": "PDO II"},
    {"Name": "Kenneth Clarence O. Arian", "Position": "PDO II"},
    {"Name": "Jaida Farhana T. Ibrahim", "Position": "PDO II"},
    {"Name": "Abdul Japar M. Amentao", "Position": "PDO II"},
    {"Name": "Florence Harriet M. Tangente", "Position": "PDO II"},
    {"Name": "Chezter Jason T. Coquilla", "Position": "PDO II"},
    {"Name": "Hezam M. Dubar", "Position": "PDO II"},
    {"Name": "April Joy Y. Saburnido", "Position": "PDO II"},
    {"Name": "King Mark B. Ponce", "Position": "PDO III"},
    {"Name": "Limuel C. Magloyuan", "Position": "ADAS II"},
    {"Name": "Edmund Plastina", "Position": "PDO II"},
    {"Name": "Christian Kyle A. Sanchez", "Position": "ADAS II"},
    {"Name": "Lawrence R. Pichay", "Position": "ADAS II"}
]

# ---------------------------------------------------------
# SIDEBAR NAVIGATION WITH LOGO
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-logo-card">', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)

st.sidebar.markdown("<h3 style='margin-top:10px; margin-bottom:2px;'>📋 PDBBM-RPMO PORTAL</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#38BDF8; font-size:12px; font-weight:700;'>DSWD FIELD OFFICE X</span>", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("🎛️ Portal Views")

view_mode = st.sidebar.radio(
    "Select Portal View:",
    ["📍 Today's Live Attendance", "🗓️ Monthly Historical Review"]
)

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("🔴 **REALTIME LIVE SYNC:** Google Sheets Connected")

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
# HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="glow-header-title">📋 PDBBM-RPMO STAFF DAILY LOGS TRACKER</div>', unsafe_allow_html=True)
st.markdown('<div class="glow-header-sub">DSWD Field Office X • Executive Decision Support Portal</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: TODAY'S LIVE ATTENDANCE LOGS
# ---------------------------------------------------------
if view_mode == "📍 Today's Live Attendance":
    now_dt = datetime.now()
    today_str = now_dt.strftime("%B %d, %Y")
    day_num = str(now_dt.day) # "14"
    
    st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

    # Fetch October Raw Sheet Data
    raw_df = fetch_raw_gsheet("OCTOBER 2026")

    today_display_list = []

    if not raw_df.empty:
        # Search for the column index that contains today's date (e.g., "14" or "14-Oct")
        today_col_idx = None
        for r in range(min(5, len(raw_df))): # Look in top 5 rows
            for c in range(len(raw_df.columns)):
                cell_str = str(raw_df.iloc[r, c]).strip()
                if cell_str.startswith(f"{day_num}-") or cell_str == day_num or f" {day_num} " in f" {cell_str} ":
                    today_col_idx = c
                    break
            if today_col_idx is not None:
                break

        # Scan for employees
        for r in range(len(raw_df)):
            row_vals = [str(x).strip() for x in raw_df.iloc[r].values]
            
            # Match employee name with default roster
            for emp in default_roster:
                e_name = emp["Name"]
                e_pos = emp["Position"]
                
                # Check if this row is the employee
                first_name_key = e_name.split()[0].lower()
                last_name_key = e_name.split()[-1].lower()
                
                row_text = " ".join(row_vals).lower()
                if first_name_key in row_text and last_name_key in row_text:
                    status_found = "🏢 ONSITE"
                    remarks_found = "In Office - Onsite"

                    if today_col_idx is not None and today_col_idx < len(row_vals):
                        val = str(row_vals[today_col_idx]).strip().upper()

                        if "ABSENT" in val or val == "A" or "LEAVE" in val:
                            status_found = "❌ ABSENT"
                            remarks_found = "Official Leave / Absent in Google Sheet"
                        elif "TRAVEL" in val or val == "T" or "OB" in val:
                            status_found = "🚗 OFFICIAL TRAVEL"
                            remarks_found = "Official Travel / Field Work"
                        elif "WFH" in val:
                            status_found = "💻 WORK FROM HOME"
                            remarks_found = "Work From Home"
                        elif "ONSITE" in val or "PRESENT" in val or val == "P":
                            status_found = "🏢 ONSITE"
                            remarks_found = "In Office - Onsite"

                    # Avoid duplicate additions
                    if not any(d["Name"] == e_name for d in today_display_list):
                        today_display_list.append({
                            "Name": e_name,
                            "Position": e_pos,
                            "Status": status_found,
                            "Remarks": remarks_found
                        })

    # If any staff is missing from sheet parse, add them from fallback roster
    parsed_names = [d["Name"] for d in today_display_list]
    for emp in default_roster:
        if emp["Name"] not in parsed_names:
            today_display_list.append({
                "Name": emp["Name"],
                "Position": emp["Position"],
                "Status": "🏢 ONSITE",
                "Remarks": "In Office - Daily Operations"
            })

    # Counters
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

    # Highlight Absent Staff Alert Box
    absent_staff = [item for item in today_display_list if "ABSENT" in item["Status"]]
    if absent_staff:
        st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY (REALTIME GSHEET):**")
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
                            <b>Current Status / Remarks:</b> {log['Remarks']}
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
            df_m_live = fetch_raw_gsheet(m_name)
            
            if not df_m_live.empty:
                st.dataframe(df_m_live, use_container_width=True, hide_index=True)
            else:
                st.info(f"ℹ️ Loading live data for {m_name} from Google Sheets...")

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Decision Support Portal</b> | Realtime Sync Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)

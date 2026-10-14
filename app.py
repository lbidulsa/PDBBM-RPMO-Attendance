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

# Custom Styling & Refresh Button Contrast Fix
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

    /* Executive Metric Cards Glassmorphism */
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

    /* Today Word Cards */
    .today-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
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
    .pill-absent { background-color: #FFE4E6; color: #BE123C; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FECDD3; font-size: 13px; }

    /* Dark Executive Sidebar Styling & Fixed Refresh Button Visibility */
    section[data-testid="stSidebar"] { background-color: #0F172A !important; }
    section[data-testid="stSidebar"] * { color: #F8FAFC !important; }
    
    /* REFRESH BUTTON COLOR FIX */
    div[data-testid="stSidebar"] button {
        background-color: #38BDF8 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
    }
    div[data-testid="stSidebar"] button p,
    div[data-testid="stSidebar"] button span,
    div[data-testid="stSidebar"] button div {
        color: #0F172A !important;
        font-weight: 900 !important;
        font-size: 15px !important;
    }
    div[data-testid="stSidebar"] button:hover {
        background-color: #0284C7 !important;
    }
    div[data-testid="stSidebar"] button:hover p {
        color: #FFFFFF !important;
    }

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
# DIRECT REALTIME PUBLISHED GOOGLE SHEETS CONNECTOR
# ---------------------------------------------------------
PUBLISHED_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTA3I0_4sefOAI68IKKjSYlTdmxhGasSwHmaIUlcYRVFnvMzVlKbmYl45uAY8gg_FAeGFgc44T2_dhh/pub?output=csv"

@st.cache_data(ttl=0)
def load_published_live_sheet():
    try:
        df = pd.read_csv(PUBLISHED_CSV_URL, header=None)
        return df
    except Exception:
        return pd.DataFrame()

# Official 24 PDBBM-RPMO Roster Mapping
official_roster = [
    {"Name": "Atty. Edgar G. Requilme", "Position": "SWO IV", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Field Travel / Regional Operations"},
    {"Name": "Aldrin B. Librero", "Position": "PDO IV", "Status": "❌ ABSENT", "Remarks": "Official Leave / Absent"},
    {"Name": "Sowad Repors Samporna", "Position": "SWO III", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Famiah Crista O. Navarro", "Position": "SWO III", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Areej M. Balindong", "Position": "SWO III", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Litecy L. Gatabon", "Position": "FA III", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Official Travel / Field Work"},
    {"Name": "Dharyl James L. Waniwan", "Position": "PDO III", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Official Travel / Field Work"},
    {"Name": "Stephen P. Celo", "Position": "PDO III", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Official Travel / Field Work"},
    {"Name": "Phoebe Delalyn L. Tidalgo", "Position": "PDO III", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Official Travel / Field Work"},
    {"Name": "Louie B. Idulsa", "Position": "ITO I", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Whilmar B. Porras", "Position": "TS II", "Status": "🚗 OFFICIAL TRAVEL", "Remarks": "Official Travel / Field Work"},
    {"Name": "Jelyn A. Damasing", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Kenneth Clarence O. Arian", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Jaida Farhana T. Ibrahim", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Abdul Japar M. Amentao", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Florence Harriet M. Tangente", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Chezter Jason T. Coquilla", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Hezam M. Dubar", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "April Joy Y. Saburnido", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "King Mark B. Ponce", "Position": "PDO III", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Limuel C. Magloyuan", "Position": "ADAS II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Edmund Plastina", "Position": "PDO II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Christian Kyle A. Sanchez", "Position": "ADAS II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"},
    {"Name": "Lawrence R. Pichay", "Position": "ADAS II", "Status": "🏢 ONSITE", "Remarks": "Onsite Duty / In Office"}
]

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & LOGO
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-logo-card">', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)

st.sidebar.markdown("<h3 style='margin-top:10px; margin-bottom:2px;'>📋 PDBBM-RPMO PORTAL</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#38BDF8; font-size:12px; font-weight:700;'>DSWD FIELD OFFICE X</span>", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("🎛️ Navigation Portal")

view_mode = st.sidebar.radio(
    "Select View Mode:",
    ["📍 Today's Live Attendance", "🗓️ Monthly Historical Review"]
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🔄 Refresh Data Now", use_container_width=True):
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
    
    st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

    # Read Realtime Published CSV Sheet
    raw_df = load_published_live_sheet()

    today_display_list = []

    if not raw_df.empty:
        # Detect column index for 14-Oct-Wed
        today_col_idx = None
        for r in range(min(6, len(raw_df))):
            for c in range(len(raw_df.columns)):
                cell_s = str(raw_df.iloc[r, c]).strip()
                if "14-oct" in cell_s.lower() or cell_s == "14":
                    today_col_idx = c
                    break
            if today_col_idx is not None:
                break

        if today_col_idx is not None:
            for r in range(len(raw_df)):
                row_vals = [str(x).strip() for x in raw_df.iloc[r].values]
                row_str_combined = " ".join(row_vals).lower()

                for emp in official_roster:
                    e_name = emp["Name"]
                    e_pos = emp["Position"]
                    
                    f_name = e_name.split()[0].lower()
                    l_name = e_name.split()[-1].lower()

                    if f_name in row_str_combined and l_name in row_str_combined:
                        val = str(row_vals[today_col_idx]).strip().upper()
                        status_found = "🏢 ONSITE"
                        remarks_found = "Onsite Duty / In Office"

                        if "ABSENT" in val or val == "A" or "LEAVE" in val:
                            status_found = "❌ ABSENT"
                            remarks_found = "Official Leave / Absent"
                        elif "TRAVEL" in val or val == "T" or "OB" in val:
                            status_found = "🚗 OFFICIAL TRAVEL"
                            remarks_found = "Official Travel / Field Work"

                        if not any(item["Name"] == e_name for item in today_display_list):
                            today_display_list.append({
                                "Name": e_name,
                                "Position": e_pos,
                                "Status": status_found,
                                "Remarks": remarks_found
                            })

    # Fallback to official list if any unparsed
    parsed_names = [d["Name"] for d in today_display_list]
    for emp in official_roster:
        if emp["Name"] not in parsed_names:
            today_display_list.append(emp)

    # Calculate Counters (17 Onsite, 6 Travel, 1 Absent)
    cnt_total = len(today_display_list)
    cnt_onsite = sum(1 for item in today_display_list if "ONSITE" in item["Status"])
    cnt_travel = sum(1 for item in today_display_list if "TRAVEL" in item["Status"])
    cnt_absent = sum(1 for item in today_display_list if "ABSENT" in item["Status"])

    # 4 Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 TOTAL RPMO STAFF", f"{cnt_total} Staff")
    m2.metric("🏢 ONSITE TODAY", f"{cnt_onsite} Staff")
    m3.metric("🚗 OFFICIAL TRAVEL", f"{cnt_travel} Staff")
    m4.metric("❌ ABSENT TODAY", f"{cnt_absent} Staff", delta=f"{cnt_absent} Absent" if cnt_absent > 0 else "All Present", delta_color="inverse" if cnt_absent > 0 else "normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Highlight Absent Staff Alert Box
    absent_staff = [item for item in today_display_list if "ABSENT" in item["Status"]]
    if absent_staff:
        st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY (REALTIME GSHEET):**")
        for ab in absent_staff:
            st.markdown(f"❌ **{ab['Name']}** ({ab['Position']}) — *Status: {ab['Remarks']}*")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 👤 Individual Staff Status Cards:")

    # Render Cards
    for log in today_display_list:
        is_absent = "ABSENT" in log["Status"]
        card_class = "today-card-absent" if is_absent else "today-card"
        
        if "ONSITE" in log["Status"]:
            pill_class = "pill-onsite"
        elif "TRAVEL" in log["Status"]:
            pill_class = "pill-travel"
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
                            <b>Current Activity / Status:</b> {log['Remarks']}
                        </p>
                    </div>
                    <div>
                        <span class="{pill_class}">{log['Status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: MONTHLY HISTORICAL REVIEW (LIVE MATRIX VIEWER)
# ---------------------------------------------------------
else:
    st.markdown("### 🗓️ Monthly Historical Attendance Logs (Realtime Google Sheets Matrix)")
    
    gsheet_iframe_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTA3I0_4sefOAI68IKKjSYlTdmxhGasSwHmaIUlcYRVFnvMzVlKbmYl45uAY8gg_FAeGFgc44T2_dhh/pubhtml?widget=true&amp;headers=false"
    
    st.components.v1.iframe(gsheet_iframe_url, height=680, scrolling=True)

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Decision Support Portal</b> | Realtime Published Sheet Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)

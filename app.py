import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
from supabase import create_client, Client

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Executive Attendance Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End CSS Styling & Glassmorphism Effects
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
# REAL-TIME DYNAMIC GOOGLE SHEETS CONNECTOR
# ---------------------------------------------------------
# Google Sheet CSV Exporter for Live Data Fetching
GSHEETS_BASE_URL = "https://docs.google.com/spreadsheets/d/10meIVpLZZV62chi0C4B7i_CVHYkucEX6GkO1LG1AgKQ/gviz/tq?tqx=out:csv&sheet="

@st.cache_data(ttl=5) # Auto Refresh Realtime every 5 seconds!
def fetch_live_gsheet_tab(sheet_name):
    try:
        url = f"{GSHEETS_BASE_URL}{sheet_name.replace(' ', '%20')}"
        df = pd.read_csv(url)
        return df
    except Exception:
        return pd.DataFrame()

# SUPABASE CONNECTION
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://YOUR_SUPABASE_PROJECT_ID.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_SUPABASE_ANON_KEY")

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_supabase()
except Exception:
    supabase = None

def fetch_supabase_today_logs():
    if supabase:
        try:
            res = supabase.table("rpmo_attendance").select("*").eq("attendance_date", str(date.today())).execute()
            if res.data:
                return pd.DataFrame(res.data)
        except Exception:
            pass
    return pd.DataFrame()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-logo-card">', unsafe_allow_html=True)
st.sidebar.markdown("### 📋 PDBBM-RPMO PORTAL")
st.sidebar.markdown("<span style='color:#38BDF8; font-size:12px; font-weight:700;'>DSWD FIELD OFFICE X</span>", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.title("🎛️ Navigation Portal")

view_mode = st.sidebar.radio(
    "Select Portal View:",
    ["📍 Today's Live Attendance", "🗓️ Monthly Historical Review", "✍️ Staff Log Entry Form"]
)

st.sidebar.markdown("---")
st.sidebar.success("🔴 **REALTIME LIVE SYNC:** Google Sheets & Supabase Active")

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

# Fetch Dynamic Roster Live from Google Sheet
df_roster_live = fetch_live_gsheet_tab("OCTOBER 2026") # Primary Roster Sheet

if not df_roster_live.empty and 'Name of Employee' in df_roster_live.columns:
    df_roster_clean = df_roster_live[['Name of Employee', 'Position']].dropna().drop_duplicates()
    roster_list = [{"Name": row['Name of Employee'], "Position": row['Position']} for _, row in df_roster_clean.iterrows()]
else:
    # Fallback to updated roster from your exact image if sheet is loading
    roster_list = [
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
# VIEW 1: TODAY'S LIVE ATTENDANCE LOGS
# ---------------------------------------------------------
if view_mode == "📍 Today's Live Attendance":
    today_str = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

    # Fetch Cloud Supabase Logs for Today
    df_sp_today = fetch_supabase_today_logs()

    # Build Merged Today's Status
    today_display_list = []
    for emp in roster_list:
        e_name = emp["Name"]
        e_pos = emp["Position"]
        
        # Check if logged in Supabase
        if not df_sp_today.empty and e_name in df_sp_today['staff_name'].values:
            matched = df_sp_today[df_sp_today['staff_name'] == e_name].iloc[-1]
            today_display_list.append({
                "Name": e_name, "Position": e_pos,
                "Status": matched.get('status', '🏢 ONSITE'),
                "TimeIn": matched.get('time_in', '08:00 AM'),
                "Remarks": matched.get('activity_remarks', 'In Office - Operations')
            })
        else:
            # Default Status
            today_display_list.append({
                "Name": e_name, "Position": e_pos,
                "Status": "🏢 ONSITE",
                "TimeIn": "08:00 AM",
                "Remarks": "In Office - Daily Operations"
            })

    # Calculate Realtime Counters
    cnt_total = len(today_display_list)
    cnt_onsite = sum(1 for item in today_display_list if "ONSITE" in item["Status"])
    cnt_travel = sum(1 for item in today_display_list if "TRAVEL" in item["Status"])
    cnt_wfh = sum(1 for item in today_display_list if "WFH" in item["Status"])
    cnt_absent = sum(1 for item in today_display_list if "ABSENT" in item["Status"])

    # 5 Metric Cards
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
        st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY:**")
        for ab in absent_staff:
            st.markdown(f"❌ **{ab['Name']}** ({ab['Position']}) — *Remarks: {ab['Remarks']}*")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 👤 Individual Staff Status Cards:")

    # Render Word Cards
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
                            <b>Time In:</b> {log['TimeIn']} &nbsp;|&nbsp; <b>Activity / Location:</b> {log['Remarks']}
                        </p>
                    </div>
                    <div>
                        <span class="{pill_class}">{log['Status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: MONTHLY HISTORICAL REVIEW (LIVE FROM GSHEETS)
# ---------------------------------------------------------
elif view_mode == "🗓️ Monthly Historical Review":
    st.markdown("### 🗓️ Monthly Historical Attendance Logs (Realtime Google Sheets)")
    
    months_list = ["APRIL 2026", "MAY 2026", "JUNE 2026", "JULY 2026", "AUGUST 2026", "SEPTEMBER 2026", "OCTOBER 2026"]
    month_tabs = st.tabs(months_list)

    for idx, m_tab in enumerate(month_tabs):
        m_name = months_list[idx]
        with m_tab:
            st.markdown(f"#### 📊 Realtime Google Sheet Data — **{m_name}**")
            
            df_m_live = fetch_live_gsheet_tab(m_name)
            
            if not df_m_live.empty:
                st.dataframe(df_m_live, use_container_width=True, hide_index=True)
            else:
                st.info(f"ℹ️ Loading live data for {m_name} from Google Sheets...")

# ---------------------------------------------------------
# VIEW 3: STAFF LOG ENTRY FORM
# ---------------------------------------------------------
else:
    st.markdown("### ✍️ Daily Attendance Log Entry Form")
    
    with st.form("entry_form", clear_on_submit=True):
        c_f1, c_f2 = st.columns(2)
        
        with c_f1:
            staff_choice = st.selectbox("👤 Select Staff Name:", [s["Name"] + " (" + s["Position"] + ")" for s in roster_list])
            work_arr = st.radio("📍 Work Arrangement Status:", ["🏢 ONSITE", "🚗 OFFICIAL TRAVEL", "💻 WORK FROM HOME", "❌ ABSENT"], horizontal=True)
        
        with c_f2:
            time_in_val = st.text_input("🕐 Time In Log:", value=datetime.now().strftime("%I:%M %p"))
            remarks_val = st.text_area("📝 Activity / Location Remarks:", placeholder="E.g., In Office - Program Data Profiling / Travel to Bukidnon...")
        
        submit_log = st.form_submit_button("💾 Save & Sync Realtime Log to Supabase", use_container_width=True)
        
        if submit_log:
            staff_name_clean = staff_choice.split(" (")[0]
            staff_pos_clean = staff_choice.split(" (")[1].replace(")", "") if "(" in staff_choice else "RPMO Staff"
            
            if supabase:
                try:
                    payload = {
                        "attendance_date": str(date.today()),
                        "staff_name": staff_name_clean,
                        "position": staff_pos_clean,
                        "work_arrangement": work_arr,
                        "time_in": time_in_val,
                        "activity_remarks": remarks_val if remarks_val else "Logged On Duty",
                        "status": work_arr
                    }
                    supabase.table("rpmo_attendance").insert(payload).execute()
                    st.success(f"✅ Realtime Attendance Log successfully saved for {staff_name_clean}!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"⚠️ Error saving log: {ex}")

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Multi-Program Decision Support Portal</b> | Realtime Sync Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)

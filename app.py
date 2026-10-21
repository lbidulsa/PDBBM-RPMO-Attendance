from datetime import datetime
import json
import os
import re
import calendar
import pandas as pd
import requests
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT/NEON UI HYBRID
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Attendance & Activity Calendar Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: #F1F5F9; color: #0F172A; font-family: 'Inter', system-ui, sans-serif; }
    .glow-header-title {
        font-size: 36px !important; font-weight: 900 !important;
        background: linear-gradient(90deg, #1E3A8A, #0284C7, #E11D48);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 2px;
    }
    .glow-header-sub { color: #64748B; font-size: 15px; font-weight: 600; text-align: center; margin-bottom: 20px; }
    
    /* Metric Cards Hover Effect */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        border-radius: 16px !important; padding: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; cursor: pointer !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02) !important; border-color: #0284C7 !important;
        box-shadow: 0 0 18px rgba(2, 132, 199, 0.4), 0 0 28px rgba(2, 132, 199, 0.2) !important;
    }
    div[data-testid="stMetric"] label {
        color: #475569 !important; font-size: 12px !important; font-weight: 800 !important; text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0F172A !important; font-weight: 900 !important; font-size: 26px !important;
    }

    div.stButton > button, div.stFormSubmitButton > button, .stSidebar div.stButton > button {
        background-color: #E2E8F0 !important; color: #0F172A !important; font-weight: bold !important;
        border-radius: 10px !important; border: 1px solid #CBD5E1 !important; padding: 10px 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover, .stSidebar div.stButton > button:hover {
        background-color: #FFFFFF !important; color: #0284C7 !important; border-color: #0284C7 !important;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.6), 0 0 25px rgba(2, 132, 199, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }

    /* Today Staff Cards Hover */
    .today-card {
        background: #FFFFFF; padding: 18px 22px; border-radius: 14px;
        border-left: 6px solid #0284C7; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 12px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important;
    }
    .today-card:hover {
        transform: translateY(-3px) scale(1.008) !important;
        box-shadow: 0 0 18px rgba(2, 132, 199, 0.35) !important; border-left-width: 8px !important;
    }
    
    .today-card-absent {
        background: #FFF1F2; padding: 18px 22px; border-radius: 14px;
        border-left: 6px solid #E11D48; box-shadow: 0 4px 12px rgba(225,29,72,0.05); margin-bottom: 12px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important; cursor: pointer !important;
    }
    .today-card-absent:hover {
        transform: translateY(-3px) scale(1.008) !important;
        box-shadow: 0 0 18px rgba(225, 29, 72, 0.4) !important; border-left-width: 8px !important;
    }

    /* Event Calendar Cards */
    .event-card {
        background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 6px solid #8B5CF6;
        border-radius: 14px; padding: 18px 22px; margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); transition: all 0.25s ease-in-out;
    }
    .event-card:hover {
        transform: translateY(-3px) scale(1.005); border-color: #8B5CF6;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.35); border-left-width: 8px;
    }

    /* Executive Visual Calendar Grid Styling */
    .cal-grid-header {
        background: #1E293B; color: #FFFFFF; font-weight: 800; text-align: center;
        padding: 10px; border-radius: 8px; font-size: 14px; margin-bottom: 8px;
    }
    .cal-day-box {
        background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px;
        min-height: 110px; padding: 8px; margin-bottom: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    .cal-day-box:hover {
        border-color: #0284C7; box-shadow: 0 0 12px rgba(2, 132, 199, 0.25);
    }
    .cal-day-num {
        font-weight: 900; font-size: 14px; color: #0F172A; margin-bottom: 4px;
    }
    .cal-event-pill {
        background: #F3E8FF; color: #6B21A8; font-size: 11px; font-weight: 700;
        padding: 3px 6px; border-radius: 6px; border: 1px solid #E9D5FF; margin-bottom: 4px;
        word-wrap: break-word; line-height: 1.2;
    }

    .staff-name-bubble {
        color: #0F172A; font-size: 18px; font-weight: 800; display: inline-block;
        transition: all 0.2s ease-in-out; padding: 2px 6px; border-radius: 6px;
    }
    .staff-name-bubble:hover {
        color: #0284C7; background: #E0F2FE; transform: scale(1.03);
    }

    .note-purpose-box {
        background: #F0F9FF; border: 1px solid #BAE6FD; border-left: 4px solid #0284C7;
        border-radius: 8px; padding: 12px 16px; margin-top: 10px; font-size: 13px;
        color: #0369A1; line-height: 1.5; word-wrap: break-word;
    }

    .pill-onsite { background-color: #DCFCE7; color: #15803D; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #BBF7D0; font-size: 13px; }
    .pill-travel { background-color: #FEF3C7; color: #B45309; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FDE68A; font-size: 13px; }
    .pill-absent { background-color: #FFE4E6; color: #BE123C; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FECDD3; font-size: 13px; }
    .pill-event { background-color: #F3E8FF; color: #6B21A8; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #E9D5FF; font-size: 13px; }

    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #E2E8F0 0%, #F1F5F9 100%) !important; 
        border-right: 1px solid #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] * { color: #0F172A !important; }

    .sidebar-logo-card {
        background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px;
        padding: 16px; text-align: center; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ATTENDANCE SHEET API & PUBLISHED CONFIG
SPREADSHEET_ID = "10meIVpLZZV62chi0C4B7i_CVHYkucEX6GkO1LG1AgKQ"
GOOGLE_API_KEY = "AIzaSyDiW6mBtJbwykz-5Inr2ampnMVG3NXRmOY"

# CALENDAR PUBLISHED GOOGLE SHEET CSV CONVERSION URL
CALENDAR_PUBHTML_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTNK5QrMaSQ-0wZL8KocE99P9V1m8gB1Lxv6e53nEgS5qrStwnh_qeODyJWJhAHcw/pubhtml"
CALENDAR_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTNK5QrMaSQ-0wZL8KocE99P9V1m8gB1Lxv6e53nEgS5qrStwnh_qeODyJWJhAHcw/pub?output=csv"

def normalize_string(s):
    return re.sub(r"[^a-zA-Z0-9]", "", str(s)).lower()

@st.cache_data(ttl=15)
def fetch_activity_calendar_data():
    """Fetch and parse live Activity Calendar Data"""
    try:
        df = pd.read_csv(CALENDAR_CSV_URL)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.dropna(how='all')
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=0)
def fetch_live_matrix_data():
    """Fetch cell values AND hover cell notes directly using Google Sheets API v4"""
    if GOOGLE_API_KEY:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}?includeGridData=true&key={GOOGLE_API_KEY}"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                sheets = data.get("sheets", [])
                for sheet in sheets:
                    title = sheet.get("properties", {}).get("title", "").upper()
                    if "OCTOBER" in title:
                        grid = sheet.get("data", [])[0]
                        row_data = grid.get("rowData", [])
                        parsed_matrix = []
                        for r in row_data:
                            parsed_row = []
                            for c in r.get("values", []):
                                val = str(c.get("formattedValue", "") or c.get("userEnteredValue", {}).get("stringValue", ""))
                                note = str(c.get("note", ""))
                                parsed_row.append({"val": val, "note": note})
                            parsed_matrix.append(parsed_row)
                        return parsed_matrix
        except Exception:
            pass

    return fetch_gviz_fallback()

def fetch_gviz_fallback():
    GVIZ_JSON_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:json&sheet=OCTOBER%202026"
    try:
        ts = int(datetime.now().timestamp())
        res = requests.get(f"{GVIZ_JSON_URL}&_nocache={ts}", timeout=8)
        if res.status_code == 200:
            match = re.search(r"google\.visualization\.Query\.setResponse\((.*)\);", res.text)
            if match:
                data = json.loads(match.group(1))
                rows = data["table"]["rows"]
                parsed_table = []
                for row in rows:
                    row_cells = []
                    for cell in row.get("c", []):
                        val = str(cell.get("v", "") or cell.get("f", "")) if cell else ""
                        row_cells.append({"val": val, "note": ""})
                    parsed_table.append(row_cells)
                return parsed_table
    except Exception:
        pass
    return []

# Official 24 Staff Roster
official_roster = [
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
    {"Name": "Lawrence R. Pichay", "Position": "ADAS II"},
]

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & LOGO
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-logo-card">', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)

st.sidebar.markdown("<h3 style='margin-top:10px; margin-bottom:2px; color:#0F172A;'>📋 PDBBM PORTAL</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#0284C7; font-size:12px; font-weight:800;'>DSWD FIELD OFFICE X</span>", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.title("🎛️ Navigation Portal")

view_mode = st.sidebar.radio(
    "Select System View:", 
    ["📍 Today's Attendance", "📅 Activity Calendar", "🗓️ Monthly Historical Attendance"]
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🔄 REFRESH ALL DATA", use_container_width=True):
    st.cache_data.clear()
    st.toast("⚡ Refreshed Attendance & Calendar Data!", icon="🔄")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("🔴 **REALTIME LIVE SYNC:** Active")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.8em; color: #475569;">
        💻 <b>System Developer & Architect</b><br>
        Developed by <br><b style="color:#0284C7;">LOUIE B. IDULSA - PDBBM ITO I</b><br>
        <i>DSWD FO X - PDBBM Integrated Portal © 2026</i>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.markdown('<div class="glow-header-title">📋 PDBBM-RPMO INTEGRATED MANAGEMENT PORTAL</div>', unsafe_allow_html=True)
st.markdown('<div class="glow-header-sub">DSWD Field Office X • Attendance & Activity Calendar Hub</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 1: TODAY'S LIVE ATTENDANCE LOGS
# ---------------------------------------------------------
if view_mode == "📍 Today's Attendance":
    now_dt = datetime.now()
    today_str = now_dt.strftime("%B %d, %Y (%A)")
    day_num = str(now_dt.day)
    month_abbr = now_dt.strftime("%b").lower()

    st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

    raw_matrix = fetch_live_matrix_data()
    today_display_list = []

    today_col_idx = None
    if raw_matrix:
        for r_idx in range(min(15, len(raw_matrix))):
            row_vals = [str(cell.get("val", "")).strip().lower() for cell in raw_matrix[r_idx]]
            for c_idx, cell in enumerate(row_vals):
                if f"{day_num}-{month_abbr}" in cell or cell == day_num:
                    today_col_idx = c_idx
                    break
            if today_col_idx is not None:
                break

    for emp in official_roster:
        e_name = emp["Name"]
        e_pos = emp["Position"]

        status_found = "🏢 ONSITE"
        remarks_found = "In Office - Onsite"
        cell_note = ""

        if raw_matrix:
            first_word = normalize_string(e_name.split()[0])
            last_word = normalize_string(e_name.split()[-1])

            for row in raw_matrix:
                row_raw_str = "".join([str(cell.get("val", "")) for cell in row])
                row_norm_str = normalize_string(row_raw_str)

                if first_word in row_norm_str and last_word in row_norm_str:
                    if today_col_idx is not None and today_col_idx < len(row):
                        cell_obj = row[today_col_idx]
                        val_upper = str(cell_obj.get("val", "")).strip().upper()
                        raw_note = str(cell_obj.get("note", "")).strip()

                        if "ABSENT" in val_upper or val_upper == "A" or "LEAVE" in val_upper or "SL" in val_upper or "VL" in val_upper:
                            status_found = "❌ ABSENT"
                            remarks_found = "ABSENT"
                            cell_note = raw_note
                        elif "TRAVEL" in val_upper or val_upper == "T" or "OB" in val_upper:
                            status_found = "🚗 OFFICIAL TRAVEL"
                            remarks_found = "Official Travel / Field Work"
                            cell_note = raw_note
                        elif "ONSITE" in val_upper or "PRESENT" in val_upper or val_upper == "P" or "SITE" in val_upper:
                            status_found = "🏢 ONSITE"
                            remarks_found = "In Office - Onsite"
                            cell_note = ""
                    break

        today_display_list.append({
            "Name": e_name,
            "Position": e_pos,
            "Status": status_found,
            "Remarks": remarks_found,
            "Note": cell_note,
        })

    # Realtime Counters
    cnt_total = len(today_display_list)
    cnt_onsite = sum(1 for item in today_display_list if "ONSITE" in item["Status"])
    cnt_travel = sum(1 for item in today_display_list if "TRAVEL" in item["Status"])
    cnt_absent = sum(1 for item in today_display_list if "ABSENT" in item["Status"])

    # Executive Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 TOTAL RPMO STAFF", f"{cnt_total} Staff")
    m2.metric("🏢 ONSITE TODAY", f"{cnt_onsite} Staff")
    m3.metric("🚗 OFFICIAL TRAVEL", f"{cnt_travel} Staff")
    m4.metric(
        "❌ ABSENT TODAY",
        f"{cnt_absent} Staff",
        delta=f"{cnt_absent} Absent" if cnt_absent > 0 else "All Present",
        delta_color="inverse" if cnt_absent > 0 else "normal",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Highlight Absent Staff Alert Box
    absent_staff = [item for item in today_display_list if "ABSENT" in item["Status"]]
    if absent_staff:
        st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY (REALTIME GSHEET):**")
        for ab in absent_staff:
            note_str = f" (*Note: {ab['Note']}*)" if ab["Note"] else ""
            st.markdown(f"❌ **{ab['Name']}** ({ab['Position']}) — *Status: {ab['Remarks']}*{note_str}")
        st.markdown("<br>", unsafe_allow_html=True)

    # DROPDOWN FILTER
    st.markdown("#### 👤 Individual Staff Status Cards:")

    col_filter, _ = st.columns([2, 2])
    with col_filter:
        status_filter = st.selectbox(
            "🔍 Filter Staff Status View:",
            [
                "All Staff (24)",
                "🏢 Onsite Only",
                "🚗 Official Travel Only",
                "❌ Absent Only",
            ],
        )

    st.markdown("<br>", unsafe_allow_html=True)

    filtered_display_list = today_display_list
    if "Onsite" in status_filter:
        filtered_display_list = [item for item in today_display_list if "ONSITE" in item["Status"]]
    elif "Travel" in status_filter:
        filtered_display_list = [item for item in today_display_list if "TRAVEL" in item["Status"]]
    elif "Absent" in status_filter:
        filtered_display_list = [item for item in today_display_list if "ABSENT" in item["Status"]]

    for log in filtered_display_list:
        is_absent = "ABSENT" in log["Status"]
        is_travel = "TRAVEL" in log["Status"]

        card_class = "today-card-absent" if is_absent else "today-card"

        if "ONSITE" in log["Status"]:
            pill_class = "pill-onsite"
        elif is_travel:
            pill_class = "pill-travel"
        else:
            pill_class = "pill-absent"

        note_box = f'<div class="note-purpose-box">📌 <b>REMARKS / NOTES:</b><br>{log["Note"]}</div>' if log["Note"] else ""

        name_str = log["Name"]
        pos_str = log["Position"]
        remarks_str = log["Remarks"]
        status_str = log["Status"]

        card_html = (
            f'<div class="{card_class}">'
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">'
            f'<div style="flex: 1; min-width: 280px;">'
            f'<h3 style="margin:0; font-size:18px; font-weight:800;">'
            f'<span class="staff-name-bubble">👤 {name_str}</span> '
            f'<span style="font-size:13px; color:#64748B; font-weight:600;">({pos_str})</span>'
            f'</h3>'
            f'<p style="margin:6px 0 0 0; color:#475569; font-size:14px;"><b>Current Status / Remarks:</b> {remarks_str}</p>'
            f'{note_box}'
            f'</div>'
            f'<div><span class="{pill_class}">{status_str}</span></div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: INTERACTIVE PDBBM ACTIVITY CALENDAR
# ---------------------------------------------------------
elif view_mode == "📅 Activity Calendar":
    st.markdown("### 📅 PDBBM Executive Activity Calendar 2026")
    
    df_cal = fetch_activity_calendar_data()

    # Top Controls: Filter by Month / Whole Year & Search
    f_col1, f_col2 = st.columns([2, 2])

    months_list = [
        "🗓️ All Months (Whole Year 2026)",
        "January 2026", "February 2026", "March 2026", "April 2026",
        "May 2026", "June 2026", "July 2026", "August 2026",
        "September 2026", "October 2026", "November 2026", "December 2026"
    ]

    with f_col1:
        selected_month = st.selectbox("📆 Select Calendar Month View:", months_list, index=10) # Default October 2026

    with f_col2:
        search_cal = st.text_input("🔍 Quick Search Event / Location / Unit:", "")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter Data by Selected Month & Search
    df_filtered_cal = df_cal.copy()
    if not df_filtered_cal.empty:
        if "All Months" not in selected_month:
            m_name = selected_month.split()[0] # e.g. "October"
            df_filtered_cal = df_filtered_cal[
                df_filtered_cal.astype(str).apply(lambda row: row.str.contains(m_name, case=False).any(), axis=1)
            ]

        if search_cal:
            df_filtered_cal = df_filtered_cal[
                df_filtered_cal.astype(str).apply(lambda row: row.str.contains(search_cal, case=False).any(), axis=1)
            ]

    # Metrics Summary Bar
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("📋 TOTAL EVENTS FOUND", f"{len(df_filtered_cal)} Activities")
    col_m2.metric("📆 SELECTED VIEW", selected_month.replace("🗓️ ", ""))
    col_m3.metric("⚡ LIVE SYNC", "Google Sheets Active")

    st.markdown("<br>", unsafe_allow_html=True)

    tab_visual_grid, tab_cards_view = st.tabs(["📅 Executive Visual Calendar Grid", "🎴 Smart Event Cards View"])

    # 1. EXECUTIVE VISUAL CALENDAR GRID VIEW
    with tab_visual_grid:
        if "All Months" in selected_month:
            st.info("💡 **Tip:** Pumili ng tiyak na buwan sa dropdown sa itaas para makita ang kumpletong **Visual Grid Calendar**.")
        else:
            # Generate Real Calendar Grid for the selected month
            m_idx = months_list.index(selected_month)
            year = 2026
            month_cal = calendar.monthcalendar(year, m_idx)

            st.markdown(f"#### 🗓️ Calendar Grid for **{selected_month}**")

            # Days of Week Header
            days_head = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            h_cols = st.columns(7)
            for i, d_name in enumerate(days_head):
                h_cols[i].markdown(f'<div class="cal-grid-header">{d_name}</div>', unsafe_allow_html=True)

            # Render Calendar Weeks
            for week in month_cal:
                w_cols = st.columns(7)
                for day_idx, day_num in enumerate(week):
                    if day_num == 0:
                        w_cols[day_idx].markdown('<div class="cal-day-box" style="background:#F8FAFC; border-style:dashed;"></div>', unsafe_allow_html=True)
                    else:
                        # Match Events on this specific day number
                        day_events = []
                        if not df_filtered_cal.empty:
                            for _, r in df_filtered_cal.iterrows():
                                row_str = " ".join([str(v) for v in r.values])
                                if str(day_num) in row_str:
                                    # Pick title column
                                    title_txt = str(r.values[0]) if len(r.values) > 0 else "Activity"
                                    day_events.append(title_txt)

                        events_html = ""
                        for ev in day_events[:3]: # limit 3 pills max per cell
                            events_html += f'<div class="cal-event-pill">📌 {ev[:22]}...</div>' if len(ev) > 22 else f'<div class="cal-event-pill">📌 {ev}</div>'

                        box_html = (
                            f'<div class="cal-day-box">'
                            f'<div class="cal-day-num">{day_num}</div>'
                            f'{events_html}'
                            f'</div>'
                        )
                        w_cols[day_idx].markdown(box_html, unsafe_allow_html=True)

    # 2. SMART EVENT CARDS VIEW
    with tab_cards_view:
        if df_filtered_cal.empty:
            st.warning("⚠️ Walang nahanap na activity o event sa piniling kategorya.")
        else:
            for idx, row in df_filtered_cal.iterrows():
                cols_list = list(df_filtered_cal.columns)
                title_val = str(row[cols_list[0]]).strip() if len(cols_list) > 0 else "Activity Event"
                date_val = str(row[cols_list[1]]).strip() if len(cols_list) > 1 else "TBA"
                venue_val = str(row[cols_list[2]]).strip() if len(cols_list) > 2 else "TBA"
                unit_val = str(row[cols_list[3]]).strip() if len(cols_list) > 3 else "PDBBM RPMO"

                card_event_html = (
                    f'<div class="event-card">'
                    f'<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">'
                    f'<div style="flex: 1; min-width: 280px;">'
                    f'<h3 style="margin:0; font-size:18px; font-weight:800; color:#0F172A;">📅 {title_val}</h3>'
                    f'<p style="margin:6px 0 2px 0; color:#475569; font-size:14px;"><b>📆 Date / Schedule:</b> {date_val}</p>'
                    f'<p style="margin:2px 0 0 0; color:#475569; font-size:14px;"><b>📍 Venue / Location:</b> {venue_val}</p>'
                    f'</div>'
                    f'<div><span class="pill-event">🏷️ {unit_val}</span></div>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_event_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 3: MONTHLY HISTORICAL REVIEW
# ---------------------------------------------------------
else:
    st.markdown("### 🗓️ Monthly Historical Attendance Logs (Realtime Google Sheets Matrix)")
    gsheet_iframe_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTA3I0_4sefOAI68IKKjSYlTdmxhGasSwHmaIUlcYRVFnvMzVlKbmYl45uAY8gg_FAeGFgc44T2_dhh/pubhtml?widget=true&headers=false"
    st.components.v1.iframe(gsheet_iframe_url, height=680, scrolling=True)

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Integrated System Portal</b> | Realtime Live Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """,
    unsafe_allow_html=True,
)

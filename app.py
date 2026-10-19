from datetime import datetime
import json
import os
import re
import pandas as pd
import requests
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI WITH BUBBLE EFFECTS
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Executive Attendance Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-End Styling & Interactive Hover Cursor / Bubble Effects
st.markdown(
    """
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

    /* Metric Cards Bubble Hover Effect */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 16px !important;
        padding: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        cursor: pointer !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02) !important;
        border-color: #E11D48 !important;
        box-shadow: 0 0 18px rgba(225, 29, 72, 0.5), 0 0 28px rgba(225, 29, 72, 0.25) !important;
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

    div.stButton > button, 
    div.stFormSubmitButton > button,
    .stSidebar div.stButton > button {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 10px 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    div.stButton > button:hover, 
    div.stFormSubmitButton > button:hover,
    .stSidebar div.stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #E11D48 !important;
        border-color: #E11D48 !important;
        box-shadow: 0 0 15px rgba(225, 29, 72, 0.6), 0 0 25px rgba(225, 29, 72, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }

    /* Today Staff Cards Hover & Bubble Effects */
    .today-card {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    .today-card:hover {
        transform: translateY(-3px) scale(1.008) !important;
        box-shadow: 0 0 18px rgba(2, 132, 199, 0.35) !important;
        border-left-width: 8px !important;
    }
    
    .today-card-absent {
        background: #FFF1F2;
        padding: 18px 22px;
        border-radius: 14px;
        border-left: 6px solid #E11D48;
        box-shadow: 0 4px 12px rgba(225,29,72,0.05);
        margin-bottom: 12px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    .today-card-absent:hover {
        transform: translateY(-3px) scale(1.008) !important;
        box-shadow: 0 0 18px rgba(225, 29, 72, 0.4) !important;
        border-left-width: 8px !important;
    }

    /* Interactive Name Glow Bubble Style */
    .staff-name-bubble {
        color: #0F172A;
        font-size: 18px;
        font-weight: 800;
        display: inline-block;
        transition: all 0.2s ease-in-out;
        padding: 2px 6px;
        border-radius: 6px;
    }
    .staff-name-bubble:hover {
        color: #0284C7;
        background: #E0F2FE;
        transform: scale(1.03);
    }

    .note-purpose-box {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 4px solid #0284C7;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        font-size: 13px;
        color: #0369A1;
        line-height: 1.5;
        word-wrap: break-word;
    }

    .pill-onsite { background-color: #DCFCE7; color: #15803D; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #BBF7D0; font-size: 13px; }
    .pill-travel { background-color: #FEF3C7; color: #B45309; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FDE68A; font-size: 13px; }
    .pill-absent { background-color: #FFE4E6; color: #BE123C; font-weight: 800; padding: 6px 16px; border-radius: 20px; border: 1px solid #FECDD3; font-size: 13px; }

    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #E2E8F0 0%, #F1F5F9 100%) !important; 
        border-right: 1px solid #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] * { 
        color: #0F172A !important; 
    }

    .sidebar-logo-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# DIRECT LIVE JSON GVIZ PARSER
# ---------------------------------------------------------
SPREADSHEET_ID = "10meIVpLZZV62chi0C4B7i_CVHYkucEX6GkO1LG1AgKQ"
GVIZ_JSON_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:json&sheet=OCTOBER%202026"


def normalize_string(s):
  return re.sub(r"[^a-zA-Z0-9]", "", str(s)).lower()


@st.cache_data(ttl=0)
def fetch_live_matrix_data():
  try:
    ts = int(datetime.now().timestamp())
    res = requests.get(f"{GVIZ_JSON_URL}&_nocache={ts}", timeout=8)
    if res.status_code == 200:
      match = re.search(
          r"google\.visualization\.Query\.setResponse\((.*)\);", res.text
      )
      if match:
        data = json.loads(match.group(1))
        rows = data["table"]["rows"]
        parsed_table = []
        for row in rows:
          row_cells = []
          for cell in row.get("c", []):
            val = ""
            formatted_val = ""
            if cell:
              val = str(cell.get("v", "") or "")
              formatted_val = str(cell.get("f", "") or "")
            row_cells.append({"val": val, "formatted": formatted_val})
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

st.sidebar.markdown(
    "<h3 style='margin-top:10px; margin-bottom:2px; color:#0F172A;'>📋"
    " PDBBM-RPMO PORTAL</h3>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<span style='color:#0284C7; font-size:12px; font-weight:800;'>DSWD FIELD"
    " OFFICE X</span>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.title("🎛️ Navigation Portal")

view_mode = st.sidebar.radio(
    "Select View Mode:",
    ["📍 Today's Live Attendance", "🗓️ Monthly Historical Review"],
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🔄 REFRESH DATA NOW", use_container_width=True):
  st.rerun()

st.sidebar.markdown("---")
st.sidebar.success("🔴 **REALTIME LIVE SYNC:** Active")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.8em; color: #475569;">
        💻 <b>System Developer & Architect</b><br>
        Developed by <br><b style="color:#0284C7;">LOUIE B. IDULSA - PDBBM ITO I</b><br>
        <i>DSWD FO X - PDBBM Attendance Portal © 2026</i>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------------
st.markdown(
    '<div class="glow-header-title">📋 PDBBM-RPMO STAFF DAILY LOGS'
    " TRACKER</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="glow-header-sub">DSWD Field Office X • Executive Decision'
    " Support Portal</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# VIEW 1: TODAY'S LIVE ATTENDANCE LOGS
# ---------------------------------------------------------
if view_mode == "📍 Today's Live Attendance":
  now_dt = datetime.now()
  today_str = now_dt.strftime("%B %d, %Y (%A)")
  day_num = str(now_dt.day)
  month_abbr = now_dt.strftime("%b").lower()

  st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

  raw_matrix = fetch_live_matrix_data()

  today_display_list = []

  # Dynamic Column Index Search for Today's Date
  today_col_idx = None
  if raw_matrix:
    for r_idx in range(min(15, len(raw_matrix))):
      row_vals = [
          str(cell.get("val", "")).strip().lower() for cell in raw_matrix[r_idx]
      ]
      for c_idx, cell in enumerate(row_vals):
        if f"{day_num}-{month_abbr}" in cell or cell == day_num:
          today_col_idx = c_idx
          break
      if today_col_idx is not None:
        break

  # Extract Status and Dynamic Notes per Staff
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
            raw_val = str(cell_obj.get("val", "")).strip()
            fmt_val = str(cell_obj.get("formatted", "")).strip()
            
            combined_text = f"{raw_val} {fmt_val}".strip()
            val_upper = combined_text.upper()

            if (
                "ABSENT" in val_upper
                or val_upper == "A"
                or "LEAVE" in val_upper
                or "SL" in val_upper
                or "VL" in val_upper
            ):
              status_found = "❌ ABSENT"
              remarks_found = "ABSENT"
              clean_note = re.sub(r'^(ABSENT|LEAVE|SL|VL|A)\s*[-:]*\s*', '', combined_text, flags=re.IGNORECASE).strip()
              cell_note = clean_note if len(clean_note) > 3 else ""

            elif "TRAVEL" in val_upper or val_upper == "T" or "OB" in val_upper:
              status_found = "🚗 OFFICIAL TRAVEL"
              remarks_found = "Official Travel / Field Work"
              clean_note = re.sub(r'^(TRAVEL|OFFICIAL TRAVEL|T|OB)\s*[-:]*\s*', '', combined_text, flags=re.IGNORECASE).strip()
              cell_note = clean_note if len(clean_note) > 3 else ""

            elif (
                "ONSITE" in val_upper
                or "PRESENT" in val_upper
                or val_upper == "P"
                or "SITE" in val_upper
            ):
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
  cnt_onsite = sum(
      1 for item in today_display_list if "ONSITE" in item["Status"]
  )
  cnt_travel = sum(
      1 for item in today_display_list if "TRAVEL" in item["Status"]
  )
  cnt_absent = sum(
      1 for item in today_display_list if "ABSENT" in item["Status"]
  )

  # 4 Executive Metric Cards
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
  absent_staff = [
      item for item in today_display_list if "ABSENT" in item["Status"]
  ]
  if absent_staff:
    st.error("⚠️ **ABSENT STAFF SUMMARY FOR TODAY (REALTIME GSHEET):**")
    for ab in absent_staff:
      note_str = f" (*Note: {ab['Note']}*)" if ab["Note"] else ""
      st.markdown(
          f"❌ **{ab['Name']}** ({ab['Position']}) — *Status:"
          f" {ab['Remarks']}*{note_str}"
      )
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

  # Filtered List Logic
  filtered_display_list = today_display_list
  if "Onsite" in status_filter:
    filtered_display_list = [
        item for item in today_display_list if "ONSITE" in item["Status"]
    ]
  elif "Travel" in status_filter:
    filtered_display_list = [
        item for item in today_display_list if "TRAVEL" in item["Status"]
    ]
  elif "Absent" in status_filter:
    filtered_display_list = [
        item for item in today_display_list if "ABSENT" in item["Status"]
    ]

  # Render Cards with preserved Bubble / Hover Effects
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

    # Display Note Box if note exists
    note_box = (
        '<div class="note-purpose-box">📌 <b>REMARKS /'
        f' NOTES:</b><br>{log["Note"]}</div>'
        if log["Note"]
        else ""
    )

    card_html = (
        f'<div class="{card_class}"><div style="display: flex;'
        " justify-content: space-between; align-items: flex-start; flex-wrap:"
        ' wrap; gap: 10px;"><div style="flex: 1; min-width: 280px;"><h3'
        ' style="margin:0; font-size:18px; font-weight:800;"><span'
        f' class="staff-name-bubble">👤 {log["Name"]}</span> <span'
        ' style="font-size:13px; color:#64748B;'
        f' font-weight:600;">({log["Position"]})</span></h3><p'
        ' style="margin:6px 0 0 0; color:#475569; font-size:14px;"><b>Current'
        f' Status / Remarks:</b> {log["Remarks"]}</p>{note_box}</div><div><span'
        f' class="{pill_class}">{log["Status"]}</span></div></div></div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW 2: MONTHLY HISTORICAL REVIEW
# ---------------------------------------------------------
else:
  st.markdown(
      "### 🗓️ Monthly Historical Attendance Logs (Realtime Google Sheets"
      " Matrix)"
  )

  gsheet_iframe_url = (
      "https://docs.google.com/spreadsheets/d/e/2PACX-1vTA3I0_4sefOAI68IKKjSYlTdmxhGasSwHmaIUlcYRVFnvMzVlKbmYl45uAY8gg_FAeGFgc44T2_dhh/pubhtml?widget=true&headers=false"
  )

  st.components.v1.iframe(gsheet_iframe_url, height=680, scrolling=True)

# FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Decision Support Portal</b> | Realtime Live Engine<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """,
    unsafe_allow_html=True,
)

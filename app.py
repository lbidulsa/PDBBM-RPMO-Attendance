import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM-RPMO Staff Attendance Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp {
        background: #F1F5F9;
        color: #0F172A;
    }
    .main-title {
        font-size: 36px !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #E11D48, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #64748B;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 25px;
    }
    .today-card {
        background: #FFFFFF;
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 14px !important;
    }
    
    /* CUSTOM STYLING FOR MONTHLY TABS */
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        background-color: #E2E8F0 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 16px !important;
        margin-right: 4px !important;
    }
    button[aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATABASE DATASET (EMBEDDED DIRECTLY)
# ---------------------------------------------------------
staff_list = [
    {"Name": "Atty. Edgar G. Requilme", "Position": "RPMO Regional Coordinator / Legal Focal"},
    {"Name": "LOUIE B. IDULSA", "Position": "PDBBM ITO I"},
    {"Name": "Whilmar Porras", "Position": "RPMO PDO III"},
    {"Name": "Maria Santos", "Position": "RPMO PDO II"},
    {"Name": "Roberto Gomez", "Position": "RPMO AA VI"}
]

# Attendance Dataset mapped to Google Sheet Monthly Tabs (April 2026 - October 2026)
monthly_data = {
    "APRIL 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 17, "TRAVEL": 3, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 19, "TRAVEL": 1, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 12, "TRAVEL": 8, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 18, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 20, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "MAY 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 16, "TRAVEL": 4, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 20, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 11, "TRAVEL": 9, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 19, "TRAVEL": 1, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 20, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "JUNE 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 18, "TRAVEL": 3, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 19, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 13, "TRAVEL": 8, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 20, "TRAVEL": 1, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 21, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "JULY 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 19, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 20, "TRAVEL": 1, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 15, "TRAVEL": 6, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 21, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 21, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "AUGUST 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 17, "TRAVEL": 3, "WFH": 1, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 21, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 12, "TRAVEL": 9, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 18, "TRAVEL": 3, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 21, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "SEPTEMBER 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 18, "TRAVEL": 4, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 20, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 14, "TRAVEL": 8, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 19, "TRAVEL": 3, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 22, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    },
    "OCTOBER 2026": {
        "Atty. Edgar G. Requilme": {"ONSITE": 10, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "LOUIE B. IDULSA": {"ONSITE": 11, "TRAVEL": 1, "WFH": 0, "ABSENT": 0},
        "Whilmar Porras": {"ONSITE": 8, "TRAVEL": 4, "WFH": 0, "ABSENT": 0},
        "Maria Santos": {"ONSITE": 10, "TRAVEL": 2, "WFH": 0, "ABSENT": 0},
        "Roberto Gomez": {"ONSITE": 12, "TRAVEL": 0, "WFH": 0, "ABSENT": 0},
    }
}

# Today's Live Attendance Log
today_logs = [
    {"Name": "Atty. Edgar G. Requilme", "Position": "Regional Coordinator", "Status": "🏢 ONSITE", "TimeIn": "07:48 AM", "Remarks": "In Office - Regional Operations Review"},
    {"Name": "LOUIE B. IDULSA", "Position": "PDBBM ITO I", "Status": "🏢 ONSITE", "TimeIn": "07:55 AM", "Remarks": "In Office - System Architecture & Server Monitoring"},
    {"Name": "Whilmar Porras", "Position": "PDO III", "Status": "🚗 OFFICIAL TRAVEL", "TimeIn": "08:00 AM", "Remarks": "Field Monitoring in Bukidnon"},
    {"Name": "Maria Santos", "Position": "PDO II", "Status": "🏢 ONSITE", "TimeIn": "08:05 AM", "Remarks": "In Office - SCMS Data Encoding"},
    {"Name": "Roberto Gomez", "Position": "AA VI", "Status": "🏢 ONSITE", "TimeIn": "07:50 AM", "Remarks": "In Office - Document Processing"},
]

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown('<div class="main-title">📋 PDBBM-RPMO STAFF DAILY LOGS TRACKER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DSWD Field Office X • Executive Attendance Decision Support System</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: TODAY'S LIVE ATTENDANCE (IN WORDS / CARDS)
# ---------------------------------------------------------
today_str = datetime.now().strftime("%B %d, %Y")
st.markdown(f"### 📍 Attendance Status Today — **{today_str}**")

cnt_onsite = sum(1 for item in today_logs if "ONSITE" in item["Status"])
cnt_travel = sum(1 for item in today_logs if "TRAVEL" in item["Status"])
cnt_wfh = sum(1 for item in today_logs if "WFH" in item["Status"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 TOTAL RPMO STAFF", f"{len(today_logs)} Staff")
c2.metric("🏢 ONSITE TODAY", f"{cnt_onsite} Staff")
c3.metric("🚗 ON OFFICIAL TRAVEL", f"{cnt_travel} Staff")
c4.metric("💻 WFH / REMOTE", f"{cnt_wfh} Staff")

st.markdown("<br>", unsafe_allow_html=True)

# Display Word Cards
for log in today_logs:
    st.markdown(f"""
        <div class="today-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin:0; color:#0F172A; font-size:18px;">👤 {log['Name']} <span style="font-size:13px; color:#64748B; font-weight:normal;">({log['Position']})</span></h3>
                    <p style="margin:4px 0 0 0; color:#475569; font-size:14px;"><b>Time In:</b> {log['TimeIn']} &nbsp;|&nbsp; <b>Activity / Location:</b> {log['Remarks']}</p>
                </div>
                <div>
                    <span style="font-size:16px; font-weight:800; padding:6px 14px; border-radius:20px; background:#F8FAFC; border:1px solid #E2E8F0;">{log['Status']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# SECTION 2: MONTHLY TABS (APRIL 2026 TO OCTOBER 2026)
# ---------------------------------------------------------
st.markdown("### 🗓️ Historical Attendance Logs per Month")

# Dynamic Tabs Generation from April 2026 to October 2026
months_list = ["APRIL 2026", "MAY 2026", "JUNE 2026", "JULY 2026", "AUGUST 2026", "SEPTEMBER 2026", "OCTOBER 2026"]
month_tabs = st.tabs(months_list)

for idx, m_tab in enumerate(month_tabs):
    m_name = months_list[idx]
    with m_tab:
        st.markdown(f"#### 📊 Summary Report — **{m_name}**")
        
        m_dict = monthly_data.get(m_name, {})
        
        col_filter, col_disp = st.columns([1, 2])
        
        with col_filter:
            selected_emp = st.selectbox(
                f"👤 Select Staff Member to View Breakdown ({m_name}):",
                ["All Staff Members"] + list(m_dict.keys()),
                key=f"sb_{m_name}"
            )
            
            if selected_emp == "All Staff Members":
                st.write("**Staff Summary Overview:**")
                for staff_n, stats in m_dict.items():
                    st.markdown(f"""
                        * **{staff_n}**:  
                          🏢 Onsite: **{stats['ONSITE']}** | 🚗 Travel: **{stats['TRAVEL']}** | 💻 WFH: **{stats['WFH']}** | ❌ Absent: **{stats['ABSENT']}**
                    """)
            else:
                s_stats = m_dict[selected_emp]
                st.info(f"**Staff Member:** {selected_emp}\n\n"
                        f"* 🏢 **Onsite Work:** {s_stats['ONSITE']} Days\n"
                        f"* 🚗 **Official Travel:** {s_stats['TRAVEL']} Days\n"
                        f"* 💻 **Work From Home:** {s_stats['WFH']} Days\n"
                        f"* ❌ **Absences:** {s_stats['ABSENT']} Days")
                
        with col_disp:
            if selected_emp != "All Staff Members":
                s_stats = m_dict[selected_emp]
                chart_df = pd.DataFrame({
                    "Work Status": ["Onsite", "Official Travel", "WFH", "Absent"],
                    "Days": [s_stats['ONSITE'], s_stats['TRAVEL'], s_stats['WFH'], s_stats['ABSENT']]
                })
                fig = px.pie(chart_df, names="Work Status", values="Days", title=f"Attendance Distribution ({selected_emp} - {m_name})", hole=0.4)
                fig.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Overall Monthly Breakdown Bar Chart
                summary_rows = []
                for s_name, s_vals in m_dict.items():
                    summary_rows.append({"Staff": s_name, "Onsite": s_vals['ONSITE'], "Travel": s_vals['TRAVEL'], "WFH": s_vals['WFH']})
                df_sum = pd.DataFrame(summary_rows)
                
                fig_bar = px.bar(df_sum, x="Staff", y=["Onsite", "Travel", "WFH"], title=f"Staff Work Mode Distribution ({m_name})", barmode="stack")
                fig_bar.update_layout(height=280, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------------------------------------
# SIDEBAR CONTROLS & FOOTER
# ---------------------------------------------------------
st.sidebar.title("🎛️ Navigation Controls")
st.sidebar.info("💡 **For Atty. Edgar:** Simply click on any Month Tab (April 2026 to October 2026) above to quickly review historical staff attendance logs!")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #94A3B8;">
        ⚙️ <b>PDBBM-RPMO Attendance System</b><br>
        Designed & Developed by <br><b style="color:#38BDF8;">LOUIE B. IDULSA - PDBBM ITO I</b><br>
        <i>DSWD FO X - PDBBM Portal © 2026</i>
    </div>
    """, 
    unsafe_allow_html=True
)
"""
ACM Club Portal (Streamlit)
- Two-page layout: "User Dashboard" and "Project Overview"
- Local CSV persistence for quick prototyping (attendance.csv, projects.csv)
- Minimal custom CSS for a dark sidebar + small typography tweaks
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# ---------- PAGE BOOT + GLOBAL STYLE -----------------------------------------
# Wide page gives us more room for the three dashboard cards
st.set_page_config(page_title="ACM Portal", layout="wide", page_icon="🚀")

# CSS: set a dark sidebar (fixes readability in dark mode) and a few small
# typography tweaks. We keep this lightweight so it doesn't fight Streamlit's theme.
st.markdown("""
<style>
:root {
  --accent: #7bb662;   /* one place to change the green brand color */
  --sidebar-bg: #111827;   /* dark slate background for the sidebar */
  --sidebar-fg: #f8fafc;   /* near-white text in sidebar */
}

/* Sidebar colors (solves the "white text on light bg" issue) */
[data-testid="stSidebar"]{
  background: var(--sidebar-bg) !important;
}
[data-testid="stSidebar"] *{
  color: var(--sidebar-fg) !important;
}

/* Small global spacing/weight tweaks so things feel tighter */
.block-container { padding-top: 1.2rem; }
h1,h2,h3 { margin-bottom:.4rem; }
div[data-testid="stMetricValue"] { font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ---------- FILE PATHS (local persistence) -----------------------------------
# CSV files keep this demo simple; swap for a DB later if needed.
ATT_CSV   = "attendance.csv"
PROJ_CSV  = "projects.csv"

# ---------- HELPERS: ATTENDANCE + PROJECTS -----------------------------------
def load_attendance() -> pd.DataFrame:
    """Return the attendance table; create an empty frame on first run."""
    if os.path.exists(ATT_CSV):
        return pd.read_csv(ATT_CSV)
    return pd.DataFrame(columns=["Name", "Date", "Time"])

def save_attendance(df: pd.DataFrame) -> None:
    """Persist attendance to disk. (Simple, not concurrency-safe.)"""
    df.to_csv(ATT_CSV, index=False)

def load_projects() -> pd.DataFrame:
    """
    Return the projects table; seed with a few rows if the CSV doesn't exist.
    Dates are parsed to datetime so we can sort/filter and then pretty-print.
    """
    if os.path.exists(PROJ_CSV):
        return pd.read_csv(PROJ_CSV, parse_dates=["Start Date","Due Date"])
    # Seed data so the UI isn't empty the first time you open it
    df = pd.DataFrame([
        {"Project":"Member Onboarding", "Owner":"Afaf", "Status":"In Progress",
         "Start Date":pd.to_datetime("2025-08-01"), "Due Date":pd.to_datetime("2025-09-01")},
        {"Project":"Website Refresh", "Owner":"Team Web", "Status":"Planned",
         "Start Date":pd.to_datetime("2025-08-20"), "Due Date":pd.to_datetime("2025-10-05")},
        {"Project":"Hack Night", "Owner":"Events", "Status":"Completed",
         "Start Date":pd.to_datetime("2025-07-10"), "Due Date":pd.to_datetime("2025-07-25")},
    ])
    df.to_csv(PROJ_CSV, index=False)
    return df

def save_projects(df: pd.DataFrame) -> None:
    """Persist projects to disk."""
    df.to_csv(PROJ_CSV, index=False)

# ---------- STATIC SAMPLE DATA (swap w/ real sources later) ------------------
deadlines = pd.DataFrame({
    "Assignment": ["Essay", "Presentation", "Final Report"],
    "Due Date": pd.to_datetime(["2025-08-20", "2025-08-30", "2025-09-10"])
})

upcoming_events = pd.DataFrame({
    "Event": ["Welcome Mixer", "Git Workshop", "LeetCode Night"],
    "When":  pd.to_datetime(["2025-08-22 18:00", "2025-08-27 17:00", "2025-09-03 19:00"]),
    "Where": ["Student Union A", "Lab 301", "Online"]
})

# ---------- SIDEBAR: QUICK STATS + NAV ---------------------------------------
# Using the sidebar keeps the main canvas clean (like your mockup).
with st.sidebar:
    st.markdown("### ⚡ Quick Stats")
    att_df  = load_attendance()
    proj_df = load_projects()

    # Tiny KPI grid using two columns per row
    colA, colB = st.columns(2)
    colA.metric("Members checked-in", f"{att_df['Name'].nunique()}")
    colB.metric("Attendance logs", f"{len(att_df)}")
    colC, colD = st.columns(2)
    colC.metric("Active projects", f"{(proj_df['Status']!='Completed').sum()}")
    colD.metric("Completed", f"{(proj_df['Status']=='Completed').sum()}")

    st.divider()
    st.caption("Navigate:")
    # Radio = simple page routing between the two main views
    page = st.radio("", ["User Dashboard", "Project Overview"], label_visibility="collapsed")

# ---------- HEADER ------------------------------------------------------------
st.title("🚀 ACM Club Portal")

# ============================ PAGE 1: USER DASHBOARD ==========================
if page == "User Dashboard":
    # Asymmetric grid: skinny left (quick links) + wide right (cards)
    left, right = st.columns([1, 3], vertical_alignment="top")

    # LEFT: lightweight quick links / guidance
    with left:
        st.subheader("Quick Links")
        st.markdown("- 📥 [Submit Idea](#)\n- 🧠 [Mentor Hours](#)\n- 🧰 [Resources](#)")
        st.caption("Tip: mark your attendance and check this week's deadlines.")

    # RIGHT: three “cards” in a row. We use `container(border=True)` to mimic cards.
    c1, c2, c3 = right.columns(3)

    # Card 1: Upcoming events
    with c1.container(border=True):
        st.markdown("#### 📆 Upcoming Events")
        st.dataframe(
            upcoming_events.sort_values("When").reset_index(drop=True),
            hide_index=True,
            use_container_width=True
        )

    # Card 2: Attendance (form + collapsible log)
    with c2.container(border=True):
        st.markdown("#### 📝 Attendance")
        name = st.text_input("Your name", key="att_name")
        # Button is inside the card so the form feels self-contained
        if st.button("Mark Attendance", use_container_width=True):
            if name.strip():
                df  = load_attendance()
                now = datetime.now()
                new = {"Name": name.strip(),
                       "Date": str(now.date()),
                       "Time": now.strftime("%H:%M:%S")}
                # concat keeps schema stable and avoids SettingWithCopy warnings
                df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                save_attendance(df)
                st.success(f"{name} marked present at {new['Time']}")
            else:
                st.error("Please enter your name.")
        # Log is tucked away so the card stays compact
        with st.expander("Attendance Log"):
            st.dataframe(load_attendance(), use_container_width=True)

    # Card 3: Deadlines
    with c3.container(border=True):
        st.markdown("#### 📌 Assignment Deadlines")
        st.dataframe(
            deadlines.sort_values("Due Date"),
            hide_index=True,
            use_container_width=True
        )

# ============================ PAGE 2: PROJECT OVERVIEW ========================
else:
    # Big content left (tables), narrow side right (form + chart)
    main, side = st.columns([3, 1], vertical_alignment="top")

    with main:
        # Ongoing projects table
        with st.container(border=True):
            st.markdown("#### 🚧 Ongoing Projects")
            df = load_projects()
            ongoing = df[df["Status"] != "Completed"].sort_values("Due Date")
            if len(ongoing) == 0:
                st.info("No ongoing projects. Add one on the right.")
            else:
                # Convert datetimes to date for cleaner display in the table
                st.dataframe(
                    ongoing.assign(
                        **{
                            "Start Date": ongoing["Start Date"].dt.date,
                            "Due Date": ongoing["Due Date"].dt.date,
                        }
                    ),
                    hide_index=True,
                    use_container_width=True
                )

        # Completed projects table
        with st.container(border=True):
            st.markdown("#### ✅ Completed")
            done = df[df["Status"] == "Completed"].sort_values("Due Date", ascending=False)
            st.dataframe(
                done.assign(
                    **{
                        "Start Date": done["Start Date"].dt.date,
                        "Due Date": done["Due Date"].dt.date,
                    }
                ),
                hide_index=True,
                use_container_width=True
            )

    with side:
        # Right column: project creation form
        with st.container(border=True):
            st.markdown("#### ➕ Add New Project")
            # `st.form` batches inputs so we only write when "Submit" is clicked
            with st.form("add_project", clear_on_submit=True):
                p_name  = st.text_input("Project name")
                p_owner = st.text_input("Owner")
                p_status= st.selectbox("Status", ["Planned", "In Progress", "Blocked", "Completed"])
                col1, col2 = st.columns(2)
                s_date = col1.date_input("Start", value=date.today())
                d_date = col2.date_input("Due", value=date.today())
                submitted = st.form_submit_button("Add Project", use_container_width=True)

                if submitted:
                    if p_name.strip():
                        df = load_projects()
                        new = {
                            "Project": p_name.strip(),
                            "Owner": p_owner.strip() or "Unassigned",
                            "Status": p_status,
                            "Start Date": pd.to_datetime(s_date),
                            "Due Date": pd.to_datetime(d_date),
                        }
                        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                        save_projects(df)
                        st.success("Project added.")
                    else:
                        st.error("Project name is required.")

        # Small status chart (bar) to mimic the “mini analytics” in your mockup
        with st.container(border=True):
            st.markdown("#### 📊 Project Status Summary")
            df = load_projects()
            counts = df["Status"].value_counts().rename_axis("Status").to_frame("Count")
            st.bar_chart(counts)   # Streamlit auto-renders a clean bar chart
            st.caption("Tip: Use the sidebar stats for a quick glance.")

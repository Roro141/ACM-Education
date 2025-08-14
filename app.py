import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="ACM Portal", layout="wide")
st.title("🚀 ACM Club Portal")

# === Attendance Section ===
st.header("📅 Attendance")
name = st.text_input("Enter your name")

if st.button("Mark Attendance"):
    if name.strip():
        # Create or append to attendance.csv
        if os.path.exists("attendance.csv"):
            df = pd.read_csv("attendance.csv")
        else:
            df = pd.DataFrame(columns=["Name", "Date", "Time"])
        
        now = datetime.now()
        new_entry = {"Name": name, "Date": now.date(), "Time": now.strftime("%H:%M:%S")}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv("attendance.csv", index=False)
        
        st.success(f"{name} marked present at {new_entry['Time']}")
    else:
        st.error("Please enter your name.")

# Show attendance log
if os.path.exists("attendance.csv"):
    st.subheader("📜 Attendance Log")
    st.dataframe(pd.read_csv("attendance.csv"))

# === Deadlines Section ===
st.header("📌 Assignment Deadlines")
deadlines = pd.DataFrame({
    "Assignment": ["Essay", "Presentation", "Final Report"],
    "Due Date": ["2025-08-20", "2025-08-30", "2025-09-10"]
})
st.table(deadlines)

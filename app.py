import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
try:
    df = pd.read_csv("login_activity.csv")

    # Normalize column names to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Ensure timestamp is datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

except FileNotFoundError:
    st.error("❌ login-activity.csv not found. Please place it in the same folder as app.py.")
    st.stop()

# Title
st.title("🔐 Login Activity Dashboard")

# --- Metrics ---
total_logins = df.shape[0]
success_count = df[df["login_status"].str.lower() == "success"].shape[0]
fail_count = df[df["login_status"].str.lower() == "failed"].shape[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Total Logins", total_logins)
with col2:
    st.metric("✅ Successful Logins", success_count)
with col3:
    st.metric("❌ Failed Logins", fail_count)

st.markdown("---")

# --- Charts ---
# 1. Success vs Failed logins
status_count = df["login_status"].value_counts().reset_index()
status_count.columns = ["Login Status", "Count"]

fig1 = px.bar(status_count, x="Login Status", y="Count",
              color="Login Status", title="Success vs Failed Logins",
              text="Count")
st.plotly_chart(fig1, use_container_width=True)

# 2. Logins over time
if "timestamp" in df.columns:
    logins_over_time = df.groupby([df["timestamp"].dt.date, "login_status"]).size().reset_index(name="count")
    fig2 = px.line(logins_over_time, x="timestamp", y="count", color="login_status",
                   title="Logins Over Time")
    st.plotly_chart(fig2, use_container_width=True)

# 3. Device breakdown
if "device" in df.columns:
    device_count = df["device"].value_counts().reset_index()
    device_count.columns = ["Device", "Count"]
    fig3 = px.pie(device_count, names="Device", values="Count", title="Device Breakdown")
    st.plotly_chart(fig3, use_container_width=True)

# 4. Location breakdown
if "location" in df.columns:
    location_count = df["location"].value_counts().reset_index()
    location_count.columns = ["Location", "Count"]
    fig4 = px.bar(location_count, x="Location", y="Count",
                  title="Logins by Location", text="Count")
    st.plotly_chart(fig4, use_container_width=True)

# --- Raw Data Preview ---
st.subheader("📄 Raw Data Preview")
st.dataframe(df.head(20))

import streamlit as st
import pandas as pd
import urllib.error

# ✅ Correct CSV File Path (GitHub Raw URL)
CSV_FILE_PATH = "https://raw.githubusercontent.com/johnosHH/pace/main/Pace-People%20-%20Sheet1.csv"

# --- Load Data from CSV ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
            CSV_FILE_PATH,
            encoding="utf-8",  # Handles encoding issues
            on_bad_lines="skip",  # Skips malformed lines
            delimiter=",",  # Ensures correct column separation
            dtype=str,  # Treats everything as text to avoid conversion issues
        )
        return df
    except urllib.error.HTTPError as e:
        st.error(f"❌ Failed to load CSV. HTTP Error: {e.code}")
        return pd.DataFrame()  # Empty DataFrame to prevent app crashes
    except pd.errors.ParserError:
        st.error("❌ CSV parsing failed. Please check the file format.")
        return pd.DataFrame()

df = load_data()

# Ensure expected columns are present
expected_columns = ["First Name", "Last Name", "Email", "Company", "Title", "Research"]
if not all(col in df.columns for col in expected_columns):
    st.error(f"CSV file is missing required columns! Found: {df.columns.tolist()}")
    st.stop()

# --- Streamlit UI ---
st.title("Pace People BD Hub")

# --- Dropdown Filters ---
company_choice = st.selectbox("Filter by Company", ["All"] + sorted(df["Company"].dropna().unique().tolist()))
filtered_df = df if company_choice == "All" else df[df["Company"] == company_choice]

title_choice = st.selectbox("Filter by Title", ["All"] + sorted(filtered_df["Title"].dropna().unique().tolist()))
filtered_df = filtered_df if title_choice == "All" else filtered_df[filtered_df["Title"] == title_choice]

# --- Select Lead ---
name_options = [f"{row['First Name']} {row['Last Name']}" for _, row in filtered_df.iterrows()]
selected_name = st.selectbox("Select Name", name_options) if name_options else None

# --- Get Selected Lead Data ---
selected_record = filtered_df[filtered_df["First Name"] + " " + filtered_df["Last Name"] == selected_name].iloc[0] if selected_name else None

# --- Sidebar: Lead Details ---
with st.sidebar:
    st.subheader("Lead Information")
    if selected_record is not None:
        st.write(f"**Name:** {selected_record['First Name']} {selected_record['Last Name']}")
        st.write(f"**Company:** {selected_record['Company']}")
        st.write(f"**Title:** {selected_record['Title']}")

        # Expandable Research Section
        with st.expander("View Research"):
            st.write(selected_record["Research"])
    else:
        st.write("Select a lead to view details.")

# --- Email Writing ---
st.subheader("Write Email")
if selected_record is not None:
    st.markdown(f"**Recipient:** {selected_record['First Name']} {selected_record['Last Name']} ({selected_record['Email']})")

# ✅ Subject Line Input
subject_line = st.text_input("Email Subject", value="Your Subject Here")

# ✅ Email Body Input
email_body = st.text_area("Email Body", height=200)

# --- Email Preview & Send Button ---
if email_body and selected_record is not None:
    st.markdown("### Email Preview")
    st.markdown(f"**To:** {selected_record['First Name']} {selected_record['Last Name']} ({selected_record['Email']})")
    st.markdown(f"**Subject:** {subject_line}")
    st.markdown(f"**Body:**\n{email_body}")

    # --- Send to Instantly Button (Demo) ---
    if st.button("🚀 Send to Instantly"):
        st.success(f"✅ Demo: Email to {selected_record['Email']} would be sent to Instantly.")

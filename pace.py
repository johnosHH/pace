import streamlit as st
import pandas as pd

# ✅ Load CSV file (Update this path if needed)
CSV_FILE_PATH = "https://github.com/johnosHH/pace/blob/main/Pace-People%20-%20Sheet1.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE_PATH, on_bad_lines='skip')  # Ensures no errors from extra characters
    return df

# --- Load Data from CSV ---
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE_PATH)

    # Clean column names (strip spaces and remove UTF-8 BOM)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\ufeff", "")

    # ✅ Rename columns if needed
    column_mapping = {
        "First Name": "First Name",
        "Last Name": "Last Name",
        "Email Address": "Email",
        "Company": "Company",
        "Title": "Title",
        "Research": "Research"
    }
    df.rename(columns=column_mapping, inplace=True)

    return df

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

# ✅ New Field: Subject Line Input
subject_line = st.text_input("Email Subject", value="Your Subject Here")

# ✅ Email Body Input
email_body = st.text_area("Email Body", height=200)

# --- Email Preview & Send Button ---
if email_body and selected_record is not None:
    st.markdown("### Email Preview")
    st.markdown(f"**To:** {selected_record['First Name']} {selected_record['Last Name']} ({selected_record['Email']})")
    st.markdown(f"**Subject:** {subject_line}")  # Updated to use user input
    st.markdown(f"**Body:**\n{email_body}")

    # --- Send to Instantly Button (Demo) ---
    if st.button("🚀 Send to Instantly"):
        st.success(f"✅ Demo: Email to {selected_record['Email']} would be sent to Instantly.")

import streamlit as st
import pandas as pd

# Title of the app
st.title('CSV Merger')

# Subtitle
st.markdown(
    """
    by [Florian Potier](https://twitter.com/FloPots) - [Intrepid Digital](https://www.intrepidonline.com/)
    """,
    unsafe_allow_html=True
)

# File upload section
uploaded_files = st.file_uploader("Choose CSV files", accept_multiple_files=True, type=['csv'])

if uploaded_files:
    # Create a list of dataframes from uploaded files
    dataframes = [pd.read_csv(file) for file in uploaded_files]
    # Concatenate all dataframes into one
    combined_csv = pd.concat(dataframes, ignore_index=True)
    # Show combined data on the page
    st.write("Here's a preview of the combined CSV:")
    st.dataframe(combined_csv)
    # Download link for the combined CSV
    csv = combined_csv.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Merged CSV", data=csv, file_name="merged.csv", mime='text/csv')

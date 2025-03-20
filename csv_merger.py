import streamlit as st
import pandas as pd

# Custom CSS for styling and external stylesheet
st.markdown(
    """
    <style>
        p,.appview-container,h1,.stHeadingWithActionElements,.stWidgetLabel,.stMarkdown,.st-ae,.st-bd,.st-be,.st-bf,.st-bg,.st-bh,.st-bi,.st-bj,.st-bk,.st-bl,.st-bm,.st-ah,.st-bn,.st-bo,.st-bp,.st-bq,.st-br,.st-bs,.st-bt,.st-bu,.st-ax,.st-ay,.st-az,.st-bv,.st-b1,.st-b2,.st-bc,.st-bw,.st-bx,.st-by{
        color: black !important;
        font-family: "Raleway", Sans-serif;
        }

        .appview-container,h1,.stHeadingWithActionElements,.stWidgetLabel,.stMarkdown,.st-ae,.st-bd,.st-be,.st-bf,.st-bg,.st-bh,.st-bi,.st-bj,.st-bk,.st-bl,.st-bm,.st-ah,.st-bn,.st-bo,.st-bp,.st-bq,.st-br,.st-bs,.st-bt,.st-bu,.st-ax,.st-ay,.st-az,.st-bv,.st-b1,.st-b2,.st-bc,.st-bw,.st-bx,.st-by{
        background-color: white !important;
        }
        
        button{
        background-color: #1098A7 !important;
        border: none;
        outline: none;
        font-family: "Raleway", Sans-serif;
        font-size: 16px;
        font-weight: 500;
        border-radius: 0px 0px 0px 0px;
        }    
    </style>
    """,
    unsafe_allow_html=True
)

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
    dataframes = []
    for file in uploaded_files:
        try:
            df = pd.read_csv(file)  # Auto-detect delimiter
            dataframes.append(df)  # Append without modifying the structure
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
    
    if dataframes:
        # Concatenate all dataframes into one BEFORE adding the source file column
        combined_csv = pd.concat(dataframes, ignore_index=True)

        # Remove duplicates BEFORE adding "Source File"
        combined_csv.drop_duplicates(inplace=True)

        # Now add "Source File" column for reference
        combined_csv["Source File"] = ""

        # Show combined data on the page
        st.write("Here's a preview of the combined CSV:")
        st.dataframe(combined_csv)
        
        # Download link for the combined CSV
        csv = combined_csv.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download Merged CSV", data=csv, file_name="merged.csv", mime='text/csv')


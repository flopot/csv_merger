"""CSV Merger, Streamlit version pushed as close to the gointrepid.com style as Streamlit allows.
Same logic as github.com/flopot/csv_merger. Theme in .streamlit/config.toml; the rest is CSS below. No site menu: logo + link back to the tools page."""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CSV File Merger | Intrepid Digital", layout="centered")

CSS = """
<style>
/* Streamlit chrome: hide the top bar, its menu and the status widget. */
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 900px !important; }

/* Top row: the site logo at the size gointrepid.com uses (63px tall) and a link back to the tools page. */
.id-top { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 28px 0 0; }
.id-top img { height: 63px; width: auto; display: block; }
.id-back { font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  color: #a2ff2c !important; text-decoration: none !important; white-space: nowrap; }
.id-back:hover { color: #95ff0e !important; }
@media (max-width: 640px) { .id-top img { height: 48px; } }

/* Hero */
.id-hero { padding: 56px 0 36px; }
.id-hero h1 { font-size: clamp(36px, 5.5vw, 64px) !important; line-height: 1.08 !important; letter-spacing: -.02em; padding: 0 0 18px !important; }
.id-hero h1 { margin: 0 !important; }
.id-hero p { margin: 4px 0 0 !important; font-size: 18px; line-height: 1.6; color: #bfbaba; max-width: 700px; }
.id-hero p strong { color: #e8eaf0; }

/* Tool card: the outer block gets the site's surface + volt edge. */
.st-key-tool { background: #1e1c1c; border: 1px solid rgba(255,255,255,.08); border-left: 3px solid #a2ff2c; padding: 36px 36px 32px; }

/* Uploader: dashed drop zone, centred. */
[data-testid="stFileUploaderDropzone"] { border: 1.5px dashed rgba(255,255,255,.18) !important; background: rgba(255,255,255,.02) !important; padding: 32px 20px !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: #a2ff2c !important; background: rgba(162,255,44,.05) !important; }
[data-testid="stWidgetLabel"] p { font-family: 'IBM Plex Mono', monospace; font-size: 11px !important; letter-spacing: .14em; text-transform: uppercase; color: #6b6666 !important; }

/* Buttons: volt, dark ink, uppercase, as the site CTAs. */
.stDownloadButton button, [data-testid="stFileUploaderDropzone"] button { border-radius: 2px !important; }
.stDownloadButton button { background: #a2ff2c !important; border: 0 !important; padding: 14px 28px !important; }
.stDownloadButton button:hover { background: #95ff0e !important; }
.stDownloadButton button p { color: #0a0b0f !important; font-weight: 700 !important; font-size: 13px !important; letter-spacing: .04em; text-transform: uppercase; }

/* Metrics as the stat tiles. */
[data-testid="stMetric"] { background: #2a2828; padding: 14px 18px; }
[data-testid="stMetricValue"] { font-family: Outfit, sans-serif; font-weight: 800; }
[data-testid="stMetricLabel"] p { font-family: 'IBM Plex Mono', monospace; font-size: 11px !important; letter-spacing: .12em; text-transform: uppercase; color: #6b6666 !important; }
</style>
"""
st.html(CSS)
st.html("""
<div class="id-top">
  <a href="https://www.gointrepid.com/tools/" target="_blank" rel="noopener"><img src="app/static/logo-white.png" alt="Intrepid Digital"></a>
  <a class="id-back" href="https://www.gointrepid.com/tools/" target="_blank" rel="noopener">&larr; All Tools</a>
</div>
<div class="id-hero">
  <h1>CSV File Merger Tool</h1>
  <p>Combine CSV exports into one file with a <strong>Source File</strong> column, and duplicate rows removed.</p>
</div>
""")

with st.container(key="tool"):
    uploaded_files = st.file_uploader("CSV files", accept_multiple_files=True, type=["csv"])

    if uploaded_files:
        dataframes = []
        for file in uploaded_files:
            try:
                df = pd.read_csv(file)
                df["Source File"] = file.name
                dataframes.append(df)
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")

        if dataframes:
            raw = pd.concat(dataframes, ignore_index=True)
            combined_csv = raw.drop_duplicates()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Files", len(dataframes))
            c2.metric("Rows", f"{len(combined_csv):,}")
            c3.metric("Columns", len(combined_csv.columns))
            c4.metric("Duplicates", f"{len(raw) - len(combined_csv):,}")
            csv = combined_csv.to_csv(index=False).encode("utf-8")
            st.download_button(label="Download Merged CSV", data=csv, file_name="merged.csv", mime="text/csv")
            st.dataframe(combined_csv, hide_index=True)

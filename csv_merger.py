"""CSV Merger, Streamlit version pushed as close to the gointrepid.com style as Streamlit allows.
Same logic as github.com/flopot/csv_merger. Theme in .streamlit/config.toml; the rest is CSS below."""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CSV File Merger | Intrepid Digital", layout="centered")

CSS = """
<style>
/* Streamlit chrome: hide the top bar, its menu and the status widget. */
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 900px !important; }

/* Site nav (static copy: links work, dropdowns and mobile menu do not). */
.id-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 999990; height: 96px; display: flex; align-items: center;
  justify-content: space-between; padding: 0 40px; background: rgba(10,11,15,.92); border-bottom: 1px solid rgba(255,255,255,.06); }
.id-nav img { height: 24px; }
.id-nav ul { display: flex; gap: 36px; list-style: none; margin: 0; }
.id-nav ul a { color: #bfbaba !important; text-decoration: none !important; font-size: 14px; letter-spacing: .06em; text-transform: uppercase; }
.id-nav .cta { background: #a2ff2c; color: #0a0b0f !important; padding: 10px 24px; font-weight: 700; font-size: 13px; letter-spacing: .04em;
  text-transform: uppercase; text-decoration: none !important; border-radius: 2px; }
@media (max-width: 860px) { .id-nav ul { display: none; } .id-nav { padding: 0 20px; height: 72px; } }

/* Hero */
.id-hero { padding: 150px 0 36px; }
.id-eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 500; letter-spacing: .2em; text-transform: uppercase; color: #a2ff2c; margin-bottom: 22px; }
.id-hero h1 { font-size: clamp(36px, 5.5vw, 64px) !important; line-height: 1.08 !important; letter-spacing: -.02em; padding: 0 0 18px !important; }
.id-hero p { font-size: 18px; line-height: 1.6; color: #bfbaba; max-width: 700px; }
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
<nav class="id-nav">
  <a href="https://www.gointrepid.com/"><img src="app/static/logo-white.png" alt="Intrepid Digital"></a>
  <ul><li><a href="https://www.gointrepid.com/our-work/">Our Work</a></li><li><a href="https://www.gointrepid.com/blog/">Blog</a></li>
      <li><a href="https://www.gointrepid.com/about/">About</a></li><li><a href="https://www.gointrepid.com/tools/">Tools</a></li></ul>
  <a class="cta" href="https://www.gointrepid.com/work-with-us/">Work With Us</a>
</nav>
<div class="id-hero">
  <div class="id-eyebrow">Free SEO Tool</div>
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

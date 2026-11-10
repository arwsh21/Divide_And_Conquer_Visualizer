"""
app.py - Streamlit Visualizer for Closest Pair of Points and Karatsuba Multiplication.
Theme: Bougie Blossom #F78CA8 background, white rounded cards, Dolce Pink #FADADD inner panels.

Key Features & Fixes:
1. True white card containers using st.container(border=True) enclosing all controls & views.
2. Sliders styled with Magenta (#E91E63) active track and Dolce Pink (#FADADD) inactive rail.
   All default yellow text selection / value highlights removed.
3. Dataset Selector dropdown and Upload Dataset card share identical dark-slate (#1F242D) theme with crisp white text & icons.
4. Top-right fullscreen icons styled with bright white icon contrast.
5. Closest pair 2D visualizer with small non-overlapping points (s=10), outside legend, and dynamic best-pair tracking.
6. Unified parity across both Closest Pair and Karatsuba cards.
"""

import os
import time
import streamlit as st
import matplotlib.pyplot as plt
import algorithms

# ---------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Divide & Conquer Visualizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------
# CUSTOM CSS THEME
# ---------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* ── Main Page Background ── */
.stApp {
    background-color: #F78CA8 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

header[data-testid="stHeader"] {
    background-color: #F78CA8 !important;
}

/* Base text color: black on light surfaces */
.stApp p, .stApp span, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp div, .stMarkdown {
    color: #000000 !important;
}

/* ── White Rounded Card Containers (Enclosing all widgets & views) ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1.5px solid #272A2A !important;
    padding: 22px 26px !important;
    margin-bottom: 30px !important;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.12) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: #FFFFFF !important;
}

/* ── Inner Panels (Dolce Pink) ── */
.inner-panel {
    background-color: #FADADD !important;
    border-radius: 12px;
    padding: 15px 18px;
    margin-top: 4px;
    margin-bottom: 12px;
    border: 1.5px solid #C8A0A8;
}
.inner-panel * {
    color: #000000 !important;
}

/* ── Formula Code Blocks (Crisp Green Text on Dark Slate) ── */
/* To change the formula code text color, edit the 'color: #00FF66 !important;' below */
code, .formula-code {
    background-color: #1F242D !important;
    color: #00FF66 !important; /* Bright high-contrast green text */
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 4px 10px !important;
    border-radius: 6px !important;
    border: 1.5px solid #2E7D32 !important;
    display: inline-block !important;
    margin: 4px 0 !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
}
code *, .formula-code *,
code sub, .formula-code sub,
code sup, .formula-code sup,
.inner-panel code, .inner-panel .formula-code,
.inner-panel code *, .inner-panel .formula-code * {
    color: #00FF66 !important; /* Ensures sub/sup (i, j, 2m, m) inherit the exact bright green color */
}
sub, sup {
    color: inherit !important;
}

/* ── Step Caption Box ── */
.caption-box {
    background-color: #FADADD !important;
    border-radius: 10px;
    padding: 13px 18px;
    margin-top: 10px;
    margin-bottom: 10px;
    border-left: 6px solid #272A2A;
    border-top: 1px solid #C8A0A8;
    border-right: 1px solid #C8A0A8;
    border-bottom: 1px solid #C8A0A8;
    font-size: 1.0rem;
    font-weight: 500;
    color: #000000 !important;
}

/* ── Green Outlined Result Box ── */
.result-box {
    background-color: #F3F9F3 !important;
    border: 2.5px solid #2E7D32 !important;
    border-radius: 12px;
    padding: 15px 20px;
    margin-top: 14px;
    margin-bottom: 14px;
}
.result-box * {
    color: #000000 !important;
}
.result-box h4 {
    color: #2E7D32 !important;
}

/* ── Buttons ── */
div.stButton > button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1.5px solid #272A2A !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    transition: all 0.15s ease;
}
div.stButton > button:hover {
    background-color: #FADADD !important;
    border-color: #E91E63 !important;
    color: #000000 !important;
}

/* ── Sliders: Magenta Active Track, Solid Light Peach Inactive Rail, No Yellow Highlights ── */
div[data-testid="stSlider"] {
    user-select: none !important;
    -webkit-user-select: none !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"] {
    padding-top: 14px !important;
    padding-bottom: 14px !important;
}
/* Inactive/Unfilled Rail: Solid Light Peach #FCE4E4 with thin dark outline */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background-color: #FCE4E4 !important;
    height: 8px !important;
    border-radius: 5px !important;
    border: 1.5px solid #272A2A !important;
}
/* Active/Filled Track: Magenta #E91E63 */
div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div > div {
    background-color: #E91E63 !important;
    height: 8px !important;
    border-radius: 5px !important;
}
/* Thumb Knob: Magenta with dark border */
div[data-testid="stSlider"] [role="slider"] {
    background-color: #E91E63 !important;
    border: 2px solid #272A2A !important;
    width: 20px !important;
    height: 20px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
}
/* Kill default yellow text highlights on values and ticks */
div[data-testid="stSlider"] *::selection {
    background: transparent !important;
    color: inherit !important;
}
.stApp div[data-testid="stSlider"] div[data-testid="stSliderThumbValue"],
.stApp div[data-testid="stSlider"] div[data-testid="stSliderThumbValue"] * {
    background: transparent !important;
    color: #000000 !important;
    box-shadow: none !important;
    border: none !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
}
/* Always show start/end tick definitions (e.g. Slow, Very Fast, 1, 5) in BOLD without needing to hover */
div[data-testid="stSlider"] [data-testid="stSliderTickBar"],
div[data-testid="stSlider"] [data-testid="stTickBarMin"],
div[data-testid="stSlider"] [data-testid="stTickBarMax"],
div[data-testid="stSlider"] [data-testid="stTickBarTick"],
div[data-testid="stSlider"] div[data-baseweb="slider"] + div,
div[data-testid="stSlider"] div[data-baseweb="slider"] + div * {
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
    color: #000000 !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}
mark {
    background: transparent !important;
    color: inherit !important;
}
::selection {
    background: #FADADD !important;
    color: #000000 !important;
}
::-moz-selection {
    background: #FADADD !important;
    color: #000000 !important;
}

/* ── Dataset Selector & Upload Custom Dataset: Consistent Dark Slate #1F242D Theme ── */
.stApp div[data-testid="stSelectbox"] > div > div {
    background-color: #1F242D !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #3E4654 !important;
}
.stApp div[data-testid="stSelectbox"] div,
.stApp div[data-testid="stSelectbox"] span,
.stApp div[data-testid="stSelectbox"] p {
    color: #FFFFFF !important;
}
.stApp div[data-testid="stSelectbox"] svg {
    fill: #FFFFFF !important;
}

/* Upload Custom Dataset Card: Dark Slate matching dropdown */
.stApp [data-testid="stFileUploader"] {
    background-color: #1F242D !important;
    border-radius: 8px !important;
    border: 1px solid #3E4654 !important;
    padding: 6px !important;
}
.stApp [data-testid="stFileUploader"] section {
    background-color: #1F242D !important;
    border: 1.5px dashed #6B7280 !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
.stApp [data-testid="stFileUploader"] section:hover {
    border-color: #E91E63 !important;
}
.stApp [data-testid="stFileUploader"] span,
.stApp [data-testid="stFileUploader"] p,
.stApp [data-testid="stFileUploader"] div,
.stApp [data-testid="stFileUploader"] small {
    color: #FFFFFF !important;
}
.stApp [data-testid="stFileUploader"] button {
    background-color: #2D3748 !important;
    color: #FFFFFF !important;
    border: 1px solid #4A5568 !important;
    border-radius: 6px !important;
}
.stApp [data-testid="stFileUploader"] button * {
    color: #FFFFFF !important;
}
.stApp [data-testid="stFileUploader"] svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}
.stApp [data-testid="stFileUploader"] small {
    color: #E2E8F0 !important;
}
.stApp [data-testid="stFileUploaderUploadedFiles"] {
    background-color: #1F242D !important;
    border-radius: 6px !important;
}
.stApp [data-testid="stFileUploaderUploadedFiles"] * {
    color: #FFFFFF !important;
}

/* ── Fullscreen & Floating Action Icons (White Icon Design) ── */
/* NOTE: To change the fullscreen button background color to white, change '#1F242D' to '#FFFFFF' below */
.stApp button[title="View fullscreen"],
.stApp button[aria-label="View fullscreen"],
.stApp [data-testid="StyledFullScreenButton"] {
    background-color: #1F242D !important;
    color: #FFFFFF !important;
    border: 1.5px solid #4A5568 !important;
    border-radius: 8px !important;
    opacity: 0.95 !important;
}
/* White fullscreen icon and all its vector path/rect/line elements */
.stApp button[title="View fullscreen"] svg,
.stApp button[aria-label="View fullscreen"] svg,
.stApp [data-testid="StyledFullScreenButton"] svg,
.stApp button[title="View fullscreen"] svg *,
.stApp button[aria-label="View fullscreen"] svg *,
.stApp [data-testid="StyledFullScreenButton"] svg * {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}
.stApp button[title="View fullscreen"]:hover,
.stApp button[aria-label="View fullscreen"]:hover,
.stApp [data-testid="StyledFullScreenButton"]:hover {
    background-color: #E91E63 !important;
    opacity: 1 !important;
}

/* ── "View Full Exact Product" Dropdown & Text Area High Contrast (WCAG Accessible) ── */
.stApp [data-testid="stExpander"] {
    background-color: #1F242D !important;
    border: 1.5px solid #3E4654 !important;
    border-radius: 10px !important;
    margin-top: 12px !important;
    overflow: hidden !important;
}
.stApp [data-testid="stExpander"] summary {
    background-color: #1F242D !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
}
.stApp [data-testid="stExpander"] summary:hover {
    background-color: #2D3748 !important;
}
.stApp [data-testid="stExpander"] summary p,
.stApp [data-testid="stExpander"] summary span,
.stApp [data-testid="stExpander"] summary div {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.0rem !important;
}
.stApp [data-testid="stExpander"] summary svg {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
}
.stApp [data-testid="stExpanderDetails"] {
    background-color: #1F242D !important;
    padding: 12px 14px !important;
}
.stApp [data-testid="stTextArea"] label,
.stApp [data-testid="stTextArea"] label p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}
.stApp [data-testid="stTextArea"] textarea {
    background-color: #12161E !important;
    color: #FFFFFF !important; /* Pure white high-contrast text for exact product */
    border: 1.5px solid #4A5568 !important;
    border-radius: 8px !important;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    line-height: 1.5 !important;
}
.stApp [data-testid="stTextArea"] textarea:focus {
    border-color: #E91E63 !important;
    box-shadow: 0 0 0 2px rgba(233, 30, 99, 0.4) !important;
}

/* ── Color Badge Helpers ── */
.badge {
    border-radius: 6px;
    padding: 3px 10px;
    font-weight: 600;
    display: inline-block;
    margin: 2px 4px;
}
.badge-blue   { background:#A7D8DB; border:1.5px solid #272A2A; color:#000 !important; }
.badge-yellow { background:#FFE08A; border:1.5px solid #272A2A; color:#000 !important; }
.badge-peach  { background:#FFD1B6; border:1.5px solid #272A2A; color:#000 !important; }
.badge-pink   { background:#E91E63; border:1.5px solid #272A2A; color:#fff !important; }
.badge-green  { background:#2E7D32; border:1.5px solid #272A2A; color:#fff !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# CACHED DATA LOADERS
# ---------------------------------------------------------------------
@st.cache_data
def load_closest_pair_dataset(content_or_path, max_depth):
    points = algorithms.parse_closest_pair_file(content_or_path)
    steps = algorithms.compute_closest_pair_steps(points, max_depth=max_depth)
    return points, steps

@st.cache_data
def load_karatsuba_dataset(content_or_path, max_depth):
    x, y = algorithms.parse_integer_mult_file(content_or_path)
    steps, tree = algorithms.compute_karatsuba_steps(x, y, max_depth=max_depth)
    return x, y, steps, tree


# ---------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------------------
for key, val in [
    ('cp_step', 0), ('cp_slider_version', 0), ('cp_playing', False), ('cp_last_file', ''),
    ('k_step',  0), ('k_slider_version', 0),  ('k_playing',  False), ('k_last_file',  ''),
]:
    if key not in st.session_state:
        st.session_state[key] = val


# ---------------------------------------------------------------------
# PAGE HEADER (Directly on Bougie Blossom background, no floating card)
# ---------------------------------------------------------------------
st.markdown("""
<div style="text-align:center; padding: 18px 0 10px 0;">
  <h1 style="color:#000; font-weight:800; font-size:2.2rem; margin-bottom:6px;">
    Divide &amp; Conquer Algorithm Visualizer
  </h1>
  <p style="color:#000; font-size:1.1rem; font-weight:500; margin-bottom:14px;">
    Interactive step-by-step exploration of 2D Closest Pair of Points and Karatsuba Integer Multiplication.
  </p>
  <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin-bottom:4px;">
    <span class="badge badge-blue">Light Blue — Left / High / z2</span>
    <span class="badge badge-yellow">Yellow — Right / Low / z0</span>
    <span class="badge badge-peach">Peach — Merge Strip / Cross z1</span>
    <span class="badge badge-pink">Pink — Comparing / Active Pair</span>
    <span class="badge badge-green">Dark Green — Best Pair / Final Answer</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# HELPER CONTROLS & SCRUBBER (Versioned State Sync)
# ---------------------------------------------------------------------
def render_controls(prefix, total_steps):
    b1, b2, b3, b4, bspeed = st.columns([1, 1, 1, 1, 2.2])
    with b1:
        if st.button("◀ Prev", key=f"{prefix}_btn_prev", use_container_width=True):
            st.session_state[f'{prefix}_playing'] = False
            st.session_state[f'{prefix}_step'] = max(0, st.session_state[f'{prefix}_step'] - 1)
            st.session_state[f'{prefix}_slider_version'] = st.session_state.get(f'{prefix}_slider_version', 0) + 1
            st.rerun()
    with b2:
        if st.session_state[f'{prefix}_playing']:
            if st.button("⏸ Pause", key=f"{prefix}_btn_pause", use_container_width=True):
                st.session_state[f'{prefix}_playing'] = False
                st.rerun()
        else:
            if st.button("▶ Play", key=f"{prefix}_btn_play", use_container_width=True):
                if st.session_state[f'{prefix}_step'] >= total_steps - 1:
                    st.session_state[f'{prefix}_step'] = 0
                    st.session_state[f'{prefix}_slider_version'] = st.session_state.get(f'{prefix}_slider_version', 0) + 1
                st.session_state[f'{prefix}_playing'] = True
                st.rerun()
    with b3:
        if st.button("Next ▶", key=f"{prefix}_btn_next", use_container_width=True):
            st.session_state[f'{prefix}_playing'] = False
            st.session_state[f'{prefix}_step'] = min(total_steps - 1, st.session_state[f'{prefix}_step'] + 1)
            st.session_state[f'{prefix}_slider_version'] = st.session_state.get(f'{prefix}_slider_version', 0) + 1
            st.rerun()
    with b4:
        if st.button("↺ Reset", key=f"{prefix}_btn_reset", use_container_width=True):
            st.session_state[f'{prefix}_playing'] = False
            st.session_state[f'{prefix}_step'] = 0
            st.session_state[f'{prefix}_slider_version'] = st.session_state.get(f'{prefix}_slider_version', 0) + 1
            st.rerun()
    with bspeed:
        st.select_slider(
            "Speed",
            options=["Slow", "Moderate", "Fast", "Very Fast"],
            value="Moderate",
            key=f"{prefix}_speed_select",
            label_visibility="collapsed"
        )


def render_scrubber(prefix, total_steps):
    sc1, sc2 = st.columns([3, 1])
    with sc1:
        cur_step = st.session_state[f'{prefix}_step']
        version = st.session_state.get(f'{prefix}_slider_version', 0)
        val = st.slider(
            f"{prefix} step",
            min_value=1,
            max_value=total_steps,
            value=cur_step + 1,
            key=f"{prefix}_scrubber_{version}",
            label_visibility="collapsed"
        )
        if val - 1 != cur_step:
            st.session_state[f'{prefix}_step'] = val - 1
            st.session_state[f'{prefix}_playing'] = False
            st.rerun()
    with sc2:
        st.markdown(
            f'<div style="text-align:right; font-weight:700; font-size:1rem; padding-top:8px; color:#000;">'
            f'Step {st.session_state[f"{prefix}_step"]+1} of {total_steps}</div>',
            unsafe_allow_html=True
        )


# =====================================================================
# CARD 1 – CLOSEST PAIR OF POINTS (2D)
# Enclosed fully in a white rounded card container
# =====================================================================
with st.container(border=True):

    st.markdown("""
    <h2 style="color:#000; font-weight:700; border-bottom:2px solid #272A2A;
               padding-bottom:8px; margin-top:0;">
      1. Closest Pair of Points (2D Plane)
    </h2>
    """, unsafe_allow_html=True)

    # ── Educational panels ──
    pov1, pov2 = st.columns(2)
    with pov1:
        st.markdown("""
        <div class="inner-panel">
          <h4 style="margin-top:0; font-weight:700;">📖 Algorithm Overview</h4>
          <p style="margin-bottom:6px;">
            <strong>Problem:</strong> Given <em>n</em> points in a 2D plane, find the pair
            with minimum Euclidean distance:<br>
            <code class="formula-code">d = √((x<sub>i</sub> - x<sub>j</sub>)² + (y<sub>i</sub> - y<sub>j</sub>)²)</code>
          </p>
          <p style="margin-bottom:6px;">
            <strong>Brute-Force:</strong> Checks every pair &rarr; <strong>O(n²)</strong> time.
          </p>
          <p style="margin-bottom:0;">
            <strong>Divide &amp; Conquer:</strong> Splits at median x into halves, recurses,
            and tests only points within a 2δ strip &rarr; <strong>O(n log n)</strong>!
          </p>
        </div>
        """, unsafe_allow_html=True)

    with pov2:
        st.markdown("""
        <div class="inner-panel">
          <h4 style="margin-top:0; font-weight:700;">📐 Key Strategy &amp; The Strip Trick</h4>
          <p style="margin-bottom:6px;">
            1. <strong>Sort &amp; Divide:</strong> Pre-sort by X and Y. Divide at median x into
            <span class="badge badge-blue" style="font-size:0.82rem;">Light Blue Left</span> and
            <span class="badge badge-yellow" style="font-size:0.82rem;">Yellow Right</span>.
          </p>
          <p style="margin-bottom:6px;">
            2. <strong>Conquer:</strong> Recursively find δ<sub>L</sub>, δ<sub>R</sub>;
            set δ = min(δ<sub>L</sub>, δ<sub>R</sub>).
          </p>
          <p style="margin-bottom:0;">
            3. <strong>Strip Trick:</strong> Any cross-boundary pair closer than δ lies in a
            <span class="badge badge-peach" style="font-size:0.82rem;">Peach strip</span> of width 2δ.
            Each point checks only the next <strong>7</strong> neighbours by Y.
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 16px 0; border:none; border-top:1px solid #ECC4CC;'>",
                unsafe_allow_html=True)

    # ── Controls inside the card ──
    cf1, cf2, cf3 = st.columns([1.6, 1.6, 1.2])
    cp_folder = "Closest_Pair"
    cp_files = sorted(f for f in os.listdir(cp_folder) if f.endswith(".txt")) \
               if os.path.exists(cp_folder) else []

    with cf1:
        selected_cp = st.selectbox(
            "Select Closest Pair Dataset:",
            cp_files,
            index=0 if cp_files else None,
            key="cp_file_select"
        )
    with cf2:
        uploaded_cp = st.file_uploader(
            "Or Upload Custom Dataset (.txt):",
            type=["txt"],
            key="cp_file_upload"
        )
    with cf3:
        cp_max_depth = st.slider(
            "Max recursion depth shown:",
            min_value=1,
            max_value=5,
            value=3,
            key="cp_depth_slider",
            help="Deeper levels run silently and appear as one collapsed step."
        )

    # ── Determine active source ──
    if uploaded_cp is not None:
        cp_content = uploaded_cp.getvalue().decode("utf-8")
        cp_file_id = f"up_{uploaded_cp.name}_{cp_max_depth}"
    else:
        cp_content = os.path.join(cp_folder, selected_cp) if selected_cp else ""
        cp_file_id = f"dk_{selected_cp}_{cp_max_depth}"

    if st.session_state['cp_last_file'] != cp_file_id:
        st.session_state.update({
            'cp_step': 0,
            'cp_slider_version': st.session_state.get('cp_slider_version', 0) + 1,
            'cp_playing': False,
            'cp_last_file': cp_file_id
        })

    cp_points, cp_steps = (load_closest_pair_dataset(cp_content, cp_max_depth)
                           if cp_content else ([], []))
    total_cp = len(cp_steps)

    if total_cp == 0:
        st.warning("No points found in dataset.")
    else:
        if st.session_state['cp_step'] >= total_cp:
            st.session_state['cp_step'] = total_cp - 1

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        render_controls("cp", total_cp)
        render_scrubber("cp", total_cp)

        # Caption box
        cur_cp = cp_steps[st.session_state['cp_step']]
        st.markdown(
            f'<div class="caption-box"><strong>Step {st.session_state["cp_step"]+1}:'
            f'</strong> {cur_cp.get("caption","")}</div>',
            unsafe_allow_html=True
        )

        # Plot with outside legend and small points
        fig_cp = algorithms.plot_closest_pair_step(cp_points, cur_cp)
        st.pyplot(fig_cp, use_container_width=True)
        plt.close(fig_cp)

        # Result box
        bp = cur_cp.get('best_pair_so_far')
        bd = cur_cp.get('best_dist_so_far')
        if bp is not None and bd is not None and bd < float('inf'):
            lbl = "Final Closest Pair Found" if cur_cp.get('type') == 'final' else "Best Pair So Far"
            st.markdown(f"""
            <div class="result-box">
              <h4 style="margin-top:0; color:#2E7D32; font-weight:800;">{lbl}</h4>
              <p style="margin-bottom:4px;">
                <strong>Point 1:</strong> ({bp[0][0]}, {bp[0][1]})
                &nbsp;&nbsp;&nbsp;
                <strong>Point 2:</strong> ({bp[1][0]}, {bp[1][1]})
              </p>
              <p style="margin-bottom:0; font-size:1.05rem; font-weight:700; color:#2E7D32;">
                Minimum Distance: {bd:.4f}
              </p>
            </div>
            """, unsafe_allow_html=True)


# =====================================================================
# CARD 2 – KARATSUBA INTEGER MULTIPLICATION
# Enclosed fully in a white rounded card container
# =====================================================================
with st.container(border=True):

    st.markdown("""
    <h2 style="color:#000; font-weight:700; border-bottom:2px solid #272A2A;
               padding-bottom:8px; margin-top:0;">
      2. Karatsuba Integer Multiplication
    </h2>
    """, unsafe_allow_html=True)

    # ── Educational panels ──
    kpov1, kpov2 = st.columns(2)
    with kpov1:
        st.markdown("""
        <div class="inner-panel">
          <h4 style="margin-top:0; font-weight:700;">📖 Algorithm Overview</h4>
          <p style="margin-bottom:6px;">
            <strong>Classical Method:</strong> Multiplies every digit pair &rarr; <strong>O(n²)</strong>.
          </p>
          <p style="margin-bottom:6px;">
            <strong>Karatsuba's Insight (1960):</strong> Divide &amp; conquer —
            only <strong>3 recursive multiplications</strong> instead of 4!
          </p>
          <p style="margin-bottom:0;">
            <strong>Complexity:</strong> T(n) = 3T(n/2) + O(n)
            &rarr; <strong>O(n<sup>1.585</sup>)</strong> — significantly faster for large integers.
          </p>
        </div>
        """, unsafe_allow_html=True)

    with kpov2:
        st.markdown("""
        <div class="inner-panel">
          <h4 style="margin-top:0; font-weight:700;">🔑 Key Formula</h4>
          <p style="margin-bottom:6px;">
            Split at m = ⌊n/2⌋:&nbsp;
            x = a·10<sup>m</sup> + b,&nbsp;
            y = c·10<sup>m</sup> + d<br>
            (<span class="badge badge-blue" style="font-size:.82rem;">a, c = High</span>
             &nbsp;
             <span class="badge badge-yellow" style="font-size:.82rem;">b, d = Low</span>)
          </p>
          <p style="margin-bottom:6px;">
            Three sub-products:<br>
            <span class="badge badge-blue" style="font-size:.82rem;">z2 = a × c</span>
            &nbsp;
            <span class="badge badge-yellow" style="font-size:.82rem;">z0 = b × d</span>
            &nbsp;
            <span class="badge badge-peach" style="font-size:.82rem;">z1 = (a + b)(c + d)</span>
          </p>
          <p style="margin-bottom:0;">
            <strong>Cross-term:</strong> ad + bc = z1 − z2 − z0<br>
            <strong>Result:</strong>
            <code class="formula-code">x · y = z2·10<sup>2m</sup> + (z1 − z2 − z0)·10<sup>m</sup> + z0</code>
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:6px 0 16px 0; border:none; border-top:1px solid #ECC4CC;'>",
                unsafe_allow_html=True)

    # ── Controls inside the card ──
    kf1, kf2, kf3 = st.columns([1.6, 1.6, 1.2])
    k_folder = "Integer_Multiplication"
    k_files = sorted(f for f in os.listdir(k_folder) if f.endswith(".txt")) \
              if os.path.exists(k_folder) else []

    with kf1:
        selected_k = st.selectbox(
            "Select Multiplication Dataset:",
            k_files,
            index=0 if k_files else None,
            key="k_file_select"
        )
    with kf2:
        uploaded_k = st.file_uploader(
            "Or Upload Custom Dataset (.txt):",
            type=["txt"],
            key="k_file_upload"
        )
    with kf3:
        k_max_depth = st.slider(
            "Max depth shown:",
            min_value=1,
            max_value=5,
            value=3,
            key="k_depth_slider",
            help="Deeper calls display 'computed recursively → result'."
        )

    # ── Determine active source ──
    if uploaded_k is not None:
        k_content = uploaded_k.getvalue().decode("utf-8")
        k_file_id = f"up_{uploaded_k.name}_{k_max_depth}"
    else:
        k_content = os.path.join(k_folder, selected_k) if selected_k else ""
        k_file_id = f"dk_{selected_k}_{k_max_depth}"

    if st.session_state['k_last_file'] != k_file_id:
        st.session_state.update({
            'k_step': 0,
            'k_slider_version': st.session_state.get('k_slider_version', 0) + 1,
            'k_playing': False,
            'k_last_file': k_file_id
        })

    k_x, k_y, k_steps, _tree = (load_karatsuba_dataset(k_content, k_max_depth)
                                if k_content else (0, 0, [], []))
    total_k = len(k_steps)

    if total_k == 0:
        st.warning("No integers found in dataset.")
    else:
        if st.session_state['k_step'] >= total_k:
            st.session_state['k_step'] = total_k - 1

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        render_controls("k", total_k)
        render_scrubber("k", total_k)

        # Caption box
        cur_k = k_steps[st.session_state['k_step']]
        st.markdown(
            f'<div class="caption-box"><strong>Step {st.session_state["k_step"]+1}:'
            f'</strong> {cur_k.get("caption","")}</div>',
            unsafe_allow_html=True
        )

        # Matplotlib visual diagram for Karatsuba
        fig_k = algorithms.plot_karatsuba_step(cur_k)
        st.pyplot(fig_k, use_container_width=True)
        plt.close(fig_k)

        # Final result box
        if cur_k.get('type') == 'final':
            final_val = cur_k.get('result', 0)
            digits_count = cur_k.get('digits', len(str(final_val)))
            is_verified = cur_k.get('verified', False)
            n_dig = max(len(str(k_x)), len(str(k_y)))
            grade_mults = n_dig ** 2
            k_mults = int(3 ** (algorithms.math.log2(n_dig))) if n_dig > 1 else 1
            speedup = grade_mults / k_mults if k_mults else 1.0
            v_badge = ('<span class="badge badge-green">&#10003; Verified</span>'
                       " — matches Python's native x × y!"
                       if is_verified else "Mismatch detected")

            st.markdown(f"""
            <div class="result-box">
              <h4 style="margin-top:0; color:#2E7D32; font-weight:800;">
                Final Answer: Karatsuba Product Verified!
              </h4>
              <p style="font-size:1rem; margin-bottom:6px;">
                <strong>Total digits:</strong> {digits_count}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <strong>Correctness:</strong> {v_badge}
              </p>
              <div style="background:#FADADD; border:1px solid #C8A0A8;
                          border-radius:8px; padding:12px 16px; margin-top:10px;">
                <strong>Complexity Comparison (n = {n_dig} digits):</strong>
                <ul style="margin:6px 0 0; color:#000;">
                  <li><strong>Grade-School O(n²):</strong>
                      ~{grade_mults:,} single-digit multiplications</li>
                  <li><strong>Karatsuba O(n<sup>1.585</sup>):</strong>
                      3 mults/level ≈ {k_mults:,} recursive multiplications</li>
                  <li><strong>Speedup:</strong> ~{speedup:.1f}× fewer multiplications!</li>
                </ul>
              </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View Full Exact Product"):
                st.text_area("Full product:", value=str(final_val), height=140)


# ---------------------------------------------------------------------
# AUTOPLAY ENGINE
# ---------------------------------------------------------------------
delay_map = {"Slow": 1.1, "Moderate": 0.5, "Fast": 0.2, "Very Fast": 0.05}
needs_rerun = False

if st.session_state.get('cp_playing') and total_cp > 0:
    if st.session_state['cp_step'] < total_cp - 1:
        time.sleep(delay_map.get(st.session_state.get('cp_speed_select', 'Moderate'), 0.5))
        st.session_state['cp_step'] += 1
        st.session_state['cp_slider_version'] = st.session_state.get('cp_slider_version', 0) + 1
        needs_rerun = True
    else:
        st.session_state['cp_playing'] = False
        needs_rerun = True

if st.session_state.get('k_playing') and total_k > 0:
    if st.session_state['k_step'] < total_k - 1:
        time.sleep(delay_map.get(st.session_state.get('k_speed_select', 'Moderate'), 0.5))
        st.session_state['k_step'] += 1
        st.session_state['k_slider_version'] = st.session_state.get('k_slider_version', 0) + 1
        needs_rerun = True
    else:
        st.session_state['k_playing'] = False
        needs_rerun = True

if needs_rerun:
    st.rerun()

# Divide & Conquer Algorithm Visualizer

An interactive Streamlit visualizer demonstrating two fundamental Divide and Conquer algorithms:
1. **2D Closest Pair of Points** ($O(n \log n)$ vs $O(n^2)$)
2. **Karatsuba Integer Multiplication** ($O(n^{1.585})$ vs $O(n^2)$)

---

## Features

- **Interactive Visualizations**:
  - **Closest Pair**: Real-time Euclidean distance checks, median dashed vertical divider, light blue/yellow partitions, peach merge strip ($2\delta$), candidate pair highlights (pink), and dynamic global best pair line (dark green).
  - **Karatsuba Multiplication**: Digit partitioning into high/low halves ($a, c$ and $b, d$), recursive computation of the three sub-products ($z_2, z_0, z_1$), combination formula, native Python product verification ($\checkmark$), and complexity comparison table.
- **Playback Controls**: Step scrubber slider, manual step navigation (`◀ Prev`, `Next ▶`), play/pause with adjustable speed (`Slow` to `Very Fast`), and instant reset.
- **Data Support**: Pre-loaded with 10 sample datasets for both algorithms, plus support for uploading custom `.txt` files.
- **WCAG Accessible UI**: High-contrast dark containers (`#1F242D`), neon green formulas (`#00FF66`), white action icons, and pastel division palettes.

---

## Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DAA_Project.git
   cd DAA_Project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the visualizer**:
   ```bash
   streamlit run app.py
   ```

---

## Deployment on Streamlit Community Cloud

1. Fork or push this repository to your GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select this repository.
4. Set the **Main file path** to `app.py`.
5. Click **Deploy**.

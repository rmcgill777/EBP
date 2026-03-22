import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import pandas as pd

# -------------------------
# STYLING (SAFE & CLEAN)
# -------------------------
st.markdown("""
<style>

/* App background (William & Mary green) */
.stApp {
    background-color: #115740;
}

/* Keep text readable */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #F4F4F4;
}

/* Buttons (Download + Info) */
.stButton button, .stDownloadButton button {
    background-color: #d4af37;
    color: black;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    padding: 0.4em 1em;
}

/* Hover effect */
.stButton button:hover, .stDownloadButton button:hover {
    background-color: #b8962e;
}

/* Subtle section spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* --- SIDEBAR TEXT FIX --- */

st.sidebar.markdown("""
**Instructions**

Enter values from a 2×2 contingency table:

- **TP (True Positives):** Test positive & condition present  
- **FP (False Positives):** Test positive & condition absent  
- **FN (False Negatives):** Test negative & condition present  
- **TN (True Negatives):** Test negative & condition absent  

Values should be raw counts (not percentages).
""")

/* Sidebar background (force contrast) */
section[data-testid="stSidebar"] {
    background-color: #f0f2f6 !important;
}

/* Sidebar labels (TP, FP, FN, TN) */
section[data-testid="stSidebar"] label {
    color: black !important;
    font-weight: 600;
}

/* Sidebar header ("2×2 Contingency Table") */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: black !important;
} 


/* Sidebar numbers inside inputs */
section[data-testid="stSidebar"] input {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SAFE EXPANDER STYLING (WORKING)
# -------------------------
st.markdown("""
<style>

/* Target expander header correctly */
[data-testid="stExpander"] summary {
    background-color: #d4af37 !important;
    color: black !important;
    font-weight: bold;
    padding: 6px 10px;
    border-radius: 6px;
}

/* Hover */
[data-testid="stExpander"] summary:hover {
    background-color: #b8962e !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #f0f2f6 !important;
}

/* Force ALL sidebar text visible */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* Make labels bold */
section[data-testid="stSidebar"] label {
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# 👇 THEN YOUR APP
st.title("EBA Essentials")

st.markdown("### ℹ️ Information")

with st.expander("View definitions and disclaimer"):

    st.markdown("#### Diagnostic Statistics")

    st.markdown("""
- **Sensitivity**: Proportion of true positives correctly identified.
- **Specificity**: Proportion of true negatives correctly identified.
- **PPV (Positive Predictive Value)**: Probability that a positive test reflects the condition.
- **NPV (Negative Predictive Value)**: Probability that a negative test reflects absence of the condition.
    """)

    st.markdown("#### Likelihood Ratios")

    st.markdown("""
- **LR+**: Increase in odds of the condition given a positive test.
- **LR−**: Decrease in odds of the condition given a negative test.
- **log(LR)**: Log-transformed likelihood ratios for interpretive scaling.
- **DOR (Diagnostic Odds Ratio)**: Overall measure of test effectiveness (LR+ / LR−).
    """)

    st.markdown("#### Discrimination")

    st.markdown("""
- **AUC (ROC)**: Area under the empirical ROC curve based on sensitivity and specificity as an approximate model estimate absent a specific threshold.
    """)   
    st.markdown("#### Bayesian Updating")

    st.markdown("""
- **Pre-test Probability**: Estimated likelihood of the condition before testing.
- **Post-test Probability**: Updated probability after applying likelihood ratios.
- **Fagan Nomogram**: Visual representation of Bayesian updating using likelihood ratios.
    """)

    st.markdown("---")

    st.markdown("#### Disclaimer")

    st.markdown("""
This tool is provided for informational and educational purposes only. No warranty is expressed or implied regarding its accuracy or fitness for a particular purpose. Results should be interpreted with professional judgment and in the context of additional clinical information. The user assumes full responsibility for any decisions or interpretations derived from this tool.
<br>

&copy; 2026 Ryan J. McGill, PhD. All rights reserved.
""", unsafe_allow_html=True)

# -------------------------
# INPUTS
# -------------------------
st.sidebar.header("2×2 Contingency Table")
tp = st.sidebar.number_input("TP", 0, 5000, 50)
fp = st.sidebar.number_input("FP", 0, 5000, 10)
fn = st.sidebar.number_input("FN", 0, 5000, 5)
tn = st.sidebar.number_input("TN", 0, 5000, 100)
# --- CONTINGENCY TABLE (HTML - ALWAYS WORKS) ---
st.markdown("<h4 style='color:white;'>Contingency Table</h4>", unsafe_allow_html=True)

st.markdown(f"""
<table style="border-collapse: collapse; width: 100%; background-color: white; color: black;">
    <tr>
        <th style="border:1px solid black; padding:8px;"></th>
        <th style="border:1px solid black; padding:8px;">Condition Positive</th>
        <th style="border:1px solid black; padding:8px;">Condition Negative</th>
    </tr>
    <tr>
        <th style="border:1px solid black; padding:8px;">Test Positive</th>
        <td style="border:1px solid black; padding:8px;">{tp}</td>
        <td style="border:1px solid black; padding:8px;">{fp}</td>
    </tr>
    <tr>
        <th style="border:1px solid black; padding:8px;">Test Negative</th>
        <td style="border:1px solid black; padding:8px;">{fn}</td>
        <td style="border:1px solid black; padding:8px;">{tn}</td>
    </tr>
</table>
""", unsafe_allow_html=True)
# -------------------------
# COMPUTE
# -------------------------
eps = 1e-10

sens = tp/(tp+fn+eps)
spec = tn/(tn+fp+eps)
ppv = tp/(tp+fp+eps)
npv = tn/(tn+fn+eps)

lrp = sens/(1-spec+eps)
lrn = (1-sens+eps)/spec
dor = lrp / lrn

lorp = np.log(lrp+eps)
lorn = np.log(lrn+eps)

auc = (sens + spec)/2
prev = (tp+fn)/(tp+fp+fn+tn+eps)

# -------------------------
# DISPLAY
# -------------------------
st.write("### Diagnostic Stats")
st.write(f"Sensitivity: {sens:.3f}")
st.write(f"Specificity: {spec:.3f}")
st.write(f"PPV: {ppv:.3f}")
st.write(f"NPV: {npv:.3f}")

st.subheader("Likelihood Ratios")
st.write(f"LR+: {lrp:.3f}")
st.write(f"LR-: {lrn:.3f}")
st.write(f"log(LR+): {lorp:.3f}")
st.write(f"log(LR-): {lorn:.3f}")
st.write(f"Diagnostic Odds Ratio (DOR): {dor:.3f}")

# --- INTERPRETATIONS (SIMPLE & STABLE) ---

st.write("### Provisional Odds Interpretations")

# LR+ interpretation
if lrp >= 10:
    st.write("LR+: Large increase in likelihood")
elif lrp >= 5:
    st.write("LR+: Moderate increase in likelihood")
elif lrp >= 2:
    st.write("LR+: Small increase in likelihood")
else:
    st.write("LR+: Minimal change in likelihood")

# LR- interpretation
if lrn <= 0.1:
    st.write("LR-: Large decrease in likelihood")
elif lrn <= 0.2:
    st.write("LR-: Moderate decrease in likelihood")
elif lrn <= 0.5:
    st.write("LR-: Small decrease in likelihood")
else:
    st.write("LR-: Minimal change in likelihood")

# DOR interpretation
if dor >= 10:
    st.write("DOR: Strong diagnostic evidence")
elif dor >= 3:
    st.write("DOR: Moderate diagnostic evidence")
else:
    st.write("DOR: Weak diagnostic evidence")

st.write("### AUC (derived)")
st.write(f"{auc:.3f}")

# -------------------------
# FAGAN NOMOGRAM
# -------------------------
def prob_to_odds(p): return p/(1-p)
def odds_to_prob(o): return o/(1+o)

pre = st.slider("Pre-test probability", 0.01, 0.99, float(prev))
pre_odds = prob_to_odds(pre)

post_pos = odds_to_prob(pre_odds * lrp)
post_neg = odds_to_prob(pre_odds * lrn)

fig, ax = plt.subplots()
ax.plot([0,1],[pre,post_pos])
ax.plot([0,1],[pre,post_neg], linestyle="dashed")
ax.set_title("Fagan Nomogram (simplified)")
st.pyplot(fig)

st.write(f"Post+ : {post_pos:.3f}")
st.write(f"Post- : {post_neg:.3f}")

# -------------------------
# EBA INTERPRETATION (POSTERIOR PROBABILITY)
# -------------------------
st.write("### EBA Interpretation (Posterior Probability)")

# Thresholds (can later make these user-adjustable)
wait_threshold = 0.10
treat_threshold = 0.70

# Interpretation logic
if post_pos < wait_threshold:
    st.success("Low probability (Wait-Rule Out Threshold): Condition likely ruled out. No further assessment needed unless new information emerges.")
    
elif post_pos < treat_threshold:
    st.warning("Intermediate probability (Assessment Zone): Additional assessment is recommended before making a treatment decision.")
    
else:
    st.error("High probability (Treat-Rule In Threshold): Condition likely present. Consider initiating treatment.")

# Optional: show thresholds for transparency
with st.expander("View decision thresholds"):
    st.write(f"Wait-Rule Out Threshold: {wait_threshold:.2f}")
    st.write(f"Treat-Rule In Threshold: {treat_threshold:.2f}")

    st.markdown("---")
    st.caption(
        "Source: Youngstrom, E. A., Choukas-Bradley, S., Calhoun, C. D., & Jensen-Doss, A. (2015). "
        "Clinical guide to the evidence-based assessment approach to diagnosis and treatment. "
        "Cognitive and Behavioral Practice, 22(1), 20–35."
    )

buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    "Download Nomogram",
    buf.getvalue(),
    file_name="nomogram.png",
    mime="image/png"
)

if st.button("EBA Care Package"):
    st.markdown(
        "<meta http-equiv='refresh' content='0; url=https://ericyoungstrom.web.unc.edu/evidence-based-assessment/'>",
        unsafe_allow_html=True
    )

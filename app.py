import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

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
- **AUC (Single Threshold Estimate)**: Approximation based on sensitivity and specificity.
- **AUC (ROC)**: Area under the empirical ROC curve when multiple thresholds are provided.
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
    """)
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

st.write("### AUC (derived)")
st.write(f"{auc:.3f}")

st.subheader("Interpretation")

# -------------------------
# LR+ (Rule-in)
# -------------------------
if lrp > 10:
    st.success("LR+: Strong evidence to rule IN the condition.")
elif lrp > 5:
    st.info("LR+: Moderate evidence to rule IN the condition.")
elif lrp > 2:
    st.warning("LR+: Weak evidence to rule IN the condition.")
else:
    st.error("LR+: Minimal evidence to rule IN the condition.")

# -------------------------
# LR- (Rule-out)
# -------------------------
if lrn < 0.1:
    st.success("LR-: Strong evidence to rule OUT the condition.")
elif lrn < 0.2:
    st.info("LR-: Moderate evidence to rule OUT the condition.")
elif lrn < 0.5:
    st.warning("LR-: Weak evidence to rule OUT the condition.")
else:
    st.error("LR-: Minimal evidence to rule OUT the condition.")

# -------------------------
# DOR (Overall test performance)
# -------------------------
if dor > 100:
    st.success("DOR: Very strong overall test performance.")
elif dor > 20:
    st.info("DOR: Good overall test performance.")
elif dor > 5:
    st.warning("DOR: Moderate test performance.")
else:
    st.error("DOR: Limited discriminative value.")

# -------------------------
# AUC (Discrimination)
# -------------------------
if auc > 0.9:
    st.success("AUC: Excellent discrimination.")
elif auc > 0.8:
    st.info("AUC: Good discrimination.")
elif auc > 0.7:
    st.warning("AUC: Acceptable discrimination.")
else:
    st.error("AUC: Poor discrimination.")

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

buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    "Download Nomogram",
    buf.getvalue(),
    file_name="nomogram.png",
    mime="image/png"
)



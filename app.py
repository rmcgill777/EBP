import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.markdown("""
<style>
h2, h3 {
    border-bottom: 2px solid #d4af37;
    padding-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Target download button specifically */
.stDownloadButton button {
    background-color: #d4af37 !important;  /* W&M gold */
    color: black !important;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    padding: 0.5em 1em;
}

/* Hover effect */
.stDownloadButton button:hover {
    background-color: #b8962e !important;
    color: black !important;
}

/* Make it pop slightly */
.stDownloadButton {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Main app background */
.stApp {
    background-color: #115740;
}

/* Main content container (keeps readability) */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #115740 0%, #0C3B2E 100%);
}

/* Sidebar (optional match) */
[data-testid="stSidebar"] {
    background-color: #0C3B2E;
}

/* Make text readable */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #F4F4F4 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 10px;
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
# FAGAN NOMOGRAM (POLISHED)
# -------------------------
st.subheader("Fagan Nomogram")

def prob_to_odds(p):
    return p / (1 - p)

def odds_to_prob(o):
    return o / (1 + o)

def prob_to_logodds(p):
    return np.log10(prob_to_odds(p))

def logodds_to_prob(lo):
    return odds_to_prob(10 ** lo)

# Pre-test probability slider
pre_prob = st.slider("Pre-test probability", 0.01, 0.99, float(prevalence))

# Convert to log-odds
pre_lo = prob_to_logodds(pre_prob)
lr_pos_log = np.log10(lr_pos)
lr_neg_log = np.log10(lr_neg)

post_lo_pos = pre_lo + lr_pos_log
post_lo_neg = pre_lo + lr_neg_log

post_prob_pos = logodds_to_prob(post_lo_pos)
post_prob_neg = logodds_to_prob(post_lo_neg)

# Create plot
fig2, ax2 = plt.subplots(figsize=(10, 6))

x_pre, x_lr, x_post = 0, 1, 2

# Probability ticks
prob_ticks = np.array([0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 0.9, 0.95, 0.99])
log_ticks = prob_to_logodds(prob_ticks)

# Draw vertical axes
for x in [x_pre, x_lr, x_post]:
    ax2.plot([x, x], [log_ticks.min(), log_ticks.max()])

# Label probability axes
for p, lo in zip(prob_ticks, log_ticks):
    ax2.text(x_pre - 0.05, lo, f"{p:.2f}", ha="right", va="center")
    ax2.text(x_post + 0.05, lo, f"{p:.2f}", ha="left", va="center")

# LR axis ticks
lr_ticks = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10])
lr_log_ticks = np.log10(lr_ticks)

for lr_val, lo in zip(lr_ticks, lr_log_ticks):
    ax2.text(x_lr, lo, f"{lr_val}", ha="center", va="center")

# -------------------------
# LINES (POLISHED COLORS)
# -------------------------

# Positive test (gold)
ax2.plot(
    [x_pre, x_lr, x_post],
    [pre_lo, lr_pos_log, post_lo_pos],
    linewidth=3,
    color="#d4af37",
    label="Positive Result"
)

# Negative test (gray dashed)
ax2.plot(
    [x_pre, x_lr, x_post],
    [pre_lo, lr_neg_log, post_lo_neg],
    linestyle="dashed",
    linewidth=2,
    color="gray",
    label="Negative Result"
)

# Highlight endpoints
ax2.scatter(x_post, post_lo_pos, color="#d4af37", s=60)
ax2.scatter(x_post, post_lo_neg, color="gray", s=50)

# Labels and formatting
ax2.set_xticks([x_pre, x_lr, x_post])
ax2.set_xticklabels(["Pre-test", "LR", "Post-test"])
ax2.set_ylabel("Log Odds")
ax2.set_title("Fagan Nomogram")

ax2.legend()

st.pyplot(fig2)

# -------------------------
# POST-TEST OUTPUTS
# -------------------------
st.write(f"Post-test probability (positive): {post_prob_pos:.3f}")
st.write(f"Post-test probability (negative): {post_prob_neg:.3f}")



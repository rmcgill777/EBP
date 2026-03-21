import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# 👇 DEFINE FIRST
def add_pollock_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f1a17, #1f3d36) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 👇 THEN CALL
add_pollock_background()

# 👇 THEN YOUR APP
st.title("EBA Essentials")

# -------------------------
# INPUTS
# -------------------------
st.sidebar.header("2×2 Contingency Table")
tp = st.sidebar.number_input("TP", 0, 1000, 50)
fp = st.sidebar.number_input("FP", 0, 1000, 10)
fn = st.sidebar.number_input("FN", 0, 1000, 5)
tn = st.sidebar.number_input("TN", 0, 1000, 100)

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

st.write("### Likelihood Ratios")
st.write(f"LR+: {lrp:.3f}")
st.write(f"LR-: {lrn:.3f}")
st.write(f"log(LR+): {lorp:.3f}")
st.write(f"log(LR-): {lorn:.3f}")

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

buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    "Download Nomogram",
    buf.getvalue(),
    file_name="nomogram.png",
    mime="image/png"
)



import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Monopoly vs Competition", layout="wide")
st.title("Monopoly Market Simulation")

# ---------------- Sidebar: Inputs ----------------
st.sidebar.header("Market Settings (Inputs)")
Q_max = st.sidebar.slider("Max Quantity (Demand intercept on Q)", 50, 500, 200, step=10)
P_max = st.sidebar.slider("Max Price (Demand intercept on P)", 50, 500, 120, step=5)
MC = st.sidebar.slider("Marginal Cost (constant)", 0, 300, 40, step=1)

# Optional: probe a quantity just to inspect points on the chart
probe_Q = st.sidebar.slider("Probe a Quantity (for inspection)", 0, Q_max, int(Q_max*0.5), step=1)

# ---------------- Model ----------------
# Linear demand: P(Q) = a - bQ
a = P_max
b = P_max / Q_max if Q_max > 0 else 0.0
demand = lambda q: a - b*q
mr      = lambda q: a - 2*b*q  # MR for linear demand with zero intercept

# Competitive outcome: P = MC  -> a - bQc = MC
Qc = (a - MC) / b if b > 0 else 0.0
Qc = float(np.clip(Qc, 0, Q_max))
Pc = float(MC)

# Monopoly outcome: MR = MC  -> a - 2bQm = MC
Qm = (a - MC) / (2*b) if b > 0 else 0.0
Qm = float(np.clip(Qm, 0, Q_max))
Pm = float(demand(Qm))

# Deadweight loss (triangle): 0.5 * (Pm - Pc) * (Qc - Qm)
DWL = 0.5 * max(Pm - Pc, 0) * max(Qc - Qm, 0)

# ---------------- Chart ----------------
fig, ax = plt.subplots(figsize=(10, 6))
q = np.linspace(0, Q_max, 300)

ax.plot(q, demand(q), label="Demand", linewidth=3)
ax.plot(q, mr(q), label="MR", linestyle="--", linewidth=2)
ax.axhline(MC, label="MC", linewidth=2)

# Fill DWL region (only if Qc > Qm)
if Qc > Qm:
    q_fill = np.linspace(Qm, Qc, 200)
    ax.fill_between(q_fill, demand(q_fill), MC, alpha=0.3, label=f"DWL = ${DWL:,.0f}")

# Points: Monopoly (Qm, Pm) and Competition (Qc, Pc)
ax.scatter([Qm], [Pm], s=100, zorder=5)
ax.scatter([Qc], [Pc], s=100, zorder=5)

# Optional probe point
P_probe = demand(probe_Q)
ax.scatter([probe_Q], [P_probe], s=60, zorder=5)

# Annotations
ax.annotate("Monopoly (Qm, Pm)", (Qm, Pm), xytext=(Qm*0.6, Pm+P_max*0.06),
            arrowprops=dict(arrowstyle="->", lw=1))
ax.annotate("Competition (Qc, Pc)", (Qc, Pc), xytext=(Qc*0.6, Pc+P_max*0.06),
            arrowprops=dict(arrowstyle="->", lw=1))

ax.set_xlabel("Quantity")
ax.set_ylabel("Price")
ax.set_title("Monopoly vs Perfect Competition")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# ---------------- Metrics ----------------
st.subheader("Outcomes (Computed)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Monopoly Quantity Qm", f"{Qm:.2f}")
col2.metric("Monopoly Price Pm", f"${Pm:.2f}")
col3.metric("Competitive Quantity Qc", f"{Qc:.2f}")
col4.metric("Competitive Price Pc", f"${Pc:.2f}")

st.caption("Left sliders are inputs that shape demand and MC. Monopoly outcome is computed where MR = MC. "
           "The probe slider only inspects points on the demand curve; it does not set the monopoly choice.")

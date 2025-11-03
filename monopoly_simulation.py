import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Monopoly vs Competition", layout="wide")
st.title("Monopoly Market Simulation")

st.sidebar.header("Market Settings")
Q_max = st.sidebar.slider("Max Quantity", 50, 200, 100)
P_max = st.sidebar.slider("Max Price", 50, 200, 100)
MC = st.sidebar.slider("Marginal Cost", 10, 50, 20)

b = P_max / Q_max
demand = lambda q: P_max - b * q
mr = lambda q: P_max - 2 * b * q

Q_comp = (P_max - MC) / b
P_comp = MC

st.sidebar.header("Monopolist Decision")
Q_mono = st.sidebar.slider("Choose Quantity", 1, Q_max, Q_max//3)
P_mono = demand(Q_mono)
profit_mono = P_mono * Q_mono - MC * Q_mono

Q_dwl = np.linspace(Q_mono, Q_comp, 50)
P_demand = demand(Q_dwl)
P_mc = np.full_like(Q_dwl, MC)
dwl = np.trapz(P_demand - P_mc, Q_dwl) / 2

fig, ax = plt.subplots(figsize=(10, 6))
q = np.linspace(0, Q_max, 100)
ax.plot(q, demand(q), label="Demand", color="blue", linewidth=3)
ax.plot(q, [mr(qq) for qq in q], label="MR", color="purple", linestyle="--")
ax.axhline(MC, color="red", label="MC", linewidth=2)

ax.scatter([Q_mono], [P_mono], color="black", s=100)
ax.scatter([Q_comp], [P_comp], color="green", s=100)

ax.fill_between(Q_dwl, P_demand, P_mc, color="red", alpha=0.3, label=f"DWL = ${dwl:.0f}")

ax.set_xlabel("Quantity")
ax.set_ylabel("Price")
ax.set_title("Monopoly vs Perfect Competition")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.metric("Monopoly Price", f"${P_mono:.0f}")
    st.metric("Profit", f"${profit_mono:.0f}")
with col2:
    st.metric("Competitive Price", f"${P_comp:.0f}")
    st.metric("Deadweight Loss", f"${dwl:.0f}")
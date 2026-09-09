import streamlit as st
import pickle
import numpy as np
import time
import plotly.graph_objects as go

# -------------------- PAGE SETTINGS --------------------
st.set_page_config(page_title="Bitcoin Dashboard", layout="wide")

# -------------------- UI STYLE --------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc) !important;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2563eb;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border-radius: 10px;
    height: 3em;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# -------------------- LOAD MODEL --------------------
model = pickle.load(open("bitcoin_model.pkl", "rb"))

# -------------------- HEADER --------------------
st.title("💰 Bitcoin Price Prediction Dashboard")
st.caption("Interactive ML-based system for predicting Bitcoin prices")

st.markdown("---")

# -------------------- SAMPLE BUTTON --------------------
if st.button("🔄 Use Sample Market Data"):
    st.session_state.open_p = 45000.0
    st.session_state.high_p = 46000.0
    st.session_state.low_p = 44000.0
    st.session_state.close_p = 45500.0
    st.session_state.volume = 35000.0

# -------------------- INPUT --------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 📥 Enter Market Data")

col1, col2 = st.columns(2)

with col1:
    open_p = st.number_input("📂 Open Price (₹)", min_value=0.0, step=100.0, key="open_p")
    low_p = st.number_input("📉 Low Price (₹)", min_value=0.0, step=100.0, key="low_p")
    volume = st.number_input("📊 Volume", min_value=0.0, step=1000.0, key="volume")

with col2:
    high_p = st.number_input("📈 High Price (₹)", min_value=0.0, step=100.0, key="high_p")
    close_p = st.number_input("🔒 Close Price (₹)", min_value=0.0, step=100.0, key="close_p")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- PREDICT --------------------
if st.button("🚀 Predict"):

    if open_p == 0 or high_p == 0 or low_p == 0 or close_p == 0 or volume == 0:
        st.warning("⚠️ Please enter all values")

    elif high_p < low_p:
        st.error("❌ High must be greater than Low")

    elif close_p < low_p or close_p > high_p:
        st.error("❌ Close must be between Low and High")

    else:
        data = np.array([[open_p, high_p, low_p, close_p, volume]])
        prediction = model.predict(data)[0]

        # TREND
        if prediction > close_p:
            trend = "📈 UPWARD TREND"
            color = "green"
            box_color = "#22c55e"
        else:
            trend = "📉 DOWNWARD TREND"
            color = "red"
            box_color = "#ef4444"

        # -------------------- RESULT --------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("## 💡 Prediction Result")

        placeholder = st.empty()

        for i in range(0, int(prediction), int(prediction/40) + 1):
            placeholder.markdown(f"""
            <div style="
                background:{box_color};
                padding:20px;
                border-radius:12px;
                color:white;
                text-align:center;
                font-size:22px;
                font-weight:bold;">
                💰 Predicted Price: ₹ {i:,.0f}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.01)

        placeholder.markdown(f"""
        <div style="
            background:{box_color};
            padding:20px;
            border-radius:12px;
            color:white;
            text-align:center;
            font-size:22px;
            font-weight:bold;">
            💰 Predicted Price: ₹ {prediction:,.2f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### Trend: :{color}[{trend}]")

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------- GRAPH --------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("## 📊 Price Visualization")

        labels = ["Open", "High", "Low", "Close", "Predicted"]
        values = [open_p, high_p, low_p, close_p, prediction]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=labels,
            y=values,
            mode='lines+markers',
            line=dict(color="#7c3aed", width=3),
            marker=dict(color="black", size=8)
        ))

        fig.update_layout(
            title=dict(
                text="📊 Bitcoin Price Comparison",
                font=dict(size=20, color="black")
            ),

            plot_bgcolor="white",
            paper_bgcolor="white",

            font=dict(color="black"),

            xaxis=dict(
                title=dict(text="Type", font=dict(color="black")),
                tickfont=dict(color="black"),
                showgrid=False
            ),

            yaxis=dict(
                title=dict(text="Price", font=dict(color="black")),
                tickfont=dict(color="black"),
                showgrid=True,
                gridcolor="#e5e7eb"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # -------------------- SUMMARY --------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown("## 📌 Summary Dashboard")

        c1, c2, c3 = st.columns(3)
        c1.metric("📂 Open", f"₹ {open_p:,.0f}")
        c2.metric("📈 High", f"₹ {high_p:,.0f}")
        c3.metric("📉 Low", f"₹ {low_p:,.0f}")

        c4, c5, c6 = st.columns(3)
        c4.metric("🔒 Close", f"₹ {close_p:,.0f}")
        c5.metric("📊 Volume", f"{volume:,.0f}")
        c6.metric("💡 Predicted", f"₹ {prediction:,.0f}")

        st.markdown('</div>', unsafe_allow_html=True)

        st.caption("⚠️ Prediction is based on historical data and may vary due to market volatility.")
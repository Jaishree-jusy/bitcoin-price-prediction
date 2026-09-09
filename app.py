import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Bitcoin Price Prediction",
    page_icon="₿",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    with open("bitcoin_model.pkl", "rb") as file:
        return pickle.load(file)


model = load_model()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("₿ Bitcoin Price Prediction")
st.markdown(
    "### Predict the next Bitcoin closing price using Machine Learning"
)

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.subheader("📊 Enter Bitcoin Market Data")

col1, col2 = st.columns(2)

with col1:
    open_p = st.number_input(
        "Open Price",
        min_value=0.0,
        value=50000.0,
        step=100.0
    )

    high_p = st.number_input(
        "High Price",
        min_value=0.0,
        value=51000.0,
        step=100.0
    )

    low_p = st.number_input(
        "Low Price",
        min_value=0.0,
        value=49000.0,
        step=100.0
    )

with col2:
    close_p = st.number_input(
        "Current Close Price",
        min_value=0.0,
        value=50500.0,
        step=100.0
    )

    volume = st.number_input(
        "Trading Volume",
        min_value=0.0,
        value=1000000.0,
        step=10000.0
    )

st.divider()

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if st.button("🚀 Predict Bitcoin Price", use_container_width=True):

    # Basic validation
    if open_p == 0 or high_p == 0 or low_p == 0 or close_p == 0 or volume == 0:
        st.warning("⚠️ Please enter all values.")

    elif high_p < low_p:
        st.error("❌ High Price must be greater than Low Price.")

    elif close_p < low_p or close_p > high_p:
        st.error("❌ Current Close Price must be between Low Price and High Price.")

    else:

        # --------------------------------------------------
        # MODEL INPUT
        # --------------------------------------------------
        # The trained model expects ONLY these 4 features:
        # Open, High, Low, Volume
        #
        # Close Price is NOT passed to the model.
        # It is only used for comparison/trend display.

        data = np.array([
            [open_p, high_p, low_p, volume]
        ])

        # Make prediction
        prediction = model.predict(data)[0]

        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        st.success("✅ Prediction generated successfully!")

        st.subheader("💰 Predicted Bitcoin Closing Price")

        st.metric(
            label="Predicted Price",
            value=f"${prediction:,.2f}"
        )

        # --------------------------------------------------
        # PRICE COMPARISON
        # --------------------------------------------------

        difference = prediction - close_p

        if difference > 0:
            st.success(
                f"📈 Bitcoin may increase by approximately "
                f"${difference:,.2f}"
            )

        elif difference < 0:
            st.warning(
                f"📉 Bitcoin may decrease by approximately "
                f"${abs(difference):,.2f}"
            )

        else:
            st.info("➡️ Bitcoin price may remain approximately the same.")

        # --------------------------------------------------
        # CHART
        # --------------------------------------------------

        st.subheader("📈 Price Comparison")

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Current Close", "Predicted Close"],
                y=[close_p, prediction],
                text=[
                    f"${close_p:,.2f}",
                    f"${prediction:,.2f}"
                ],
                textposition="auto"
            )
        )

        fig.update_layout(
            title="Current vs Predicted Bitcoin Price",
            xaxis_title="Price Type",
            yaxis_title="Bitcoin Price (USD)",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("🤖 About the Model")

st.write(
    """
    This application uses a Machine Learning model trained on Bitcoin
    market data to predict the next closing price.

    **Features used by the deployed model:**
    - Open Price
    - High Price
    - Low Price
    - Trading Volume

    The Current Close Price is displayed for comparison with the prediction.
    """
)

st.info(
    "⚠️ This prediction is for educational/project purposes and should not "
    "be considered financial advice."
)
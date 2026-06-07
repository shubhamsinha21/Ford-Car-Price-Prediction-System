import streamlit as st
import pandas as pd
import pickle
import os
import gdown

# ==========================
# Load Artifacts
# ==========================

MODEL_FILE = "ford_price_model.pkl"
FILE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID"

if not os.path.exists(MODEL_FILE):
    url = f"https://drive.google.com/uc?id={1zhmJNu0LH-pZXP2ScOCCSb1wLHlm_dZC}"
    gdown.download(url, MODEL_FILE, quiet=False)

model = pickle.load(open(MODEL_FILE, "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

GBP_TO_INR = 115

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Ford Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ==========================
# Header
# ==========================
st.title("🚗 Ford Car Price Predictor")

st.markdown("""
### Machine Learning Powered Vehicle Valuation System

Predict the resale value of Ford vehicles using historical market data.

**Model:** Random Forest Regressor | **R² Score:** 0.921
""")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    [
        "🚗 Predict",
        "📊 Model Insights",
        "ℹ️ About Project"
    ]
)

# ==========================
# Sidebar Inputs
# ==========================
st.sidebar.header("⚙️ Vehicle Configuration")

car_model = st.sidebar.selectbox(
    "Model",
    [
        ' B-MAX',
        ' C-MAX',
        ' EcoSport',
        ' Edge',
        ' Escort',
        ' Fiesta',
        ' Focus',
        ' Fusion',
        ' Galaxy',
        ' Grand C-MAX',
        ' Grand Tourneo Connect',
        ' KA',
        ' Ka+',
        ' Kuga',
        ' Mondeo',
        ' Mustang',
        ' Puma',
        ' Ranger',
        ' S-MAX',
        ' Streetka',
        ' Tourneo Connect',
        ' Tourneo Custom',
        ' Transit Tourneo',
        'Focus'
    ]
)

year = st.sidebar.number_input(
    "Year",
    min_value=1996,
    max_value=2025,
    value=2020
)

transmission = st.sidebar.selectbox(
    "Transmission",
    ["Automatic", "Manual", "Semi-Auto"]
)

mileage = st.sidebar.number_input(
    "Mileage",
    min_value=0,
    max_value=200000,
    value=20000,
    step=1000
)

fuel_type = st.sidebar.selectbox(
    "Fuel Type",
    ["Diesel", "Electric", "Hybrid", "Other", "Petrol"]
)

tax = st.sidebar.number_input(
    "Tax",
    min_value=0,
    max_value=600,
    value=150
)

mpg = st.sidebar.number_input(
    "MPG",
    min_value=20.0,
    max_value=220.0,
    value=58.0,
    step=0.1
)

engine_size = st.sidebar.number_input(
    "Engine Size (L)",
    min_value=0.0,
    max_value=5.0,
    value=1.5,
    step=0.1
)

predict_btn = st.sidebar.button("🔮 Predict Price")

# ==========================
# Model Performance
# ==========================
# ==========================
# TABS
# ==========================

with tab1:

    st.subheader("📊 Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("R² Score", "0.921")
    col2.metric("MAE", "£894")
    col3.metric("RMSE", "£1339")

    st.markdown("---")

    if predict_btn:

        input_data = pd.DataFrame({
            "year": [year],
            "mileage": [mileage],
            "tax": [tax],
            "mpg": [mpg]
        })

        input_data[["year", "mileage", "tax", "mpg"]] = scaler.transform(
            input_data[["year", "mileage", "tax", "mpg"]]
        )

        final_df = pd.DataFrame(
            0,
            index=[0],
            columns=model_columns
        )

        final_df["year"] = input_data["year"]
        final_df["mileage"] = input_data["mileage"]
        final_df["tax"] = input_data["tax"]
        final_df["mpg"] = input_data["mpg"]
        final_df["engineSize"] = engine_size

        model_col = f"model_{car_model}"
        if model_col in final_df.columns:
            final_df[model_col] = 1

        transmission_col = f"transmission_{transmission}"
        if transmission_col in final_df.columns:
            final_df[transmission_col] = 1

        fuel_col = f"fuelType_{fuel_type}"
        if fuel_col in final_df.columns:
            final_df[fuel_col] = 1

        prediction = model.predict(final_df)[0]

        price_inr = prediction * GBP_TO_INR

        st.subheader("💰 Estimated Market Value")

        with st.container(border=True):

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric(
                    "Price (GBP)",
                    f"£{prediction:,.0f}"
                )

            with result_col2:
                st.metric(
                    "Price (INR)",
                    f"₹{price_inr:,.0f}"
                )

        if prediction > 20000:
            st.success(
                "This vehicle falls in the premium value range."
            )
        else:
            st.info(
                "This vehicle falls in the budget-to-mid range."
            )

        st.markdown("---")

        st.subheader("🚘 Vehicle Summary")

        left, right = st.columns(2)

        with left:
            st.write(f"**Model:** {car_model.strip()}")
            st.write(f"**Year:** {year}")
            st.write(f"**Transmission:** {transmission}")
            st.write(f"**Mileage:** {mileage:,}")

        with right:
            st.write(f"**Fuel Type:** {fuel_type}")
            st.write(f"**Tax:** {tax}")
            st.write(f"**MPG:** {mpg}")
            st.write(f"**Engine Size:** {engine_size} L")

        st.markdown("---")

        st.subheader("🏷️ Vehicle Segment")

        if price_inr < 500000:
            st.info("Budget Segment")
        elif price_inr < 1000000:
            st.success("Mid-Range Segment")
        elif price_inr < 2000000:
            st.warning("Premium Segment")
        else:
            st.error("Luxury Segment")

        st.markdown("---")

        st.subheader("📈 Top Factors Influencing Price")

        st.write("1. Year")
        st.write("2. Engine Size")
        st.write("3. Model")
        st.write("4. MPG")
        st.write("5. Mileage")

    else:

        st.info(
            "Configure the vehicle details from the left sidebar and click 'Predict Price'."
        )

# ==========================
# MODEL INSIGHTS TAB
# ==========================

with tab2:

    st.subheader("📊 Model Insights")

    c1, c2, c3 = st.columns(3)

    c1.metric("R² Score", "0.921")
    c2.metric("MAE", "£894")
    c3.metric("RMSE", "£1339")

    feature_data = pd.DataFrame({
        "Feature": [
            "Year",
            "Engine Size",
            "Model",
            "MPG",
            "Mileage"
        ],
        "Importance": [
            0.494826,
            0.234184,
            0.099595,
            0.083124,
            0.072410
        ]
    })

    st.subheader("Feature Importance")

    st.bar_chart(
        feature_data.set_index("Feature")
    )

# ==========================
# ABOUT TAB
# ==========================

with tab3:

    st.subheader("ℹ️ About This Project")

    st.markdown("""
### Dataset
Ford Car Price Prediction Dataset (Kaggle)

### Dataset Size
17,966 Ford Vehicles

### Features Used
- Model
- Year
- Transmission
- Mileage
- Fuel Type
- Tax
- MPG
- Engine Size

### Feature Engineering
- One-Hot Encoding
- Standard Scaling

### Models Compared
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

### Final Model
Random Forest Regressor

### Performance
- R² Score: 0.921
- MAE: £894
- RMSE: £1339

### Deployment
- Streamlit
- Scikit-Learn
- Pandas
    """)

# ==========================
# Footer
# ==========================

st.markdown("---")

st.caption(
    """
Built by Shubham Sinha

Tech Stack:
Python | Streamlit | Pandas | Scikit-Learn | Random Forest
"""
)
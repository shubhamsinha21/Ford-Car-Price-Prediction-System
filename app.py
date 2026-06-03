import streamlit as st
import pandas as pd
import pickle

# ==========================
# Load Artifacts
# ==========================
model = pickle.load(open("ford_price_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
model_columns = pickle.load(open("model_columns.pkl", "rb"))

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Ford Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Ford Car Price Predictor")
st.write("Predict the selling price of a Ford car using Machine Learning")

# ==========================
# User Inputs
# ==========================

car_model = st.selectbox(
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

year = st.number_input(
    "Year",
    min_value=1996,
    max_value=2025,
    value=2020
)

transmission = st.selectbox(
    "Transmission",
    ["Automatic", "Manual", "Semi-Auto"]
)

mileage = st.number_input(
    "Mileage",
    min_value=0,
    max_value=200000,
    value=20000,
    step=1000
)

fuel_type = st.selectbox(
    "Fuel Type",
    ["Diesel", "Electric", "Hybrid", "Other", "Petrol"]
)

tax = st.number_input(
    "Tax",
    min_value=0,
    max_value=600,
    value=150
)

mpg = st.number_input(
    "MPG",
    min_value=20.0,
    max_value=220.0,
    value=58.0,
    step=0.1
)

engine_size = st.number_input(
    "Engine Size",
    min_value=0.0,
    max_value=5.0,
    value=1.5,
    step=0.1
)

# ==========================
# Prediction
# ==========================

if st.button("Predict Price"):

    input_data = pd.DataFrame(
        {
            "year": [year],
            "mileage": [mileage],
            "tax": [tax],
            "mpg": [mpg],
            "engineSize": [engine_size]
        }
    )

    # Scale numeric columns
    input_data[["year", "mileage", "tax", "mpg"]] = scaler.transform(
        input_data[["year", "mileage", "tax", "mpg"]]
    )

    # Create empty dataframe with all model columns
    final_df = pd.DataFrame(
        0,
        index=[0],
        columns=model_columns
    )

    # Fill numeric values
    final_df["year"] = input_data["year"]
    final_df["mileage"] = input_data["mileage"]
    final_df["tax"] = input_data["tax"]
    final_df["mpg"] = input_data["mpg"]
    final_df["engineSize"] = engine_size

    # One-Hot Encoding for model
    model_col = f"model_{car_model}"

    if model_col in final_df.columns:
        final_df[model_col] = 1

    # One-Hot Encoding for transmission
    transmission_col = f"transmission_{transmission}"

    if transmission_col in final_df.columns:
        final_df[transmission_col] = 1

    # One-Hot Encoding for fuel type
    fuel_col = f"fuelType_{fuel_type}"

    if fuel_col in final_df.columns:
        final_df[fuel_col] = 1

    # Predict
    prediction = model.predict(final_df)[0]

    gbp_to_inr = 115

    price_inr = prediction * gbp_to_inr

    st.success(
        f"""
        Estimated Ford Car Price:

        £{prediction:,.2f}

        ₹{price_inr:,.0f}
        """
    )   
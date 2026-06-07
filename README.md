# Ford Car Price Predictor

A Machine Learning-powered web application that predicts the resale value of Ford vehicles using historical vehicle data and a Random Forest Regressor.

## Project Overview

This project analyzes historical Ford car listings and predicts vehicle prices based on:

* Model
* Year
* Transmission
* Mileage
* Fuel Type
* Tax
* MPG
* Engine Size

The application is deployed using Streamlit and provides an interactive interface for estimating vehicle prices.

---

## Dataset

Dataset: Ford Car Price Prediction Dataset

Total Records: 17,966

Features:

* Model
* Year
* Transmission
* Mileage
* Fuel Type
* Tax
* MPG
* Engine Size
* Price (Target Variable)

---

## Machine Learning Pipeline

### Data Preprocessing

* One-Hot Encoding for categorical features
* Standard Scaling for numerical features
* Train-Test Split

### Models Evaluated
```

| Model                   | R² Score |
| ----------------------- | -------- |
| Linear Regression       | 0.84     |
| Decision Tree Regressor | 0.88     |
| Random Forest Regressor | 0.92     |
```

### Final Model

Random Forest Regressor

Performance:

* R² Score: 0.921
* MAE: £894
* RMSE: £1339

---

## Feature Importance

Top factors affecting vehicle price:

1. Year
2. Engine Size
3. Model
4. MPG
5. Mileage

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* Matplotlib
* Streamlit

---

## Project Structure

```
ford-car-price-predictor/

├── app.py

├── ford_price_model.pkl

├── scaler.pkl

├── model_columns.pkl

├── data/

│ └── ford.csv

├── notebooks/

│ └── Ford_Car_Price_Prediction.ipynb

├── requirements.txt

└── README.md
```

---

## Running Locally

```
Install dependencies:

pip install -r requirements.txt

Run Streamlit:

streamlit run app.py
```

---

## Future Improvements

* Batch CSV predictions
* Downloadable prediction reports
* Cloud deployment
* Advanced model experimentation

---

## Author

Shubham Sinha

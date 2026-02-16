import streamlit as st
import pandas as pd
import os
import joblib
import numpy as np

st.set_page_config(page_title="EduPro Forecasting Dashboard", layout="wide")

st.title("📊 EduPro Course Demand & Revenue Dashboard")

# -----------------------------
# SAFE PATH HANDLING
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "data")
model_path = os.path.join(BASE_DIR, "models")

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    courses = pd.read_csv(os.path.join(data_path, "courses.csv"))
    teachers = pd.read_csv(os.path.join(data_path, "teachers.csv"))
    transactions = pd.read_csv(os.path.join(data_path, "transactions.csv"))
except Exception as e:
    st.error(f"Error loading CSV files: {e}")
    st.stop()

# -----------------------------
# AGGREGATE TRANSACTIONS
# -----------------------------
course_summary = transactions.groupby("CourseID").agg(
    Enrollment_Count=("TransactionID", "count"),
    Total_Revenue=("Amount", "sum")
).reset_index()

df = courses.merge(course_summary, on="CourseID", how="left")
df.fillna(0, inplace=True)

st.subheader("📌 Course Performance Overview")
st.dataframe(df)

# -----------------------------
# CATEGORY REVENUE CHART
# -----------------------------
st.subheader("📊 Category-Level Revenue")

category_revenue = df.groupby("CourseCategory")["Total_Revenue"].sum()
st.bar_chart(category_revenue)

# -----------------------------
# LOAD MODELS SAFELY
# -----------------------------
enrollment_model = None
revenue_model = None

try:
    enrollment_model = joblib.load(os.path.join(model_path, "enrollment_model.pkl"))
    revenue_model = joblib.load(os.path.join(model_path, "revenue_model.pkl"))

    le_category = joblib.load(os.path.join(model_path, "le_category.pkl"))
    le_level = joblib.load(os.path.join(model_path, "le_level.pkl"))
    le_type = joblib.load(os.path.join(model_path, "le_type.pkl"))

except Exception as e:
    st.warning("⚠ Models not loaded. Running in demo mode.")

# -----------------------------
# PREDICTION SECTION
# -----------------------------
st.subheader("🔮 Predict Enrollment & Revenue")

price = st.number_input("Course Price", min_value=1000, max_value=10000, value=3000)
duration = st.number_input("Course Duration (days)", min_value=10, max_value=90, value=30)
rating = st.slider("Course Rating", 1.0, 5.0, 4.5)

category_input = st.selectbox("Course Category", courses["CourseCategory"].unique())
level_input = st.selectbox("Course Level", courses["CourseLevel"].unique())
type_input = st.selectbox("Course Type", courses["CourseType"].unique())

# -----------------------------
# IF MODELS AVAILABLE → REAL ML
# -----------------------------
if enrollment_model and revenue_model:

    try:
        category_encoded = le_category.transform([category_input])[0]
        level_encoded = le_level.transform([level_input])[0]
        type_encoded = le_type.transform([type_input])[0]

        input_data = pd.DataFrame([[category_encoded,
                                    type_encoded,
                                    level_encoded,
                                    price,
                                    duration,
                                    rating]],
                                  columns=[
                                      "CourseCategory",
                                      "CourseType",
                                      "CourseLevel",
                                      "CoursePrice",
                                      "CourseDuration",
                                      "CourseRating"
                                  ])

        predicted_enrollment = enrollment_model.predict(input_data)[0]
        predicted_revenue = revenue_model.predict(input_data)[0]

        st.success(f"📈 Predicted Enrollment: {int(predicted_enrollment)}")
        st.success(f"💰 Predicted Revenue: ₹ {int(predicted_revenue)}")

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# -----------------------------
# DEMO MODE (IF MODEL FAILS)
# -----------------------------
else:
    predicted_enrollment = int((5 - rating) * 10 + (10000 - price) / 500)
    predicted_revenue = predicted_enrollment * price

    st.info("Running in Demo Mode (Model not loaded)")
    st.success(f"📈 Estimated Enrollment: {predicted_enrollment}")
    st.success(f"💰 Estimated Revenue: ₹ {predicted_revenue}")

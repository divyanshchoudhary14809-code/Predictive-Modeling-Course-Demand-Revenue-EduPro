# Predictive Modeling for Course Demand and Revenue Forecasting on EduPro

## 📌 Project Overview

This project introduces predictive intelligence into EduPro’s online learning platform.  
The goal is to forecast:

- Course Enrollment Demand
- Course-Level Revenue
- Category-Level Revenue

The system helps stakeholders make data-driven decisions for:
- Launching new courses
- Optimizing pricing strategies
- Instructor onboarding

---

## 📊 Dataset Description

The project uses three datasets:

### 1️⃣ courses.csv
Contains course-level information:
- CourseID
- CourseCategory
- CourseType
- CourseLevel
- CoursePrice
- CourseDuration
- CourseRating

### 2️⃣ teachers.csv
Contains instructor information:
- TeacherID
- Expertise
- YearsOfExperience
- TeacherRating

### 3️⃣ transactions.csv
Contains enrollment transaction data:
- TransactionID
- CourseID
- TransactionDate
- Amount

---

## 🧠 Feature Engineering

Engineered features include:

- Price Bands
- Duration Buckets
- Rating Tiers
- Experience Buckets
- Enrollment Count
- Revenue per Course

---

## 🤖 Models Used

- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

---

## 📈 Evaluation Metrics

- MAE (Mean Absolute Error)
- RMSE (Root Mean Square Error)
- R² Score

---

## 🚀 Streamlit Dashboard Features

- Course Demand Prediction
- Revenue Forecast Visualization
- Category-Level Comparison
- Feature Importance Explorer

---

## ▶️ How to Run the Project

1. Clone repository
2. Install requirements:


3. Run Streamlit:


---

## 📌 Conclusion

This project transforms EduPro’s historical data into forward-looking intelligence, enabling strategic planning and revenue optimization.

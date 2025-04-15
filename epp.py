# app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- Load model and preprocessing tools ---
model = joblib.load("rf_model.pkl")
imputer = joblib.load("imputer_final.pkl")
scaler = joblib.load("scaler_final.pkl")
feature_cols = pd.read_csv("feature_columns.csv", header=None).squeeze().tolist()

# --- Page configuration ---
st.set_page_config(page_title="ART Adherence Predictor", layout="centered")

st.title("💊 ART Adherence Predictor (Kenyan Adolescents)")
st.markdown("Enter patient details below to predict ART adherence.")

# --- Input form ---
with st.form("adherence_form"):
    age = st.slider("Age", 10, 19, step=1)
    cd4 = st.number_input("CD4 Count", min_value=0, max_value=2000, value=500)
    viral_load = st.number_input("Viral Load", min_value=0, max_value=120000, value=1000)
    duration = st.slider("Treatment Duration (months)", 0, 60, value=12)
    awareness = st.selectbox("Awareness of HIV Status", ["Yes", "No"])
    support_awareness = st.selectbox("Support × Awareness Interaction", ["Yes", "No"])
    distance_score = st.number_input("Location-Distance Score", min_value=0.0, max_value=200.0, value=20.0)
    complexity = st.slider("Treatment Complexity Score", 0, 5, value=2)

    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.selectbox("Location", ["Urban", "Rural"])
    side_effects = st.selectbox("Severe Side Effects", ["Yes", "No"])
    age_14_16 = st.selectbox("Is Age 14-16?", ["Yes", "No"])
    age_17_19 = st.selectbox("Is Age 17-19?", ["Yes", "No"])
    suppressed = st.selectbox("Viral Suppression Status", ["Suppressed", "Unsuppressed"])

    submitted = st.form_submit_button("Predict")

# --- Prepare and predict ---
if submitted:
    input_dict = {
        "Age": age,
        "CD4_Count": cd4,
        "Viral_Load": viral_load,
        "Treatment_Duration": duration,
        "Awareness_Status": 1 if awareness == "Yes" else 0,
        "Support_Awareness_Interaction": 1 if support_awareness == "Yes" else 0,
        "Location_Distance_Interaction": distance_score,
        "Treatment_Complexity_Score": complexity,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Location_Urban": 1 if location == "Urban" else 0,
        "Side_Effects_Severe": 1 if side_effects == "Yes" else 0,
        "Age_Group_14-16": 1 if age_14_16 == "Yes" else 0,
        "Age_Group_17-19": 1 if age_17_19 == "Yes" else 0,
        "Viral_Suppression_Status_Unsuppressed": 1 if suppressed == "Unsuppressed" else 0
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Align columns
    input_df = input_df.reindex(columns=feature_cols, fill_value=0)

    # Apply imputation and scaling
    input_imputed = imputer.transform(input_df)
    input_scaled = scaler.transform(input_imputed)

    # Debug print
    st.markdown("### 🔎 DEBUG - Final Input to Model")
    st.write(input_df)


    # Predict
    prediction = model.predict(input_scaled)[0]

    st.markdown("### 🔍 Prediction:")
    if prediction == 0:
        st.error("🔴 Non-Adherent")
    else:
        st.success("🟢 Adherent")

    # --- Clinical Logic Explanation ---
    st.markdown("---")
    st.subheader("🧠 Clinical Insight Summary")

    strengths = []
    weaknesses = []

    if cd4 >= 500:
        strengths.append("Strong immune recovery (CD4 ≥ 500)")
    if viral_load <= 1000:
        strengths.append("Low viral load")
    if awareness == "Yes":
        strengths.append("Patient is aware of their HIV status")
    if support_awareness == "Yes":
        strengths.append("Receives psychosocial support")
    if duration >= 12:
        strengths.append("Has been on treatment for over 1 year")
    if suppressed == "Suppressed":
        strengths.append("Viral load clinically suppressed")
    if location == "Urban":
        strengths.append("Urban residence — better access to care")

    if side_effects == "Yes":
        weaknesses.append("Experiencing severe side effects")
    if distance_score > 50:
        weaknesses.append("Significant travel distance to clinic")
    if complexity >= 4:
        weaknesses.append("On a complex treatment regimen")
    if suppressed == "Unsuppressed":
        weaknesses.append("Viral load not suppressed — risk of treatment failure")
    if awareness == "No":
        weaknesses.append("Patient unaware of HIV status")

    st.markdown("#### ✅ Patient Strengths")
    if strengths:
        for s in strengths:
            st.markdown(f"- {s}")
    else:
        st.markdown("- None identified")

    st.markdown("#### ⚠️ Risk Factors / Weaknesses")
    if weaknesses:
        for w in weaknesses:
            st.markdown(f"- {w}")
    else:
        st.markdown("- None identified")

    st.markdown("#### 💡 Prediction Logic")
    if prediction == 1:
        st.markdown("Model flagged patient as **Adherent**. Clinical indicators (like immune status, awareness, suppression) outweighed the risks.")
    else:
        st.markdown("Model flagged patient as **Non-Adherent**. Several clinical or behavioral risks elevated concern for poor adherence.")

    st.caption("This logic summary is for interpretability purposes and does not replace clinical judgment.")

# app.py

import streamlit as st
import pandas as pd
import joblib

# --- Load model and preprocessing tools ---
model = joblib.load("rf_model.pkl")
imputer = joblib.load("imputer_final.pkl")
scaler = joblib.load("scaler_final.pkl")
feature_cols = pd.read_csv("feature_columns.csv", header=None).squeeze().tolist()

# --- Page Setup ---
st.set_page_config(page_title="ART Adherence Predictor", layout="centered")
st.title("💊 ART Adherence Predictor (Kenyan Adolescents)")
st.markdown("Enter patient details below to predict ART adherence.")

# --- Input Form ---
with st.form("adherence_form"):
    awareness = st.selectbox("Awareness of HIV Status", ["Yes", "No"])
    support_awareness = st.selectbox("Support × Awareness Interaction", ["Yes", "No"])
    peer_support = st.selectbox("Peer Support Present?", ["Yes", "No"])
    cd4 = st.number_input("CD4 Count", min_value=0, max_value=2000, value=500)
    viral_load = st.number_input("Viral Load", min_value=0, max_value=120000, value=1000)
    duration = st.slider("Treatment Duration (months)", 0, 60, value=12)
    complexity = st.slider("Treatment Complexity Score", 0, 5, value=2)
    distance_score = st.number_input("Location-Distance Score", min_value=0.0, max_value=200.0, value=20.0)
    gender = st.selectbox("Gender", ["Male", "Female"])
    location = st.selectbox("Location", ["Urban", "Rural"])
    side_effects = st.selectbox("Severe Side Effects", ["Yes", "No"])
    age_14_16 = st.selectbox("Is Age 14-16?", ["Yes", "No"])
    age_17_19 = st.selectbox("Is Age 17-19?", ["Yes", "No"])
    suppressed = st.selectbox("Viral Suppression Status", ["Suppressed", "Unsuppressed"])

    submitted = st.form_submit_button("Predict")

# --- Predict if Submitted ---
if submitted:
    # --- Format Input ---
    input_dict = {
        "Awareness_Status": 1 if awareness == "Yes" else 0,
        "Support_Awareness_Interaction": 1 if support_awareness == "Yes" else 0,
        "Peer_Support": 1 if peer_support == "Yes" else 0,
        "CD4_Count": cd4,
        "Viral_Load": viral_load,
        "Treatment_Duration": duration,
        "Treatment_Complexity_Score": complexity,
        "Location_Distance_Interaction": distance_score,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Location_Urban": 1 if location == "Urban" else 0,
        "Side_Effects_Severe": 1 if side_effects == "Yes" else 0,
        "Age_Group_14-16": 1 if age_14_16 == "Yes" else 0,
        "Age_Group_17-19": 1 if age_17_19 == "Yes" else 0,
        "Viral_Suppression_Status_Unsuppressed": 1 if suppressed == "Unsuppressed" else 0
    }

    # --- Prepare DataFrame and align column order ---
    input_df = pd.DataFrame([input_dict])
    input_df = input_df.reindex(columns=feature_cols, fill_value=0)

    # --- Preprocessing ---
    input_imputed = imputer.transform(input_df)
    input_scaled = scaler.transform(input_imputed)

    # --- Prediction ---
    prediction = model.predict(input_scaled)[0]

    # --- Display Result ---
    st.markdown("### 🔍 Prediction:")
    if prediction == 0:
        st.error("🔴 Non-Adherent")
    else:
        st.success("🟢 Adherent")

    # --- Clinical Explanation Block ---
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
    st.markdown("- None identified" if not strengths else "\n".join([f"- {s}" for s in strengths]))

    st.markdown("#### ⚠️ Risk Factors / Weaknesses")
    st.markdown("- None identified" if not weaknesses else "\n".join([f"- {w}" for w in weaknesses]))

    st.markdown("#### 💡 Prediction Logic")
    if prediction == 1:
        st.markdown("Model flagged patient as **Adherent**. Clinical indicators (like immune status, awareness, suppression) outweighed the risks.")
    else:
        st.markdown("Model flagged patient as **Non-Adherent**. Several clinical or behavioral risks elevated concern for poor adherence.")

    # --- Conditional Dilemma Explanation ---
    dilemma_triggered = False
    dilemma_note = ""

    if (
        awareness == "No" and 
        viral_load > 80000 and 
        cd4 < 400 and 
        suppressed == "Unsuppressed"
    ):
        dilemma_triggered = True
        dilemma_note = (
            "**🤔 Why was this flagged as Adherent?**\n\n"
            "Although the patient shows high viral load and low CD4 count, being *unaware* of their status suggests they may be **newly diagnosed** or **early in care**. "
            "The model sometimes interprets this as a transitional phase, where non-adherence is not yet evident — like a student who's just enrolled but hasn’t taken the exam yet."
        )

    elif (
        awareness == "Yes" and 
        viral_load > 80000 and 
        suppressed == "Unsuppressed"
    ):
        dilemma_triggered = True
        dilemma_note = (
            "**🤔 Why was this flagged as Non-Adherent?**\n\n"
            "Despite being aware and in a supportive setting, the model treats **high viral load in an aware patient** as a sign of treatment failure. "
            "It’s like a student who's attended classes (aware) but keeps failing — a deeper issue may be present, like lack of follow-through or drug resistance."
        )

    elif (
        cd4 >= 900 and 
        viral_load <= 1000 and 
        all(val == "No" for val in [support_awareness, peer_support]) and 
        distance_score > 100 and 
        suppressed == "Suppressed"
    ):
        dilemma_triggered = True
        dilemma_note = (
            "**🤔 Why was this still flagged as Adherent despite several challenges?**\n\n"
            "The model places **immense weight on CD4 and viral load**, which are clinical gold standards. "
            "Even without social support, strong lab values pull the prediction toward adherence — like a student passing every exam despite never joining a study group."
        )

    if dilemma_triggered:
        st.markdown("---")
        st.subheader("🧠 Advanced Clinical Interpretation")
        st.markdown(dilemma_note)

    st.caption("This summary helps explain prediction and guide follow-up. Final decisions should include clinical judgment.")

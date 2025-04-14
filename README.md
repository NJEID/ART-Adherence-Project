
# 💊 ART Adherence Prediction for Kenyan Adolescents

This project implements a machine learning pipeline to predict ART (Antiretroviral Therapy) adherence among Kenyan adolescents living with HIV. The prediction model is built using a synthetic dataset that reflects real-world clinical, demographic, and psychosocial factors. The ultimate goal is to support targeted interventions and enhance retention in care.

---

## 📌 Project Objectives

### 🎯 General Objective
To develop a predictive model that classifies adolescents as adherent or non-adherent to ART based on key features.

### 📚 Specific Objectives
- Generate a realistic synthetic dataset for ART adherence.
- Conduct Exploratory Data Analysis (EDA) to uncover patterns in adherence.
- Build and evaluate machine learning models with emphasis on recall (non-adherent class).
- Deploy the final model using Streamlit for real-time prediction and interpretability.

---

## 🧠 Key Features Used

- **Awareness_Status** – Whether the patient is aware of their HIV status.
- **Support_Awareness_Interaction** – Interaction between family support and status awareness.
- **Peer_Support**, **Location_Urban**, **Side_Effects_Severe**, etc.
- **CD4 Count**, **Viral Load**, **Treatment Duration**, **Viral Suppression Status** – Clinical indicators.
- **Age Groups** – Categorical representation of age.

---

## 🛠️ Tools & Technologies

- **Python**
- **Jupyter Notebook**
- **Scikit-learn, Seaborn, Matplotlib, Pandas**
- **Streamlit** for deployment
- **Kaggle** for collaboration & analysis

---

## 🚀 Deployment

The Streamlit app provides:
- A user-friendly interface for entering patient data.
- Predictive classification of adherence.
- An interpretability block offering real-time clinical insights.

👉 Access the deployed interface locally via:
```bash
streamlit run app.py

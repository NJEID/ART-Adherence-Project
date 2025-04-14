# 💊 ART Adherence Prediction for Kenyan Adolescents  
*Using Synthetic Data, Clinical Reasoning & Machine Learning*

---

## 📘 Overview

This project is focused on building a predictive model that identifies **ART adherence** levels among **Kenyan adolescents living with HIV**, using a synthesized dataset that simulates real-world demographic, clinical, and behavioral factors.

It combines **clinical insight**, **machine learning**, and **user-centered design** (via Streamlit) to build a tool that’s both data-driven and practical for healthcare decision-makers.

---

## 🎯 Project Objectives

### 🔹 General Objective
To build a data-driven model that predicts ART adherence among Kenyan adolescents using synthetic data, and deploy it via an interpretable Streamlit application.

### 🔸 Specific Objectives
- ✅ Generate a high-quality synthetic dataset based on realistic clinical and behavioral assumptions.
- ✅ Perform Exploratory Data Analysis (EDA) with interpretation-rich visualizations.
- ✅ Preprocess the data including missing values, outlier handling, encoding, and scaling.
- ✅ Train multiple models and select the best-performing classifier.
- ✅ Evaluate feature importance with clinical reasoning.
- ✅ Build a Streamlit app for interactive prediction and post-prediction explanation.

---

## 🧪 Technologies Used

| Tool | Purpose |
|------|---------|
| **Python** | Core data science programming |
| **Pandas / NumPy** | Data manipulation |
| **Matplotlib / Seaborn** | EDA visualizations |
| **Scikit-learn** | Machine learning pipeline |
| **Streamlit** | Web deployment |
| **SMOTE** | Class imbalance handling |
| **MySQL Connector** | Optional backend storage (proposal integration) |

---

## 🗂️ Dataset Summary

| Feature Category | Examples |
|------------------|----------|
| **Demographic** | Age, Gender, Location |
| **Clinical** | CD4 Count, Viral Load, Side Effects |
| **Behavioral** | Peer Support, Awareness of Status |
| **Engineered** | Age Groups, Distance-Location Score, Complexity Score |
| **Target** | Adherence_Status (1 = Adherent, 0 = Non-Adherent) |

The dataset consists of **10,000 records**, with controlled missingness, injected outliers, and engineered risk-based labels. Saved as `art_adherence_data.csv`.

---

## 🔍 EDA & Feature Insights

EDA was conducted through:
- 📊 Histograms, Boxplots, Correlation Heatmaps
- 📌 Chi-square tests for categorical associations
- 🌲 Feature importance using Random Forest

**Top predictors of adherence:**
1. Viral Suppression Status
2. CD4 Count
3. Awareness of HIV Status
4. Support × Awareness Interaction
5. Peer Support

✅ These insights guided final feature selection for model training.

---

## 🤖 Model Training

Final model: **Random Forest Classifier**

- Balanced class weights  
- Trained on scaled + imputed data  
- Achieved strong **recall on non-adherent cases**

The model was saved as `rf_model.pkl` and deployed via Streamlit.

---

## 🌐 Streamlit Web App

The app collects patient inputs and provides:

- 🔮 A prediction of **Adherent / Non-Adherent**
- 📋 A breakdown of **strengths vs. risk factors**
- 💡 An **interpretability block** for dilemma cases

Example use:

> “A 17-year-old urban male with high VL but unaware of his status is flagged as adherent — why?”  
> The app explains this by highlighting early-care logic, low complexity, and suppressed VL.

📌 *Deployed locally or via Streamlit Cloud.*

---

## 🧠 Sample Prediction (via GUI)

```text
Input:
Age: 16
CD4 Count: 900
Viral Load: 450
Treatment Duration: 14 months
Awareness: Yes
Support: Yes
Suppression: Suppressed

🔍 Output:
🟢 Adherent

✅ Strengths:
- Strong immune recovery (CD4 ≥ 500)
- Viral load clinically suppressed
- Receives psychosocial support

⚠️ Weaknesses:
- None identified
ART-Adherence-Project/
│
├── art_adherence_data.csv
├── selected_features.csv
├── rf_model.pkl
├── imputer_final.pkl
├── scaler_final.pkl
├── feature_columns.csv
├── app.py
└── README.md  👈 (this file)


👤 Author
Dancun Ngugi
Final Year Data Science Student
Meru University of Science and Technology



📧 Email: dancunngugi408@gmail.com
🔗 LinkedIn: linkedin.com/in/dancun-ngugi-a87486263
🐙 GitHub: github.com/NJEID
📊 Kaggle: kaggle.com/dancunngugi


🙏 Acknowledgment
This project is part of my final year capstone and is inspired by real-world gaps in adolescent HIV care. Special thanks to my university lecturers and mentors who guided me through this journey.

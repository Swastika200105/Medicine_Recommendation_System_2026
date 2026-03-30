from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# ===============================
# Load ML Components
# ===============================
model = joblib.load("models/disease_prediction_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

description_df = pd.read_csv("datasets/Description_df.csv")
precautions_df = pd.read_csv("datasets/Precaution_df.csv")
workout_df = pd.read_csv("datasets/Workouts_df.csv")
medication_df = pd.read_csv("datasets/Medications_df.csv")
diet_df = pd.read_csv("datasets/Diets_df.csv")
doctor_df = pd.read_csv("datasets/doctors.csv")



# ===============================
# Prediction Function
# ===============================
# def predict_and_recommend(symptom_list):
#
#     # # Create empty input vector
#     feature_columns = joblib.load("models/feature_columns.pkl")
#     input_data = [0] * len(feature_columns)

    # for symptom in symptom_list:
    #     if symptom in feature_columns:
    #     index = feature_columns.get_loc(symptom)
    #     input_data[index] = 1
def predict_and_recommend(symptom_list):

    # ✅ Clean symptoms (VERY IMPORTANT)
    symptom_list = [s.strip().lower() for s in symptom_list]

    # ✅ Use already loaded feature_columns (DO NOT reload)
    input_data = [0] * len(feature_columns)

    matched_symptoms = []

    for symptom in symptom_list:
        if symptom in feature_columns:
            index = feature_columns.get_loc(symptom)
            input_data[index] = 1
            matched_symptoms.append(symptom)

    # ✅ Debug (you can remove later)
    print("User Symptoms:", symptom_list)
    print("Matched Symptoms:", matched_symptoms)


    # Convert to DataFrame
    input_df = pd.DataFrame([input_data], columns=feature_columns)

    # ===============================
    # Model Prediction (CLEAN VERSION)
    # ===============================

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Main predicted disease
    disease = label_encoder.inverse_transform([prediction])[0]
    confidence = float(round(max(probabilities) * 100, 2))

    # ===============================
    # Top 3 Predictions (CORRECT)
    # ===============================

    top3_idx = np.argsort(probabilities)[::-1][:3]

    top3 = []
    for i in top3_idx:
        encoded_label = model.classes_[i]  # Correct mapping
        disease_name = label_encoder.inverse_transform([encoded_label])[0]
        prob = float(round(probabilities[i] * 100, 2))
        top3.append((disease_name, prob))

    # ===============================
    # Description
    # ===============================
    desc_row = description_df[description_df['Disease'] == disease]
    description = "No description available."
    if len(desc_row) > 0:
        description = desc_row['Description'].values[0]
        if description:
            description = description.replace(f"{disease},", "").replace('"', '').strip()

    # ===============================
    # Medication
    # ===============================
    med_row = medication_df[medication_df['Disease'] == disease]
    medication = []
    if len(med_row) > 0:
        med_str = med_row['Medication'].values[0]
        if med_str:
            import ast
            try:
                medication = ast.literal_eval(med_str)
            except:
                medication = [med_str]

    # ===============================
    # Precautions
    # ===============================
    precaution_row = precautions_df[precautions_df['Disease'] == disease]
    precautions = []
    if len(precaution_row) > 0:
        precautions = precaution_row[
            ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
        ].values.flatten().tolist()
        precautions = [p for p in precautions if pd.notna(p)]

    # ===============================
    # Workout
    # ===============================
    workout_details = {}
    workout_row = workout_df[workout_df['Disease'] == disease]
    if len(workout_row) > 0:
        row = workout_row.iloc[0]
        exercises = [row.get(f'Exercise_{i}') for i in range(1, 5)]
        exercises = [e for e in exercises if pd.notna(e)]
        workout_details = {
            "Exercises": exercises,
            "Intensity": row['Intensity'] if pd.notna(row['Intensity']) else "Not specified",
            "Duration": row['Duration'] if pd.notna(row['Duration']) else "Not specified",
            "Frequency": row['Frequency'] if pd.notna(row['Frequency']) else "Not specified",
            "Notes": row['Notes'] if pd.notna(row['Notes']) else "No additional notes"
        }

    # ===============================
    # Diets
    # ===============================
    diet_row = diet_df[diet_df['Disease'] == disease]
    diets = []
    if len(diet_row) > 0:
        diets = [d for d in diet_row.iloc[0][['Diet_1','Diet_2','Diet_3','Diet_4']] if pd.notna(d)]

    # ===============================
    # Doctor / Specialist
    # ===============================
    doctor_row = doctor_df[doctor_df['Disease'] == disease]
    doctor = "General Physician"
    if len(doctor_row) > 0 and 'Specialization' in doctor_row.columns:
        doc_name = doctor_row['Specialization'].values[0]
        if pd.notna(doc_name) and doc_name != "":
            doctor = doc_name

    # ===============================
    # Low Confidence Handling
    # ===============================
    if confidence < 10:
        disease = "Unknown / Low Confidence"
        confidence = float(round(max(probabilities) * 100, 2))

    # ===============================
    # Return All Details
    # ===============================
    return {
        "Disease": disease,
        "Confidence": confidence,
        "Top_3_Predictions": top3,
        "Description": description,
        "Medication": medication,
        "Precautions": precautions,
        "Workout": workout_details,
        "Diets": diets,
        "Doctor": doctor
    }






@app.route('/predict', methods=['POST'])
def predict():
    # Get checkbox symptoms
    checkbox_symptoms = request.form.getlist('symptoms')

    # Get text input
    text_input = request.form.get('symptoms_text')

    text_symptoms = []
    if text_input:
        text_symptoms = [s.strip().lower() for s in text_input.split(',') if s.strip()]

    # Merge both
    symptoms = checkbox_symptoms + text_symptoms

    print("FINAL SYMPTOMS:", symptoms)

    if not symptoms:
        return render_template("index.html",
                               error="Please select at least one symptom.")

    result = predict_and_recommend(symptoms)

    # Confidence safety rule
    if result["Confidence"] < 40:
        result["Warning"] = "Low confidence prediction. Symptoms may match multiple diseases. Please consult a doctor."


    result["Disclaimer"] = (
        "This AI system provides prediction based on symptoms. "
        "It does not replace professional medical advice."
    )
    return render_template(
        "result.html",
        result=result,
        top3=result.get('Top_3_Predictions', []),
        user_symptoms=symptoms,
        predicted_disease=result.get('Disease', 'Unknown'),
        dis_med=result.get('Medication', []),
        dis_pre=result.get('Precautions', []),
        dis_diet=result.get('Diets', []),
        dis_workout=result.get('Workout', {}),
        dis_doc=result.get('Doctor', 'General Physician'),
        dis_des=result.get('Description', 'No description available.')
    )
# ===============================
# Routes
# ===============================
@app.route('/')
def home():
    return render_template("index.html", breadcrumb=[
        {"name": "Home", "url": "/"}
    ])


@app.route('/about')
def about():
    return render_template("about.html", breadcrumb=[
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "/about"}
    ])


@app.route('/contact', methods=['GET', 'POST'])
def contact():

    breadcrumb = [
        {"name": "Home", "url": "/"},
        {"name": "Contact", "url": "/contact"}
    ]

    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("NEW MESSAGE:", name, email, message)

        return render_template(
            "contact.html",
            success=True,
            breadcrumb=breadcrumb
        )

    return render_template(
        "contact.html",
        success=False,
        breadcrumb=breadcrumb
    )


@app.route('/developer')
def developer():
    return render_template("developer.html", breadcrumb=[
        {"name": "Home", "url": "/"},
        {"name": "Developer", "url": "/developer"}
    ])


@app.route('/blog')
def blog():
    return render_template("blog.html", breadcrumb=[
        {"name": "Home", "url": "/"},
        {"name": "Blog", "url": "/blog"}
    ])

if __name__ == '__main__':
    app.run(debug=True)



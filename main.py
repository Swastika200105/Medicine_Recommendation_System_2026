from flask import Flask, request, render_template, jsonify, session
import pandas as pd
import numpy as np
import pickle





# flask app
app = Flask(__name__)
app.secret_key = "supersecret123"







# LOAD TRAINED MODEL
# ===============================
model = pickle.load(open("models/model.pkl","rb"))
le = pickle.load(open("models/label_encoder.pkl","rb"))
cols = pickle.load(open("models/columns.pkl","rb"))

# load database========================================

symtoms_df = pd.read_csv('datasets/symtoms_df.csv')

precautions_df = pd.read_csv("datasets/precautions_df.csv")
workout_df = pd.read_csv("datasets/workout_df.csv")
description_df = pd.read_csv("datasets/description.csv")
medications_df = pd.read_csv("datasets/medications.csv")
diets_df = pd.read_csv("datasets/diets.csv")
doctor_df = pd.read_csv("datasets/Doctor.csv")


# HELPER FUNCTION
# ===============================
import ast

def helper(disease):
    # clean disease name
    disease_clean = disease.strip().lower()
    description_df["Disease"] = description_df["Disease"].str.strip().str.lower()

    desc_row = description_df[description_df["Disease"] == disease_clean]["Description"]

    if len(desc_row) > 0:
        desc = desc_row.values[0]

        # remove extra disease name if repeated
        if "," in desc:
            desc = desc.split(",", 1)[1]

        desc = desc.replace('"', "").strip()
    else:
        desc = "No description available."

    # precaution
    precaution = precautions_df[precautions_df["Disease"] == disease].iloc[:,1:].values.flatten().tolist()

    # medicine
    med_row = medications_df[medications_df["Disease"] == disease]["Medication"]

    if len(med_row) > 0:
        med_text = med_row.values[0]

        # convert string list -> real list
        if isinstance(med_text, str) and med_text.startswith("["):
            medicine = ast.literal_eval(med_text)
        else:
            medicine = [med_text]
    else:
        medicine = ["No medication found"]

    # diet
    diet_row = diets_df[diets_df["Disease"] == disease]["Diet"]

    if len(diet_row) > 0:
        diet_text = diet_row.values[0]

        if isinstance(diet_text, str) and diet_text.startswith("["):
            diet = ast.literal_eval(diet_text)
        else:
            diet = [diet_text]
    else:
        diet = ["No diet found"]

    # workout
    workout = workout_df[workout_df["disease"] == disease]["workout"].tolist()

    # doctor specialization
    doc = doctor_df[doctor_df["Disease"] == disease]["Specialization"]
    doc = doc.values[0] if len(doc)>0 else "General Physician"

    return desc, precaution, medicine, diet, workout, doc
# PREDICT FUNCTION
# ===============================
def predict_disease(symptoms_list):

    input_vector = [0]*len(cols)

    for s in symptoms_list:
        s = s.strip()
        if s in cols:
            idx = cols.index(s)
            input_vector[idx] = 1

    input_array = np.array(input_vector).reshape(1,-1)

    pred = model.predict(input_array)[0]
    disease = le.inverse_transform([pred])[0]

    probs = model.predict_proba(input_array)[0]
    top3_idx = probs.argsort()[-3:][::-1]

    top3 = []
    for i in top3_idx:
        d = le.inverse_transform([i])[0]
        p = round(probs[i]*100,2)
        top3.append((d,p))

    return disease, top3


# ================= ROUTES =================
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])

def predict():

    symptoms = request.form.get("symptoms")

    if not symptoms:
        return render_template("index.html", message="Enter symptoms")

    user_symptoms = [s.strip().lower() for s in symptoms.split(",")]

    if len(user_symptoms) < 3:
        return render_template("index.html", message="Enter at least 3 symptoms")

    predicted_disease, top3 = predict_disease(user_symptoms)

    # save for chatbot
    session["predicted_disease"] = predicted_disease
    session["confidence"] = top3[0][1]
    session["top3"] = top3

    desc, precaution, medicine, diet, workout, doctor = helper(predicted_disease)

    print("Medicine:", medicine)
    print("Diet:", diet)
    print("Precaution:", precaution)
    print("Workout:", workout)
    print("Doctor:", doctor)

    return render_template(
        "result.html",
        predicted_disease=predicted_disease,
        top3=top3,
        user_symptoms=user_symptoms,
        dis_des=desc,
        dis_pre=precaution,
        dis_med=medicine,
        dis_diet=diet,
        dis_wrkout=workout,
        dis_doc=doctor
    )

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("NEW MESSAGE:", name, email, message)  # optional save later

        # show thank you message
        return render_template("contact.html", success=True)

    return render_template("contact.html")


@app.route('/developer')
def developer():
    return render_template("developer.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")
# ================= AI CHATBOT ROUTE =================
import requests
from flask import request, jsonify


# ================= SMART OFFLINE CHATBOT =================
from chatbot_engine import medical_chatbot

@app.route("/chatbot", methods=["POST"])
def chatbot():

    user_msg = request.json.get("message")

    disease = session.get("predicted_disease","")
    confidence = session.get("confidence","")

    # get details again
    desc, precaution, medicine, diet, workout, doctor = helper(disease)

    reply = medical_chatbot(
        user_msg,
        disease,
        confidence,
        desc,
        precaution,
        medicine,
        diet,
        workout,
        doctor
    )

    return jsonify({"reply": reply})





if __name__ == "__main__":
    app.run(debug=True)

import random

def clean_list(data):
    if isinstance(data, list):
        return ", ".join(str(x).replace("[","").replace("]","").replace("'","") for x in data if x)
    return str(data)

def medical_chatbot(user_msg, disease, confidence,
                    desc, precaution, medicine, diet, workout, doctor):

    msg = user_msg.lower().strip()

    medicine = clean_list(medicine)
    diet = clean_list(diet)
    precaution = clean_list(precaution)
    workout = clean_list(workout)

    # ---------------- greetings ----------------
    if msg in ["hi","hello","hey","hii","hallo","hy"]:
        return "Hello 👋 I am your AI medical assistant. Ask me anything about your disease."
    # if msg in ["Namaste","Namaskar"]:
    #     return "Namaste Hajur "

    # ---------------- want to learn ----------------
    if "learn" in msg or "study" in msg:
        return f"Great 😊 let's learn about {disease}. You can ask causes, symptoms, diet, medicine, doctor or danger level."

    # ---------------- what disease ----------------
    if "what is" in msg or "about disease" in msg:
        return f"{disease}: {desc}"

    # ---------------- symptoms ----------------
    if "symptom" in msg:
        return f"Common symptoms of {disease}: {desc}"

    # ---------------- cause ----------------
    if "cause" in msg or "how i get" in msg or "why" in msg:
        return f"{disease} occurs due to infection, immunity issues or lifestyle factors. {desc}"

    # ---------------- danger ----------------
    if "danger" in msg or "serious" in msg:
        return f"{disease} can become serious if untreated. Early treatment and proper care helps recovery."

    # ---------------- treatment ----------------
    if "treatment" in msg or "recover" in msg or "cure" in msg:
        return f"Treatment includes proper medication, healthy diet and doctor's guidance."

    # ---------------- medicine ----------------
    if "medicine" in msg or "drug" in msg:
        return f"Common medicines for {disease}: {medicine}. Consult doctor before taking any medicine."

    # ---------------- doctor ----------------
    if "doctor" in msg or "specialist" in msg:
        return f"For {disease}, you should consult a {doctor}."

    # ---------------- diet ----------------
    if "diet" in msg or "food" in msg or "eat" in msg:
        return f"Recommended diet for {disease}: {diet}"

    # ---------------- precautions ----------------
    if "precaution" in msg or "care" in msg:
        return f"Precautions: {precaution}"

    # ---------------- workout ----------------
    if "exercise" in msg or "gym" in msg or "workout" in msg:
        return f"Workout tips: {workout}"

    # ---------------- confidence ----------------
    if "percent" in msg or "confidence" in msg or "accurate" in msg:
        return f"AI prediction confidence for {disease} is {confidence}%. For confirmation consult doctor."

    # ---------------- cause ----------------
    if "how i get" in msg or "cause" in msg or "why" in msg:
         return f"{disease} happens due to infection, weak immunity or medical conditions. {desc}"
        # ---------------- death fear ----------------
    if "die" in msg or "death" in msg:
        return f"Don't worry ❤️, {disease} is usually not life-threatening if treated properly. However, consult a {doctor} if symptoms become severe."
    # ---------------- thanks/love ----------------
    if "thank" in msg:
        return "You're welcome 😊 Always here to help with your health."

    if "love" in msg:
        return "Haha 😄 I care about your health. Stay safe and healthy."


    # ---------------- bye ----------------
    if "bye" in msg:
        return "Take care 😊 Stay healthy and safe."

    # ---------------- fallback ----------------
    return f"""
You are predicted with {disease} ({confidence}% confidence)

Ask me:
• Symptoms
• Causes
• Medicine
• Diet
• Doctor
• Danger level
• Treatment
"""


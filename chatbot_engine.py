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
    if msg in ["hi","hello","hey","hii","hallo","hy","babe","sweetie","darling","friend","hy ai"]:
        return "Hello 👋 I am your AI medical assistant. Ask me anything about your disease."
    # ---------------- how are you ----------------
    if "how are you" in msg:
        replies = [
            "I am functioning perfectly 😊 How can I assist you with your health today?",
            "I'm doing great and ready to help with medical guidance.",
            "All good here 🤖 How can I help you today?",
            "I am fine. Ask me anything about your health or this project."
        ]
        return random.choice(replies)
    # ---------------- precautions / prevention ----------------
    if ("precaution" in msg or
            "care" in msg or
            "prevent" in msg or
            "prevention" in msg or
            "avoid" in msg or
            "safety" in msg):
        return f"To prevent {disease}, follow these precautions: {precaution}"
    if "how to prevent" in msg:
        return f"To prevent {disease}, follow these precautions: {precaution}"

    if "how to cure" in msg:
        return f"{disease} can be managed with proper treatment, care and medicines. Consult a {doctor} for best treatment."

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
    # ---------------- who made you ----------------
    if "who made you" in msg or "developer" in msg:
        return "I was developed as an AI Medical Assistant project to help predict diseases and guide patients."

    # ---------------- what can you do ----------------
    if "what can you do" in msg:
        return "I can tell you about disease description, symptoms, medicine, diet, precautions, workout and doctor suggestions."

    # ---------------- are you real doctor ----------------
    if "real doctor" in msg:
        return "I am an AI assistant 🤖 not a real doctor, but I provide guidance based on medical data."

    # ---------------- how accurate ----------------
    if "how accurate" in msg:
        return f"My prediction accuracy depends on symptoms provided. Current confidence for {disease} is {confidence}%."
    if "project" in msg:
        return "This AI medical recommendation system predicts disease using machine learning and provides diet, medicine and doctor suggestions."

    ALL_DISEASES = [
        "fungal infection", "allergy", "gerd", "chronic cholestasis", "drug reaction",
        "peptic ulcer disease", "aids", "diabetes", "gastroenteritis", "bronchial asthma",
        "hypertension", "migraine", "cervical spondylosis", "paralysis", "jaundice",
        "malaria", "chicken pox", "dengue", "typhoid", "hepatitis a", "hepatitis b",
        "hepatitis c", "hepatitis d", "hepatitis e", "alcoholic hepatitis", "tuberculosis",
        "common cold", "pneumonia", "piles", "heart attack", "varicose veins",
        "hypothyroidism", "hyperthyroidism", "hypoglycemia", "osteoarthritis", "arthritis",
        "vertigo", "acne", "urinary tract infection", "psoriasis", "impetigo"
    ]
    # ---------------- asking about another disease ----------------
    # ----------- user asking about any disease -------------
    for d in ALL_DISEASES:
        if d in msg:
            if d.lower() == disease.lower():
                return f"You are predicted with {disease}. Ask me about symptoms, medicine, diet, precautions or doctor."

            else:
                return f"You are currently predicted with {disease}, but you asked about {d}. I can give general guidance, but for accurate diagnosis please consult doctor or run prediction with symptoms of {d}."

    # -------- general disease info ----------
    if "tell me about" in msg or "what is" in msg:
        for d in ALL_DISEASES:
            if d in msg:
                return f"{d.title()} is a medical condition that requires proper diagnosis and treatment. Maintain healthy lifestyle and consult specialist if symptoms appear."

    motivation = [
        "Stay positive 😊 recovery is faster with good care.",
        "Health is wealth 💚 take proper rest.",
        "Follow doctor advice and stay safe.",
        "Early treatment gives best results."
    ]

    if "scared" in msg or "worried" in msg:
        return random.choice(motivation)
    # ---------------- dataset question ----------------
    if "dataset" in msg or "data set" in msg:
        return "This system uses a disease prediction dataset containing symptoms and corresponding diseases. It includes 40+ diseases and 130+ symptoms used to train the machine learning model."

    # ---------------- model used ----------------
    if "model" in msg or "algorithm" in msg:
        return "I use a Random Forest Machine Learning model to predict diseases based on selected symptoms."

    # ---------------- why this model ----------------
    if "why random forest" in msg:
        return "Random Forest provides high accuracy, handles multiple symptoms well and is ideal for medical classification problems."

    # ---------------- accuracy ----------------
    if "accuracy" in msg:
        return "The model gives high accuracy depending on symptoms provided, generally around 90% or more for trained dataset."

    # ---------------- technology ----------------
    if "technology" in msg or "tech stack" in msg or "language" in msg:
        return "This project is built using Python, Flask for backend, HTML CSS Bootstrap for frontend and Scikit-learn for machine learning."

    # ---------------- about project ----------------
    if "project" in msg or "system" in msg:
        return "This is an AI-based medical recommendation system that predicts diseases from symptoms and provides medicine, diet, precautions, workout and specialist doctor suggestions."

    # ---------------- how it works ----------------
    if "how works" in msg or "how it works" in msg or "process" in msg:
        return "User selects symptoms, system sends them to machine learning model, model predicts disease and shows complete medical guidance with confidence score."

    # ---------------- future improvement ----------------
    if "future" in msg or "improve" in msg:
        return "Future improvements include adding real hospital data, improving accuracy using deep learning and deploying the system online for public use."

    # ---------------- who made ----------------
    if "who made you" in msg:
        return "I was developed as an AI medical assistant project to help users get early health guidance using machine learning."

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

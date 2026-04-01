# ===============================
# Local AI Chatbot (FINAL VERSION)
# ===============================
import random
from gpt4all import GPT4All

# Load model
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# Conversation memory
conversation_history = []


# ---------------- PROJECT INFO ----------------
def get_project_info(msg):

    if "project" in msg or "system" in msg:
        return "This is an AI-based medical recommendation system that predicts diseases from symptoms and provides guidance like medicine, diet, precautions and doctor suggestions."

    if "how it works" in msg or "working" in msg:
        return "User selects symptoms, the system uses a machine learning model to predict the disease and provides recommendations with confidence score."

    if "algorithm" in msg or "model" in msg:
        return "This project uses a Random Forest machine learning algorithm for disease prediction."

    if "technology" in msg or "tech stack" in msg:
        return "This system is built using Python, Flask, HTML, CSS and Scikit-learn."

    if "accuracy" in msg:
        return "The model provides high accuracy depending on symptoms, usually around 90%."

    if "dataset" in msg:
        return "The model is trained on a dataset of diseases and symptoms used for prediction."

    if "developer" in msg or "who made" in msg:
        return "This project was developed as an AI Medical Assistant for disease prediction and guidance."

    return "This is a machine learning based medical recommendation system."


# ---------------- AI RESPONSE ----------------
def get_ai_response(message, disease=None):

    global conversation_history

    msg = message.lower().strip()

    # -------- BASIC CHAT --------
    if msg in ["hi", "hello", "hey", "hii"]:
        return "Hello 👋 How can I help you today?"

    if "how are you" in msg:
        return random.choice([
            "I'm doing great 😊 How can I help you?",
            "All good here 🤖 What would you like to know?",
        ])

    if "thank" in msg:
        return "You're welcome 😊"

    if msg in ["ok", "okay", "okey"]:
        return "Alright 👍"

    if "what can you do" in msg:
        return "I can help you understand diseases, symptoms, treatments and also explain how this project works."

    # -------- PROJECT QUESTIONS (HIGH PRIORITY) --------
    if any(word in msg for word in [
        "project", "system", "algorithm", "model",
        "how it works", "technology", "tech stack", "dataset"
    ]):
        return get_project_info(msg)

    # -------- STORE MESSAGE --------
    conversation_history.append({"role": "user", "content": message})

    # -------- SAFE PROMPT --------
    prompt = """
You are a safe and helpful medical assistant.

RULES:
- Answer only what user asks
- Do NOT assume disease
- Do NOT say "you have"
- Keep answer short (2-4 lines)
- Use simple, calm language

Conversation:
"""

    for item in conversation_history[-6:]:
        prompt += f"{item['role']}: {item['content']}\n"

    if disease:
        prompt += f"\nContext Disease: {disease}\n"

    prompt += "\nAnswer:"

    # -------- GENERATE --------
    try:
        with model.chat_session():
            response = model.generate(prompt, max_tokens=120)

        if not response or not isinstance(response, str):
            return "AI is temporarily unavailable."

        response = response.strip()

        # -------- SAFETY FILTER (SMART) --------
        bad_phrases = ["you have", "you are suffering"]
        if any(p in response.lower() for p in bad_phrases):
            response = "I recommend consulting a doctor for proper guidance."

        # Remove unwanted lists
        if "1." in response:
            response = response.split("1.")[0]

        # Save response
        conversation_history.append({"role": "assistant", "content": response})

        return response

    except Exception as e:
        print("AI Error:", e)
        return "AI is temporarily unavailable."


# ---------------- RULE-BASED MEDICAL ----------------
def medical_chatbot(user_msg, disease=None, confidence=None,
                    desc=None, precaution=None, medicine=None,
                    diet=None, workout=None, doctor=None):

    msg = user_msg.lower().strip()

    # -------- GREETING --------
    if msg in ["hi", "hello", "hey"]:
        return "Hello 👋 I am your AI medical assistant."

    # -------- SYMPTOMS --------
    if "symptom" in msg and desc:
        return f"Common symptoms of {disease}: {desc}"

    # -------- MEDICINE --------
    if "medicine" in msg and medicine:
        return f"Medicines for {disease}: {medicine}. Please consult a doctor."

    # -------- DIET --------
    if "diet" in msg and diet:
        return f"Recommended diet for {disease}: {diet}"

    # -------- WORKOUT --------
    if "workout" in msg or "exercise" in msg:
        if workout:
            return f"Workout advice: {workout}"
        else:
            return "Light exercise like walking or yoga is helpful. Consult a doctor before starting."

    # -------- DOCTOR --------
    if "doctor" in msg and doctor:
        return f"You should consult a {doctor}."

    # -------- FALLBACK TO AI --------
    return get_ai_response(user_msg, disease)
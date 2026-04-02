import random
from gpt4all import GPT4All

# GPT4All instance
gpt_model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# Keep conversation history for context
conversation_history = []

# Safe phrases filter
BAD_PHRASES = ["you have", "you are suffering", "diagnose", "cure"]

# ------------------ AI PROMPT GENERATION ------------------
def generate_ai_reply(user_msg, disease=None, context=None, max_tokens=150):
    global conversation_history

    # Append user message
    conversation_history.append({"role": "user", "content": user_msg})

    prompt = "You are a professional, safe, and helpful medical assistant.\n"
    prompt += "Answer only based on context and keep replies short (2-4 sentences).\n"
    if disease:
        prompt += f"Context Disease: {disease}\n"
    if context:
        prompt += f"Context Info: {context}\n"
    prompt += "\nConversation:\n"

    for item in conversation_history[-6:]:
        role = "User" if item['role'] == "user" else "Assistant"
        prompt += f"{role}: {item['content']}\n"

    prompt += "Assistant:"

    try:
        with gpt_model.chat_session():
            response = gpt_model.generate(prompt, max_tokens=max_tokens)
        response = response.strip()

        # Remove bad phrases
        for phrase in BAD_PHRASES:
            if phrase in response.lower():
                response = "I recommend consulting a qualified doctor for proper guidance."

        # Save assistant response
        conversation_history.append({"role": "assistant", "content": response})
        return response

    except Exception as e:
        print("GPT4All Error:", e)
        return "AI is temporarily unavailable."

# ------------------ PROFESSIONAL MEDICAL CHAT ------------------
def professional_medical_chat(user_msg, prediction_result=None):
    """
    Uses structured disease prediction result to give professional responses.
    prediction_result: dict from predict_and_recommend()
    """
    disease = prediction_result.get("Disease") if prediction_result else None
    desc = prediction_result.get("Description") if prediction_result else None
    med = prediction_result.get("Medication") if prediction_result else None
    diet = prediction_result.get("Diets") if prediction_result else None
    workout = prediction_result.get("Workout") if prediction_result else None
    precautions = prediction_result.get("Precautions") if prediction_result else None
    doctor = prediction_result.get("Doctor") if prediction_result else None

    msg = user_msg.lower().strip()

    # Pre-defined professional responses
    if msg in ["hi", "hello", "hey"]:
        return "Hello 👋 I am your AI medical assistant. How can I help you today?"

    if "symptom" in msg or "sign" in msg:
        if disease and desc:
            return f"Common symptoms of {disease}: {desc}"
        else:
            return generate_ai_reply(user_msg, disease)

    if "medicine" in msg or "medication" in msg:
        if disease and med:
            med_str = ', '.join(med) if isinstance(med, list) else str(med)
            return f"Recommended medications for {disease}: {med_str}. Please consult a doctor before taking any medicine."
        else:
            return generate_ai_reply(user_msg, disease)

    if "diet" in msg or "food" in msg:
        if disease and diet:
            diet_str = ', '.join(diet)
            return f"Suggested diet for {disease}: {diet_str}"
        else:
            return generate_ai_reply(user_msg, disease)

    if "workout" in msg or "exercise" in msg:
        if workout:
            return f"Workout advice for {disease}: {workout}"
        else:
            return "Light exercise like walking or yoga is recommended. Always consult your doctor before starting any new routine."

    if "precaution" in msg or "prevent" in msg:
        if precautions:
            prec_str = ', '.join(precautions)
            return f"Precautions for {disease}: {prec_str}"
        else:
            return generate_ai_reply(user_msg, disease)

    if "doctor" in msg or "specialist" in msg:
        if doctor:
            return f"For {disease}, you should consult a {doctor}."
        else:
            return generate_ai_reply(user_msg, disease)

    # Fallback to GPT4All
    return generate_ai_reply(user_msg, disease)
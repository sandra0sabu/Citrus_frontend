import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Setup Google Gemini
# Ensure your .env has: GEMINI_API_KEY=your_key_here
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# We use the 'flash-lite' model for speed and efficiency
# System instruction ensures the bot stays in character as AgroScan AI
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction="You are AgroScan AI, a helpful and friendly agricultural expert. "
                       "You specialize in identifying plant diseases and suggesting solutions. "
                       "Keep your answers concise and conversational."
)

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.json
    user_msg = user_data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message."})

    try:
        # Generate a response using Gemini
        # This replaces the complex payload and headers needed for Hugging Face
        response = model.generate_content(user_msg)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "I'm having trouble understanding that. Could you describe the plant symptoms?"})

    except Exception as e:
        print(f"Gemini Error: {e}")
        return jsonify({"reply": "❌ Connection to AgroScan AI failed. Please check your API key."})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
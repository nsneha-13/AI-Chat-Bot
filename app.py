from flask import Flask, request, jsonify
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from flask_cors import CORS  # To allow frontend connection

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests

# Load your model
model_name = "facebook/blenderbot-400M-distill"   # or "./blenderbot_trained" if you fine-tuned it
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input.strip():
        return jsonify({"reply": "Please enter a message."})
    
    inputs = tokenizer(user_input, return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=100)
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)

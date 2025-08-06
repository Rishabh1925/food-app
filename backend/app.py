from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image
import io

app = Flask(__name__)

# Load your model
model = load_model("../model/food_model.keras")

# Class names (must match training order)
class_names = [
    'chocolate_cake', 'donuts', 'french_fries', 'grilled_cheese_sandwich',
    'ice_cream', 'pancakes', 'pizza', 'samosa', 'sushi', 'tacos'
]

# Image preprocessing function
def preprocess_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))  # Resize to model's input size
    img_array = np.array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img_bytes = file.read()

    try:
        img_array = preprocess_image(img_bytes)
        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_label = class_names[predicted_index]
        confidence = float(prediction[predicted_index])

        return jsonify({
            "class": predicted_label,
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from werkzeug.utils import secure_filename
import io
import base64
import gdown

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

MODEL_PATH = "model.keras"
GDRIVE_FILE_ID = "your_file_id_here"

# Download model only if not already downloaded
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id=1OsRuB1z0k9FoWj4rMS88DXIKMkAEsO1z", MODEL_PATH, quiet=False)


# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Food classes - update these based on your model
FOOD_CLASSES = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito'
]

# Load your model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image
    image = image.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def predict_food(image):
    """Make prediction on uploaded image"""
    if model is None:
        return None, None, None
    
    try:
        # Preprocess image
        processed_image = preprocess_image(image)

        print(f"Image shape before prediction: {processed_image.shape}")
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        predicted_class = FOOD_CLASSES[predicted_class_idx]
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = []
        
        for idx in top_3_idx:
            top_3_predictions.append({
                'class': FOOD_CLASSES[idx],
                'confidence': float(predictions[0][idx])
            })
        
        return predicted_class, confidence, top_3_predictions
    
    import traceback  # Make sure this is at the top of your file!

    except Exception as e:
        print("Prediction error:")
        traceback.print_exc()
        return None, None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        try:
            # Read image
            image = Image.open(file.stream)
            
            # Make prediction
            predicted_class, confidence, top_3 = predict_food(image)
            
            if predicted_class is None:
                return jsonify({'error': 'Model not available'}), 500
            
            # Convert image to base64 for display
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='JPEG')
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            
            return jsonify({
                'success': True,
                'prediction': predicted_class.replace('_', ' ').title(),
                'confidence': f"{confidence:.2%}",
                'confidence_raw': confidence,
                'top_predictions': top_3,
                'image': f"data:image/jpeg;base64,{img_str}"
            })
        
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)

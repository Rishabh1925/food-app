// Food categories matching your dataset
const foodCategories = [
    'chocolate_cake',
    'donuts', 
    'french_fries',
    'grilled_cheese_sandwich',
    'tacos',
    'ice_cream',
    'pancakes',
    'pizza',
    'samosa',
    'sushi'
];

const foodEmojis = {
    'chocolate_cake': '🍰',
    'donuts': '🍩',
    'french_fries': '🍟',
    'grilled_cheese_sandwich': '🥪',
    'ice_cream': '🍦',
    'pancakes': '🥞',
    'pizza': '🍕',
    'samosa': '🥟',
    'sushi': '🍣',
    'tacos': '🌮'
};

let model = null;

// Initialize the model (placeholder - you'll need to replace this with your actual model)
async function loadModel() {
    try {
        // Replace this URL with your actual model path
        // For now, we'll simulate the model loading
        console.log('Model loading simulated - replace with actual model loading');
        // model = await tf.loadLayersModel('/path/to/your/model.json');
        return true;
    } catch (error) {
        console.error('Error loading model:', error);
        return false;
    }
}

// Preprocess image for prediction
function preprocessImage(imageElement) {
    return tf.tidy(() => {
        // Convert image to tensor
        const tensor = tf.browser.fromPixels(imageElement);
        
        // Resize to model input size (usually 224x224 for food classification)
        const resized = tf.image.resizeBilinear(tensor, [224, 224]);
        
        // Normalize pixel values to [0, 1]
        const normalized = resized.div(255.0);
        
        // Add batch dimension
        const batched = normalized.expandDims(0);
        
        return batched;
    });
}

// Simulate prediction (replace with actual model prediction)
async function predictFood(imageElement) {
    // Simulate loading time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Simulate prediction results (replace with actual model prediction)
    const randomIndex = Math.floor(Math.random() * foodCategories.length);
    const confidence = Math.random() * 0.4 + 0.6; // Random confidence between 60-100%
    
    return {
        predictedClass: foodCategories[randomIndex],
        confidence: confidence
    };
    
    /* 
    // Actual prediction code (uncomment when you have your model):
    const preprocessed = preprocessImage(imageElement);
    const predictions = await model.predict(preprocessed).data();
    const maxIndex = predictions.indexOf(Math.max(...predictions));
    
    return {
        predictedClass: foodCategories[maxIndex],
        confidence: predictions[maxIndex]
    };
    */
}

// Handle file upload
document.getElementById('fileInput').addEventListener('change', handleFileSelect);

// Handle drag and drop
const uploadArea = document.querySelector('.upload-area');
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file.');
        return;
    }

    // Show image preview
    const reader = new FileReader();
    reader.onload = function(e) {
        const imagePreview = document.getElementById('imagePreview');
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
        imagePreview.onload = () => classifyImage(imagePreview);
    };
    reader.readAsDataURL(file);
}

async function classifyImage(imageElement) {
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';

    // Reset category highlights
    document.querySelectorAll('.category-item').forEach(item => {
        item.classList.remove('predicted');
    });

    try {
        const result = await predictFood(imageElement);
        displayResult(result);
    } catch (error) {
        console.error('Prediction error:', error);
        showError('Error analyzing image. Please try again.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

function displayResult(result) {
    const { predictedClass, confidence } = result;
    
    // Format the class name for display
    const displayName = predictedClass.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    const emoji = foodEmojis[predictedClass] || '🍽️';
    const confidencePercent = Math.round(confidence * 100);
    
    // Update result display
    document.getElementById('predictionResult').innerHTML = 
        `${emoji} This looks like <strong>${displayName}</strong>!`;
    
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceFill.textContent = `${confidencePercent}% confident`;
    
    // Highlight the predicted category
    const categories = document.querySelectorAll('.category-item');
    categories.forEach((item, index) => {
        if (foodCategories[index] === predictedClass) {
            item.classList.add('predicted');
        }
    });
    
    document.getElementById('resultContainer').style.display = 'block';
}

function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadModel();
});
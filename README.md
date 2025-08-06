# 🍕 Food Image Classifier

A web-based AI application that classifies food images using deep learning. Built with TensorFlow and deployed as a client-side web app.

## 🎯 What it does

Upload an image of food and get instant AI-powered classification! The model can identify these 10 food categories:

- 🍰 Chocolate Cake
- 🍩 Donuts  
- 🍟 French Fries
- 🥪 Grilled Cheese Sandwich
- 🍦 Ice Cream
- 🥞 Pancakes
- 🍕 Pizza
- 🥟 Samosa
- 🍣 Sushi
- 🌮 Tacos

## 🚀 Live Demo

**[Try it here!](https://yourusername.github.io/food-classifier)** *(Update with your actual GitHub Pages URL)*

## 🛠️ How it works

1. **Deep Learning Model**: Trained using TensorFlow/Keras on food image dataset
2. **Web Conversion**: Model converted to TensorFlow.js for browser deployment
3. **Real-time Classification**: Instant predictions directly in your browser
4. **No Server Required**: Everything runs client-side using WebGL acceleration

## 📁 Project Structure

```
food-classifier/
├── index.html              # Web interface
├── styles.css              # Styling & animations  
├── script.js               # AI integration & UI logic
├── model/                  # TensorFlow.js model files
│   ├── model.json         # Model architecture
│   ├── model.weights.bin  # Model weights
│   └── food_categories.json # Class labels
├── food_classifier_model.keras # Original trained model
└── README.md              # This file
```

## 🔧 Local Development

To run locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/food-classifier.git
cd food-classifier

# Start a local server (required for TensorFlow.js)
python -m http.server 8000

# Open in browser
open http://localhost:8000
```

## 🧠 Model Details

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 224×224×3 (RGB images)
- **Output**: 10 food categories with confidence scores
- **Framework**: TensorFlow/Keras → TensorFlow.js
- **Performance**: Optimized for real-time browser inference

## 📊 Features

- ✅ **Drag & Drop Upload**: Easy image upload interface
- ✅ **Instant Results**: Real-time classification with confidence scores
- ✅ **Mobile Friendly**: Responsive design works on all devices
- ✅ **No Data Collection**: Everything processes locally in your browser
- ✅ **Visual Feedback**: Progress indicators and result visualization

## 🎨 Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI/ML**: TensorFlow.js, WebGL acceleration
- **Design**: CSS Grid, Flexbox, CSS animations
- **Deployment**: GitHub Pages (static hosting)

## 📈 Future Improvements

- [ ] Add more food categories
- [ ] Implement model confidence thresholding
- [ ] Add nutritional information lookup
- [ ] Support for batch image processing
- [ ] Model performance analytics

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Share your results!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Food image dataset contributors
- TensorFlow.js team for browser ML capabilities
- GitHub Pages for free hosting

---

**Made with ❤️ and AI** | [GitHub](https://github.com/yourusername/food-classifier) | [Demo](https://yourusername.github.io/food-classifier)
# Medical AI Chatbot - Complete Guide

A full-featured medical chatbot with AI-powered conversations, disease prediction, and conversation history management.

## 🌟 Features

### 1. **AI-Powered Chat**
- Conversational AI using OpenRouter API (Llama 3.3 70B)
- Multi-turn conversations with context awareness
- Empathetic and informative medical responses

### 2. **Disease Prediction**
- Machine Learning-based disease prediction from symptoms
- Random Forest model with 98%+ accuracy
- Top 3 disease predictions with confidence scores

### 3. **Conversation History**
- Automatic saving of chat history
- Session-based conversation tracking
- Load previous conversations on page reload
- Clear history option

### 4. **Disease Information**
- Detailed disease descriptions
- Severity assessment (Mild, Moderate, Severe, Critical)
- Recommended precautions for each disease

### 5. **Modern Web Interface**
- Beautiful gradient UI design
- Responsive layout for all devices
- Real-time message updates
- Loading indicators and animations

## 📁 Project Structure

```
chatbot/
├── app.py                          # Flask backend server
├── trainmodel.py                   # Model training script
├── ai.py                          # Standalone prediction system
├── requirements.txt               # Python dependencies
├── README_CHATBOT.md             # This file
├── dataset/                       # Training datasets
│   ├── dataset.csv
│   ├── symptom_Description.csv
│   ├── symptom_precaution.csv
│   └── Symptom-severity.csv
├── templates/                     # HTML templates
│   └── index.html
├── static/                        # Static files
│   ├── style.css
│   └── script.js
├── chat_history/                  # Auto-created for storing chats
├── random_forest_model.pkl       # Trained model (after training)
└── model_data.pkl                # Model data (after training)
```

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Pandas (data manipulation)
- NumPy (numerical computing)
- Scikit-learn (machine learning)
- Requests (HTTP library)

### Step 2: Train the Model

Before using the chatbot, train the disease prediction model:

```bash
python trainmodel.py
```

This will:
- Load and preprocess datasets
- Train a Random Forest classifier
- Save the model files (`.pkl` files)
- Display training metrics

**Note:** You only need to do this once, unless you update the datasets.

### Step 3: Get OpenRouter API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Set it as an environment variable:

**Windows (Command Prompt):**
```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
```

**Linux/Mac:**
```bash
export OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Alternative:** Edit `app.py` and replace the API key directly:
```python
OPENROUTER_API_KEY = 'sk-or-v1-your-api-key-here'
```

### Step 4: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

Open your browser and navigate to:
```
http://localhost:5000
```

## 💬 Using the Chatbot

### AI Chat Feature

1. Type your health question in the input box
2. Press Enter or click "Send"
3. Wait for the AI response
4. Continue the conversation - context is maintained

**Example Questions:**
- "What causes headaches?"
- "How can I prevent the flu?"
- "What are the symptoms of diabetes?"
- "Tell me about high blood pressure treatment"
- "I have itching, skin_rash, vomiting - what could it be?" (triggers disease prediction)

### Disease Prediction Feature (Integrated)

The disease prediction is now seamlessly integrated into the chat. Simply mention your symptoms in natural language or list them comma-separated, and the chatbot will:

1. Detect symptom-related queries automatically
2. Run disease prediction using the ML model
3. Provide top 3 predictions with confidence scores, severity, descriptions, and precautions
4. Continue with AI-powered medical advice

**Example Chat Inputs:**
- "I have itching, skin_rash, nodal_skin_eruptions"
- "Symptoms: vomiting, fatigue, headache"
- "Predict disease from: cough, fever, sore_throat"

**Output Format:**
- Disease predictions appear first, followed by AI medical advice
- Each prediction includes confidence %, severity level, description, and precautions

### Managing Conversation History

- **Automatic Saving**: All conversations are saved automatically
- **Session-Based**: Each browser session has its own chat history
- **Reload Persistence**: History persists when you refresh the page
- **Clear History**: Click "Clear History" button to delete current session

## 🔧 API Endpoints

### `/` (GET)
- Main page - renders the chatbot interface

### `/api/chat` (POST)
- Send message to AI and get response
- **Request Body:** `{"message": "your message"}`
- **Response:** `{"response": "AI response", "timestamp": "..."}`

### `/api/history` (GET)
- Get chat history for current session
- **Response:** `{"history": [...]}`

### `/api/clear` (POST)
- Clear chat history for current session
- **Response:** `{"message": "Chat history cleared"}`

### `/api/predict-disease` (POST)
- Predict disease from symptoms
- **Request Body:** `{"symptoms": ["symptom1", "symptom2"]}`
- **Response:** `{"predictions": [...], "matched_symptoms": [...]}`

### `/api/symptoms` (GET)
- Get list of all available symptoms
- **Response:** `{"symptoms": [...]}`

## 🎨 Customization

### Changing the AI Model

Edit `app.py` and change the model in the API call:

```python
"model": "meta-llama/llama-3.3-70b-instruct:free",
# Change to:
"model": "openai/gpt-3.5-turbo",
```

Available models on OpenRouter:
- `meta-llama/llama-3.3-70b-instruct:free` (Free)
- `openai/gpt-3.5-turbo`
- `openai/gpt-4`
- `anthropic/claude-2`

### Customizing the System Prompt

Edit the `system_message` in `app.py`:

```python
system_message = {
    'role': 'system',
    'content': 'Your custom system prompt here...'
}
```

### Styling Changes

Edit `static/style.css` to customize:
- Colors
- Fonts
- Layout
- Animations

## 📊 Model Performance

- **Algorithm:** Random Forest Classifier
- **Estimators:** 200 trees
- **Training Accuracy:** ~99%
- **Testing Accuracy:** ~98%
- **Diseases:** 40+ medical conditions
- **Symptoms:** 130+ unique symptoms

## 🔒 Privacy & Security

- **Session-Based:** Each user has isolated chat history
- **Local Storage:** Chat histories stored locally on server
- **API Key Security:** Store API key in environment variables
- **No Database:** Simple file-based storage for easy deployment

## ⚠️ Important Disclaimers

1. **Not for Medical Diagnosis:** This system is for educational and informational purposes only
2. **Consult Professionals:** Always consult qualified healthcare providers for medical advice
3. **AI Limitations:** AI responses may not be 100% accurate
4. **Emergency Situations:** Call emergency services for urgent medical issues

## 🐛 Troubleshooting

### Model Files Not Found
**Error:** `Model not found. Please train the model first.`

**Solution:** Run `python trainmodel.py` to train the model

### API Key Issues
**Error:** Connection errors or authentication failures

**Solution:** 
- Check your API key is correct
- Ensure environment variable is set
- Verify you have API credits on OpenRouter

### Port Already in Use
**Error:** `Address already in use`

**Solution:**
```python
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Import Errors
**Error:** `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment

**Using Gunicorn (Linux/Mac):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Using Waitress (Windows):**
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Cloud Platforms
- **Heroku:** Add `Procfile` with `web: gunicorn app:app`
- **AWS/Azure:** Deploy as Flask application
- **Docker:** Create Dockerfile for containerization

## 📝 Future Enhancements

- [ ] User authentication and accounts
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Export chat history as PDF
- [ ] Voice input for symptoms
- [ ] Multi-language support
- [ ] Medical image analysis
- [ ] Integration with health APIs
- [ ] Mobile app version

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

For issues or questions, please check the troubleshooting section or review the code comments.

---

**Remember:** This is a learning project. Always prioritize real medical advice from qualified healthcare professionals! 🏥

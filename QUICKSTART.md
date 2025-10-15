# 🚀 Quick Start Guide - Medical AI Chatbot

## Get Started in 3 Simple Steps!

### Step 1: Train the Model (One-time setup)
```bash
python trainmodel.py
```
⏱️ Takes about 1-2 minutes

### Step 2: Set Your OpenRouter API Key
```cmd
set OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

**Don't have an API key?**
1. Visit: https://openrouter.ai/
2. Sign up (it's free!)
3. Get your API key from dashboard

### Step 3: Run the Chatbot
```bash
python app.py
```

Then open in browser: **http://localhost:5000**

---

## 🎯 What You Can Do

### 1. Chat with AI
- Ask health questions
- Get medical information
- Have natural conversations
- **Example:** "What are the symptoms of diabetes?"

### 2. Predict Diseases
- Click "Check Symptoms" button
- Enter symptoms like: `fever, headache, cough`
- Get instant predictions with precautions

### 3. View History
- All conversations saved automatically
- Reload page to see previous chats
- Clear history anytime

---

## 📝 Example Symptoms to Try

**Fungal Infection:**
```
itching, skin_rash, nodal_skin_eruptions
```

**Diabetes:**
```
fatigue, weight_loss, excessive_hunger, increased_appetite
```

**Common Cold:**
```
continuous_sneezing, chills, fatigue, cough
```

**GERD:**
```
stomach_pain, acidity, ulcers_on_tongue, vomiting
```

---

## ⚡ Troubleshooting

**Problem:** Model files not found
**Solution:** Run `python trainmodel.py` first

**Problem:** API connection error
**Solution:** Check your API key and internet connection

**Problem:** Port 5000 already in use
**Solution:** Close other apps using port 5000 or change port in app.py

---

## 🎨 Interface Guide

```
┌─────────────────────────────────────────────────┐
│           🏥 Medical AI Chatbot                 │
├──────────────┬──────────────────────────────────┤
│              │                                  │
│  Features    │     Chat Area                    │
│              │  ┌────────────────────────────┐  │
│  [AI Chat]   │  │ Bot: Hello! How can I     │  │
│              │  │      help you?            │  │
│  [Disease    │  └────────────────────────────┘  │
│   Predict]   │  ┌────────────────────────────┐  │
│              │  │ You: What is diabetes?    │  │
│  [Clear      │  └────────────────────────────┘  │
│   History]   │                                  │
│              │  [Type message here...] [Send]   │
└──────────────┴──────────────────────────────────┘
```

---

## 🌐 Access URLs

- **Main Interface:** http://localhost:5000
- **Chat API:** http://localhost:5000/api/chat
- **Predict API:** http://localhost:5000/api/predict-disease
- **History API:** http://localhost:5000/api/history

---

## 💡 Tips

✅ Be specific with symptoms for better predictions
✅ Use underscores in symptom names (e.g., `skin_rash`)
✅ Conversations are saved automatically
✅ The AI remembers context within each session
✅ Check precautions in disease predictions
✅ Always consult real doctors for serious issues

---

## 🎓 Learn More

- See **README_CHATBOT.md** for complete documentation
- See **README.md** for model training details

---

**Ready to start? Run:** `python app.py` 🚀

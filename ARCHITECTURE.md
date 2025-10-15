# 🏗️ System Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Web Interface (index.html)                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────────┐ │  │
│  │  │  Sidebar │  │   Chat   │  │   Disease Predictor    │ │  │
│  │  │          │  │   Area   │  │       Modal            │ │  │
│  │  │ Features │  │          │  │                        │ │  │
│  │  └──────────┘  └──────────┘  └────────────────────────┘ │  │
│  │                                                          │  │
│  │  JavaScript (script.js) - Handles UI interactions       │  │
│  │  CSS (style.css) - Styling and animations              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │ AJAX/Fetch API
                         │ (HTTP/JSON)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK SERVER (app.py)                      │
│                         Port: 5000                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                         │  │
│  │                                                          │  │
│  │  GET  /              → Render HTML                      │  │
│  │  POST /api/chat      → AI Conversation                  │  │
│  │  GET  /api/history   → Load Chat History               │  │
│  │  POST /api/clear     → Clear History                    │  │
│  │  POST /api/predict   → Disease Prediction               │  │
│  │  GET  /api/symptoms  → List Symptoms                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────┐        ┌──────────────────────────────┐  │
│  │  Session        │        │   Model Management           │  │
│  │  Management     │        │                              │  │
│  │  - User IDs     │        │  - Load RF Model (.pkl)      │  │
│  │  - History      │        │  - Feature Engineering       │  │
│  │    Tracking     │        │  - Prediction Logic          │  │
│  └─────────────────┘        └──────────────────────────────┘  │
└──────────────┬──────────────────────────┬───────────────────────┘
               │                          │
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌────────────────────────────────┐
│   EXTERNAL AI SERVICE    │  │     LOCAL STORAGE              │
│   (OpenRouter API)       │  │                                │
│                          │  │  ┌──────────────────────────┐  │
│  Model: Llama 3.3 70B    │  │  │  chat_history/           │  │
│  Endpoint: /completions  │  │  │    session_id.json       │  │
│  Auth: Bearer Token      │  │  │    ...                   │  │
│                          │  │  └──────────────────────────┘  │
└──────────────────────────┘  │                                │
                              │  ┌──────────────────────────┐  │
                              │  │  Models/                 │  │
                              │  │    random_forest_model   │  │
                              │  │      .pkl                │  │
                              │  │    model_data.pkl        │  │
                              │  └──────────────────────────┘  │
                              │                                │
                              │  ┌──────────────────────────┐  │
                              │  │  dataset/                │  │
                              │  │    dataset.csv           │  │
                              │  │    symptom_*.csv         │  │
                              │  └──────────────────────────┘  │
                              └────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. AI Chat Flow

```
User Types Message
      │
      ├─→ JavaScript captures input
      │
      ├─→ POST /api/chat
      │        │
      │        ├─→ Load chat history (session-based)
      │        │
      │        ├─→ Add user message to history
      │        │
      │        ├─→ Prepare API request
      │        │        │
      │        │        └─→ Send to OpenRouter API
      │        │                  │
      │        │                  ├─→ Process with Llama 3.3
      │        │                  │
      │        │                  └─→ Return AI response
      │        │
      │        ├─→ Add AI response to history
      │        │
      │        ├─→ Save history to file
      │        │
      │        └─→ Return JSON response
      │
      └─→ Display in chat UI
```

### 2. Disease Prediction Flow

```
User Enters Symptoms
      │
      ├─→ Parse symptoms (comma-separated)
      │
      ├─→ POST /api/predict-disease
      │        │
      │        ├─→ Load trained ML model
      │        │
      │        ├─→ Create feature vector
      │        │        │
      │        │        ├─→ Match symptoms to features
      │        │        │
      │        │        └─→ Binary encoding [0,1,0,1,...]
      │        │
      │        ├─→ Model.predict_proba()
      │        │        │
      │        │        └─→ Get probabilities for all diseases
      │        │
      │        ├─→ Sort by confidence
      │        │
      │        ├─→ Get top 3 predictions
      │        │
      │        ├─→ Fetch disease info
      │        │        │
      │        │        ├─→ Description
      │        │        ├─→ Precautions
      │        │        └─→ Severity
      │        │
      │        └─→ Return JSON response
      │
      └─→ Display predictions with styling
```

### 3. Session Management Flow

```
User Opens Browser
      │
      ├─→ Initialize session
      │        │
      │        ├─→ Check for existing session ID
      │        │
      │        └─→ Generate new ID if needed
      │
      ├─→ Load chat history
      │        │
      │        ├─→ Find session file
      │        │
      │        ├─→ Parse JSON
      │        │
      │        └─→ Return messages
      │
      └─→ Display in UI

User Closes Browser
      │
      └─→ Session file persists for future visits
```

---

## Component Breakdown

### Frontend Components

```
┌────────────────────────────────────────────────┐
│              index.html                        │
├────────────────────────────────────────────────┤
│                                                │
│  ├─ Header                                     │
│  │   ├─ Title                                  │
│  │   └─ Subtitle                               │
│  │                                             │
│  ├─ Sidebar                                    │
│  │   ├─ AI Chat Card                           │
│  │   ├─ Disease Prediction Button              │
│  │   ├─ Features List                          │
│  │   └─ Clear History Button                   │
│  │                                             │
│  ├─ Chat Container                             │
│  │   ├─ Messages Area (scrollable)             │
│  │   │   ├─ Welcome Message                    │
│  │   │   ├─ User Messages                      │
│  │   │   └─ Bot Messages                       │
│  │   │                                         │
│  │   └─ Input Area                             │
│  │       ├─ Text Input                         │
│  │       └─ Send Button                        │
│  │                                             │
│  └─ Modal Dialog                               │
│      ├─ Close Button                           │
│      ├─ Symptoms Input (textarea)              │
│      ├─ Analyze Button                         │
│      └─ Results Area                           │
│                                                │
└────────────────────────────────────────────────┘
```

### Backend Components

```
┌────────────────────────────────────────────────┐
│                app.py                          │
├────────────────────────────────────────────────┤
│                                                │
│  Configuration                                 │
│  ├─ API Key                                    │
│  ├─ Secret Key                                 │
│  └─ Directories                                │
│                                                │
│  Helper Functions                              │
│  ├─ get_session_id()                           │
│  ├─ load_chat_history()                        │
│  ├─ save_chat_history()                        │
│  └─ call_openrouter_api()                      │
│                                                │
│  Routes                                        │
│  ├─ / (index)                                  │
│  ├─ /api/chat (POST)                           │
│  ├─ /api/history (GET)                         │
│  ├─ /api/clear (POST)                          │
│  ├─ /api/predict-disease (POST)                │
│  └─ /api/symptoms (GET)                        │
│                                                │
│  Main Execution                                │
│  └─ app.run()                                  │
│                                                │
└────────────────────────────────────────────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────┐
│          Frontend Stack                 │
├─────────────────────────────────────────┤
│  HTML5        - Structure               │
│  CSS3         - Styling & Animations    │
│  JavaScript   - Interactivity           │
│  Fetch API    - AJAX Requests           │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          Backend Stack                  │
├─────────────────────────────────────────┤
│  Python 3.11  - Language                │
│  Flask 2.3+   - Web Framework           │
│  Requests     - HTTP Client             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Machine Learning Stack            │
├─────────────────────────────────────────┤
│  Scikit-learn - ML Framework            │
│  Pandas       - Data Processing         │
│  NumPy        - Numerical Computing     │
│  Pickle       - Model Serialization     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          External Services              │
├─────────────────────────────────────────┤
│  OpenRouter   - AI API Provider         │
│  Llama 3.3    - Language Model          │
└─────────────────────────────────────────┘
```

---

## File Structure Tree

```
chatbot/
│
├── 📱 Frontend
│   ├── templates/
│   │   └── index.html              (Main UI)
│   └── static/
│       ├── style.css               (Styling)
│       └── script.js               (Logic)
│
├── 🐍 Backend
│   ├── app.py                      (Flask Server)
│   ├── trainmodel.py               (ML Training)
│   └── ai.py                       (CLI Tool)
│
├── 📊 Data
│   ├── dataset/
│   │   ├── dataset.csv             (Disease-Symptom)
│   │   ├── symptom_Description.csv (Descriptions)
│   │   ├── symptom_precaution.csv  (Precautions)
│   │   └── Symptom-severity.csv    (Severity Weights)
│   │
│   ├── chat_history/               (Auto-generated)
│   │   └── *.json                  (Session Chats)
│   │
│   ├── random_forest_model.pkl     (Trained Model)
│   └── model_data.pkl              (Model Metadata)
│
├── 📖 Documentation
│   ├── README.md                   (Model Docs)
│   ├── README_CHATBOT.md           (Chatbot Guide)
│   ├── QUICKSTART.md               (Quick Start)
│   ├── PROJECT_SUMMARY.md          (Overview)
│   ├── API_KEY_GUIDE.md            (API Setup)
│   └── ARCHITECTURE.md             (This File)
│
├── ⚙️ Configuration
│   ├── requirements.txt            (Dependencies)
│   └── .env.example                (Config Template)
│
└── 🚀 Scripts
    ├── setup.bat                   (Setup Script)
    └── run_chatbot.bat             (Launch Script)
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────┐
│            Security Layers                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. API Key Protection                          │
│     ├─ Environment Variables                    │
│     ├─ Never committed to Git                   │
│     └─ Masked in logs                           │
│                                                 │
│  2. Session Management                          │
│     ├─ Random session IDs                       │
│     ├─ Server-side storage                      │
│     └─ No client-side secrets                   │
│                                                 │
│  3. Input Validation                            │
│     ├─ Sanitize user input                      │
│     ├─ Type checking                            │
│     └─ Length limits                            │
│                                                 │
│  4. Error Handling                              │
│     ├─ Graceful error messages                  │
│     ├─ No stack traces to client                │
│     └─ Logging for debugging                    │
│                                                 │
│  5. File System Security                        │
│     ├─ Isolated session files                   │
│     ├─ No path traversal                        │
│     └─ Limited file access                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Scalability Considerations

### Current Design
- ✅ Single server
- ✅ File-based storage
- ✅ Synchronous requests
- ✅ Good for: Small-medium traffic

### For Production Scale
```
┌──────────────────────────────────────┐
│      Load Balancer (nginx)           │
└──────────┬───────────────────────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
┌─────────┐ ┌─────────┐
│ Flask 1 │ │ Flask 2 │ ... (Multiple instances)
└────┬────┘ └────┬────┘
     │           │
     └─────┬─────┘
           │
           ▼
┌──────────────────────┐
│  Redis / Database    │ (Shared session storage)
└──────────────────────┘
```

---

## Performance Metrics

```
Component              Response Time    Throughput
─────────────────────────────────────────────────
Page Load              < 1s             N/A
Model Loading          < 1s             Once
Disease Prediction     < 100ms          100+ req/s
AI Response            2-5s             API-limited
Chat History Load      < 50ms           1000+ req/s
```

---

## Deployment Options

### Local Development
```
Python app.py → localhost:5000
```

### Production Server
```
Gunicorn/Waitress → Multiple workers → Production port
```

### Cloud Deployment
```
Heroku / AWS / Azure / Google Cloud
  ├─ Auto-scaling
  ├─ Load balancing
  ├─ Database integration
  └─ CDN for static files
```

---

## Integration Points

### Current Integrations
1. **OpenRouter API** - AI responses
2. **Scikit-learn** - ML predictions
3. **Flask Sessions** - User tracking

### Possible Future Integrations
- 🔮 Database (PostgreSQL, MongoDB)
- 🔮 Redis (Caching, Sessions)
- 🔮 Authentication (OAuth, JWT)
- 🔮 Analytics (Google Analytics)
- 🔮 Monitoring (Sentry, Datadog)
- 🔮 CDN (CloudFront, Cloudflare)

---

This architecture is designed for:
✓ Easy understanding
✓ Simple deployment
✓ Future scalability
✓ Educational purposes

**Happy Building!** 🏗️

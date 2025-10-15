from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime
import secrets
from ai import DiseasePredictionSystem

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Store conversation history in a simple file-based system
CHAT_HISTORY_DIR = "chat_history"
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

# Initialize RAG system
rag_system = None

# Initialize Disease Prediction System
predictor = None

def initialize_rag():
    """Initialize or load RAG system"""
    global rag_system
    try:
        from rag_system import MedicalRAG
        rag_system = MedicalRAG()
        
        # Try to load existing RAG system
        if os.path.exists('rag_system.pkl'):
            if rag_system.load('rag_system.pkl'):
                print("RAG system loaded successfully!")
                return True
        
        # If not found, build new one
        print("Building new RAG system...")
        if rag_system.load_medical_knowledge() and rag_system.build_index():
            rag_system.save()
            print("RAG system built and saved!")
            return True
        
        return False
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return False


def initialize_predictor():
    """Initialize the disease prediction system"""
    global predictor
    try:
        predictor = DiseasePredictionSystem()
        print("Disease prediction system loaded successfully!")
        return True
    except Exception as e:
        print(f"Error initializing disease prediction system: {e}")
        return False


def get_session_id():
    """Get or create a session ID for the current user"""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
    return session['session_id']


def get_chat_history_file():
    """Get the chat history file path for the current session"""
    session_id = get_session_id()
    return os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")


def load_chat_history():
    """Load chat history from file"""
    history_file = get_chat_history_file()
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_chat_history(history):
    """Save chat history to file"""
    history_file = get_chat_history_file()
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def call_openrouter_api(messages):
    """
    Call OpenRouter API with message history
    
    Parameters:
    messages: List of message dictionaries with 'role' and 'content'
    
    Returns:
    Response text from the AI
    """
    try:
        response = requests.post(
            url=OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Disease Prediction Chatbot",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": messages,
            }),
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn't generate a response."
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to AI service: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def index():
    """Render the main chatbot interface"""
    # Initialize session
    get_session_id()
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with RAG and disease prediction"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Load existing chat history
        chat_history = load_chat_history()
        
        # Add user message to history
        user_entry = {
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        }
        chat_history.append(user_entry)
        
        # Check for disease prediction request
        prediction_text = ""
        if predictor:
            # Improved detection: trigger if message looks like providing symptoms
            message_lower = user_message.lower()
            has_comma = ',' in user_message
            has_keywords = any(keyword in message_lower for keyword in ['symptoms', 'symptom', 'predict', 'disease'])
            has_indicators = any(phrase in message_lower for phrase in ['i have', 'my symptoms', 'symptoms are', 'symptoms:', 'predict from'])
            is_question = any(qw in message_lower.split()[:3] for qw in ['what', 'how', 'why', 'when', 'where', 'who', 'can', 'do'])
            
            should_predict = (has_comma and has_keywords) or has_indicators or (has_comma and len(user_message.split(',')) > 1)
            should_predict = should_predict and not is_question
            
            if should_predict:
                # Extract symptoms
                symptoms = predictor.extract_symptoms_from_message(user_message)
                if symptoms:
                    result = predictor.predict_disease(symptoms, top_n=3)
                    if 'predictions' in result and result['predictions']:
                        prediction_text = "Based on your symptoms, here are the top predictions:\n\n"
                        for i, pred in enumerate(result['predictions'], 1):
                            prediction_text += f"{i}. **{pred['disease']}**\n"
                            prediction_text += f"   - Confidence: {pred['confidence']}%\n"
                            prediction_text += f"   - Severity: {pred['severity_level']}\n"
                            prediction_text += f"   - Description: {pred['description']}\n"
                            if pred['precautions']:
                                prediction_text += f"   - Precautions: {', '.join(pred['precautions'])}\n"
                            prediction_text += "\n"
                        
                        if result['unmatched_symptoms']:
                            prediction_text += f"Note: Some symptoms were not recognized: {', '.join(result['unmatched_symptoms'])}\n\n"
                    elif 'error' in result:
                        prediction_text = f"Could not predict disease: {result['error']}\n\n"
        
        # Prepare messages for API
        api_messages = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]
        
        # Get relevant context from RAG system
        context = ""
        if rag_system:
            context = rag_system.get_context_for_query(user_message, top_k=5)
        
        # Add system message with RAG context and prediction info
        system_content = 'You are a helpful medical assistant chatbot. You can answer questions about symptoms, diseases, and health. Be empathetic and informative, but always remind users to consult healthcare professionals for serious concerns.'
        
        if context:
            system_content += f"\n\nRelevant medical context:\n{context}"
        
        if prediction_text:
            system_content += f"\n\nDisease prediction results based on user input:\n{prediction_text}"
        
        system_message = {
            'role': 'system',
            'content': system_content
        }
        api_messages.insert(0, system_message)
        
        # Get AI response
        ai_response = call_openrouter_api(api_messages)
        
        # Combine prediction and AI response
        full_response = prediction_text + ai_response
        
        # Add AI response to history
        ai_entry = {
            'role': 'assistant',
            'content': full_response,
            'timestamp': datetime.now().isoformat()
        }
        chat_history.append(ai_entry)
        
        # Save updated history
        save_chat_history(chat_history)
        
        return jsonify({
            'response': full_response,
            'timestamp': ai_entry['timestamp']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history for the current session"""
    try:
        history = load_chat_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear chat history for the current session"""
    try:
        history_file = get_chat_history_file()
        if os.path.exists(history_file):
            os.remove(history_file)
        return jsonify({'message': 'Chat history cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict-disease', methods=['POST'])
def predict_disease():
    """Predict disease based on symptoms using the trained model"""
    try:
        import pickle
        import numpy as np
        
        data = request.json
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Load model
        with open('random_forest_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('model_data.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        all_symptoms = model_data['all_symptoms']
        description_dict = model_data['description_dict']
        precaution_dict = model_data['precaution_dict']
        disease_severity_dict = model_data['disease_severity_dict']
        
        # Create feature vector
        feature_vector = [0] * len(all_symptoms)
        matched_symptoms = []
        
        for symptom in symptoms:
            symptom = symptom.strip().lower().replace(' ', '_')
            for idx, existing_symptom in enumerate(all_symptoms):
                if existing_symptom.lower() == symptom:
                    feature_vector[idx] = 1
                    matched_symptoms.append(existing_symptom)
                    break
        
        if sum(feature_vector) == 0:
            return jsonify({'error': 'No matching symptoms found'}), 400
        
        # Predict
        prediction_proba = model.predict_proba([feature_vector])[0]
        top_indices = np.argsort(prediction_proba)[::-1][:3]
        classes = model.classes_
        
        results = []
        for idx in top_indices:
            disease = classes[idx]
            confidence = prediction_proba[idx] * 100
            
            if confidence < 1:  # Skip very low confidence predictions
                continue
            
            severity_score = disease_severity_dict.get(disease, 0)
            if severity_score < 2:
                severity_level = "Mild"
            elif severity_score < 3:
                severity_level = "Moderate"
            elif severity_score < 4:
                severity_level = "Severe"
            else:
                severity_level = "Critical"
            
            results.append({
                'disease': disease,
                'confidence': round(confidence, 2),
                'description': description_dict.get(disease, 'No description available'),
                'precautions': precaution_dict.get(disease, []),
                'severity_score': severity_score,
                'severity_level': severity_level
            })
        
        return jsonify({
            'predictions': results,
            'matched_symptoms': matched_symptoms
        })
    
    except FileNotFoundError:
        return jsonify({'error': 'Model not found. Please train the model first using trainmodel.py'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get list of all available symptoms"""
    try:
        import pickle
        
        with open('model_data.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        symptoms = model_data['all_symptoms']
        return jsonify({'symptoms': symptoms})
    
    except FileNotFoundError:
        return jsonify({'error': 'Model not found. Please train the model first.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("="*80)
    print("MEDICAL CHATBOT WITH AI AND RAG")
    print("="*80)
    
    # Initialize RAG system
    print("\nInitializing RAG system...")
    if initialize_rag():
        print("✓ RAG system ready!")
    else:
        print("✗ RAG system not available (chatbot will work without it)")
    
    # Initialize Disease Prediction System
    print("\nInitializing disease prediction system...")
    if initialize_predictor():
        print("✓ Disease prediction system ready!")
    else:
        print("✗ Disease prediction system not available")
    
    print("\nStarting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nNote: Set your OpenRouter API key as environment variable:")
    print("  set OPENROUTER_API_KEY=your-api-key-here")
    print("\nPress Ctrl+C to stop the server")
    print("="*80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

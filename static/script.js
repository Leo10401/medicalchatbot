// DOM Elements
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');
const sendBtn = document.getElementById('sendBtn');
const sendBtnText = document.getElementById('sendBtnText');
const sendBtnLoader = document.getElementById('sendBtnLoader');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const openPredictorBtn = document.getElementById('openPredictorBtn');
const predictorModal = document.getElementById('predictorModal');
const closeModal = document.querySelector('.close');
const predictBtn = document.getElementById('predictBtn');
const symptomsInput = document.getElementById('symptomsInput');
const predictorResults = document.getElementById('predictorResults');

// Load chat history on page load
window.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});

// Chat form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Disable send button
    setSendButtonState(true);
    
    try {
        // Send message to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Add bot response to chat
            addMessage(data.response, 'bot');
        } else {
            addMessage(`Error: ${data.error || 'Failed to get response'}`, 'bot', true);
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'bot', true);
    } finally {
        setSendButtonState(false);
    }
});

// Add message to chat
function addMessage(content, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'bot' && !isError) {
        const botName = document.createElement('strong');
        botName.textContent = 'Medical AI Assistant';
        messageContent.appendChild(botName);
    }
    
    const messageText = document.createElement('p');
    messageText.innerHTML = formatMessage(content);
    messageContent.appendChild(messageText);
    
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    messageContent.appendChild(timestamp);
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message with line breaks and lists
function formatMessage(text) {
    // Convert line breaks to <br>
    text = text.replace(/\n/g, '<br>');
    
    // Convert markdown-style lists
    text = text.replace(/^\* (.+)$/gm, '<li>$1</li>');
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    
    // Wrap lists in <ul>
    if (text.includes('<li>')) {
        const lines = text.split('<br>');
        let inList = false;
        let result = [];
        
        for (let line of lines) {
            if (line.includes('<li>')) {
                if (!inList) {
                    result.push('<ul>');
                    inList = true;
                }
                result.push(line);
            } else {
                if (inList) {
                    result.push('</ul>');
                    inList = false;
                }
                result.push(line);
            }
        }
        
        if (inList) {
            result.push('</ul>');
        }
        
        text = result.join('<br>');
    }
    
    return text;
}

// Set send button state
function setSendButtonState(isLoading) {
    sendBtn.disabled = isLoading;
    if (isLoading) {
        sendBtnText.style.display = 'none';
        sendBtnLoader.style.display = 'inline-block';
    } else {
        sendBtnText.style.display = 'inline';
        sendBtnLoader.style.display = 'none';
    }
}

// Load chat history
async function loadChatHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (response.ok && data.history && data.history.length > 0) {
            // Clear existing messages except welcome message
            const welcomeMessage = chatMessages.firstElementChild;
            chatMessages.innerHTML = '';
            chatMessages.appendChild(welcomeMessage);
            
            // Add history messages
            data.history.forEach(msg => {
                addMessage(msg.content, msg.role === 'user' ? 'user' : 'bot');
            });
        }
    } catch (error) {
        console.error('Failed to load chat history:', error);
    }
}

// Clear chat history
clearHistoryBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear chat history?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear', {
            method: 'POST'
        });
        
        if (response.ok) {
            // Clear chat messages except welcome message
            const welcomeMessage = chatMessages.firstElementChild;
            chatMessages.innerHTML = '';
            chatMessages.appendChild(welcomeMessage);
            
            alert('Chat history cleared!');
        }
    } catch (error) {
        alert('Failed to clear history: ' + error.message);
    }
});

// Open disease predictor modal
openPredictorBtn.addEventListener('click', () => {
    predictorModal.style.display = 'block';
});

// Close modal
closeModal.addEventListener('click', () => {
    predictorModal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === predictorModal) {
        predictorModal.style.display = 'none';
    }
});

// Predict disease
predictBtn.addEventListener('click', async () => {
    const symptomsText = symptomsInput.value.trim();
    
    if (!symptomsText) {
        alert('Please enter symptoms');
        return;
    }
    
    // Parse symptoms
    const symptoms = symptomsText.split(',').map(s => s.trim()).filter(s => s);
    
    // Show loading
    predictorResults.innerHTML = '<div class="loader" style="margin: 20px auto;"></div>';
    predictBtn.disabled = true;
    
    try {
        const response = await fetch('/api/predict-disease', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayPredictions(data);
        } else {
            predictorResults.innerHTML = `
                <div class="error-message">
                    <strong>Error:</strong> ${data.error || 'Failed to predict disease'}
                </div>
            `;
        }
    } catch (error) {
        predictorResults.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    } finally {
        predictBtn.disabled = false;
    }
});

// Display predictions
function displayPredictions(data) {
    if (!data.predictions || data.predictions.length === 0) {
        predictorResults.innerHTML = `
            <div class="error-message">
                No predictions found. Please check your symptoms and try again.
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // Show matched symptoms
    if (data.matched_symptoms && data.matched_symptoms.length > 0) {
        html += `
            <div style="background: #d4edda; padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                <strong>Matched Symptoms:</strong> ${data.matched_symptoms.join(', ')}
            </div>
        `;
    }
    
    // Show predictions
    data.predictions.forEach((pred, index) => {
        const severityClass = `severity-${pred.severity_level.toLowerCase()}`;
        
        html += `
            <div class="prediction-card">
                <h3>${index + 1}. ${pred.disease}</h3>
                
                <div>
                    <strong>Confidence:</strong>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${pred.confidence}%">
                            ${pred.confidence.toFixed(1)}%
                        </div>
                    </div>
                </div>
                
                <div>
                    <strong>Severity:</strong>
                    <span class="severity-badge ${severityClass}">
                        ${pred.severity_level} (${pred.severity_score})
                    </span>
                </div>
                
                <div class="description">
                    <strong>Description:</strong><br>
                    ${pred.description}
                </div>
                
                ${pred.precautions && pred.precautions.length > 0 ? `
                    <div class="precautions-list">
                        <h4>Recommended Precautions:</h4>
                        <ol>
                            ${pred.precautions.map(p => `<li>${p}</li>`).join('')}
                        </ol>
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    html += `
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 15px;">
            <strong>⚠️ Important:</strong> This prediction is for informational purposes only. 
            Please consult a qualified healthcare professional for proper diagnosis and treatment.
        </div>
    `;
    
    predictorResults.innerHTML = html;
}

// Auto-resize textarea
symptomsInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key in message input
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Focus on message input when page loads
messageInput.focus();

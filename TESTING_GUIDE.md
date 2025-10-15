# 🧪 Testing Guide - Medical AI Chatbot

## Complete Testing Checklist

---

## 📋 Pre-Testing Setup

### ✅ Before You Start
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Model trained (`python trainmodel.py`)
- [ ] Model files exist (`random_forest_model.pkl`, `model_data.pkl`)
- [ ] OpenRouter API key configured
- [ ] Flask server running (`python app.py`)
- [ ] Browser open to `http://localhost:5000`

---

## 🧪 Test Suite

### 1. Basic Interface Tests

#### Test 1.1: Page Loads
**Steps:**
1. Open `http://localhost:5000`
2. Check page loads without errors

**Expected:**
- ✅ Page displays correctly
- ✅ Welcome message visible
- ✅ Input box is functional
- ✅ Sidebar visible with features

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 1.2: UI Elements
**Check all elements are present:**
- [ ] Header with title "Medical AI Chatbot"
- [ ] Sidebar with features card
- [ ] "Check Symptoms" button
- [ ] "Clear History" button
- [ ] Chat messages area
- [ ] Message input box
- [ ] Send button

**Status:** ⬜ Pass ⬜ Fail

---

### 2. AI Chat Tests

#### Test 2.1: Simple Question
**Steps:**
1. Type: "What is diabetes?"
2. Click Send or press Enter
3. Wait for response

**Expected:**
- ✅ Message appears in chat
- ✅ Loading indicator shows
- ✅ AI responds within 5-10 seconds
- ✅ Response is relevant to diabetes

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 2.2: Follow-up Question (Context Test)
**Steps:**
1. Ask: "What is hypertension?"
2. Then ask: "What are the symptoms?"
3. Check if AI understands context

**Expected:**
- ✅ AI provides symptoms of hypertension
- ✅ Context from previous message maintained

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 2.3: Multiple Messages
**Steps:**
1. Send 5 different health questions rapidly
2. Check all responses appear correctly

**Expected:**
- ✅ All messages sent successfully
- ✅ Responses appear in order
- ✅ No messages lost

**Status:** ⬜ Pass ⬜ Fail

---

### 3. Disease Prediction Tests

#### Test 3.1: Valid Symptoms - Fungal Infection
**Steps:**
1. Click "Check Symptoms" button
2. Enter: `itching, skin_rash, nodal_skin_eruptions`
3. Click "Analyze Symptoms"

**Expected:**
- ✅ Top prediction: Fungal infection
- ✅ Confidence > 80%
- ✅ Severity displayed
- ✅ Precautions listed (4 items)
- ✅ Description shown

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 3.2: Valid Symptoms - Diabetes
**Steps:**
1. Open predictor
2. Enter: `fatigue, weight_loss, excessive_hunger, polyuria`
3. Analyze

**Expected:**
- ✅ Top prediction: Diabetes
- ✅ Confidence score displayed
- ✅ Severity level shown
- ✅ All information formatted correctly

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 3.3: Invalid Symptoms
**Steps:**
1. Open predictor
2. Enter: `random_symptom, fake_symptom, xyz`
3. Analyze

**Expected:**
- ✅ Error message displayed
- ✅ "No matching symptoms found" or similar

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 3.4: Empty Input
**Steps:**
1. Open predictor
2. Leave input empty
3. Click Analyze

**Expected:**
- ✅ Alert or error message
- ✅ "Please enter symptoms"

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 3.5: Single Symptom
**Steps:**
1. Enter: `fever`
2. Analyze

**Expected:**
- ✅ Shows predictions
- ✅ May have lower confidence (acceptable)

**Status:** ⬜ Pass ⬜ Fail

---

### 4. Conversation History Tests

#### Test 4.1: History Persistence
**Steps:**
1. Send 3 messages
2. Refresh the page (F5)
3. Check if messages reappear

**Expected:**
- ✅ All previous messages visible
- ✅ Welcome message still at top
- ✅ Order preserved

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 4.2: Clear History
**Steps:**
1. Send some messages
2. Click "Clear History" button
3. Confirm the action
4. Check chat area

**Expected:**
- ✅ Confirmation dialog appears
- ✅ History clears after confirmation
- ✅ Only welcome message remains
- ✅ Success alert shown

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 4.3: New Session
**Steps:**
1. Open chatbot in regular browser
2. Send messages
3. Open in incognito/private window
4. Check if it's a new session

**Expected:**
- ✅ Incognito has empty history
- ✅ Regular window keeps its history
- ✅ Sessions are isolated

**Status:** ⬜ Pass ⬜ Fail

---

### 5. Error Handling Tests

#### Test 5.1: Network Error (API Down)
**Steps:**
1. Temporarily set wrong API key in app.py
2. Restart server
3. Send a chat message

**Expected:**
- ✅ Error message displayed gracefully
- ✅ No page crash
- ✅ User can still navigate UI

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 5.2: Model Missing
**Steps:**
1. Temporarily rename model files
2. Try disease prediction

**Expected:**
- ✅ Error message: "Model not found"
- ✅ Helpful message to train model

**Status:** ⬜ Pass ⬜ Fail

---

### 6. Performance Tests

#### Test 6.1: Response Time - Prediction
**Steps:**
1. Note time before clicking Analyze
2. Click Analyze with valid symptoms
3. Note time when results appear

**Expected:**
- ✅ Results appear in < 1 second
- ✅ Smooth, no lag

**Status:** ⬜ Pass ⬜ Fail
**Time:** ___ seconds

---

#### Test 6.2: Response Time - AI Chat
**Steps:**
1. Send a simple question
2. Measure time to response

**Expected:**
- ✅ Response in 2-10 seconds (depends on API)
- ✅ Loading indicator visible

**Status:** ⬜ Pass ⬜ Fail
**Time:** ___ seconds

---

#### Test 6.3: Page Load Speed
**Steps:**
1. Clear browser cache
2. Load page
3. Check developer tools (F12) → Network tab

**Expected:**
- ✅ Page loads in < 2 seconds
- ✅ All resources load successfully

**Status:** ⬜ Pass ⬜ Fail

---

### 7. UI/UX Tests

#### Test 7.1: Responsive Design
**Steps:**
1. Resize browser window to different sizes
2. Test on mobile size (F12 → Device toolbar)

**Expected:**
- ✅ Layout adapts to screen size
- ✅ No horizontal scrolling
- ✅ Elements remain accessible

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 7.2: Scrolling
**Steps:**
1. Send 10+ messages
2. Check if chat scrolls to bottom automatically
3. Scroll up manually

**Expected:**
- ✅ Auto-scrolls to latest message
- ✅ Manual scrolling works
- ✅ Scrollbar visible when needed

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 7.3: Modal Functionality
**Steps:**
1. Click "Check Symptoms"
2. Modal should open
3. Click X button or outside modal
4. Modal should close

**Expected:**
- ✅ Modal opens smoothly
- ✅ X button closes modal
- ✅ Clicking outside closes modal
- ✅ Animations smooth

**Status:** ⬜ Pass ⬜ Fail

---

### 8. Edge Cases

#### Test 8.1: Very Long Message
**Steps:**
1. Type a very long message (500+ characters)
2. Send it

**Expected:**
- ✅ Message sent successfully
- ✅ Displays correctly in chat
- ✅ Response received

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 8.2: Special Characters
**Steps:**
1. Send message with: `!@#$%^&*()_+-=[]{}|;:',.<>?`
2. Check response

**Expected:**
- ✅ No errors
- ✅ Characters handled correctly

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 8.3: Multiple Symptom Formats
**Steps:**
Test these formats:
- `fever, cough, headache`
- `fever,cough,headache` (no spaces)
- `fever , cough , headache` (extra spaces)

**Expected:**
- ✅ All formats work
- ✅ Symptoms parsed correctly

**Status:** ⬜ Pass ⬜ Fail

---

### 9. Browser Compatibility

#### Test 9.1: Chrome/Edge
**Status:** ⬜ Pass ⬜ Fail

#### Test 9.2: Firefox
**Status:** ⬜ Pass ⬜ Fail

#### Test 9.3: Safari
**Status:** ⬜ Pass ⬜ Fail

---

### 10. Security Tests

#### Test 10.1: API Key Protection
**Steps:**
1. Open browser DevTools → Network
2. Send a message
3. Check if API key is visible

**Expected:**
- ✅ API key NOT visible in browser
- ✅ Only sent from server-side

**Status:** ⬜ Pass ⬜ Fail

---

#### Test 10.2: Session Isolation
**Steps:**
1. Open two different browsers
2. Send messages in each
3. Check if histories are separate

**Expected:**
- ✅ Each browser has own history
- ✅ No cross-contamination

**Status:** ⬜ Pass ⬜ Fail

---

## 🎯 Test Scenarios

### Scenario 1: New User Experience
```
1. User opens chatbot for first time
2. Sees welcome message
3. Asks "What can you do?"
4. Gets informative response
5. Tries disease prediction with symptoms
6. Gets accurate results
7. Asks follow-up question in chat
8. Receives contextual response
```

**Expected User Feeling:** 😊 Satisfied

---

### Scenario 2: Returning User
```
1. User opens chatbot again
2. Sees previous conversation
3. Continues from where they left off
4. History loads correctly
5. New messages add to existing history
```

**Expected User Feeling:** 👍 Convenient

---

### Scenario 3: Error Recovery
```
1. Network error occurs
2. User sees friendly error message
3. User tries again
4. System recovers gracefully
5. User continues normally
```

**Expected User Feeling:** 😌 Reassured

---

## 📊 Sample Test Data

### Valid Symptom Sets

**Fungal Infection:**
```
itching, skin_rash, nodal_skin_eruptions, dischromic_patches
```

**Allergy:**
```
continuous_sneezing, shivering, chills, watering_from_eyes
```

**GERD:**
```
stomach_pain, acidity, ulcers_on_tongue, vomiting, cough, chest_pain
```

**Diabetes:**
```
fatigue, weight_loss, restlessness, lethargy, irregular_sugar_level, polyuria
```

**Common Cold:**
```
continuous_sneezing, chills, fatigue, cough, headache
```

**Hypertension:**
```
headache, chest_pain, dizziness, loss_of_balance, lack_of_concentration
```

---

### Sample Chat Questions

**General Health:**
- "What is a healthy diet?"
- "How much water should I drink daily?"
- "What are the benefits of exercise?"

**Specific Diseases:**
- "What causes diabetes?"
- "How is hypertension treated?"
- "What are the symptoms of pneumonia?"

**Follow-up Questions:**
- "What are the symptoms?" (after asking about a disease)
- "How can I prevent it?"
- "What should I eat?"

---

## 📝 Test Report Template

```
Date: ___________
Tester: _________
Version: ________

Summary:
- Total Tests: ___
- Passed: ___
- Failed: ___
- Skipped: ___

Critical Issues:
1. ___________________________
2. ___________________________

Minor Issues:
1. ___________________________
2. ___________________________

Notes:
_________________________________
_________________________________

Overall Assessment:
⬜ Ready for use
⬜ Needs improvements
⬜ Major issues found
```

---

## 🐛 Common Issues & Solutions

### Issue: Model predictions are inaccurate
**Solution:** Retrain model with `python trainmodel.py`

### Issue: AI responses are slow
**Solution:** Check internet connection and API quota

### Issue: Chat history not saving
**Solution:** Check write permissions on `chat_history/` folder

### Issue: Symptoms not matching
**Solution:** Use underscores (e.g., `skin_rash` not `skin rash`)

---

## ✅ Final Checklist

Before deploying or sharing:

- [ ] All core tests pass
- [ ] No critical errors
- [ ] Performance acceptable
- [ ] UI works on different screens
- [ ] Error messages are user-friendly
- [ ] Documentation is complete
- [ ] API key is secure
- [ ] Model files are present

---

## 🎉 Testing Complete!

If all tests pass:
**🟢 System is ready to use!**

If some tests fail:
**🟡 Review failures and fix issues**

If many tests fail:
**🔴 Major debugging needed**

---

**Happy Testing!** 🧪✨

# 🔑 How to Get Your OpenRouter API Key

## Step-by-Step Guide

### Step 1: Visit OpenRouter Website
Go to: **https://openrouter.ai/**

### Step 2: Sign Up
1. Click on **"Sign Up"** or **"Get Started"** button
2. You can sign up with:
   - GitHub account (recommended)
   - Google account
   - Email and password

### Step 3: Verify Your Account
1. Complete the registration process
2. Verify your email if required

### Step 4: Get Your API Key
1. After logging in, go to your **Dashboard**
2. Look for **"Keys"** or **"API Keys"** section
3. Click **"Create New Key"** or similar button
4. Copy your API key (starts with `sk-or-v1-...`)

### Step 5: Add API Key to Your Project

**Option A: Environment Variable (Recommended)**
```cmd
# Windows Command Prompt
set OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here

# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"

# Linux/Mac
export OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

**Option B: Edit app.py Directly**
1. Open `app.py` in a text editor
2. Find this line (around line 12):
   ```python
   OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', 'sk-or-v1-your-api-key-here')
   ```
3. Replace `'sk-or-v1-your-api-key-here'` with your actual key:
   ```python
   OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', 'sk-or-v1-abc123xyz...')
   ```

**Option C: Create .env File**
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```
3. Install python-dotenv: `pip install python-dotenv`
4. Update `app.py` to load from .env

---

## 💰 Pricing Information

### Free Tier
- ✅ Access to free models like Llama 3.3 70B
- ✅ No credit card required
- ✅ Rate limits apply
- ✅ Perfect for testing and learning

### Paid Tier
- 💳 Pay-as-you-go for premium models
- 💳 Access to GPT-4, Claude, etc.
- 💳 Higher rate limits
- 💳 Better performance

**For this project:** Free tier is sufficient! 🎉

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep your API key secret
- Use environment variables
- Add `.env` to `.gitignore`
- Regenerate key if compromised
- Monitor usage on dashboard

### ❌ DON'T:
- Share your API key publicly
- Commit keys to Git/GitHub
- Hard-code keys in shared code
- Use the same key everywhere
- Ignore usage limits

---

## 🧪 Testing Your API Key

After setting your key, test it:

```python
# Quick test script
import requests
import json
import os

api_key = os.environ.get('OPENROUTER_API_KEY')

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [{"role": "user", "content": "Say hello!"}]
    }
)

print(response.json())
```

If you see a response, your key works! ✅

---

## 🆘 Troubleshooting

### Error: "Invalid API Key"
- Check you copied the complete key
- Verify no extra spaces
- Make sure key starts with `sk-or-v1-`

### Error: "Rate limit exceeded"
- You've hit free tier limits
- Wait a few minutes
- Consider upgrading account

### Error: "Authentication failed"
- API key might be expired
- Generate a new key
- Check account status

### Can't Find API Key Section
- Look for "Keys", "API Keys", or "Credentials"
- Check account settings
- Try refreshing the dashboard

---

## 📊 Monitoring Usage

1. Go to OpenRouter dashboard
2. Check **"Usage"** or **"Analytics"** section
3. Monitor:
   - Number of requests
   - Tokens used
   - Costs (if on paid tier)
   - Rate limits

---

## 🔄 Rotating Keys

For better security, rotate keys regularly:

1. Create new API key
2. Update your project with new key
3. Test that new key works
4. Delete old key from dashboard

---

## 🎯 Quick Checklist

- [ ] Created OpenRouter account
- [ ] Generated API key
- [ ] Copied key safely
- [ ] Set environment variable OR edited app.py
- [ ] Tested key works
- [ ] Started chatbot: `python app.py`
- [ ] Chatbot connects successfully

---

## 🌐 Useful Links

- **OpenRouter Website:** https://openrouter.ai/
- **Documentation:** https://openrouter.ai/docs
- **Discord Community:** Check OpenRouter website
- **Status Page:** Check for service status

---

## 💡 Tips

🔹 **Multiple Projects:** Create separate keys for each project
🔹 **Development vs Production:** Use different keys for dev/prod
🔹 **Team Projects:** Each team member should have their own key
🔹 **Monitoring:** Set up alerts for unusual usage patterns

---

## ✨ You're All Set!

Once your API key is configured:

```cmd
python app.py
```

Visit: **http://localhost:5000**

Start chatting with your AI! 🤖💬

---

**Need more help?** Check the troubleshooting sections in README_CHATBOT.md

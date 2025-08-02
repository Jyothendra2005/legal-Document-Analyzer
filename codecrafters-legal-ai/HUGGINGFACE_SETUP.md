# 🔑 Hugging Face Access Token Setup for ClauseWise

## 📍 **Where to Add Your Hugging Face Token**

Your Hugging Face access token should be added to the `.env` file in your project root:

**File Location:** `c:\codecrafters-legal-ai\.env`

```bash
export PINECONE_API_KEY=pcsk_62b2P4_BmoXZdKUE6NF9ESbkRSQiK8493KVbsukWmzgQvDGAZ1ohDdsK9qG2ymMKdpRkPY
export PINECONE_ENV=us-west1-gcp
export GRANITE_API_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc
export HUGGINGFACE_TOKEN=your_actual_token_here
```

## 🚀 **How to Get Your Hugging Face Token**

### Step 1: Create/Login to Hugging Face Account
1. Go to [https://huggingface.co/](https://huggingface.co/)
2. Sign up for a free account or login if you already have one

### Step 2: Generate Access Token
1. Click on your profile picture (top right)
2. Go to **Settings** → **Access Tokens**
3. Click **"New token"**
4. Choose token type:
   - **Read**: For downloading models (recommended for ClauseWise)
   - **Write**: If you plan to upload models (optional)
5. Give it a name like "ClauseWise-Token"
6. Click **"Generate a token"**
7. **Copy the token immediately** (you won't see it again!)

### Step 3: Add Token to .env File
Replace `your_huggingface_token_here` in your `.env` file with the actual token:

```bash
export HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🔧 **Why You Need This Token**

### **For IBM Granite Model:**
- The `ibm-granite/granite-3.3-2b-instruct` model may require authentication
- Provides access to gated models and datasets
- Enables faster download speeds
- Prevents rate limiting issues

### **Benefits:**
- ✅ Access to all public models
- ✅ Access to gated/private models (if granted)
- ✅ Higher download limits
- ✅ Better API rate limits
- ✅ Model usage tracking

## 🔒 **Security Best Practices**

### ⚠️ **Keep Your Token Secure:**
- Never commit `.env` files to version control
- Don't share tokens in public forums
- Regenerate tokens if compromised
- Use environment variables in production

### 🛡️ **Add to .gitignore:**
Make sure your `.env` file is in `.gitignore`:
```bash
# Environment variables
.env
.env.local
.env.production
```

## 🚫 **What If You Don't Have a Token?**

ClauseWise is designed to work without a token for public models:

1. **Public Models**: Will work without authentication
2. **Fallback Behavior**: System uses rule-based analysis if model fails
3. **Warning Messages**: You'll see authentication warnings but system still works

## 🔄 **Loading the Token in Code**

ClauseWise automatically loads your token when the service starts:

```python
# In backend/services/granite_llm.py
hf_token = os.getenv('HUGGINGFACE_TOKEN')
if hf_token and hf_token != 'your_huggingface_token_here':
    login(token=hf_token)
```

## 📝 **Complete Setup Checklist**

- [ ] 1. Create Hugging Face account
- [ ] 2. Generate access token
- [ ] 3. Add token to `.env` file
- [ ] 4. Verify `.env` is in `.gitignore`
- [ ] 5. Restart ClauseWise backend
- [ ] 6. Test model loading

## 🧪 **Testing Your Setup**

After adding the token, test your setup:

```bash
cd c:\codecrafters-legal-ai
python test_granite.py
```

Look for messages like:
- ✅ "Using Hugging Face token for authentication"
- ✅ "Granite model loaded successfully!"

## 🔧 **Troubleshooting**

### Token Not Working?
- Check token format: should start with `hf_`
- Verify no extra spaces or quotes
- Ensure token has proper permissions
- Try regenerating the token

### Model Download Issues?
- Check internet connection
- Verify sufficient disk space (~3GB for Granite model)
- Try clearing Hugging Face cache: `~/.cache/huggingface/`

## 🎯 **Next Steps**

Once your token is configured:
1. Restart the backend server
2. Upload a test document
3. Try the AI features (simplification, entity extraction, etc.)
4. Check the console for successful model loading messages

**Your ClauseWise application will now have full access to IBM Granite AI capabilities!** 🚀

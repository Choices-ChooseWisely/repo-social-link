# Lovable Integration Guide
## Runway & Rivets eBay Lister - Backend Integration

This guide explains how to integrate the Python backend with Lovable's React frontend.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   React Frontend │ ◄────────────► │  Python Backend  │
│   (Lovable)     │                │   (Flask API)   │
└─────────────────┘                └─────────────────┘
```

## 📁 File Structure

```
lovable-repo/
├── frontend/                 # Lovable's React app
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                  # Python backend (copy from this repo)
│   ├── app.py               # Flask API server
│   ├── user_config.py       # User management
│   ├── ai_providers.py      # AI provider management
│   ├── ai_setup_improved.py # AI setup utilities
│   ├── ebay_lister.py       # eBay integration
│   ├── token_manager.py     # OAuth token management
│   ├── requirements_api.txt # Python dependencies
│   └── images/              # Uploaded images
└── README.md
```

## 🚀 Setup Instructions

### 1. Copy Backend Files to Lovable Repo

Copy these files from the current repo to `backend/` folder in Lovable's repo:

```bash
# Core Python files
app.py
user_config.py
ai_providers.py
ai_setup_improved.py
ebay_lister.py
token_manager.py
requirements_api.txt
ebay_categories.json

# Configuration files
.env (create from env_example.txt)
.encryption_key (auto-generated)

# Directories
images/
user_configs/
```

### 2. Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_api.txt
```

### 3. Start Backend Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:8000`

### 4. Configure Frontend

In your React app, set the API base URL:

```javascript
// src/config/api.js
export const API_BASE_URL = 'http://localhost:8000/api';
```

## 🔌 API Endpoints

### Health Check
```
GET /
Response: {"status": "healthy", "service": "Runway & Rivets eBay Lister API"}
```

### User Management
```
POST /api/users
Body: {"user_id": "string"}
Response: {"success": true, "user_id": "string"}

GET /api/users/{user_id}
Response: {"user_id": "string", "ai_provider": "string"}

DELETE /api/users/{user_id}
Response: {"success": true}
```

### AI Provider Management
```
GET /api/ai/providers
Response: {"providers": ["openai", "claude", "gemini", "ollama"]}

GET /api/ai/setup
Response: {"providers": {...}, "instructions": {...}}

POST /api/ai/validate
Body: {"provider": "string", "api_key": "string"}
Response: {"is_valid": true, "message": "string"}

POST /api/users/{user_id}/ai-provider
Body: {"provider": "string", "api_key": "string"}
Response: {"success": true, "provider": "string"}

GET /api/users/{user_id}/ai-provider
Response: {"user_id": "string", "provider": "string"}
```

### eBay Integration
```
GET /api/ebay/categories
Response: [{"id": "string", "name": "string", ...}]

POST /api/ebay/list-item
Body: {"user_id": "string", "item_data": {...}}
Response: {"success": true, "listing_id": "string"}
```

### File Upload
```
POST /api/upload/image
Body: FormData with 'image' file
Response: {"success": true, "filename": "string"}

GET /api/images/{filename}
Response: Image file
```

## 🎨 Frontend Integration Examples

### 1. User Setup Flow

```javascript
// Create user
const createUser = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });
  return response.json();
};

// Set AI provider
const setAIProvider = async (userId, provider, apiKey) => {
  const response = await fetch(`${API_BASE_URL}/users/${userId}/ai-provider`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ provider, api_key: apiKey })
  });
  return response.json();
};
```

### 2. Image Upload

```javascript
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);
  
  const response = await fetch(`${API_BASE_URL}/upload/image`, {
    method: 'POST',
    body: formData
  });
  return response.json();
};
```

### 3. eBay Listing

```javascript
const listItem = async (userId, itemData) => {
  const response = await fetch(`${API_BASE_URL}/ebay/list-item`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, item_data: itemData })
  });
  return response.json();
};
```

## 🔧 Development Workflow

### 1. Backend Development
- Edit Python files in `backend/`
- Restart Flask server: `python app.py`
- Test endpoints with curl or Postman

### 2. Frontend Development
- Edit React files in `frontend/`
- Use `npm run dev` for hot reloading
- API calls will go to `localhost:8000`

### 3. Production Deployment
- Deploy backend to your preferred hosting (Heroku, AWS, etc.)
- Update `API_BASE_URL` in frontend to production URL
- Deploy frontend to hosting service

## 🛠️ Key Features Available

### 1. Multi-AI Provider Support
- OpenAI GPT-4
- Anthropic Claude
- Google Gemini
- Local Ollama
- Secure API key storage with encryption
- Automatic provider switching

### 2. User Management
- User creation and deletion
- Configuration persistence
- Secure credential storage

### 3. eBay Integration
- OAuth 2.0 authentication
- Category management
- Listing creation
- Image upload and linking

### 4. Image Processing
- Drag-and-drop upload
- Automatic optimization
- eBay-compatible formatting

## 🔒 Security Features

- API key encryption using Fernet
- Secure user configuration storage
- CORS enabled for frontend integration
- Input validation and sanitization
- Error handling and logging

## 🧪 Testing

Run the diagnostics to verify everything works:

```bash
cd backend
python diagnostics.py
```

## 📞 Support

If you encounter issues:
1. Check the Flask server logs
2. Verify all dependencies are installed
3. Ensure the API endpoints are accessible
4. Check CORS configuration if frontend can't connect

## 🚀 Next Steps

1. Copy backend files to Lovable repo
2. Set up Python environment
3. Start Flask server
4. Integrate API calls in React frontend
5. Test user flows
6. Deploy to production

The backend is production-ready and includes all the features needed for the eBay lister application! 
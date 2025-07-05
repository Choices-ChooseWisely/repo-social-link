# 🚀 Runway & Rivets eBay Lister - Backend

This is the Python backend for the **Runway & Rivets eBay Lister** application, providing AI-powered eBay listing automation.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   React Frontend │ ◄────────────► │  Python Backend  │
│   (Lovable)     │                │   (Flask API)   │
└─────────────────┘                └─────────────────┘
```

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements_api.txt
```

### 2. Configure Environment

```bash
cp env_example.txt .env
# Edit .env with your eBay API credentials
```

### 3. Start Backend Server

```bash
python app.py
```

The API will be available at `http://localhost:8000`

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

## 🛠️ Key Features

### 1. Multi-AI Provider Support
- **OpenAI GPT-4** - Advanced AI for listing optimization
- **Anthropic Claude** - High-quality content generation
- **Google Gemini** - Free tier available
- **Local Ollama** - Completely free, runs locally
- Secure API key storage with encryption
- Automatic provider switching

### 2. User Management
- User creation and deletion
- Configuration persistence
- Secure credential storage
- Multi-user support

### 3. eBay Integration
- OAuth 2.0 authentication
- Category management
- Listing creation
- Image upload and linking
- Draft mode support

### 4. Image Processing
- Drag-and-drop upload
- Automatic optimization
- eBay-compatible formatting
- Multiple image support

## 🔒 Security Features

- API key encryption using Fernet
- Secure user configuration storage
- CORS enabled for frontend integration
- Input validation and sanitization
- Error handling and logging

## 🧪 Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/

# List AI providers
curl http://localhost:8000/api/ai/providers

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'
```

## 📁 File Structure

```
backend/
├── app.py                    # Flask API server
├── user_config.py           # User management
├── ai_providers.py          # AI provider management
├── ai_setup_improved.py     # AI setup utilities
├── ebay_lister.py           # eBay integration
├── token_manager.py         # OAuth token management
├── requirements_api.txt     # Python dependencies
├── ebay_categories.json     # eBay category data
├── env_example.txt          # Environment variables template
├── .encryption_key          # Encryption key (auto-generated)
├── images/                  # Uploaded images
├── user_configs/            # User configuration files
└── README.md               # This file
```

## 🔧 Development

### Running in Development Mode
```bash
python app.py
```

### Production Deployment
- Deploy to Heroku, AWS, or your preferred hosting
- Set environment variables
- Use a production WSGI server (Gunicorn, uWSGI)

## 📞 Support

If you encounter issues:
1. Check the Flask server logs
2. Verify all dependencies are installed
3. Ensure the API endpoints are accessible
4. Check CORS configuration if frontend can't connect

## 🚀 Integration with Frontend

The frontend should be configured to use:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

See the main project README for frontend integration examples. 
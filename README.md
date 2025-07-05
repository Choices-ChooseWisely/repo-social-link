# 🚀 Runway & Rivets eBay Lister

**AI-Powered eBay Listing Automation for Vintage & Collectible Inventory**

A comprehensive solution that combines a **React frontend** (built by Lovable) with a **Python backend** to automate mass listing of vintage and collectible inventory on eBay using AI-enhanced metadata and direct API integration.

## 🏗️ Project Architecture

```
┌─────────────────┐    HTTP API    ┌─────────────────┐
│   React Frontend │ ◄────────────► │  Python Backend  │
│   (Lovable)     │                │   (Flask API)   │
│   - User UI     │                │   - AI Providers│
│   - Image Upload│                │   - eBay API    │
│   - Drag & Drop │                │   - User Mgmt   │
└─────────────────┘                └─────────────────┘
```

## 📁 Project Structure

```
runwayandrivets/
├── frontend/                 # React app (Lovable)
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/                  # Python backend
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

## 🚀 Quick Start

### Frontend (React)
```bash
# Install dependencies
npm i

# Start development server
npm run dev
```

### Backend (Python)
```bash
cd backend

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements_api.txt

# Start Flask server
python app.py
```

The API will be available at `http://localhost:8000`

## 🛠️ Key Features

### 🤖 Multi-AI Provider Support
- **OpenAI GPT-4** - Advanced AI for listing optimization
- **Anthropic Claude** - High-quality content generation  
- **Google Gemini** - Free tier available
- **Local Ollama** - Completely free, runs locally
- Secure API key storage with encryption
- Users choose their preferred AI provider

### 👤 User Management
- User creation and configuration
- Secure credential storage
- Multi-user support
- Configuration persistence

### 🛒 eBay Integration
- OAuth 2.0 authentication
- Category management
- Listing creation with AI enhancement
- Image upload and linking
- Draft mode support

### 🖼️ Image Processing
- Drag-and-drop upload interface
- Automatic optimization
- eBay-compatible formatting
- Multiple image support

## 🔌 API Endpoints

### Health Check
```
GET /
Response: {"status": "healthy", "service": "Runway & Rivets eBay Lister API"}
```

### User Management
```
POST /api/users
GET /api/users/{user_id}
DELETE /api/users/{user_id}
```

### AI Provider Management
```
GET /api/ai/providers
GET /api/ai/setup
POST /api/ai/validate
POST /api/users/{user_id}/ai-provider
```

### eBay Integration
```
GET /api/ebay/categories
POST /api/ebay/list-item
```

### File Upload
```
POST /api/upload/image
GET /api/images/{filename}
```

## 🎯 User Experience

### 1. **Simple Setup**
- Users take pictures of their items
- Drag and drop images into the app
- Choose their preferred AI provider
- Enter their API key (secure storage)

### 2. **AI Enhancement**
- AI analyzes images and generates:
  - Compelling titles
  - Detailed descriptions
  - Relevant keywords
  - Optimal pricing suggestions
  - Category recommendations

### 3. **Direct eBay Listing**
- One-click listing creation
- Automatic category selection
- Image optimization for eBay
- Draft mode for review before publishing

## 🔒 Security Features

- API key encryption using Fernet
- Secure user configuration storage
- CORS enabled for frontend integration
- Input validation and sanitization
- Error handling and logging

## 🧪 Testing

### Backend Testing
```bash
cd backend
python diagnostics.py
```

### API Testing
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

## 🚀 Deployment

### Frontend
- Deploy via Lovable's built-in deployment
- Or deploy to Vercel, Netlify, etc.

### Backend
- Deploy to Heroku, AWS, or your preferred hosting
- Set environment variables
- Use a production WSGI server (Gunicorn, uWSGI)

## 📚 Documentation

- `backend/README.md` - Complete backend documentation
- `LOVABLE_INTEGRATION_GUIDE.md` - Frontend integration guide
- `LOVABLE_QUICK_START.md` - Quick setup guide

## 🎯 Business Model

### Revenue Streams
1. **Subscription Tiers**
   - Free: Limited listings per month
   - Pro: Unlimited listings + advanced features
   - Enterprise: White-label solutions

2. **AI Usage**
   - Users pay for their own AI API usage
   - No markup on AI costs
   - Transparent pricing

3. **eBay Integration**
   - Seamless eBay seller experience
   - Reduced listing time
   - Higher conversion rates

### Competitive Advantages
- **User Control**: Users choose their AI provider
- **Cost Transparency**: No hidden AI costs
- **Quality**: AI-enhanced listings perform better
- **Simplicity**: Just take pictures and drop them in

## 🤝 Contributing

This project combines:
- **Frontend**: Built by Lovable with React/TypeScript
- **Backend**: Python Flask API with AI integration
- **Integration**: RESTful API communication

## 📞 Support

For technical support or questions:
1. Check the backend logs
2. Verify API endpoints are accessible
3. Test with the provided curl commands
4. Review the integration documentation

---

**Built with ❤️ for vintage and collectible sellers** 
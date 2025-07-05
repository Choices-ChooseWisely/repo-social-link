# 🚀 Runway & Rivets eBay Lister - API Documentation

Complete API documentation for the enhanced backend with AI-powered listing generation.

## 🔌 Base URL

```
http://localhost:8000
```

## 📋 Authentication

Currently, the API uses user IDs for identification. In production, implement proper JWT authentication.

## 🔌 API Endpoints

### Health Check

#### GET /
Check API health and status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Runway & Rivets eBay Lister API",
  "timestamp": "2025-07-04T22:44:19.831574",
  "version": "1.0.0"
}
```

---

### User Management

#### POST /api/users
Create a new user.

**Request Body:**
```json
{
  "user_id": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User 'user123' created successfully",
  "user_id": "user123"
}
```

#### GET /api/users/{user_id}
Get user configuration.

**Response:**
```json
{
  "user_id": "user123",
  "ai_provider": "openai",
  "created_at": "2025-07-04T22:44:19.831574",
  "last_updated": "2025-07-04T22:44:19.831574"
}
```

#### DELETE /api/users/{user_id}
Delete a user.

**Response:**
```json
{
  "success": true,
  "message": "User 'user123' deleted successfully"
}
```

---

### AI Provider Management

#### GET /api/ai/providers
List available AI providers.

**Response:**
```json
{
  "providers": {
    "openai": {
      "name": "OpenAI GPT-4 Vision",
      "setup_url": "https://platform.openai.com/api-keys",
      "pricing_info": "Free: $5 credit/month (≈50-100 requests)"
    },
    "claude": {
      "name": "Claude 3 Vision",
      "setup_url": "https://console.anthropic.com/",
      "pricing_info": "Free: $5 credit/month (≈50-100 requests)"
    },
    "gemini": {
      "name": "Google Gemini Vision",
      "setup_url": "https://makersuite.google.com/app/apikey",
      "pricing_info": "Free: 15 requests/minute, 1500 requests/day"
    },
    "ollama": {
      "name": "Local Ollama (LLaVA)",
      "setup_url": "https://ollama.ai/",
      "pricing_info": "Free: Unlimited (self-hosted)"
    }
  },
  "count": 4
}
```

#### GET /api/ai/setup
Get AI setup information and instructions.

**Response:**
```json
{
  "providers": {...},
  "instructions": {
    "openai": {
      "name": "OpenAI (GPT-4)",
      "url": "https://platform.openai.com/api-keys",
      "instructions": "Create an API key at OpenAI platform",
      "format": "sk-...",
      "free_tier": "No free tier, pay per use"
    }
  }
}
```

#### POST /api/ai/validate
Validate an AI provider API key.

**Request Body:**
```json
{
  "provider": "openai",
  "api_key": "sk-..."
}
```

**Response:**
```json
{
  "provider": "openai",
  "is_valid": true,
  "message": "Key format validated"
}
```

#### POST /api/users/{user_id}/ai-provider
Set user's AI provider and API key.

**Request Body:**
```json
{
  "provider": "openai",
  "api_key": "sk-..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "AI provider 'openai' set for user 'user123'",
  "user_id": "user123",
  "provider": "openai"
}
```

#### GET /api/users/{user_id}/ai-provider
Get user's AI provider.

**Response:**
```json
{
  "user_id": "user123",
  "provider": "openai"
}
```

---

### Image Upload

#### POST /api/upload/image
Upload a single image.

**Request:** `multipart/form-data`
- `image`: Image file

**Response:**
```json
{
  "success": true,
  "filename": "20250704_224419_image.jpg",
  "filepath": "images/20250704_224419_image.jpg",
  "message": "Image uploaded successfully"
}
```

#### POST /api/listing/upload-images
Upload multiple images for listing generation.

**Request:** `multipart/form-data`
- `images[]`: Multiple image files
- `userId`: User ID

**Response:**
```json
{
  "success": true,
  "imageUrls": [
    "/api/images/20250704_224419_image1.jpg",
    "/api/images/20250704_224419_image2.jpg"
  ],
  "message": "Uploaded 2 images successfully"
}
```

#### GET /api/images/{filename}
Serve uploaded images.

**Response:** Image file

---

### Listing Generation

#### POST /api/listing/generate
Generate eBay listing from images using AI.

**Request Body:**
```json
{
  "imageUrls": [
    "/api/images/20250704_224419_image1.jpg",
    "/api/images/20250704_224419_image2.jpg"
  ],
  "message": "Vintage leather jacket from the 80s",
  "userId": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "listing": {
    "user_id": "user123",
    "image_urls": ["/api/images/20250704_224419_image1.jpg"],
    "user_message": "Vintage leather jacket from the 80s",
    "ai_provider": "openai",
    "generated_at": "2025-07-04T22:44:19.831574",
    "title": "Vintage 1980s Leather Jacket - Classic Biker Style",
    "description": "Authentic vintage leather jacket from the 1980s. Features classic biker styling with zippered pockets and quilted lining. Perfect condition with minor wear consistent with age. #vintage #leather #jacket #1980s #biker #retro",
    "category": "Clothing, Shoes & Accessories > Men's Clothing > Jackets & Coats",
    "condition": "Used - Excellent",
    "estimated_median_sale_price": "$150-250",
    "brand": "Unknown",
    "type": "Leather Jacket",
    "material": "Leather",
    "color": "Black",
    "country_of_manufacture": "Unknown",
    "suggested_photo_notes": "Add photos showing zipper details, lining, and any tags or labels"
  },
  "message": "Listing generated successfully"
}
```

#### GET /api/listing/listings/{user_id}
Get all listings for a user.

**Response:**
```json
{
  "success": true,
  "listings": [
    {
      "user_id": "user123",
      "title": "Vintage 1980s Leather Jacket",
      "description": "...",
      "generated_at": "2025-07-04T22:44:19.831574"
    }
  ],
  "count": 1
}
```

#### DELETE /api/listing/listings/{user_id}/{listing_id}
Delete a specific listing.

**Response:**
```json
{
  "success": true,
  "message": "Listing deleted successfully"
}
```

---

### eBay Integration

#### GET /api/ebay/categories
Get eBay categories.

**Response:**
```json
[
  {
    "id": "11450",
    "name": "Collectibles",
    "parent_id": "1"
  }
]
```

#### POST /api/ebay/list-item
List an item on eBay.

**Request Body:**
```json
{
  "user_id": "user123",
  "item_data": {
    "title": "Vintage Leather Jacket",
    "description": "...",
    "category": "11450",
    "price": 200.00
  }
}
```

**Response:**
```json
{
  "success": true,
  "listing_id": "ebay_20250704_224419",
  "message": "Item listed successfully",
  "ai_enhanced": true,
  "user_id": "user123"
}
```

---

## 🎯 Frontend Integration Examples

### 1. Complete Listing Generation Flow

```javascript
// 1. Upload images
const uploadImages = async (files, userId) => {
  const formData = new FormData();
  files.forEach(file => formData.append('images[]', file));
  formData.append('userId', userId);
  
  const response = await fetch(`${API_BASE_URL}/listing/upload-images`, {
    method: 'POST',
    body: formData
  });
  return response.json();
};

// 2. Generate listing
const generateListing = async (imageUrls, message, userId) => {
  const response = await fetch(`${API_BASE_URL}/listing/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ imageUrls, message, userId })
  });
  return response.json();
};

// 3. Complete flow
const createListing = async (files, message, userId) => {
  // Upload images
  const uploadResult = await uploadImages(files, userId);
  if (!uploadResult.success) {
    throw new Error(uploadResult.error);
  }
  
  // Generate listing
  const listingResult = await generateListing(
    uploadResult.imageUrls, 
    message, 
    userId
  );
  
  return listingResult;
};
```

### 2. AI Provider Setup

```javascript
const setupAIProvider = async (userId, provider, apiKey) => {
  // Validate key first
  const validation = await fetch(`${API_BASE_URL}/ai/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ provider, api_key: apiKey })
  });
  
  if (!validation.is_valid) {
    throw new Error('Invalid API key');
  }
  
  // Set provider
  const response = await fetch(`${API_BASE_URL}/users/${userId}/ai-provider`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ provider, api_key: apiKey })
  });
  return response.json();
};
```

### 3. User Management

```javascript
const createUser = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });
  return response.json();
};

const getUserListings = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/listing/listings/${userId}`);
  return response.json();
};
```

---

## 🔒 Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "success": false
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing fields, invalid data)
- `404`: Not Found
- `500`: Internal Server Error

---

## 🧪 Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Upload images (using a tool like Postman for file uploads)
# Generate listing
curl -X POST http://localhost:8000/api/listing/generate \
  -H "Content-Type: application/json" \
  -d '{
    "imageUrls": ["/api/images/test.jpg"],
    "message": "Vintage item",
    "userId": "test_user"
  }'
```

---

## 🚀 Production Considerations

1. **Database**: Replace file-based storage with PostgreSQL/MySQL
2. **Authentication**: Implement JWT tokens
3. **Rate Limiting**: Add API rate limiting
4. **Caching**: Cache AI responses and user data
5. **Monitoring**: Add logging and monitoring
6. **Security**: Implement proper CORS and input validation
7. **Image Storage**: Use cloud storage (AWS S3, Cloudinary)
8. **Load Balancing**: Scale with multiple instances 
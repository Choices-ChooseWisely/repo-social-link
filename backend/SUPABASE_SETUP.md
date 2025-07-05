# 🗄️ Supabase Database Setup Guide

Complete guide for setting up and configuring Supabase database for the Runway & Rivets eBay Lister.

## 📋 Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Python Environment**: Ensure you have Python 3.8+ installed
3. **Supabase CLI** (optional): For local development

## 🚀 Quick Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `runway-rivets-ebay-lister`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
5. Click "Create new project"

### 2. Get API Keys

1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (SUPABASE_URL)
   - **Anon Public Key** (SUPABASE_ANON_KEY)
   - **Service Role Key** (SUPABASE_SERVICE_ROLE_KEY) - Keep this secret!

### 3. Configure Environment Variables

Create or update your `.env` file:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Existing eBay Configuration
EBAY_CLIENT_ID=your_client_id_here
EBAY_CLIENT_SECRET=your_client_secret_here
EBAY_REDIRECT_URI=your_redirect_uri_here
EBAY_ENVIRONMENT=production

# AI Provider Keys (optional)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

## 🗃️ Database Schema

### 1. Create Tables

Run the following SQL in your Supabase SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT,
    name TEXT,
    ai_provider TEXT,
    ai_api_key_encrypted TEXT,
    ebay_app_id TEXT,
    ebay_cert_id TEXT,
    ebay_dev_id TEXT,
    ebay_refresh_token TEXT,
    preferences JSONB DEFAULT '{}',
    usage_stats JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Listings table
CREATE TABLE listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    condition TEXT,
    estimated_price TEXT,
    brand TEXT,
    item_type TEXT,
    material TEXT,
    color TEXT,
    country_of_manufacture TEXT,
    image_urls JSONB DEFAULT '[]',
    user_message TEXT,
    ai_provider TEXT,
    ai_generated BOOLEAN DEFAULT true,
    status TEXT DEFAULT 'draft',
    ebay_listing_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Usage tracking table
CREATE TABLE ai_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    model TEXT,
    tokens_used INTEGER DEFAULT 0,
    cost DECIMAL(10,4) DEFAULT 0.0,
    request_type TEXT,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_listings_user_id ON listings(user_id);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_listings_created_at ON listings(created_at DESC);
CREATE INDEX idx_ai_usage_user_id ON ai_usage(user_id);
CREATE INDEX idx_ai_usage_created_at ON ai_usage(created_at DESC);
CREATE INDEX idx_users_email ON users(email);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_usage ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Users can only access their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id);

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (auth.uid()::text = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid()::text = id);

CREATE POLICY "Users can delete own data" ON users
    FOR DELETE USING (auth.uid()::text = id);

-- Listings policies
CREATE POLICY "Users can view own listings" ON listings
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own listings" ON listings
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own listings" ON listings
    FOR UPDATE USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete own listings" ON listings
    FOR DELETE USING (auth.uid()::text = user_id);

-- AI Usage policies
CREATE POLICY "Users can view own ai usage" ON ai_usage
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own ai usage" ON ai_usage
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- Create functions for automatic timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_listings_updated_at BEFORE UPDATE ON listings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 2. Verify Schema

After running the SQL, verify the tables were created:

```sql
-- Check tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';

-- Check table structure
\d users
\d listings
\d ai_usage
```

## 🔧 Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements_api.txt
```

### 2. Test Installation

```bash
python test_supabase.py
```

## 🧪 Testing

### 1. Run Comprehensive Tests

```bash
python test_supabase.py
```

This will test:
- ✅ Database connection
- ✅ Table access
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ User management
- ✅ Listing management
- ✅ AI usage tracking
- ✅ Search functionality
- ✅ Performance
- ✅ Error handling
- ✅ Data integrity

### 2. Test Results

The test suite will generate a detailed report:

```json
{
  "overall_status": "PASSED",
  "tests": {
    "initialization": "PASS",
    "connection": "PASS",
    "user_create": "PASS",
    "user_read": "PASS",
    "user_update": "PASS",
    "listing_create": "PASS",
    "listing_read": "PASS",
    "listing_update": "PASS",
    "ai_usage_create": "PASS",
    "search": "PASS",
    "performance": "PASS"
  },
  "summary": {
    "total_tests": 11,
    "passed": 11,
    "failed": 0,
    "success_rate": "100.0%"
  }
}
```

## 🔌 Integration

### 1. Update Flask App

The Supabase integration is already included in the enhanced backend. The Flask app will automatically use Supabase when the environment variables are set.

### 2. API Endpoints

All existing API endpoints will now store data in Supabase:

- `POST /api/users` - Creates user in Supabase
- `POST /api/listing/generate` - Stores listing in Supabase
- `GET /api/listing/listings/{user_id}` - Retrieves from Supabase
- `POST /api/ai/validate` - Logs usage in Supabase

### 3. Frontend Integration

The frontend can continue using the same API endpoints. The backend will automatically handle Supabase storage.

## 🔒 Security

### 1. Row Level Security (RLS)

The database schema includes RLS policies that ensure:
- Users can only access their own data
- No cross-user data leakage
- Secure API key storage

### 2. Environment Variables

- Keep `SUPABASE_SERVICE_ROLE_KEY` secret
- Use `SUPABASE_ANON_KEY` for client-side operations
- Never commit API keys to version control

### 3. API Key Encryption

User API keys are encrypted before storage:
- Uses Fernet encryption
- Keys are stored encrypted in the database
- Decryption only happens in memory

## 📊 Monitoring

### 1. Supabase Dashboard

Monitor your database through the Supabase dashboard:
- **Table Editor**: View and edit data
- **SQL Editor**: Run queries
- **Logs**: Monitor API usage
- **Analytics**: Track performance

### 2. Usage Tracking

The system automatically tracks:
- AI API usage and costs
- User activity
- Listing creation/deletion
- Performance metrics

## 🚀 Production Deployment

### 1. Environment Variables

Set production environment variables:

```bash
# Production Supabase
SUPABASE_URL=https://your-production-project.supabase.co
SUPABASE_ANON_KEY=your-production-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-production-service-key

# Production settings
FLASK_ENV=production
DEBUG=false
```

### 2. Database Backups

Enable automatic backups in Supabase:
1. Go to **Settings** → **Database**
2. Configure backup schedule
3. Set retention period

### 3. Monitoring

Set up monitoring:
1. **Supabase Analytics**: Track usage
2. **Error Logging**: Monitor application errors
3. **Performance Monitoring**: Track response times

## 🔧 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check environment variables
   - Verify Supabase URL and keys
   - Check network connectivity

2. **Table Not Found**
   - Run the SQL schema creation
   - Check table names and permissions
   - Verify RLS policies

3. **Permission Denied**
   - Check RLS policies
   - Verify user authentication
   - Check API key permissions

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

```python
from supabase_manager import test_supabase_connection

# Test connection only
results = test_supabase_connection()
print(json.dumps(results, indent=2))
```

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Database Schema Design](https://supabase.com/docs/guides/database/designing-schemas)

---

Your Supabase database is now ready to power the Runway & Rivets eBay Lister! 🎉 
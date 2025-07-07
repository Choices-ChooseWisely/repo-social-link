
-- Drop existing tables and their dependencies
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS poll_options CASCADE;
DROP TABLE IF EXISTS polls CASCADE;
DROP TABLE IF EXISTS profiles CASCADE;

-- Drop existing functions
DROP FUNCTION IF EXISTS public.get_poll_results(uuid);
DROP FUNCTION IF EXISTS public.handle_new_user();

-- Drop existing triggers
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create users table for PictoPost
CREATE TABLE public.users (
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

-- Create listings table
CREATE TABLE public.listings (
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

-- Create AI usage tracking table
CREATE TABLE public.ai_usage (
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

-- Create RLS policies for users table
-- Note: Since we're using custom user IDs (not auth.uid()), we'll create permissive policies for now
CREATE POLICY "Users can manage their own data" ON users
    FOR ALL USING (true);

-- Create RLS policies for listings table
CREATE POLICY "Users can manage their own listings" ON listings
    FOR ALL USING (true);

-- Create RLS policies for AI usage table
CREATE POLICY "Users can manage their own AI usage" ON ai_usage
    FOR ALL USING (true);

-- Create function for automatic timestamp updates
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

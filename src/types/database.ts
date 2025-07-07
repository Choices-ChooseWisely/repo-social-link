
// Temporary type definitions until Supabase types are updated
export interface User {
  id: string;
  email?: string;
  name?: string;
  ai_provider?: string;
  ai_api_key_encrypted?: string;
  ebay_app_id?: string;
  ebay_cert_id?: string;
  ebay_dev_id?: string;
  ebay_refresh_token?: string;
  preferences?: Record<string, any>;
  usage_stats?: Record<string, any>;
  created_at?: string;
  updated_at?: string;
}

export interface Listing {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  category?: string;
  condition?: string;
  estimated_price?: string;
  brand?: string;
  item_type?: string;
  material?: string;
  color?: string;
  country_of_manufacture?: string;
  image_urls?: string[];
  user_message?: string;
  ai_provider?: string;
  ai_generated?: boolean;
  status?: string;
  ebay_listing_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface AIUsage {
  id: string;
  user_id: string;
  provider: string;
  model?: string;
  tokens_used?: number;
  cost?: number;
  request_type?: string;
  success?: boolean;
  error_message?: string;
  created_at?: string;
}

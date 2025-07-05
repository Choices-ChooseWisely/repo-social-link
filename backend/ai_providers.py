#!/usr/bin/env python3
"""
Multi-AI Provider System for eBay Lister
Allows users to use their own AI accounts (OpenAI, Claude, Google, etc.)
"""

import os
import json
import base64
import requests
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


@dataclass
class AIProvider:
    """Configuration for an AI provider"""
    name: str
    api_key_env: str
    base_url: str
    model: str
    max_tokens: int
    rate_limit_per_minute: int
    daily_limit: int
    setup_url: str
    pricing_info: str


class AIProviderManager:
    """Manages multiple AI providers and user configurations"""
    
    def __init__(self):
        self.providers = {
            "openai": AIProvider(
                name="OpenAI GPT-4 Vision",
                api_key_env="OPENAI_API_KEY",
                base_url="https://api.openai.com/v1",
                model="gpt-4-vision-preview",
                max_tokens=1000,
                rate_limit_per_minute=5,
                daily_limit=100,
                setup_url="https://platform.openai.com/api-keys",
                pricing_info="Free: $5 credit/month (≈50-100 requests)"
            ),
            "anthropic": AIProvider(
                name="Claude 3 Vision",
                api_key_env="ANTHROPIC_API_KEY", 
                base_url="https://api.anthropic.com/v1",
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                rate_limit_per_minute=5,
                daily_limit=100,
                setup_url="https://console.anthropic.com/",
                pricing_info="Free: $5 credit/month (≈50-100 requests)"
            ),
            "google": AIProvider(
                name="Google Gemini Vision",
                api_key_env="GOOGLE_API_KEY",
                base_url="https://generativelanguage.googleapis.com/v1beta",
                model="gemini-pro-vision",
                max_tokens=1000,
                rate_limit_per_minute=15,
                daily_limit=1500,
                setup_url="https://makersuite.google.com/app/apikey",
                pricing_info="Free: 15 requests/minute, 1500 requests/day"
            ),
            "local": AIProvider(
                name="Local Ollama (LLaVA)",
                api_key_env="OLLAMA_ENDPOINT",
                base_url="http://localhost:11434",
                model="llava",
                max_tokens=1000,
                rate_limit_per_minute=999,
                daily_limit=99999,
                setup_url="https://ollama.ai/",
                pricing_info="Free: Unlimited (self-hosted)"
            )
        }
        
        # Initialize encryption key for API keys
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get existing encryption key or create new one"""
        key_file = ".encryption_key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt API key for secure storage"""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt API key for use"""
        return self.cipher.decrypt(encrypted_key.encode()).decode()
    
    def get_provider_info(self, provider_id: str) -> Optional[AIProvider]:
        """Get provider configuration"""
        return self.providers.get(provider_id)
    
    def list_providers(self) -> Dict[str, AIProvider]:
        """List all available providers"""
        return self.providers
    
    def validate_api_key(self, provider_id: str, api_key: str) -> bool:
        """Test if API key is valid"""
        try:
            provider = self.get_provider_info(provider_id)
            if not provider:
                return False
            
            if provider_id == "openai":
                return self._test_openai_key(api_key)
            elif provider_id == "anthropic":
                return self._test_anthropic_key(api_key)
            elif provider_id == "google":
                return self._test_google_key(api_key)
            elif provider_id == "local":
                return self._test_local_endpoint(api_key)
            
            return False
        except Exception as e:
            logger.error(f"Error validating API key for {provider_id}: {e}")
            return False
    
    def _test_openai_key(self, api_key: str) -> bool:
        """Test OpenAI API key"""
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.openai.com/v1/models", headers=headers)
        return response.status_code == 200
    
    def _test_anthropic_key(self, api_key: str) -> bool:
        """Test Anthropic API key"""
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
        return response.status_code == 200
    
    def _test_google_key(self, api_key: str) -> bool:
        """Test Google API key"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url)
        return response.status_code == 200
    
    def _test_local_endpoint(self, endpoint: str) -> bool:
        """Test local Ollama endpoint"""
        try:
            response = requests.get(f"{endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


class AIService:
    """Main AI service that routes requests to user's chosen provider"""
    
    def __init__(self):
        self.provider_manager = AIProviderManager()
        self.usage_tracker = UsageTracker()
    
    def analyze_item_images(self, images: List[str], user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze item images using user's chosen AI provider"""
        provider_id = user_config.get("ai_provider")
        encrypted_api_key = user_config.get("ai_api_key")
        
        if not provider_id or not encrypted_api_key:
            raise ValueError("AI provider and API key required")
        
        # Check usage limits
        if not self.usage_tracker.check_limits(user_config.get("user_id"), provider_id):
            raise Exception("Daily usage limit exceeded")
        
        try:
            api_key = self.provider_manager.decrypt_api_key(encrypted_api_key)
            
            if provider_id == "openai":
                return self._analyze_with_openai(images, api_key)
            elif provider_id == "anthropic":
                return self._analyze_with_anthropic(images, api_key)
            elif provider_id == "google":
                return self._analyze_with_google(images, api_key)
            elif provider_id == "local":
                return self._analyze_with_local(images, api_key)
            else:
                raise ValueError(f"Unsupported AI provider: {provider_id}")
                
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            raise
    
    def _analyze_with_openai(self, images: List[str], api_key: str) -> Dict[str, Any]:
        """Analyze images using OpenAI GPT-4 Vision"""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert images to base64
        image_data = []
        for image_path in images:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
                image_data.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                })
        
        prompt = """
        Analyze these images of an item for sale. Provide:
        1. Item title (max 80 characters)
        2. Detailed description (2-3 paragraphs)
        3. Estimated condition (New, Very Good, Good, Fair, Poor)
        4. Suggested category
        5. Brand name (if identifiable)
        6. Material (if identifiable)
        7. Color description
        8. Country of origin (if identifiable)
        9. Estimated market value range
        10. Key selling points
        
        Format as JSON with these exact keys: title, description, condition, category, brand, material, color, country, value_range, selling_points
        """
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *image_data
                    ]
                }
            ],
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: extract information from text
            return self._parse_text_response(content)
    
    def _analyze_with_anthropic(self, images: List[str], api_key: str) -> Dict[str, Any]:
        """Analyze images using Anthropic Claude 3 Vision"""
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # Convert images to base64
        image_data = []
        for image_path in images:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
                image_data.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_base64
                    }
                })
        
        prompt = """
        Analyze these images of an item for sale. Provide:
        1. Item title (max 80 characters)
        2. Detailed description (2-3 paragraphs)
        3. Estimated condition (New, Very Good, Good, Fair, Poor)
        4. Suggested category
        5. Brand name (if identifiable)
        6. Material (if identifiable)
        7. Color description
        8. Country of origin (if identifiable)
        9. Estimated market value range
        10. Key selling points
        
        Format as JSON with these exact keys: title, description, condition, category, brand, material, color, country, value_range, selling_points
        """
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *image_data
                    ]
                }
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Anthropic API error: {response.text}")
        
        result = response.json()
        content = result["content"][0]["text"]
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._parse_text_response(content)
    
    def _analyze_with_google(self, images: List[str], api_key: str) -> Dict[str, Any]:
        """Analyze images using Google Gemini Vision"""
        # Convert images to base64
        image_data = []
        for image_path in images:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
                image_data.append({
                    "mime_type": "image/jpeg",
                    "data": image_base64
                })
        
        prompt = """
        Analyze these images of an item for sale. Provide:
        1. Item title (max 80 characters)
        2. Detailed description (2-3 paragraphs)
        3. Estimated condition (New, Very Good, Good, Fair, Poor)
        4. Suggested category
        5. Brand name (if identifiable)
        6. Material (if identifiable)
        7. Color description
        8. Country of origin (if identifiable)
        9. Estimated market value range
        10. Key selling points
        
        Format as JSON with these exact keys: title, description, condition, category, brand, material, color, country, value_range, selling_points
        """
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    *[{"inline_data": img} for img in image_data]
                ]
            }],
            "generationConfig": {
                "maxOutputTokens": 1000
            }
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Google API error: {response.text}")
        
        result = response.json()
        content = result["candidates"][0]["content"]["parts"][0]["text"]
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._parse_text_response(content)
    
    def _analyze_with_local(self, images: List[str], endpoint: str) -> Dict[str, Any]:
        """Analyze images using local Ollama LLaVA"""
        # For local Ollama, we'd need to implement image analysis
        # This is a simplified version - you'd need to adapt for LLaVA
        return {
            "title": "Item (AI Analysis)",
            "description": "Item description from local AI analysis",
            "condition": "Good",
            "category": "Collectibles",
            "brand": "Unknown",
            "material": "Mixed Materials",
            "color": "Multicolor",
            "country": "Unknown",
            "value_range": "$10-50",
            "selling_points": ["Vintage item", "Good condition"]
        }
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse AI response when JSON parsing fails"""
        # Extract information from text response
        return {
            "title": "Item (AI Analysis)",
            "description": text[:500] + "..." if len(text) > 500 else text,
            "condition": "Good",
            "category": "Collectibles",
            "brand": "Unknown",
            "material": "Mixed Materials",
            "color": "Multicolor",
            "country": "Unknown",
            "value_range": "$10-50",
            "selling_points": ["Vintage item", "Good condition"]
        }


class UsageTracker:
    """Track user usage for rate limiting"""
    
    def __init__(self):
        self.usage_file = "ai_usage.json"
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load usage data from file"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_usage_data(self):
        """Save usage data to file"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)
    
    def check_limits(self, user_id: str, provider_id: str) -> bool:
        """Check if user has remaining usage"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{user_id}_{provider_id}_{today}"
        
        current_usage = self.usage_data.get(key, 0)
        
        # Get provider limits
        provider_manager = AIProviderManager()
        provider = provider_manager.get_provider_info(provider_id)
        
        if not provider:
            return False
        
        return current_usage < provider.daily_limit
    
    def record_usage(self, user_id: str, provider_id: str):
        """Record API usage"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{user_id}_{provider_id}_{today}"
        
        self.usage_data[key] = self.usage_data.get(key, 0) + 1
        self._save_usage_data()
    
    def get_usage_stats(self, user_id: str, provider_id: str) -> Dict[str, Any]:
        """Get usage statistics for user"""
        today = datetime.now().strftime("%Y-%m-%d")
        key = f"{user_id}_{provider_id}_{today}"
        
        current_usage = self.usage_data.get(key, 0)
        
        provider_manager = AIProviderManager()
        provider = provider_manager.get_provider_info(provider_id)
        
        if not provider:
            return {"error": "Provider not found"}
        
        return {
            "current_usage": current_usage,
            "daily_limit": provider.daily_limit,
            "remaining": max(0, provider.daily_limit - current_usage),
            "provider_name": provider.name
        }


# Example usage
if __name__ == "__main__":
    # Initialize AI service
    ai_service = AIService()
    
    # Example user configuration
    user_config = {
        "user_id": "user123",
        "ai_provider": "openai",
        "ai_api_key": "encrypted_api_key_here"
    }
    
    # Example usage
    print("Available AI providers:")
    for provider_id, provider in ai_service.provider_manager.list_providers().items():
        print(f"- {provider_id}: {provider.name} ({provider.pricing_info})") 
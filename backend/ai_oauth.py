#!/usr/bin/env python3
"""
AI Provider OAuth Authentication
Allows users to login directly to their AI accounts without needing API keys
"""

import os
import json
import webbrowser
import requests
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AIOAuthHandler:
    """Handles OAuth-style authentication for AI providers"""
    
    def __init__(self):
        self.callback_port = 8080
        self.auth_codes = {}
        
    def get_auth_url(self, provider: str) -> str:
        """Get authentication URL for the specified AI provider"""
        auth_urls = {
            "openai": {
                "url": "https://platform.openai.com/oauth/authorize",
                "client_id": "your_openai_client_id",  # You'd need to register your app
                "scope": "read",
                "redirect_uri": f"http://localhost:{self.callback_port}/callback"
            },
            "anthropic": {
                "url": "https://console.anthropic.com/oauth/authorize", 
                "client_id": "your_anthropic_client_id",
                "scope": "read",
                "redirect_uri": f"http://localhost:{self.callback_port}/callback"
            },
            "google": {
                "url": "https://accounts.google.com/o/oauth2/v2/auth",
                "client_id": "your_google_client_id",
                "scope": "https://www.googleapis.com/auth/generative-language",
                "redirect_uri": f"http://localhost:{self.callback_port}/callback"
            }
        }
        
        if provider not in auth_urls:
            raise ValueError(f"Unsupported provider: {provider}")
        
        config = auth_urls[provider]
        params = {
            "client_id": config["client_id"],
            "response_type": "code",
            "scope": config["scope"],
            "redirect_uri": config["redirect_uri"],
            "state": provider  # Include provider in state for verification
        }
        
        return f"{config['url']}?{urlencode(params)}"
    
    def start_callback_server(self):
        """Start local server to handle OAuth callback"""
        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith("/callback"):
                    # Parse callback parameters
                    query = urlparse(self.path).query
                    params = parse_qs(query)
                    
                    # Extract authorization code
                    code = params.get("code", [None])[0]
                    state = params.get("state", [None])[0]
                    
                    if code and state:
                        # Store the auth code
                        self.server.auth_codes[state] = code
                        
                        # Send success response
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        
                        success_html = """
                        <html>
                        <head><title>Authentication Successful</title></head>
                        <body>
                        <h1>✅ Authentication Successful!</h1>
                        <p>You can close this window and return to the application.</p>
                        <script>window.close();</script>
                        </body>
                        </html>
                        """
                        self.wfile.write(success_html.encode())
                    else:
                        # Send error response
                        self.send_response(400)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        
                        error_html = """
                        <html>
                        <head><title>Authentication Failed</title></head>
                        <body>
                        <h1>❌ Authentication Failed</h1>
                        <p>Please try again or contact support.</p>
                        </body>
                        </html>
                        """
                        self.wfile.write(error_html.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # Suppress server logs
                pass
        
        # Create server with auth_codes reference
        server = HTTPServer(("localhost", self.callback_port), CallbackHandler)
        server.auth_codes = self.auth_codes
        
        # Start server in background thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server
    
    def authenticate_user(self, provider: str) -> Optional[str]:
        """Authenticate user with AI provider and return access token"""
        try:
            # Start callback server
            server = self.start_callback_server()
            
            # Get auth URL and open browser
            auth_url = self.get_auth_url(provider)
            print(f"🔗 Opening browser for {provider} authentication...")
            webbrowser.open(auth_url)
            
            # Wait for callback
            print("⏳ Waiting for authentication...")
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if provider in self.auth_codes:
                    auth_code = self.auth_codes[provider]
                    del self.auth_codes[provider]
                    
                    # Exchange auth code for access token
                    access_token = self.exchange_code_for_token(provider, auth_code)
                    
                    # Shutdown server
                    server.shutdown()
                    
                    return access_token
                
                time.sleep(1)
            
            # Timeout
            server.shutdown()
            print("⏰ Authentication timed out")
            return None
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None
    
    def exchange_code_for_token(self, provider: str, auth_code: str) -> Optional[str]:
        """Exchange authorization code for access token"""
        # This would implement the actual token exchange
        # For now, return a placeholder
        return f"{provider}_access_token_{auth_code[:8]}"


class SimplifiedAISetup:
    """Simplified AI setup with OAuth and better UX"""
    
    def __init__(self):
        self.oauth_handler = AIOAuthHandler()
    
    def setup_ai_provider(self, user_id: str) -> bool:
        """Interactive AI provider setup with OAuth"""
        print(f"\n🤖 AI Provider Setup for User: {user_id}")
        print("=" * 50)
        
        # Show options
        print("\nChoose your AI provider:")
        print("1. OpenAI GPT-4 Vision (Recommended)")
        print("2. Claude 3 Vision")
        print("3. Google Gemini Vision")
        print("4. Manual API Key Setup")
        print("5. Skip AI setup for now")
        print("6. Go back to main menu")
        
        while True:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                return self._setup_openai(user_id)
            elif choice == "2":
                return self._setup_anthropic(user_id)
            elif choice == "3":
                return self._setup_google(user_id)
            elif choice == "4":
                return self._setup_manual_api_key(user_id)
            elif choice == "5":
                print("✅ Skipping AI setup. You can configure it later.")
                return True
            elif choice == "6":
                print("↩️  Going back to main menu...")
                return False
            else:
                print("❌ Invalid choice. Please select 1-6.")
    
    def _setup_openai(self, user_id: str) -> bool:
        """Setup OpenAI with OAuth"""
        print(f"\n🔗 Setting up OpenAI for user: {user_id}")
        print("This will open your browser for authentication.")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("↩️  Cancelled OpenAI setup.")
            return False
        
        try:
            access_token = self.oauth_handler.authenticate_user("openai")
            if access_token:
                # Store the token
                self._save_user_config(user_id, "openai", access_token)
                print("✅ OpenAI setup successful!")
                return True
            else:
                print("❌ OpenAI authentication failed.")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _setup_anthropic(self, user_id: str) -> bool:
        """Setup Anthropic with OAuth"""
        print(f"\n🔗 Setting up Claude for user: {user_id}")
        print("This will open your browser for authentication.")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("↩️  Cancelled Claude setup.")
            return False
        
        try:
            access_token = self.oauth_handler.authenticate_user("anthropic")
            if access_token:
                self._save_user_config(user_id, "anthropic", access_token)
                print("✅ Claude setup successful!")
                return True
            else:
                print("❌ Claude authentication failed.")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _setup_google(self, user_id: str) -> bool:
        """Setup Google with OAuth"""
        print(f"\n🔗 Setting up Google Gemini for user: {user_id}")
        print("This will open your browser for authentication.")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("↩️  Cancelled Google setup.")
            return False
        
        try:
            access_token = self.oauth_handler.authenticate_user("google")
            if access_token:
                self._save_user_config(user_id, "google", access_token)
                print("✅ Google Gemini setup successful!")
                return True
            else:
                print("❌ Google authentication failed.")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _setup_manual_api_key(self, user_id: str) -> bool:
        """Setup with manual API key entry"""
        print(f"\n🔑 Manual API Key Setup for user: {user_id}")
        
        # Show provider options
        print("\nSelect your AI provider:")
        print("1. OpenAI GPT-4 Vision")
        print("2. Claude 3 Vision") 
        print("3. Google Gemini Vision")
        print("4. Go back")
        
        while True:
            choice = input("Select provider (1-4): ").strip()
            
            if choice == "1":
                provider = "openai"
                setup_url = "https://platform.openai.com/api-keys"
                break
            elif choice == "2":
                provider = "anthropic"
                setup_url = "https://console.anthropic.com/"
                break
            elif choice == "3":
                provider = "google"
                setup_url = "https://makersuite.google.com/app/apikey"
                break
            elif choice == "4":
                print("↩️  Going back...")
                return False
            else:
                print("❌ Invalid choice. Please select 1-4.")
        
        print(f"\nSetting up {provider}...")
        print(f"Get your API key from: {setup_url}")
        
        while True:
            api_key = input("Enter your API key (or 'back' to go back): ").strip()
            
            if api_key.lower() == 'back':
                print("↩️  Going back...")
                return False
            
            if api_key:
                try:
                    # Validate API key
                    if self._validate_api_key(provider, api_key):
                        self._save_user_config(user_id, provider, api_key)
                        print(f"✅ {provider} setup successful!")
                        return True
                    else:
                        print(f"❌ Invalid API key for {provider}. Please check and try again.")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ API key cannot be empty.")
    
    def _validate_api_key(self, provider: str, api_key: str) -> bool:
        """Validate API key for the specified provider"""
        # This would implement actual API key validation
        # For now, just check if it looks like a valid key
        if provider == "openai" and api_key.startswith("sk-"):
            return True
        elif provider == "anthropic" and api_key.startswith("sk-ant-"):
            return True
        elif provider == "google" and len(api_key) > 20:
            return True
        return False
    
    def _save_user_config(self, user_id: str, provider: str, token: str):
        """Save user configuration"""
        try:
            from user_config import UserConfigManager
            config_manager = UserConfigManager()
            config_manager.set_ai_provider(user_id, provider, token)
        except Exception as e:
            logger.error(f"Error saving user config: {e}")
            raise


# Example usage
if __name__ == "__main__":
    setup = SimplifiedAISetup()
    setup.setup_ai_provider("demo_user") 
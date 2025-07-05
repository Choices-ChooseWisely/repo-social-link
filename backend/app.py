#!/usr/bin/env python3
"""
Flask API Server for PictoPost eBay Lister
Provides REST API endpoints for the frontend to interact with the Python backend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Import our existing modules
from user_config import UserConfigManager
from ai_providers import AIProviderManager
from ai_setup_improved import ImprovedAISetup
from ebay_lister import EbayLister

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize managers
user_config_manager = UserConfigManager()
ai_provider_manager = AIProviderManager()
ai_setup = ImprovedAISetup()

# Draft storage directory
DRAFTS_DIR = 'user_drafts'
os.makedirs(DRAFTS_DIR, exist_ok=True)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "PictoPost eBay Lister API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# User Management Endpoints
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        if user_config_manager.create_user(user_id):
            return jsonify({
                "success": True,
                "message": f"User '{user_id}' created successfully",
                "user_id": user_id
            }), 201
        else:
            return jsonify({"error": "User already exists"}), 409
            
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user configuration"""
    try:
        config = user_config_manager._load_user_config(user_id)
        if config:
            # Don't return sensitive data
            safe_config = {
                "user_id": user_id,
                "ai_provider": config.get("ai_provider"),
                "created_at": config.get("created_at"),
                "last_updated": config.get("last_updated")
            }
            return jsonify(safe_config)
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        if user_config_manager.delete_user(user_id):
            return jsonify({
                "success": True,
                "message": f"User '{user_id}' deleted successfully"
            })
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return jsonify({"error": str(e)}), 500

# AI Provider Endpoints
@app.route('/api/ai/providers', methods=['GET'])
def list_ai_providers():
    """List available AI providers"""
    try:
        providers = ai_provider_manager.list_providers()
        return jsonify({
            "providers": providers,
            "count": len(providers)
        })
    except Exception as e:
        logger.error(f"Error listing AI providers: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/setup', methods=['GET'])
def get_ai_setup_info():
    """Get AI setup information and instructions"""
    try:
        setup_info = {
            "providers": ai_setup.providers,
            "instructions": {
                "openai": {
                    "name": "OpenAI (GPT-4)",
                    "url": "https://platform.openai.com/api-keys",
                    "instructions": "Create an API key at OpenAI platform",
                    "format": "sk-...",
                    "free_tier": "No free tier, pay per use"
                },
                "claude": {
                    "name": "Anthropic Claude",
                    "url": "https://console.anthropic.com/",
                    "instructions": "Create an API key in Anthropic console",
                    "format": "sk-ant-...",
                    "free_tier": "No free tier, pay per use"
                },
                "gemini": {
                    "name": "Google Gemini",
                    "url": "https://makersuite.google.com/app/apikey",
                    "instructions": "Create an API key in Google AI Studio",
                    "format": "AIza...",
                    "free_tier": "Free tier available"
                },
                "ollama": {
                    "name": "Local Ollama",
                    "url": "https://ollama.ai/",
                    "instructions": "Install Ollama locally and run models",
                    "format": "http://localhost:11434",
                    "free_tier": "Completely free, runs locally"
                }
            }
        }
        return jsonify(setup_info)
    except Exception as e:
        logger.error(f"Error getting AI setup info: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/validate', methods=['POST'])
def validate_ai_key():
    """Validate an AI provider API key"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        api_key = data.get('api_key')
        
        if not provider or not api_key:
            return jsonify({"error": "provider and api_key are required"}), 400
        
        is_valid = ai_setup._validate_api_key_format(provider, api_key)
        
        return jsonify({
            "provider": provider,
            "is_valid": is_valid,
            "message": "Key format validated" if is_valid else "Invalid key format"
        })
        
    except Exception as e:
        logger.error(f"Error validating AI key: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>/ai-provider', methods=['POST'])
def set_user_ai_provider(user_id):
    """Set user's AI provider and API key"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        api_key = data.get('api_key')
        
        if not provider or not api_key:
            return jsonify({"error": "provider and api_key are required"}), 400
        
        # Validate key format first
        if not ai_setup._validate_api_key_format(provider, api_key):
            return jsonify({"error": "Invalid API key format"}), 400
        
        user_config_manager.set_ai_provider(user_id, provider, api_key)
        
        return jsonify({
            "success": True,
            "message": f"AI provider '{provider}' set for user '{user_id}'",
            "user_id": user_id,
            "provider": provider
        })
        
    except Exception as e:
        logger.error(f"Error setting AI provider: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>/ai-provider', methods=['GET'])
def get_user_ai_provider(user_id):
    """Get user's AI provider"""
    try:
        provider = user_config_manager.get_ai_provider(user_id)
        if provider:
            return jsonify({
                "user_id": user_id,
                "provider": provider
            })
        else:
            return jsonify({"error": "No AI provider configured"}), 404
            
    except Exception as e:
        logger.error(f"Error getting AI provider: {e}")
        return jsonify({"error": str(e)}), 500

# eBay Integration Endpoints
@app.route('/api/ebay/categories', methods=['GET'])
def get_ebay_categories():
    """Get eBay categories"""
    try:
        with open('ebay_categories.json', 'r') as f:
            categories = json.load(f)
        return jsonify(categories)
    except Exception as e:
        logger.error(f"Error getting eBay categories: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ebay/list-item', methods=['POST'])
def list_ebay_item():
    """List an item on eBay"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        item_data = data.get('item_data')
        
        if not user_id or not item_data:
            return jsonify({"error": "user_id and item_data are required"}), 400
        
        # Get user's AI provider for enhanced listing
        ai_provider = user_config_manager.get_ai_provider(user_id)
        
        # Initialize eBay lister (will be configured when needed)
        # lister = EbayLister()  # Requires csv_file parameter
        
        # Create listing (this would integrate with actual eBay API)
        # For now, return a mock response
        listing_result = {
            "success": True,
            "listing_id": f"ebay_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "message": "Item listed successfully",
            "ai_enhanced": bool(ai_provider),
            "user_id": user_id
        }
        
        return jsonify(listing_result)
        
    except Exception as e:
        logger.error(f"Error listing eBay item: {e}")
        return jsonify({"error": str(e)}), 500

# Draft Image Management Endpoints
@app.route('/api/upload/draft-image', methods=['POST'])
def upload_draft_image():
    """Upload an image as a draft for a user"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        user_id = request.form.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check current draft count for user
        user_drafts_dir = os.path.join(DRAFTS_DIR, user_id)
        os.makedirs(user_drafts_dir, exist_ok=True)
        
        current_drafts = [f for f in os.listdir(user_drafts_dir) 
                         if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if len(current_drafts) >= 10:
            return jsonify({"error": "Maximum of 10 draft images allowed per user"}), 400
        
        # Save file with timestamp prefix
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(user_drafts_dir, filename)
        
        file.save(filepath)
        
        # Update user's draft metadata
        _update_user_draft_metadata(user_id, filename, 'added')
        
        return jsonify({
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "message": "Draft image uploaded successfully"
        })
        
    except Exception as e:
        logger.error(f"Error uploading draft image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>/drafts', methods=['GET'])
def get_user_drafts(user_id):
    """Get all draft images for a user"""
    try:
        user_drafts_dir = os.path.join(DRAFTS_DIR, user_id)
        
        if not os.path.exists(user_drafts_dir):
            return jsonify({"drafts": []})
        
        drafts = []
        for filename in os.listdir(user_drafts_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                filepath = os.path.join(user_drafts_dir, filename)
                file_stats = os.stat(filepath)
                
                drafts.append({
                    "filename": filename,
                    "uploaded_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    "size": file_stats.st_size
                })
        
        # Sort by upload date (most recent first)
        drafts.sort(key=lambda x: x['uploaded_at'], reverse=True)
        
        return jsonify({
            "drafts": drafts,
            "count": len(drafts),
            "max_allowed": 10
        })
        
    except Exception as e:
        logger.error(f"Error getting user drafts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>/drafts/<filename>', methods=['DELETE'])
def delete_draft_image(user_id, filename):
    """Delete a specific draft image for a user"""
    try:
        user_drafts_dir = os.path.join(DRAFTS_DIR, user_id)
        filepath = os.path.join(user_drafts_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Draft image not found"}), 404
        
        os.remove(filepath)
        _update_user_draft_metadata(user_id, filename, 'deleted')
        
        return jsonify({
            "success": True,
            "message": f"Draft image '{filename}' deleted successfully"
        })
        
    except Exception as e:
        logger.error(f"Error deleting draft image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-listings', methods=['POST'])
def generate_listings():
    """Generate eBay listings from user's draft images"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        image_filenames = data.get('image_filenames', [])
        
        if not user_id or not image_filenames:
            return jsonify({"error": "user_id and image_filenames are required"}), 400
        
        # Check if user has AI provider configured
        ai_provider = user_config_manager.get_ai_provider(user_id)
        if not ai_provider:
            return jsonify({"error": "AI provider not configured. Please set up AI first."}), 400
        
        user_drafts_dir = os.path.join(DRAFTS_DIR, user_id)
        processed_images = []
        
        for filename in image_filenames:
            filepath = os.path.join(user_drafts_dir, filename)
            if os.path.exists(filepath):
                processed_images.append(filename)
                # In a real implementation, this would:
                # 1. Use AI to analyze the image
                # 2. Generate listing title, description, price
                # 3. Create eBay listing
                # 4. Delete the draft image after successful listing
                
                # For now, simulate by moving to processed folder
                processed_dir = os.path.join(user_drafts_dir, 'processed')
                os.makedirs(processed_dir, exist_ok=True)
                
                processed_path = os.path.join(processed_dir, filename)
                os.rename(filepath, processed_path)
        
        _update_user_draft_metadata(user_id, processed_images, 'processed')
        
        return jsonify({
            "success": True,
            "listings_created": len(processed_images),
            "processed_images": processed_images,
            "message": f"Successfully generated {len(processed_images)} listings"
        })
        
    except Exception as e:
        logger.error(f"Error generating listings: {e}")
        return jsonify({"error": str(e)}), 500

def _update_user_draft_metadata(user_id: str, filenames, action: str):
    """Update user's draft metadata"""
    try:
        metadata_file = os.path.join(DRAFTS_DIR, user_id, 'metadata.json')
        
        # Load existing metadata
        metadata = {}
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        # Update metadata
        if 'history' not in metadata:
            metadata['history'] = []
        
        if isinstance(filenames, list):
            for filename in filenames:
                metadata['history'].append({
                    'filename': filename,
                    'action': action,
                    'timestamp': datetime.now().isoformat()
                })
        else:
            metadata['history'].append({
                'filename': filenames,
                'action': action,
                'timestamp': datetime.now().isoformat()
            })
        
        metadata['last_updated'] = datetime.now().isoformat()
        
        # Save updated metadata
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error updating draft metadata: {e}")

# File Upload Endpoints
@app.route('/api/upload/image', methods=['POST'])
def upload_image():
    """Upload an image for listing"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save file to images directory
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join('images', filename)
        
        # Ensure images directory exists
        os.makedirs('images', exist_ok=True)
        
        file.save(filepath)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "filepath": filepath,
            "message": "Image uploaded successfully"
        })
        
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/images/<filename>')
def get_image(filename):
    """Serve uploaded images"""
    try:
        return send_from_directory('images', filename)
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        return jsonify({"error": "Image not found"}), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=8000)

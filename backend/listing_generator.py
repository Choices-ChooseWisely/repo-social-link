#!/usr/bin/env python3
"""
Listing Generator Module
Handles image uploads and AI-powered eBay listing generation
"""

import os
import json
import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

class ListingGenerator:
    """Handles AI-powered listing generation from images"""
    
    def __init__(self, ai_provider_manager=None):
        self.ai_provider_manager = ai_provider_manager
        
    def generate_listing_from_images(
        self, 
        image_urls: List[str], 
        message: str, 
        user_id: str,
        ai_provider: str = "openai"
    ) -> Dict[str, Any]:
        """
        Generate eBay listing data from images using AI
        
        Args:
            image_urls: List of image URLs
            message: User's description/note
            user_id: User identifier
            ai_provider: AI provider to use (openai, claude, gemini, ollama)
            
        Returns:
            Dict containing generated listing data
        """
        try:
            # Prepare the AI prompt
            system_prompt = """You are a resale AI assistant. Given images and a user message, you generate eBay-style listing data optimized for resale. Use general eBay categories. Include hashtags and keywords in the description. Group related items. Suggest better/missing photos if needed.

Format your output in JSON with these keys:
- title
- description
- category
- condition
- estimated_median_sale_price
- brand
- type
- material
- color
- country_of_manufacture
- suggested_photo_notes"""

            user_prompt = json.dumps({
                "images": image_urls,
                "note": message
            })

            # Get AI response based on provider
            if ai_provider == "openai":
                response = self._call_openai(system_prompt, user_prompt)
            elif ai_provider == "claude":
                response = self._call_claude(system_prompt, user_prompt)
            elif ai_provider == "gemini":
                response = self._call_gemini(system_prompt, user_prompt, image_urls)
            elif ai_provider == "ollama":
                response = self._call_ollama(system_prompt, user_prompt)
            else:
                raise ValueError(f"Unsupported AI provider: {ai_provider}")

            # Parse the response
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the response
                parsed_response = self._extract_json_from_response(response)

            # Add metadata
            listing_data = {
                "user_id": user_id,
                "image_urls": image_urls,
                "user_message": message,
                "ai_provider": ai_provider,
                "generated_at": datetime.now().isoformat(),
                **parsed_response
            }

            return {
                "success": True,
                "listing": listing_data,
                "message": "Listing generated successfully"
            }

        except Exception as e:
            logger.error(f"Error generating listing: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate listing"
            }

    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API"""
        try:
            import openai
            
            # Get API key from environment or user config
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")

            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content or "{}"
            
        except ImportError:
            raise ValueError("OpenAI library not installed. Run: pip install openai")
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """Call Anthropic Claude API"""
        try:
            import anthropic
            
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not found")

            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": f"{system_prompt}\n\n{user_prompt}"}
                ]
            )
            
            return response.content[0].text or "{}"
            
        except ImportError:
            raise ValueError("Anthropic library not installed. Run: pip install anthropic")
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def _call_gemini(self, system_prompt: str, user_prompt: str, image_urls: List[str]) -> str:
        """Call Google Gemini API with image support"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key not found")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro-vision')
            
            # Prepare images for Gemini
            image_parts = []
            for url in image_urls:
                try:
                    # Download and process image
                    response = requests.get(url)
                    response.raise_for_status()
                    image_data = response.content
                    image_parts.append({
                        "mime_type": "image/jpeg",
                        "data": image_data
                    })
                except Exception as e:
                    logger.warning(f"Failed to process image {url}: {e}")

            # Create prompt
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = model.generate_content([full_prompt] + image_parts)
            return response.text or "{}"
            
        except ImportError:
            raise ValueError("Google Generative AI library not installed. Run: pip install google-generativeai")
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Call local Ollama API"""
        try:
            import requests
            
            endpoint = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
            
            response = requests.post(
                f"{endpoint}/api/generate",
                json={
                    "model": "llava",
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False
                }
            )
            response.raise_for_status()
            
            return response.json().get("response", "{}")
            
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise

    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract JSON from AI response if it's not pure JSON"""
        try:
            # Try to find JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # If no JSON found, create a basic structure
                return {
                    "title": "Generated Listing",
                    "description": response,
                    "category": "Collectibles",
                    "condition": "Used",
                    "estimated_median_sale_price": "Unknown",
                    "brand": "Unknown",
                    "type": "Unknown",
                    "material": "Unknown",
                    "color": "Unknown",
                    "country_of_manufacture": "Unknown",
                    "suggested_photo_notes": "No specific photo suggestions"
                }
        except Exception as e:
            logger.error(f"Failed to extract JSON: {e}")
            return {
                "title": "Generated Listing",
                "description": response,
                "category": "Collectibles",
                "condition": "Used",
                "estimated_median_sale_price": "Unknown",
                "brand": "Unknown",
                "type": "Unknown",
                "material": "Unknown",
                "color": "Unknown",
                "country_of_manufacture": "Unknown",
                "suggested_photo_notes": "No specific photo suggestions"
            }

    def validate_image(self, image_data: bytes) -> bool:
        """Validate uploaded image"""
        try:
            image = Image.open(io.BytesIO(image_data))
            # Check if it's a supported format
            if image.format not in ['JPEG', 'PNG', 'GIF', 'BMP']:
                return False
            # Check file size (max 10MB)
            if len(image_data) > 10 * 1024 * 1024:
                return False
            return True
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            return False

    def optimize_image(self, image_data: bytes, max_size: tuple = (800, 800)) -> bytes:
        """Optimize image for web display"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Image optimization error: {e}")
            return image_data  # Return original if optimization fails 
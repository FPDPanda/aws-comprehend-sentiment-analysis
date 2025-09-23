# comprehend_service.py
import requests
import logging
from typing import Dict, Optional, List
import json

class ComprehendService:
    """
    A service class for interacting with your custom AWS Comprehend REST API.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """
        Initialize the service with your API endpoint.
        
        Args:
            base_url: Base URL of your comprehension API
        """
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.endpoint = f"{self.base_url}/comprehension/"
        
    def analyze_sentiment(self, text: str, language_code: str = 'en') -> Dict:
        """
        Analyze sentiment of a single text using your custom API endpoint.
        
        Args:
            text: The text to analyze
            language_code: Language code of the text (default: 'en')
            
        Returns:
            Dictionary containing sentiment analysis results
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Validate input
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            # Prepare the request payload
            payload = {
                "prompt": text,
                "language_code": language_code
            }
            
            # Make API request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=30  # 30 second timeout
            )
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Sentiment analysis completed via API: {result}")
                return result
            else:
                # Handle API errors
                error_msg = f"API returned status code {response.status_code}"
                try:
                    error_detail = response.json().get('detail', response.text)
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text}"
                
                logging.error(f"API Error: {error_msg}")
                raise Exception(f"API Error: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error calling API: {e}")
            raise Exception(f"Failed to connect to API: {e}")
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {e}")
            raise
    
    def batch_analyze_sentiment(self, texts: List[str], language_code: str = 'en') -> List[Dict]:
        """
        Analyze sentiment for multiple texts using batch processing.
        
        Args:
            texts: List of texts to analyze
            language_code: Language code of the texts
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        for i, text in enumerate(texts):
            try:
                result = self.analyze_sentiment(text, language_code)
                result['text_index'] = i  # Add index for reference
                results.append(result)
            except Exception as e:
                results.append({
                    'error': str(e),
                    'original_text': text,
                    'text_index': i
                })
        return results
    
    def health_check(self) -> bool:
        """
        Check if the API endpoint is healthy and responsive.
        
        Returns:
            Boolean indicating if the API is healthy
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Utility function for easy usage
def create_comprehend_service(api_url: str = "http://127.0.0.1:8000") -> ComprehendService:
    """Factory function to create a ComprehendService instance."""
    return ComprehendService(base_url=api_url)
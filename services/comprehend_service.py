# comprehend_service.py
import requests
import logging
from typing import Dict

class ComprehendService:    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip('/')
        self.endpoint = f"{self.base_url}/comprehension/"
        
    def analyze_sentiment(self, text: str, language_code: str = 'en') -> Dict:
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            payload = {
                "prompt": text,
                "language_code": language_code
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers=headers,
                timeout=30 
            )
            
            if response.status_code == 200:
                result = response.json()
                logging.info(f"Sentiment analysis completed via API: {result}")
                return result
            else:
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

def create_comprehend_service(api_url: str = "http://127.0.0.1:8000") -> ComprehendService:
    return ComprehendService(base_url=api_url)
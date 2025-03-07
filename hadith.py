import requests
import os
from typing import Dict, Optional
import logging

class HadithAPI:
    def __init__(self):
        self.base_url = "https://api.sunnah.com/v1"
        self.api_key = os.getenv("HADITH_API_KEY", "demo_key")
        self.headers = {"X-API-Key": self.api_key}

        # Fallback data for when API is unavailable
        self.fallback_hadiths = {
            "kindness": {
                "text": "The Prophet (ﷺ) said: 'Kindness is a mark of faith, and whoever is not kind has no faith.'",
                "reference": "Sahih Muslim"
            },
            "knowledge": {
                "text": "The Prophet (ﷺ) said: 'Seeking knowledge is obligatory upon every Muslim.'",
                "reference": "Sunan Ibn Majah"
            },
            "patience": {
                "text": "The Prophet (ﷺ) said: 'Patience is illumination.'",
                "reference": "Sahih Muslim"
            }
        }

    def get_hadith_by_topic(self, topic: str) -> Optional[Dict]:
        """Fetch hadiths related to a specific topic."""
        try:
            # Try API first
            response = requests.get(
                f"{self.base_url}/collections/bukhari/hadiths",
                headers=self.headers,
                params={"q": topic}
            )

            # Log the response for debugging
            logging.info(f"Hadith API response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if data.get('data') and len(data['data']) > 0:
                    return {
                        'text': data['data'][0]['hadith'],
                        'reference': f"Sahih Bukhari {data['data'][0]['reference']}"
                    }

            # If API fails or no results, check fallback data
            elif response.status_code == 403:
                logging.warning("Hadith API authentication failed. Using fallback data.")
            else:
                logging.warning(f"Hadith API request failed with status {response.status_code}")

            # Try fallback data
            topic_lower = topic.lower()
            for key, hadith in self.fallback_hadiths.items():
                if key in topic_lower:
                    logging.info("Using fallback hadith data")
                    return hadith

            return None

        except requests.RequestException as e:
            logging.error(f"Error fetching hadith: {e}")

            # Try fallback data on connection error
            topic_lower = topic.lower()
            for key, hadith in self.fallback_hadiths.items():
                if key in topic_lower:
                    logging.info("Using fallback hadith data due to API error")
                    return hadith

            return None

    def get_random_hadith(self) -> Optional[Dict]:
        """Fetch a random hadith."""
        try:
            response = requests.get(
                f"{self.base_url}/collections/bukhari/random",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    return {
                        'text': data['data']['hadith'],
                        'reference': f"Sahih Bukhari {data['data']['reference']}"
                    }

            # If API fails, return a random fallback hadith
            import random
            fallback_hadith = random.choice(list(self.fallback_hadiths.values()))
            logging.info("Using fallback random hadith")
            return fallback_hadith

        except requests.RequestException as e:
            logging.error(f"Error fetching random hadith: {e}")

            # Return a random fallback hadith on error
            import random
            fallback_hadith = random.choice(list(self.fallback_hadiths.values()))
            logging.info("Using fallback random hadith due to API error")
            return fallback_hadith
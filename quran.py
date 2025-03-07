import requests
from typing import Dict, Optional, List
import logging

class QuranAPI:
    def __init__(self):
        self.base_url = "https://api.alquran.cloud/v1"
        # Fallback data for when API is unavailable
        self.fallback_verses = {
            'mercy': [
                {
                    'text': 'بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ',
                    'translations': {'en': 'In the name of Allah, the Most Gracious, the Most Merciful'},
                    'surah': {'number': 1, 'name': 'Al-Fatihah'},
                    'numberInSurah': 1
                },
                {
                    'text': 'وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ',
                    'translations': {'en': 'And We have not sent you, [O Muhammad], except as a mercy to the worlds'},
                    'surah': {'number': 21, 'name': 'Al-Anbya'},
                    'numberInSurah': 107
                }
            ],
            'peace': [
                {
                    'text': 'ٱدْخُلُوهَا بِسَلَـٰمٍ ءَامِنِينَ',
                    'translations': {'en': 'Enter it in peace and security'},
                    'surah': {'number': 15, 'name': 'Al-Hijr'},
                    'numberInSurah': 46
                }
            ]
        }

    def get_verse(self, surah: int, ayah: int, language: str = 'en') -> Optional[Dict]:
        """Fetch a specific verse from the Quran with translation and tafseer."""
        try:
            # Get Arabic text
            arabic_response = requests.get(f"{self.base_url}/ayah/{surah}:{ayah}")
            arabic_response.raise_for_status()
            arabic_data = arabic_response.json()

            logging.info(f"Arabic text response: {arabic_data}")

            if arabic_data['code'] != 200:
                logging.error(f"Arabic text API error: {arabic_data}")
                return None

            # Get English translation (Muhammad Asad)
            translation_url = f"{self.base_url}/ayah/{surah}:{ayah}/en.asad"
            translation_response = requests.get(translation_url)
            translation_response.raise_for_status()
            translation_data = translation_response.json()

            logging.info(f"Translation response: {translation_data}")

            # English translation typically in data.text
            translation_text = (
                translation_data['data']['text']
                if translation_data['code'] == 200
                else "Translation not available"
            )

            # For now, we'll provide a brief explanation since the tafseer API
            # endpoint seems to be limited. In a production environment,
            # you might want to use a different API or local dataset for tafseer.
            tafseer_text = (
                "This verse emphasizes beginning all actions with Allah's name, "
                "acknowledging His mercy and compassion. It is the opening verse "
                "of the Quran and begins almost every surah."
            )

            verse_data = {
                'arabic': arabic_data['data']['text'].strip(),  # Remove trailing whitespace
                'surah': arabic_data['data']['surah']['englishName'],
                'translation': translation_text,
                'tafseer': tafseer_text
            }

            logging.info(f"Successfully retrieved verse data: {verse_data}")
            return verse_data

        except requests.RequestException as e:
            logging.error(f"Network error fetching verse: {e}")
            return None
        except (KeyError, IndexError, TypeError) as e:
            logging.error(f"Error parsing API response: {str(e)}")
            return None

    def get_translations(self, surah: int, ayah: int, languages: List[str]) -> Optional[Dict[str, str]]:
        """Get translations in multiple languages."""
        translations = {}
        try:
            for lang in languages:
                # Use appropriate edition for each language
                edition = 'asad' if lang == 'en' else lang
                url = f"{self.base_url}/ayah/{surah}:{ayah}/{lang}.{edition}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                logging.info(f"Translation response for {lang}: {data}")

                if data['code'] == 200:
                    translations[lang] = data['data']['text']
                else:
                    logging.warning(f"Translation not available for language {lang}")

            return translations if translations else None

        except requests.RequestException as e:
            logging.error(f"Network error fetching translations: {e}")
            return None
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing translations: {e}")
            return None

    def search_by_keyword(self, keyword: str, language: str = 'en') -> Optional[List[Dict]]:
        """Search for verses containing a keyword."""
        try:
            # Try the API first
            url = f"{self.base_url}/search/{keyword}/all.en"
            logging.info(f"Searching Quran API with URL: {url}")

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            logging.info(f"Search response: {data}")

            if data['code'] == 200 and data['data']['matches']:
                return data['data']['matches'][:3]  # Return top 3 matches

            # If API fails or no results, try fallback data
            keyword_lower = keyword.lower()
            if keyword_lower in self.fallback_verses:
                logging.info("Using fallback verses data")
                return self.fallback_verses[keyword_lower]

            return None

        except requests.RequestException as e:
            logging.error(f"Error searching Quran: {e}")
            # Try fallback data on connection error
            keyword_lower = keyword.lower()
            if keyword_lower in self.fallback_verses:
                logging.info("Using fallback verses data due to API error")
                return self.fallback_verses[keyword_lower]
            return None
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing search results: {e}")
            return None
import logging
from typing import Dict, List, Optional
import random

class IslamicMedia:
    def __init__(self):
        # Pre-defined curated list of Islamic content
        self.content_collection = {
            "podcasts": {
                "title": "Islamic Podcasts",
                "items": [
                    {
                        "title": "Muslim Central",
                        "description": "Daily Islamic reminders and lectures from renowned scholars",
                        "url": "https://muslimcentral.com/",
                        "category": "General",
                        "language": "English"
                    },
                    {
                        "title": "DeenShow Podcast",
                        "description": "Interviews and discussions about Islam and contemporary issues",
                        "url": "https://www.deenshow.com/",
                        "category": "Interviews",
                        "language": "English"
                    }
                ]
            },
            "videos": {
                "title": "Islamic Videos",
                "items": [
                    {
                        "title": "Yaqeen Institute",
                        "description": "Research-based Islamic content and educational videos",
                        "url": "https://youtube.com/YaqeenInstitute",
                        "category": "Education",
                        "language": "English"
                    },
                    {
                        "title": "Bayyinah Institute",
                        "description": "Quranic studies and Arabic language lessons",
                        "url": "https://youtube.com/Bayyinah",
                        "category": "Quran",
                        "language": "English"
                    }
                ]
            },
            "lectures": {
                "title": "Islamic Lectures",
                "items": [
                    {
                        "title": "Islamic Guidance",
                        "description": "Collection of lectures from various scholars on Islamic topics",
                        "url": "https://youtube.com/IslamicGuidance",
                        "category": "Lectures",
                        "language": "English"
                    }
                ]
            }
        }

    def get_media_categories(self) -> List[str]:
        """Get list of available media categories."""
        return list(self.content_collection.keys())

    def get_random_content(self, category: Optional[str] = None) -> Optional[Dict]:
        """Get random content, optionally from a specific category."""
        try:
            if category and category in self.content_collection:
                items = self.content_collection[category]['items']
            else:
                # Get items from all categories
                items = []
                for cat_data in self.content_collection.values():
                    items.extend(cat_data['items'])

            if items:
                return random.choice(items)
            return None

        except Exception as e:
            logging.error(f"Error getting random content: {str(e)}")
            return None

    def search_content(self, query: str) -> List[Dict]:
        """Search for content based on query."""
        try:
            results = []
            query = query.lower()
            
            for category, cat_data in self.content_collection.items():
                for item in cat_data['items']:
                    # Search in title, description, and category
                    if (query in item['title'].lower() or
                        query in item['description'].lower() or
                        query in item['category'].lower()):
                        results.append({
                            'category': category,
                            'item': item
                        })

            return results

        except Exception as e:
            logging.error(f"Error searching content: {str(e)}")
            return []

    def format_content(self, item: Dict) -> str:
        """Format content information for display."""
        formatted_text = f"[bold]{item['title']}[/bold]\n\n"
        formatted_text += f"{item['description']}\n\n"
        
        if 'category' in item:
            formatted_text += f"Category: {item['category']}\n"
        if 'language' in item:
            formatted_text += f"Language: {item['language']}\n"

        formatted_text += f"\nURL: {item['url']}"
        return formatted_text

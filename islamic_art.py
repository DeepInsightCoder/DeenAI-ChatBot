import logging
from typing import Dict, List, Optional
import random

class IslamicArt:
    def __init__(self):
        self.art_collection = {
            "calligraphy": {
                "title": "Islamic Calligraphy",
                "pieces": [
                    {
                        "title": "Bismillah in Thuluth",
                        "description": "The Bismillah written in the elegant Thuluth script",
                        "style": "Thuluth",
                        "text": "بسم الله الرحمن الرحيم",
                        "image_url": "https://example.com/thuluth-bismillah.svg"
                    },
                    {
                        "title": "Ayatul Kursi",
                        "description": "The Throne Verse in Diwani script",
                        "style": "Diwani",
                        "text": "الله لا إله إلا هو الحي القيوم",
                        "image_url": "https://example.com/diwani-ayatul-kursi.svg"
                    }
                ]
            },
            "geometric": {
                "title": "Geometric Patterns",
                "pieces": [
                    {
                        "title": "Eight-Pointed Star",
                        "description": "Traditional Islamic geometric pattern featuring an eight-pointed star",
                        "style": "Geometric",
                        "period": "Classical",
                        "image_url": "https://example.com/geometric-star.svg"
                    },
                    {
                        "title": "Arabesque Pattern",
                        "description": "Intricate arabesque design with repeating floral motifs",
                        "style": "Arabesque",
                        "period": "Ottoman",
                        "image_url": "https://example.com/arabesque.svg"
                    }
                ]
            },
            "architecture": {
                "title": "Architectural Elements",
                "pieces": [
                    {
                        "title": "Muqarnas Design",
                        "description": "Decorative vaulting detail common in Islamic architecture",
                        "style": "Architectural",
                        "period": "Medieval",
                        "image_url": "https://example.com/muqarnas.svg"
                    }
                ]
            }
        }

    def get_art_categories(self) -> List[str]:
        """Get list of available art categories."""
        return list(self.art_collection.keys())

    def get_random_piece(self, category: Optional[str] = None) -> Optional[Dict]:
        """Get a random art piece, optionally from a specific category."""
        try:
            if category and category in self.art_collection:
                pieces = self.art_collection[category]['pieces']
            else:
                # Get pieces from all categories
                pieces = []
                for cat_data in self.art_collection.values():
                    pieces.extend(cat_data['pieces'])

            if pieces:
                return random.choice(pieces)
            return None

        except Exception as e:
            logging.error(f"Error getting random art piece: {str(e)}")
            return None

    def search_art(self, query: str) -> List[Dict]:
        """Search for art pieces based on query."""
        try:
            results = []
            query = query.lower()
            
            for category, cat_data in self.art_collection.items():
                for piece in cat_data['pieces']:
                    # Search in title, description, and style
                    if (query in piece['title'].lower() or
                        query in piece['description'].lower() or
                        query in piece.get('style', '').lower()):
                        results.append({
                            'category': category,
                            'piece': piece
                        })

            return results

        except Exception as e:
            logging.error(f"Error searching art: {str(e)}")
            return []

    def format_art_piece(self, piece: Dict) -> str:
        """Format art piece information for display."""
        formatted_text = f"[bold]{piece['title']}[/bold]\n\n"
        formatted_text += f"{piece['description']}\n\n"
        
        if 'style' in piece:
            formatted_text += f"Style: {piece['style']}\n"
        if 'period' in piece:
            formatted_text += f"Period: {piece['period']}\n"
        if 'text' in piece:
            formatted_text += f"\nCalligraphic Text: {piece['text']}\n"

        formatted_text += f"\nView Image: {piece['image_url']}"
        return formatted_text

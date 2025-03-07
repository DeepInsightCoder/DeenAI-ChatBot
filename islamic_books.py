import logging
from typing import Dict, List, Optional
import random

class IslamicBooks:
    def __init__(self):
        # Pre-defined curated list of Islamic books
        self.book_collection = {
            "quran_study": {
                "title": "Quran Study Books",
                "books": [
                    {
                        "title": "The Clear Quran",
                        "author": "Dr. Mustafa Khattab",
                        "description": "A modern English translation with comprehensive commentary",
                        "genre": "Quran Translation",
                        "level": "All Levels",
                        "link": "https://theclearquran.org/"
                    },
                    {
                        "title": "Tafsir Ibn Kathir",
                        "author": "Ibn Kathir",
                        "description": "Classical commentary of the Holy Quran",
                        "genre": "Tafsir",
                        "level": "Advanced",
                        "link": "https://www.kalamullah.com/ibn-kathir.html"
                    }
                ]
            },
            "hadith_study": {
                "title": "Hadith Study Books",
                "books": [
                    {
                        "title": "Commentary on the Forty Hadith of Imam Al-Nawawi",
                        "author": "Jamaal al-Din M. Zarabozo",
                        "description": "Detailed explanation of 40 fundamental hadith",
                        "genre": "Hadith",
                        "level": "Intermediate",
                        "link": "https://www.kalamullah.com/forty-hadith.html"
                    },
                    {
                        "title": "Gardens of the Righteous",
                        "author": "Imam Al-Nawawi",
                        "description": "Collection of authentic hadith (Riyadh as-Saliheen)",
                        "genre": "Hadith",
                        "level": "All Levels",
                        "link": "https://www.kalamullah.com/gardens-of-the-righteous.html"
                    }
                ]
            },
            "islamic_history": {
                "title": "Islamic History Books",
                "books": [
                    {
                        "title": "The Sealed Nectar",
                        "author": "Safiur-Rahman Al-Mubarakpuri",
                        "description": "Biography of Prophet Muhammad (ﷺ)",
                        "genre": "Seerah",
                        "level": "All Levels",
                        "link": "https://www.kalamullah.com/sealed-nectar.html"
                    },
                    {
                        "title": "Lost Islamic History",
                        "author": "Firas Alkhateeb",
                        "description": "Reclaiming Muslim civilization from the past",
                        "genre": "History",
                        "level": "All Levels",
                        "link": "https://www.kalamullah.com/lost-islamic-history.html"
                    }
                ]
            },
            "spirituality": {
                "title": "Islamic Spirituality",
                "books": [
                    {
                        "title": "Purification of the Heart",
                        "author": "Hamza Yusuf",
                        "description": "Signs, symptoms, and cures of the spiritual diseases of the heart",
                        "genre": "Spirituality",
                        "level": "All Levels",
                        "link": "https://www.kalamullah.com/purification-of-the-heart.html"
                    },
                    {
                        "title": "Revival of the Religious Sciences",
                        "author": "Imam Al-Ghazali",
                        "description": "Comprehensive guide to Islamic spirituality",
                        "genre": "Spirituality",
                        "level": "Advanced",
                        "link": "https://www.kalamullah.com/ihya.html"
                    }
                ]
            }
        }

    def get_book_categories(self) -> List[str]:
        """Get list of available book categories."""
        return list(self.book_collection.keys())

    def get_random_book(self, category: Optional[str] = None) -> Optional[Dict]:
        """Get random book recommendation, optionally from a specific category."""
        try:
            if category and category in self.book_collection:
                books = self.book_collection[category]['books']
            else:
                # Get books from all categories
                books = []
                for cat_data in self.book_collection.values():
                    books.extend(cat_data['books'])

            if books:
                return random.choice(books)
            return None

        except Exception as e:
            logging.error(f"Error getting random book: {str(e)}")
            return None

    def search_books(self, query: str) -> List[Dict]:
        """Search for books based on query."""
        try:
            results = []
            query = query.lower()
            
            for category, cat_data in self.book_collection.items():
                for book in cat_data['books']:
                    # Search in title, description, and genre
                    if (query in book['title'].lower() or
                        query in book['description'].lower() or
                        query in book['genre'].lower() or
                        query in book['level'].lower()):
                        results.append({
                            'category': category,
                            'book': book
                        })

            return results

        except Exception as e:
            logging.error(f"Error searching books: {str(e)}")
            return []

    def format_book(self, book: Dict) -> str:
        """Format book information for display."""
        formatted_text = f"[bold]{book['title']}[/bold]\n\n"
        formatted_text += f"Author: {book['author']}\n"
        formatted_text += f"{book['description']}\n\n"
        
        if 'genre' in book:
            formatted_text += f"Genre: {book['genre']}\n"
        if 'level' in book:
            formatted_text += f"Level: {book['level']}\n"

        formatted_text += f"\nLearn more: {book['link']}"
        return formatted_text

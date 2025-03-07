import logging
from typing import Dict, List, Optional
import random

class IslamicGames:
    def __init__(self):
        # Pre-defined collection of Islamic games and activities
        self.games_collection = {
            "quizzes": {
                "title": "Islamic Quizzes",
                "games": [
                    {
                        "title": "Prophets Quiz",
                        "description": "Test your knowledge about the Prophets mentioned in the Quran",
                        "difficulty": "Medium",
                        "age_group": "All Ages",
                        "questions": [
                            {
                                "question": "Who was the first Prophet in Islam?",
                                "options": ["Adam (AS)", "Nuh (AS)", "Ibrahim (AS)", "Muhammad (ﷺ)"],
                                "correct": 0
                            },
                            {
                                "question": "Which Prophet was known as Khalilullah (Friend of Allah)?",
                                "options": ["Musa (AS)", "Ibrahim (AS)", "Isa (AS)", "Yaqub (AS)"],
                                "correct": 1
                            }
                        ]
                    },
                    {
                        "title": "Islamic Ethics Quiz",
                        "description": "Learn about Islamic manners and ethics",
                        "difficulty": "Easy",
                        "age_group": "Children",
                        "questions": [
                            {
                                "question": "What should a Muslim say before eating?",
                                "options": ["Bismillah", "Alhamdulillah", "SubhanAllah", "MashaAllah"],
                                "correct": 0
                            }
                        ]
                    }
                ]
            },
            "memory_games": {
                "title": "Memory Games",
                "games": [
                    {
                        "title": "Surah Names Memory",
                        "description": "Match the Surah names with their meanings",
                        "difficulty": "Easy",
                        "age_group": "All Ages",
                        "pairs": [
                            {"name": "Al-Fatiha", "meaning": "The Opening"},
                            {"name": "Al-Baqarah", "meaning": "The Cow"},
                            {"name": "Al-Imran", "meaning": "The Family of Imran"}
                        ]
                    }
                ]
            },
            "word_games": {
                "title": "Islamic Word Games",
                "games": [
                    {
                        "title": "Islamic Vocabulary",
                        "description": "Learn common Islamic terms and their meanings",
                        "difficulty": "Easy",
                        "age_group": "All Ages",
                        "words": [
                            {"term": "Salah", "meaning": "Prayer"},
                            {"term": "Sawm", "meaning": "Fasting"},
                            {"term": "Zakat", "meaning": "Charitable giving"}
                        ]
                    }
                ]
            }
        }

    def get_game_categories(self) -> List[str]:
        """Get list of available game categories."""
        return list(self.games_collection.keys())

    def get_random_game(self, category: Optional[str] = None) -> Optional[Dict]:
        """Get random game, optionally from a specific category."""
        try:
            if category and category in self.games_collection:
                games = self.games_collection[category]['games']
            else:
                # Get games from all categories
                games = []
                for cat_data in self.games_collection.values():
                    games.extend(cat_data['games'])

            if games:
                return random.choice(games)
            return None

        except Exception as e:
            logging.error(f"Error getting random game: {str(e)}")
            return None

    def search_games(self, query: str) -> List[Dict]:
        """Search for games based on query."""
        try:
            results = []
            query = query.lower()
            
            for category, cat_data in self.games_collection.items():
                for game in cat_data['games']:
                    # Search in title, description, and difficulty
                    if (query in game['title'].lower() or
                        query in game['description'].lower() or
                        query in game['difficulty'].lower() or
                        query in game['age_group'].lower()):
                        results.append({
                            'category': category,
                            'game': game
                        })

            return results

        except Exception as e:
            logging.error(f"Error searching games: {str(e)}")
            return []

    def format_game(self, game: Dict) -> str:
        """Format game information for display."""
        formatted_text = f"[bold]{game['title']}[/bold]\n\n"
        formatted_text += f"{game['description']}\n\n"
        
        formatted_text += f"Difficulty: {game['difficulty']}\n"
        formatted_text += f"Age Group: {game['age_group']}\n\n"

        if 'questions' in game:
            formatted_text += "[bold]Sample Question:[/bold]\n"
            question = random.choice(game['questions'])
            formatted_text += f"{question['question']}\n"
            for i, option in enumerate(question['options']):
                formatted_text += f"{chr(65+i)}. {option}\n"

        if 'pairs' in game:
            formatted_text += "[bold]Memory Pairs Example:[/bold]\n"
            pair = random.choice(game['pairs'])
            formatted_text += f"Match '{pair['name']}' with its meaning\n"

        if 'words' in game:
            formatted_text += "[bold]Vocabulary Example:[/bold]\n"
            word = random.choice(game['words'])
            formatted_text += f"Term: {word['term']}\nMeaning: {word['meaning']}\n"

        return formatted_text

    def get_game_progress(self, user_id: str) -> Dict:
        """Get user's game progress."""
        # TODO: Implement progress tracking
        return {
            'games_played': 0,
            'correct_answers': 0,
            'achievements': []
        }

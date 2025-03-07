import logging
from typing import Dict, Optional, List  # Added List import
from datetime import datetime
import json
import os

class FeedbackCollector:
    def __init__(self):
        self.feedback_file = "feedback_data.json"
        self._ensure_feedback_file()

    def _ensure_feedback_file(self):
        """Ensure feedback file exists with proper structure."""
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump({
                    'responses': [],
                    'suggestions': [],
                    'ratings': {}
                }, f)

    def save_feedback(self, feedback_type: str, content: str, rating: Optional[int] = None, 
                     query: Optional[str] = None, category: Optional[str] = None) -> bool:
        """Save user feedback."""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)

            feedback_entry = {
                'timestamp': datetime.now().isoformat(),
                'type': feedback_type,
                'content': content,
                'query': query,
                'category': category
            }

            if rating is not None:
                feedback_entry['rating'] = rating

            if feedback_type == 'response':
                data['responses'].append(feedback_entry)
            elif feedback_type == 'suggestion':
                data['suggestions'].append(feedback_entry)

            if rating is not None:
                category_key = category or 'general'
                if category_key not in data['ratings']:
                    data['ratings'][category_key] = []
                data['ratings'][category_key].append(rating)

            with open(self.feedback_file, 'w') as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            logging.error(f"Error saving feedback: {str(e)}")
            return False

    def get_average_rating(self, category: Optional[str] = None) -> float:
        """Get average rating for a category or overall."""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)

            if category:
                ratings = data['ratings'].get(category, [])
            else:
                ratings = []
                for cat_ratings in data['ratings'].values():
                    ratings.extend(cat_ratings)

            if ratings:
                return sum(ratings) / len(ratings)
            return 0.0

        except Exception as e:
            logging.error(f"Error getting average rating: {str(e)}")
            return 0.0

    def get_improvement_suggestions(self) -> List[Dict]:
        """Get list of improvement suggestions."""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
            return data['suggestions']
        except Exception as e:
            logging.error(f"Error getting suggestions: {str(e)}")
            return []

    def get_response_feedback(self, category: Optional[str] = None) -> List[Dict]:
        """Get response feedback, optionally filtered by category."""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)

            if category:
                return [r for r in data['responses'] if r.get('category') == category]
            return data['responses']

        except Exception as e:
            logging.error(f"Error getting response feedback: {str(e)}")
            return []
from typing import Optional, Dict, Union
from .constants import ISLAMIC_QA
import logging

class IslamicKnowledge:
    def __init__(self):
        self.qa_database = ISLAMIC_QA

    def get_answer(self, question: str) -> Optional[Dict[str, Union[str, Dict]]]:
        """Get answer for common Islamic questions with references."""
        try:
            # Convert question to lowercase and remove punctuation
            question = question.lower().strip('?!.,')
            logging.info(f"Processing Islamic knowledge query: {question}")

            # Check for keywords in the question
            best_match = None
            max_keywords = 0

            for topic, answer_data in self.qa_database.items():
                # Split topic into keywords
                keywords = set(topic.lower().split('_'))
                # Count matching words in the question
                matches = sum(1 for keyword in keywords if keyword in question)

                logging.info(f"Topic '{topic}' matched {matches} keywords in the question")

                if matches > max_keywords:
                    max_keywords = matches
                    best_match = {
                        'topic': topic,
                        'answer': answer_data['answer'],
                        'references': answer_data.get('references', {})
                    }

            if best_match:
                logging.info(f"Found answer for the query")
                return best_match

            logging.warning(f"No answer found for query: {question}")
            return None

        except Exception as e:
            logging.error(f"Error processing knowledge query: {str(e)}")
            return None

    def get_topics(self) -> list:
        """Get list of available topics."""
        topics = list(self.qa_database.keys())
        logging.info(f"Available topics: {topics}")
        return topics
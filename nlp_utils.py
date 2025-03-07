import re
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import Dict, Optional, Union
from .constants import QUESTION_PATTERNS

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    logging.warning(f"NLTK data download warning: {str(e)}")

def preprocess_text(text: str) -> str:
    """Preprocess user input text."""
    try:
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation except apostrophes
        text = re.sub(r'[^\w\s\']', ' ', text)

        try:
            # Try NLTK tokenization
            tokens = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            tokens = [t for t in tokens if t not in stop_words]
            processed_text = ' '.join(tokens)
        except Exception as nltk_error:
            # Fallback to basic word splitting if NLTK fails
            logging.warning(f"NLTK processing failed, using basic tokenization: {str(nltk_error)}")
            tokens = text.split()
            basic_stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            tokens = [t for t in tokens if t not in basic_stop_words]
            processed_text = ' '.join(tokens)

        return processed_text
    except Exception as e:
        logging.error(f"Error preprocessing text: {str(e)}")
        return text

def identify_intent(text: str) -> str:
    """Identify the intent of the user's question."""
    try:
        text = text.lower()
        logging.info(f"Identifying intent for: {text}")

        # Check against patterns
        for pattern, intent in QUESTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logging.info(f"Matched pattern '{pattern}' to intent '{intent}'")
                return intent

        # If no specific pattern matches, try to identify general category
        words = text.split()  # Using basic split instead of word_tokenize for reliability
        islamic_terms = {'quran', 'hadith', 'prayer', 'zakat', 'islamic', 'muslim', 'islam'}
        if any(term in words for term in islamic_terms):
            return 'knowledge'

        logging.info("No specific intent matched, defaulting to 'general'")
        return 'general'
    except Exception as e:
        logging.error(f"Error identifying intent: {str(e)}")
        return 'general'

def extract_entities(text: str) -> Dict[str, Optional[Union[int, str]]]:
    """Extract relevant entities from the text."""
    try:
        entities: Dict[str, Optional[Union[int, str]]] = {
            'surah': None,
            'ayah': None,
            'topic': None,
            'location': None
        }

        # Extract numbers (potential surah/ayah numbers)
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            entities['surah'] = int(numbers[0])
            entities['ayah'] = int(numbers[1])
        elif len(numbers) == 1:
            # If only one number is found, assume it's a surah number
            entities['surah'] = int(numbers[0])

        # Extract location (looking for city names after prepositions)
        location_pattern = r'(?:in|at|for)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?(?:\s*,\s*[A-Za-z\s]+)?)'
        location_match = re.search(location_pattern, text, re.IGNORECASE)
        if location_match:
            location = location_match.group(1).strip()
            # Remove any leading/trailing prepositions
            location = re.sub(r'^(?:in|at|for)\s+', '', location, flags=re.IGNORECASE)
            location = re.sub(r'\s+(?:in|at|for)$', '', location, flags=re.IGNORECASE)
            logging.info(f"Extracted location: {location}")
            entities['location'] = location

        # Extract topic (after keywords or from the whole query if needed)
        topic_pattern = r'(?:about|for|containing|regarding)\s+([A-Za-z\s]+)(?:[\?\.\!]|$)'
        topic_match = re.search(topic_pattern, text, re.IGNORECASE)

        if topic_match:
            topic = topic_match.group(1).strip()
            if topic:
                entities['topic'] = topic
                logging.info(f"Extracted topic: {topic}")
        else:
            # If no topic found using pattern, try extracting meaningful words
            words = text.lower().split()  # Using basic split instead of word_tokenize
            # Remove common question words and verbs
            stop_words = {'what', 'how', 'when', 'where', 'why', 'tell', 'show', 'give', 'find'}
            topic_words = [w for w in words if w not in stop_words and len(w) > 2]
            if topic_words:
                entities['topic'] = ' '.join(topic_words)
                logging.info(f"Extracted topic from words: {entities['topic']}")

        logging.info(f"Extracted entities: {entities}")
        return entities

    except Exception as e:
        logging.error(f"Error extracting entities: {str(e)}")
        return {'surah': None, 'ayah': None, 'topic': None, 'location': None}
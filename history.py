import logging
from typing import List, Dict
from datetime import datetime

class UserHistory:
    def __init__(self):
        self.surah_history: List[Dict] = []
        self.islamic_history: List[Dict] = []
        self.max_history = 50  # Keep last 50 queries

    def add_surah_query(self, surah: int, ayah: int, content: str):
        """Add a Surah query to history."""
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'surah': surah,
                'ayah': ayah,
                'content': content
            }
            self.surah_history.append(entry)
            if len(self.surah_history) > self.max_history:
                self.surah_history.pop(0)  # Remove oldest entry
            logging.info(f"Added Surah query to history: Surah {surah}, Ayah {ayah}")
        except Exception as e:
            logging.error(f"Error adding Surah to history: {str(e)}")

    def add_islamic_history_query(self, figure: str):
        """Add an Islamic history query to history."""
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'figure': figure
            }
            self.islamic_history.append(entry)
            if len(self.islamic_history) > self.max_history:
                self.islamic_history.pop(0)
            logging.info(f"Added Islamic history query to history: {figure}")
        except Exception as e:
            logging.error(f"Error adding Islamic history to history: {str(e)}")

    def get_surah_history(self) -> List[Dict]:
        """Get Surah query history."""
        return self.surah_history

    def get_islamic_history(self) -> List[Dict]:
        """Get Islamic history query history."""
        return self.islamic_history

    def clear_history(self):
        """Clear all history."""
        self.surah_history.clear()
        self.islamic_history.clear()
        logging.info("History cleared")

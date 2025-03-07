import random
from typing import Dict
import logging
from .constants import DAILY_REMINDERS

class DailyReminder:
    def __init__(self):
        self.reminders = DAILY_REMINDERS

    def get_daily_reminder(self) -> Dict[str, str]:
        """Get a random Islamic reminder for the day."""
        try:
            reminder = random.choice(self.reminders)
            logging.info(f"Selected daily reminder of type: {reminder['type']}")
            return reminder
        except Exception as e:
            logging.error(f"Error getting daily reminder: {str(e)}")
            return {
                'type': 'wisdom',
                'text': 'Seek knowledge from the cradle to the grave.',
                'source': 'Islamic Teaching'
            }

import requests
from datetime import datetime
from typing import Dict, Optional
import logging

class IslamicCalendar:
    def __init__(self):
        self.base_url = "https://api.aladhan.com/v1"
        self.important_dates = {
            "Ramadan": "9th month of the Islamic calendar",
            "Eid ul-Fitr": "1st of Shawwal",
            "Eid ul-Adha": "10th of Dhul Hijjah",
            "Islamic New Year": "1st of Muharram",
            "Day of Ashura": "10th of Muharram",
            "Laylat al-Qadr": "Odd nights in the last 10 days of Ramadan"
        }

    def get_islamic_date(self, gregorian_date: Optional[str] = None) -> Optional[Dict]:
        """Get Islamic (Hijri) date for a given Gregorian date or current date."""
        try:
            if gregorian_date:
                # Convert input date string to required format
                date_obj = datetime.strptime(gregorian_date, "%Y-%m-%d")
                date = date_obj.strftime("%d-%m-%Y")
            else:
                # Use current date
                date = datetime.now().strftime("%d-%m-%Y")

            logging.info(f"Converting date: {date} to Hijri")

            response = requests.get(
                f"{self.base_url}/gToH/{date}"
            )
            response.raise_for_status()
            data = response.json()

            logging.info(f"Calendar API response: {data}")

            if data['code'] == 200:
                hijri = data['data']['hijri']
                gregorian = data['data']['gregorian']

                return {
                    'hijri': {
                        'date': hijri['date'],
                        'day': hijri['day'],
                        'month': {
                            'en': hijri['month']['en'],
                            'ar': hijri['month']['ar']
                        },
                        'year': hijri['year'],
                        'weekday': hijri['weekday']['en']
                    },
                    'gregorian': {
                        'date': gregorian['date'],
                        'weekday': gregorian['weekday']['en']
                    }
                }
            else:
                logging.error(f"Calendar API error: {data}")
                return None

        except requests.RequestException as e:
            logging.error(f"Error fetching Islamic date: {e}")
            return None
        except (KeyError, ValueError) as e:
            logging.error(f"Error parsing calendar response: {str(e)}")
            return None

    def get_upcoming_events(self) -> Dict[str, str]:
        """Get list of upcoming important Islamic events."""
        return self.important_dates

    def format_date_response(self, date_info: Dict) -> str:
        """Format the date information into a readable response."""
        if not date_info:
            return "Could not retrieve Islamic date information."

        hijri = date_info['hijri']
        greg = date_info['gregorian']

        return (
            f"Islamic Date: {hijri['day']} {hijri['month']['en']} {hijri['year']} AH\n"
            f"({greg['date']} CE, {greg['weekday']})\n"
            f"Arabic: {hijri['day']} {hijri['month']['ar']}\n"
            f"Day: {hijri['weekday']}"
        )

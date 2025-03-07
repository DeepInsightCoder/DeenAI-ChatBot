import requests
from datetime import datetime
from typing import Dict, Optional
import logging

class PrayerAPI:
    def __init__(self):
        self.base_url = "https://api.aladhan.com/v1"
        # Default timezone for Pakistan
        self.default_timezone = "Asia/Karachi"
        # Common Pakistan cities with their coordinates
        self.pk_cities = {
            "karachi": {"lat": 24.8607, "lng": 67.0011},
            "lahore": {"lat": 31.5204, "lng": 74.3587},
            "islamabad": {"lat": 33.6844, "lng": 73.0479},
            "rawalpindi": {"lat": 33.6007, "lng": 73.0679},
            "peshawar": {"lat": 34.0151, "lng": 71.5249},
            "quetta": {"lat": 30.1798, "lng": 66.9750},
            "multan": {"lat": 30.1575, "lng": 71.5249},
            "faisalabad": {"lat": 31.4504, "lng": 73.1350}
        }

    def get_prayer_times(self, city: str, country: str = "PK") -> Optional[Dict]:
        """Get prayer times for a specific location."""
        try:
            # Get current date
            date = datetime.now().strftime("%d-%m-%Y")

            # Clean up city name
            city = city.strip()
            if ',' in city:  # Handle "City, State" format
                city = city.split(',')[0].strip()

            logging.info(f"Fetching prayer times for {city}, {country}")

            # Check if it's a Pakistani city
            city_lower = city.lower()
            if city_lower in self.pk_cities:
                coords = self.pk_cities[city_lower]
                response = requests.get(
                    f"{self.base_url}/timings/{date}",
                    params={
                        "latitude": coords["lat"],
                        "longitude": coords["lng"],
                        "method": 1,  # Karachi method
                        "timezone": self.default_timezone
                    }
                )
            else:
                # For non-Pakistani cities, use city name
                response = requests.get(
                    f"{self.base_url}/timingsByCity/{date}",
                    params={
                        "city": city,
                        "country": country,
                        "method": 2  # Islamic Society of North America method
                    }
                )
            response.raise_for_status()
            data = response.json()

            logging.info(f"Prayer API response: {data}")

            if data['code'] == 200:
                timings = data['data']['timings']
                date_info = data['data']['date']

                # Format the response with both Gregorian and Hijri dates
                formatted_response = {
                    'timings': {
                        'Fajr': timings['Fajr'],
                        'Sunrise': timings['Sunrise'],
                        'Dhuhr': timings['Dhuhr'],
                        'Asr': timings['Asr'],
                        'Maghrib': timings['Maghrib'],
                        'Isha': timings['Isha']
                    },
                    'date': {
                        'gregorian': date_info['gregorian']['date'],
                        'hijri': f"{date_info['hijri']['day']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']} AH"
                    }
                }
                return formatted_response
            else:
                logging.error(f"Prayer API error: {data}")
                return None

        except requests.RequestException as e:
            logging.error(f"Error fetching prayer times: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            logging.error(f"Error parsing prayer times response: {str(e)}")
            return None
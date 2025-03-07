import requests
import logging
from typing import Optional, Dict
import os

class AudioRecitation:
    def __init__(self):
        self.base_url = "https://everyayah.com/data"
        self.default_qari = "Alafasy_128kbps"  # Mishary bin Rashid Alafasy
        self.qaris = {
            "Alafasy": "Alafasy_128kbps",
            "Husary": "Husary_128kbps",
            "AbdulBaset": "AbdulSamad_64kbps",
            "Minshawy": "Minshawy_Murattal_128kbps"
        }

    def get_audio_url(self, surah: int, ayah: int, qari: Optional[str] = None) -> Optional[str]:
        """Get the URL for the audio recitation of a specific verse."""
        try:
            # Format surah and ayah numbers with leading zeros
            surah_str = str(surah).zfill(3)
            ayah_str = str(ayah).zfill(3)

            # Use default qari if none specified
            qari_path = self.qaris.get(qari, self.default_qari)

            # Construct the URL
            audio_url = f"{self.base_url}/{qari_path}/{surah_str}{ayah_str}.mp3"

            # Verify if the audio file exists
            response = requests.head(audio_url)
            if response.status_code == 200:
                logging.info(f"Audio URL found for Surah {surah}, Ayah {ayah}")
                return audio_url
            else:
                logging.warning(f"Audio not found for Surah {surah}, Ayah {ayah}")
                return None

        except requests.RequestException as e:
            logging.error(f"Error fetching audio URL: {str(e)}")
            return None

    def get_available_qaris(self) -> Dict[str, str]:
        """Get list of available Qaris."""
        return self.qaris
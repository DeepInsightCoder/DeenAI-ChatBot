import logging
from typing import Dict, List, Optional

class HajjUmrahGuide:
    def __init__(self):
        self.hajj_steps = {
            "ihram": {
                "title": "1. Ihram (State of Purity)",
                "description": "Enter the sacred state of Ihram by performing ghusl, wearing Ihram garments, and making the intention.",
                "requirements": [
                    "Clean, unstitched white garments for men",
                    "Modest regular clothes for women",
                    "Avoid perfumes and cosmetics",
                    "Recite Talbiyah"
                ]
            },
            "tawaf": {
                "title": "2. Tawaf (Circumambulation)",
                "description": "Circumambulate the Kaaba seven times in a counterclockwise direction.",
                "requirements": [
                    "Start at the Black Stone",
                    "Keep Kaaba on your left",
                    "Make dua during each round",
                    "Perform two rakats after completion"
                ]
            },
            "sai": {
                "title": "3. Sa'i (Walking between Safa and Marwa)",
                "description": "Walk between the hills of Safa and Marwa seven times.",
                "requirements": [
                    "Begin at Safa",
                    "Walk to Marwa",
                    "Complete seven rounds",
                    "Make dua during the walk"
                ]
            },
            "arafat": {
                "title": "4. Day of Arafat (Hajj only)",
                "description": "Stand in prayer at Mount Arafat from noon to sunset.",
                "requirements": [
                    "Stay within Arafat boundaries",
                    "Perform Dhuhr and Asr prayers",
                    "Make extensive dua",
                    "Listen to the sermon"
                ]
            },
            "muzdalifah": {
                "title": "5. Muzdalifah (Hajj only)",
                "description": "Spend the night in Muzdalifah and collect pebbles for Jamarat.",
                "requirements": [
                    "Pray Maghrib and Isha combined",
                    "Collect 49/70 pebbles",
                    "Rest until Fajr",
                    "Leave for Mina after Fajr"
                ]
            }
        }
        
        self.faqs = {
            "difference": {
                "question": "What is the difference between Hajj and Umrah?",
                "answer": "Hajj is the mandatory pilgrimage performed during specific days of Dhul Hijjah, while Umrah is a voluntary pilgrimage that can be performed at any time of the year. Hajj includes additional rituals like standing at Arafat and staying at Muzdalifah."
            },
            "requirements": {
                "question": "What are the requirements for performing Hajj/Umrah?",
                "answer": "The main requirements are: being Muslim, being physically and financially able, having reached puberty, and for women to be accompanied by a mahram (male guardian)."
            },
            "preparation": {
                "question": "How should I prepare for Hajj/Umrah?",
                "answer": "Prepare by: settling debts, seeking forgiveness from others, learning the rituals, getting physically fit, and ensuring proper documentation (visa, travel documents)."
            }
        }

    def get_ritual_steps(self, ritual_type: str = "both") -> Dict:
        """Get steps for Hajj or Umrah or both."""
        try:
            if ritual_type.lower() == "umrah":
                # Umrah consists of only Ihram, Tawaf, and Sa'i
                return {k: v for k, v in self.hajj_steps.items() if k in ["ihram", "tawaf", "sai"]}
            elif ritual_type.lower() == "hajj":
                return self.hajj_steps
            else:
                return {
                    "hajj": self.hajj_steps,
                    "umrah": {k: v for k, v in self.hajj_steps.items() if k in ["ihram", "tawaf", "sai"]}
                }
        except Exception as e:
            logging.error(f"Error getting ritual steps: {str(e)}")
            return {}

    def get_faqs(self) -> Dict:
        """Get Hajj/Umrah FAQs."""
        return self.faqs

    def get_step_details(self, step_name: str) -> Optional[Dict]:
        """Get detailed information about a specific step."""
        try:
            step = self.hajj_steps.get(step_name.lower())
            if step:
                return step
            logging.warning(f"Step {step_name} not found")
            return None
        except Exception as e:
            logging.error(f"Error getting step details: {str(e)}")
            return None

    def format_step_info(self, step_data: Dict) -> str:
        """Format step information for display."""
        return (
            f"[bold]{step_data['title']}[/bold]\n\n"
            f"{step_data['description']}\n\n"
            "Requirements:\n" +
            "\n".join(f"• {req}" for req in step_data['requirements'])
        )

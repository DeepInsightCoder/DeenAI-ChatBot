import logging
from typing import Dict, List, Optional
import random

class IslamicCounselling:
    def __init__(self):
        # Pre-defined counselling responses with Islamic references
        self.counselling_database = {
            "anxiety": {
                "title": "Dealing with Anxiety",
                "responses": [
                    {
                        "advice": "Remember that every hardship comes with ease. Allah says in the Quran: 'Verily, with hardship comes ease.' (94:5)",
                        "practices": [
                            "Regular dhikr (remembrance of Allah)",
                            "Deep breathing with tasbih",
                            "Regular prayer and meditation"
                        ],
                        "references": {
                            "quran": ["Surah Ash-Sharh 94:5-6", "Surah Ar-Ra'd 13:28"],
                            "hadith": ["Sahih Bukhari 6366"]
                        }
                    }
                ]
            },
            "depression": {
                "title": "Coping with Depression",
                "responses": [
                    {
                        "advice": "Know that Allah's help is near. The Prophet (ﷺ) said, 'There is no disease that Allah has created, except that He also has created its treatment.'",
                        "practices": [
                            "Maintaining regular prayers",
                            "Connecting with supportive community",
                            "Seeking professional help alongside spiritual guidance"
                        ],
                        "references": {
                            "quran": ["Surah Al-Baqarah 2:186", "Surah Ad-Duha 93:3"],
                            "hadith": ["Sahih Bukhari 5678"]
                        }
                    }
                ]
            },
            "stress": {
                "title": "Managing Stress",
                "responses": [
                    {
                        "advice": "Trust in Allah's plan. The Prophet (ﷺ) said, 'How wonderful is the affair of the believer, for his affairs are all good.'",
                        "practices": [
                            "Regular salah breaks",
                            "Mindful Quran recitation",
                            "Islamic breathing exercises"
                        ],
                        "references": {
                            "quran": ["Surah At-Tawbah 9:51", "Surah Al-Imran 3:160"],
                            "hadith": ["Sahih Muslim 2999"]
                        }
                    }
                ]
            },
            "relationship": {
                "title": "Relationship Guidance",
                "responses": [
                    {
                        "advice": "Maintain kindness and patience in relationships. The Prophet (ﷺ) said, 'The best of you are those who are best to their families.'",
                        "practices": [
                            "Practice active listening",
                            "Show gratitude to family members",
                            "Regular family prayer time"
                        ],
                        "references": {
                            "quran": ["Surah Ar-Rum 30:21", "Surah An-Nisa 4:19"],
                            "hadith": ["Sunan Ibn Majah 1977"]
                        }
                    }
                ]
            }
        }

    def get_counselling_topics(self) -> List[str]:
        """Get list of available counselling topics."""
        return list(self.counselling_database.keys())

    def get_counselling(self, topic: Optional[str] = None) -> Optional[Dict]:
        """Get counselling advice for a specific topic or random if none specified."""
        try:
            if topic:
                topic = topic.lower()
                # Try exact match first
                if topic in self.counselling_database:
                    return {
                        'topic': self.counselling_database[topic]['title'],
                        'response': random.choice(self.counselling_database[topic]['responses'])
                    }
                
                # Try partial match
                for key, data in self.counselling_database.items():
                    if topic in key or key in topic:
                        return {
                            'topic': data['title'],
                            'response': random.choice(data['responses'])
                        }
                
                logging.warning(f"No counselling advice found for topic: {topic}")
                return None
            else:
                # Return random advice if no topic specified
                topic = random.choice(list(self.counselling_database.keys()))
                return {
                    'topic': self.counselling_database[topic]['title'],
                    'response': random.choice(self.counselling_database[topic]['responses'])
                }

        except Exception as e:
            logging.error(f"Error getting counselling advice: {str(e)}")
            return None

    def format_counselling_response(self, response_data: Dict) -> str:
        """Format counselling response for display."""
        formatted_text = f"[bold]{response_data['topic']}[/bold]\n\n"
        response = response_data['response']
        
        formatted_text += f"{response['advice']}\n\n"
        
        formatted_text += "[bold]Recommended Practices:[/bold]\n"
        formatted_text += "\n".join(f"• {practice}" for practice in response['practices'])
        
        if 'references' in response:
            if 'quran' in response['references']:
                formatted_text += "\n\n[bold]Quranic References:[/bold]\n"
                formatted_text += "\n".join(f"• {ref}" for ref in response['references']['quran'])
            
            if 'hadith' in response['references']:
                formatted_text += "\n\n[bold]Hadith References:[/bold]\n"
                formatted_text += "\n".join(f"• {ref}" for ref in response['references']['hadith'])
        
        formatted_text += "\n\nNote: This is basic guidance based on Islamic principles. For serious concerns, please consult with a qualified counselor or mental health professional."
        return formatted_text

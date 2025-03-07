import logging
from typing import Dict, List, Optional

class IslamicParenting:
    def __init__(self):
        self.parenting_tips = {
            "general": {
                "title": "General Islamic Parenting Principles",
                "tips": [
                    "Lead by example in practicing Islam",
                    "Start religious education early",
                    "Show love and mercy in discipline",
                    "Teach good manners and ethics"
                ],
                "references": {
                    "hadith": ["Sahih Bukhari 2469", "Sahih Muslim 2318"]
                }
            },
            "education": {
                "title": "Islamic Education Guidelines",
                "tips": [
                    "Teach Quran and basic Islamic principles",
                    "Encourage questions about faith",
                    "Make learning fun and interactive",
                    "Focus on character development"
                ],
                "references": {
                    "quran": ["Luqman 31:13-19"],
                    "hadith": ["Sunan Ibn Majah 224"]
                }
            },
            "discipline": {
                "title": "Islamic Discipline Methods",
                "tips": [
                    "Use gentle correction and explanation",
                    "Avoid physical punishment",
                    "Practice patience in teaching",
                    "Reward good behavior"
                ],
                "references": {
                    "hadith": ["Abu Dawud 495", "Sahih Muslim 2318"]
                }
            },
            "values": {
                "title": "Teaching Islamic Values",
                "tips": [
                    "Instill love for Allah and Prophet Muhammad (ﷺ)",
                    "Teach honesty and truthfulness",
                    "Encourage kindness to others",
                    "Foster respect for elders"
                ],
                "references": {
                    "quran": ["Al-Isra 17:23-24"],
                    "hadith": ["Sahih Bukhari 5971"]
                }
            }
        }

    def get_parenting_advice(self, topic: Optional[str] = None) -> Optional[Dict]:
        """Get Islamic parenting advice for a specific topic or general advice."""
        try:
            if topic and topic.lower() in self.parenting_tips:
                advice = self.parenting_tips[topic.lower()]
                logging.info(f"Retrieved parenting advice for topic: {topic}")
                return {
                    'topic': topic,
                    'advice': advice
                }
            else:
                # Return general advice if no specific topic is requested
                general_advice = self.parenting_tips['general']
                logging.info("Retrieved general parenting advice")
                return {
                    'topic': 'general',
                    'advice': general_advice
                }
        except Exception as e:
            logging.error(f"Error retrieving parenting advice: {str(e)}")
            return None

    def get_topics(self) -> List[str]:
        """Get list of available parenting topics."""
        return list(self.parenting_tips.keys())

    def format_advice(self, advice_data: Dict) -> str:
        """Format parenting advice for display."""
        if not advice_data or 'advice' not in advice_data:
            return "No advice available at this time."

        advice = advice_data['advice']
        formatted_text = f"[bold]{advice['title']}[/bold]\n\n"
        formatted_text += "\n".join(f"• {tip}" for tip in advice['tips'])

        if 'references' in advice:
            formatted_text += "\n\n[italic]References:[/italic]"
            for ref_type, refs in advice['references'].items():
                formatted_text += f"\n{ref_type.title()}: " + ", ".join(refs)

        return formatted_text

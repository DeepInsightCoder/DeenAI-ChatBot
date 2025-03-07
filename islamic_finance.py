import logging
from typing import Dict, List, Optional
from datetime import datetime

class IslamicFinance:
    def __init__(self):
        self.finance_tips = {
            "general": {
                "title": "General Islamic Finance Principles",
                "tips": [
                    "Follow Shariah-compliant investment principles",
                    "Avoid businesses dealing with alcohol, gambling, or non-halal food",
                    "Ensure transparency in all financial transactions",
                    "Keep detailed records of all financial dealings"
                ]
            },
            "riba": {
                "title": "Avoiding Riba (Interest)",
                "tips": [
                    "Avoid conventional interest-based banking",
                    "Use Islamic banking alternatives like Mudarabah and Musharakah",
                    "Consider profit-sharing arrangements instead of interest-based loans",
                    "Stay away from usury in any form"
                ],
                "references": {
                    "quran": ["Al-Baqarah 2:275-276", "Al-Imran 3:130"],
                    "hadith": ["Sahih Muslim 1598"]
                }
            },
            "investment": {
                "title": "Halal Investment Guidelines",
                "tips": [
                    "Invest in Shariah-compliant stocks and mutual funds",
                    "Consider Islamic REITs for real estate investment",
                    "Participate in halal crowdfunding platforms",
                    "Invest in ethical and sustainable businesses"
                ],
                "sectors": [
                    "Technology",
                    "Healthcare",
                    "Infrastructure",
                    "Ethical Trade",
                    "Sustainable Energy"
                ]
            },
            "zakat_management": {
                "title": "Zakat and Wealth Management",
                "tips": [
                    "Calculate and pay Zakat annually",
                    "Keep track of zakatable assets",
                    "Consider charitable endowments (Waqf)",
                    "Plan for wealth distribution according to Islamic law"
                ]
            },
            "business": {
                "title": "Islamic Business Practices",
                "tips": [
                    "Ensure clear terms in all contracts",
                    "Practice fair and ethical trading",
                    "Avoid excessive uncertainty (Gharar)",
                    "Maintain honest business relationships"
                ],
                "references": {
                    "hadith": ["Sahih Bukhari 2079", "Sahih Muslim 1532"]
                }
            }
        }

    def get_finance_advice(self, topic: Optional[str] = None) -> Optional[Dict]:
        """Get Islamic finance advice for a specific topic or general advice."""
        try:
            if topic and topic.lower() in self.finance_tips:
                advice = self.finance_tips[topic.lower()]
                logging.info(f"Retrieved finance advice for topic: {topic}")
                return {
                    'topic': topic,
                    'advice': advice
                }
            else:
                # Return general advice if no specific topic is requested
                general_advice = self.finance_tips['general']
                logging.info("Retrieved general finance advice")
                return {
                    'topic': 'general',
                    'advice': general_advice
                }
        except Exception as e:
            logging.error(f"Error retrieving finance advice: {str(e)}")
            return None

    def get_halal_investments(self) -> List[str]:
        """Get list of recommended halal investment sectors."""
        try:
            investment_data = self.finance_tips['investment']
            return investment_data.get('sectors', [])
        except Exception as e:
            logging.error(f"Error retrieving halal investments: {str(e)}")
            return []

    def get_riba_guidelines(self) -> Dict:
        """Get specific guidelines about avoiding riba."""
        try:
            riba_data = self.finance_tips['riba']
            return {
                'guidelines': riba_data['tips'],
                'references': riba_data.get('references', {})
            }
        except Exception as e:
            logging.error(f"Error retrieving riba guidelines: {str(e)}")
            return {}

    def format_advice(self, advice_data: Dict) -> str:
        """Format finance advice for display."""
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
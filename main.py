import logging
from typing import Dict, Optional, Union, Any
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from rich.panel import Panel
from rich import print as rprint
from .quran import QuranAPI
from .hadith import HadithAPI
from .prayer import PrayerAPI
from .knowledge import IslamicKnowledge
from .nlp_utils import identify_intent, extract_entities
from .zakat import ZakatCalculator
from .calendar import IslamicCalendar
import sys
from .reminders import DailyReminder
from .history import UserHistory
import re
from datetime import datetime
from .audio import AudioRecitation
import webbrowser
import os
from .hajj_guide import HajjUmrahGuide
from .islamic_finance import IslamicFinance
from .parenting import IslamicParenting  # Fixed import statement
from .islamic_art import IslamicArt
from .media import IslamicMedia # Added import
from .islamic_books import IslamicBooks  # Add this import at the top with other imports
from .counselling import IslamicCounselling
from .games import IslamicGames  # Add this import at the top
from .feedback import FeedbackCollector  # Add this import at the top
import argparse

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class IslamicChatbot:
    def __init__(self, test_mode: bool = False):
        self.console = Console()
        self.quran_api = QuranAPI()
        self.hadith_api = HadithAPI()
        self.prayer_api = PrayerAPI()
        self.knowledge_base = IslamicKnowledge()
        self.zakat_calc = ZakatCalculator()
        self.calendar = IslamicCalendar()
        self.reminder = DailyReminder()
        self.history = UserHistory()
        self.audio = AudioRecitation()
        self.hajj_guide = HajjUmrahGuide()
        self.islamic_finance = IslamicFinance()
        self.islamic_parenting = IslamicParenting()
        self.test_mode = test_mode
        self.last_query = ""
        self.islamic_art = IslamicArt()
        self.islamic_media = IslamicMedia() # Added instantiation
        self.islamic_books = IslamicBooks()  # Add this line after other initializations
        self.islamic_counselling = IslamicCounselling()
        # Add this line after other initializations
        self.islamic_games = IslamicGames()
        # Add this line after other initializations
        self.feedback_collector = FeedbackCollector()

    def format_references(self, references: Optional[Dict[str, list]]) -> str:
        """Format references for display."""
        if not references or not isinstance(references, dict):
            return ""

        formatted_text = ""
        if 'quran' in references:
            quran_refs = "\n".join(f"• {ref}" for ref in references['quran'])
            formatted_text += f"\n\n[bold]Quranic References:[/bold]\n{quran_refs}"
        if 'hadith' in references:
            hadith_refs = "\n".join(f"• {ref}" for ref in references['hadith'])
            formatted_text += f"\n\n[bold]Hadith References:[/bold]\n{hadith_refs}"
        return formatted_text

    def handle_knowledge_query(self, question: str) -> bool:
        """Handle general Islamic knowledge queries."""
        try:
            answer_data = self.knowledge_base.get_answer(question)
            if answer_data and isinstance(answer_data, dict):
                # Ensure references is a dictionary
                references = answer_data.get('references', {})
                if not isinstance(references, dict):
                    references = {}

                references_text = self.format_references(references)
                title = answer_data.get('topic', 'Knowledge').title()

                rprint(Panel(
                    f"{answer_data['answer']}\n{references_text}",
                    title=f"Islamic Knowledge: {title}",
                    border_style="magenta"
                ))
                return True
            else:
                self.console.print("Sorry, I don't have information about that topic.", style="red")
                return False
        except Exception as e:
            logging.error(f"Error processing knowledge query: {str(e)}")
            self.console.print(f"Error processing knowledge query: {str(e)}", style="red")
            return False

    def display_welcome(self):
        """Display welcome message and instructions."""
        welcome_text = """
        Welcome to DeenAI - Islamic Chatbot!

        You can ask questions about:
        - Quranic verses (e.g., "Show me Surah 1, Ayah 1")
        - Hadiths (e.g., "Tell me a hadith about kindness")
        - Prayer times (e.g., "What are the prayer times in New York?")
        - Islamic knowledge (e.g., "What is Zakat?")
        - Zakat Calculation (e.g., "Calculate my Zakat")
        - Islamic Calendar (e.g., "What is today's Islamic date?")
        - Daily Reminders (e.g., "Show me today's reminder")
        - Quranic Keyword Search (e.g., "Search the Quran for mercy")
        - Islamic History (e.g., "Tell me about Prophet Muhammad")
        - View History (e.g., "Show my Surah history")
        - Audio Recitation (e.g., "Play Surah 1, Ayah 1")
        - Islamic Q&A (e.g., "What is the importance of prayer?")
        - Hajj/Umrah Guide (e.g., "Show me Hajj steps" or "Explain Umrah ritual")
        - Islamic Finance (e.g., "Tell me about Islamic finance", "How to avoid riba?")
        - Islamic Parenting (e.g., "How to raise children Islamically", "Islamic education tips")
        - Islamic Art (e.g., "Show me Islamic art", "Tell me about Islamic calligraphy")
        - Islamic Media (e.g., "Show me Islamic podcasts", "Recommend Islamic videos")
        - Islamic Books (e.g., "Recommend Islamic books", "Find books about spirituality")
        - Islamic Counselling (e.g., "I'm feeling anxious, need Islamic guidance")
        - Islamic Games (e.g., "Show me Islamic games", "Find games for children")
        - Give Feedback (e.g., "Give feedback")


        Type 'exit' to quit.
        """
        self.console.print(Panel(welcome_text, title="DeenAI - Islamic Chatbot", border_style="green"))

    def handle_quran_query(self, entities):
        """Handle Quran-related queries."""
        try:
            if entities['surah'] and entities['ayah']:
                logging.info(f"Fetching verse for Surah {entities['surah']}, Ayah {entities['ayah']}")
                verse = self.quran_api.get_verse(entities['surah'], entities['ayah'])
                if verse:
                    # Add to history
                    self.history.add_surah_query(
                        entities['surah'],
                        entities['ayah'],
                        verse['arabic']
                    )

                    rprint(Panel(
                        f"[bold]{verse['arabic']}[/bold]\n\n"
                        f"[blue]Translation:[/blue]\n{verse['translation']}\n\n"
                        f"[green]Tafseer:[/green]\n{verse['tafseer']}",
                        title=f"Surah {verse['surah']}, Ayah {entities['ayah']}",
                        border_style="blue"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't find that verse.", style="red")
                    return False
            else:
                self.console.print("Please specify both Surah and Ayah numbers.", style="yellow")
                return False
        except Exception as e:
            logging.error(f"Error processing Quran query: {str(e)}")
            self.console.print(f"Error processing Quran query: {str(e)}", style="red")
            return False

    def handle_hadith_query(self, entities: Dict[str, Optional[str]]) -> bool:
        """Handle Hadith-related queries."""
        try:
            if entities and 'topic' in entities and entities['topic']:
                hadith = self.hadith_api.get_hadith_by_topic(entities['topic'])
                if hadith and isinstance(hadith, dict):
                    rprint(Panel(
                        f"{hadith['text']}\n\n[italic]{hadith['reference']}[/italic]",
                        title="Hadith",
                        border_style="yellow"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't find a hadith on that topic.", style="red")
                    return False
            else:
                self.console.print("Please specify a topic for the hadith.", style="yellow")
                return False
        except Exception as e:
            logging.error(f"Error processing Hadith query: {str(e)}")
            self.console.print(f"Error processing Hadith query: {str(e)}", style="red")
            return False

    def handle_prayer_query(self, entities):
        """Handle prayer time queries."""
        try:
            if entities['location']:
                times = self.prayer_api.get_prayer_times(entities['location'], "")
                if times:
                    date_info = f"Date: {times['date']['gregorian']} ({times['date']['hijri']})"
                    times_text = "\n".join([f"{prayer}: {time}" for prayer, time in times['timings'].items()])
                    rprint(Panel(
                        f"{date_info}\n\n{times_text}",
                        title=f"Prayer Times for {entities['location']}",
                        border_style="cyan"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't find prayer times for that location.", style="red")
                    return False
        except Exception as e:
            self.console.print(f"Error processing prayer times query: {str(e)}", style="red")
            return False


    def handle_zakat_calculation(self, test_input=None) -> bool:
        """Handle Zakat calculation queries."""
        try:
            self.console.print("\nZakat Calculator", style="bold green")
            self.console.print("Please enter your assets:", style="yellow")

            if self.test_mode:
                # Use sample values for testing
                cash = 5000.0
                gold = 50.0
                silver = 100.0
                self.console.print(f"Using sample values for testing:\nCash: ${cash}\nGold: {gold}g\nSilver: {silver}g")
            else:
                # Get user input for assets
                cash = FloatPrompt.ask("Enter your cash savings (in USD)")
                gold = FloatPrompt.ask("Enter your gold (in grams)")
                silver = FloatPrompt.ask("Enter your silver (in grams)")

            assets = {
                'cash': cash,
                'gold': gold,
                'silver': silver
            }

            result = self.zakat_calc.calculate_zakat(assets)

            if not result:
                self.console.print("Error calculating Zakat. Please check your inputs.", style="red")
                return False

            if result['status'] == 'below_nisab':
                rprint(Panel(
                    f"Total Assets: ${result['total_value']:.2f}\n\n"
                    f"Your assets are below the Nisab threshold:\n"
                    f"Gold Nisab: ${result['nisab_gold']:.2f}\n"
                    f"Silver Nisab: ${result['nisab_silver']:.2f}\n\n"
                    "No Zakat is due at this time.",
                    title="Zakat Calculation Result",
                    border_style="yellow"
                ))
            else:
                rprint(Panel(
                    f"Total Assets: ${result['total_value']:.2f}\n"
                    f"Breakdown:\n"
                    f"- Cash: ${result['cash_value']:.2f}\n"
                    f"- Gold: ${result['gold_value']:.2f}\n"
                    f"- Silver: ${result['silver_value']:.2f}\n\n"
                    f"Zakat Due: ${result['zakat_amount']:.2f}",
                    title="Zakat Calculation Result",
                    border_style="green"
                ))
            return True

        except Exception as e:
            logging.error(f"Error in Zakat calculation: {str(e)}")
            self.console.print("An error occurred while calculating Zakat.", style="red")
            return False

    def handle_islamic_calendar(self, date_str: Optional[str] = None) -> bool:
        """Handle Islamic calendar queries."""
        try:
            # Get Islamic date
            date_info = self.calendar.get_islamic_date(date_str)
            if date_info:
                # Format the response
                formatted_date = self.calendar.format_date_response(date_info)

                # Get upcoming events
                events = self.calendar.get_upcoming_events()
                events_text = "\n\nUpcoming Important Islamic Dates:"
                for event, description in events.items():
                    events_text += f"\n• {event}: {description}"

                rprint(Panel(
                    formatted_date + events_text,
                    title="Islamic Calendar",
                    border_style="blue"
                ))
                return True
            else:
                self.console.print("Sorry, I couldn't get the Islamic date information.", style="red")
                return False

        except Exception as e:
            logging.error(f"Error processing calendar query: {str(e)}")
            self.console.print(f"Error processing calendar query: {str(e)}", style="red")
            return False

    def handle_daily_reminder(self) -> bool:
        """Handle daily Islamic reminder requests."""
        try:
            reminder = self.reminder.get_daily_reminder()
            rprint(Panel(
                f"[bold]{reminder['text']}[/bold]\n\n"
                f"[italic]Source: {reminder['source']}[/italic]",
                title=f"Daily Islamic {reminder['type'].title()}",
                border_style="magenta"
            ))
            return True
        except Exception as e:
            logging.error(f"Error displaying daily reminder: {str(e)}")
            self.console.print("Sorry, I couldn't retrieve today's reminder.", style="red")
            return False

    def handle_quran_search(self, entities) -> bool:
        """Handle Quranic verse search queries."""
        try:
            # Extract search keyword from topic or full query
            keyword = entities.get('topic')
            if not keyword:
                # Try to extract keyword from the query after "search" or "find"
                text = self.last_query.lower()
                search_match = re.search(r'(?:search|find).*(?:about|for)?\s+([a-z\s]+)(?:\s+in\s+quran)?', text)
                if search_match:
                    keyword = search_match.group(1).strip()

            if not keyword:
                self.console.print("Please specify what you'd like to search for in the Quran.", style="yellow")
                return False

            logging.info(f"Searching Quran for keyword: {keyword}")
            results = self.quran_api.search_by_keyword(keyword)

            if results:
                rprint(Panel(
                    "\n\n".join([
                        f"[bold]{result['text']}[/bold]\n"
                        f"[blue]Translation:[/blue] {result['translations'].get('en', 'Translation not available')}\n"
                        f"[italic]Surah {result['surah']['number']}, Verse {result['numberInSurah']}[/italic]"
                        for result in results
                    ]),
                    title=f"Quranic Verses about '{keyword}'",
                    border_style="green"
                ))
                return True
            else:
                self.console.print(f"No verses found containing '{keyword}'.", style="yellow")
                return False

        except Exception as e:
            logging.error(f"Error searching Quran: {str(e)}")
            self.console.print("An error occurred while searching the Quran.", style="red")
            return False

    def handle_islamic_history(self, figure: Optional[str] = None) -> bool:
        """Handle Islamic history queries."""
        try:
            from .constants import ISLAMIC_HISTORY

            # If no figure specified, try to extract from last query
            if not figure:
                # Remove common phrases to get the actual figure name
                query = self.last_query.lower()
                for prefix in ["tell me about", "who is", "what about"]:
                    if query.startswith(prefix):
                        query = query[len(prefix):].strip()
                figure = query

            if figure:
                # Add to history
                self.history.add_islamic_history_query(figure)

                # Look for a specific figure
                figure_lower = figure.lower()
                for name, description in ISLAMIC_HISTORY.items():
                    if any(keyword in name.lower() for keyword in figure_lower.split()):
                        rprint(Panel(
                            f"[bold]{name}[/bold]\n\n{description}",
                            title="Islamic History",
                            border_style="cyan"
                        ))
                        return True

                self.console.print(f"Sorry, I couldn't find information about {figure}.", style="yellow")
                return False
            else:
                # Show all available figures
                history_text = "\n\n".join([
                    f"[bold]{name}[/bold]\n{description}"
                    for name, description in ISLAMIC_HISTORY.items()
                ])
                rprint(Panel(
                    history_text,
                    title="Islamic History",
                    border_style="cyan"
                ))
                return True

        except Exception as e:
            logging.error(f"Error displaying Islamic history: {str(e)}")
            self.console.print("An error occurred while retrieving Islamic history.", style="red")
            return False

    def handle_history_query(self) -> bool:
        """Handle history display requests."""
        try:
            # Get both Surah and Islamic history
            surah_history = self.history.get_surah_history()
            islamic_history = self.history.get_islamic_history()

            if not surah_history and not islamic_history:
                self.console.print("No history available yet.", style="yellow")
                return True

            # Format Surah history
            if surah_history:
                surah_text = "\n\n[bold]Surah History:[/bold]\n" + "\n".join([
                    f"• {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}: "
                    f"Surah {entry['surah']}, Ayah {entry['ayah']}"
                    for entry in surah_history
                ])
            else:
                surah_text = "\n[bold]Surah History:[/bold]\nNo Surah queries yet."

            # Format Islamic history
            if islamic_history:
                islamic_text = "\n\n[bold]Islamic History Queries:[/bold]\n" + "\n".join([
                    f"• {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}: "
                    f"Queried about {entry['figure']}"
                    for entry in islamic_history
                ])
            else:
                islamic_text = "\n\n[bold]Islamic History Queries:[/bold]\nNo history queries yet."

            rprint(Panel(
                surah_text + islamic_text,
                title="Query History",
                border_style="magenta"
            ))
            return True

        except Exception as e:
            logging.error(f"Error displaying history: {str(e)}")
            self.console.print("An error occurred while retrieving history.", style="red")
            return False

    def handle_audio_recitation(self, entities) -> bool:
        """Handle audio recitation requests."""
        try:
            if entities['surah'] and entities['ayah']:
                # Get the audio URL
                audio_url = self.audio.get_audio_url(entities['surah'], entities['ayah'])

                if audio_url:
                    rprint(Panel(
                        f"Audio recitation available for Surah {entities['surah']}, Ayah {entities['ayah']}\n"
                        f"URL: {audio_url}\n\n"
                        "Note: Click the URL to listen to the recitation.",
                        title="Audio Recitation",
                        border_style="blue"
                    ))
                    return True
                else:
                    self.console.print("Sorry, audio recitation not available for this verse.", style="red")
                    return False
            else:
                self.console.print("Please specify both Surah and Ayah numbers for audio recitation.", style="yellow")
                return False

        except Exception as e:
            logging.error(f"Error processing audio recitation request: {str(e)}")
            self.console.print("An error occurred while fetching the audio recitation.", style="red")
            return False

    def handle_islamic_qa(self, question: str) -> bool:
        """Handle Islamic Q&A queries with references."""
        try:
            answer_data = self.knowledge_base.get_answer(question)
            if answer_data and isinstance(answer_data, dict):
                # Ensure references is a dictionary
                references = answer_data.get('references', {})
                if not isinstance(references, dict):
                    references = {}

                references_text = self.format_references(references)
                title = answer_data.get('topic', 'Islamic Q&A').title()

                rprint(Panel(
                    f"{answer_data['answer']}\n{references_text}",
                    title=f"Islamic Q&A: {title}",
                    border_style="cyan"
                ))
                return True
            else:
                # Try the knowledge query handler as fallback
                return self.handle_knowledge_query(question)

        except Exception as e:
            logging.error(f"Error processing Islamic Q&A query: {str(e)}")
            self.console.print("An error occurred while processing your question.", style="red")
            return False

    def handle_hajj_guide(self, query: str) -> bool:
        """Handle Hajj and Umrah guide queries."""
        try:
            # Determine if query is about Hajj or Umrah
            ritual_type = "hajj" if "hajj" in query.lower() else "umrah" if "umrah" in query.lower() else "both"

            if "faq" in query.lower() or "requirement" in query.lower():
                faqs = self.hajj_guide.get_faqs()
                faq_text = "\n\n".join([
                    f"[bold]{faq['question']}[/bold]\n{faq['answer']}"
                    for faq in faqs.values()
                ])
                rprint(Panel(
                    faq_text,
                    title="Hajj & Umrah FAQs",
                    border_style="blue"
                ))
                return True

            # Get ritual steps
            steps = self.hajj_guide.get_ritual_steps(ritual_type)

            if ritual_type == "both":
                # Display both Hajj and Umrah steps
                hajj_steps = "\n\n".join([
                    self.hajj_guide.format_step_info(step)
                    for step in steps['hajj'].values()
                ])
                umrah_steps = "\n\n".join([
                    self.hajj_guide.format_step_info(step)
                    for step in steps['umrah'].values()
                ])

                rprint(Panel(
                    f"[bold]Hajj Steps:[/bold]\n\n{hajj_steps}\n\n"
                    f"[bold]Umrah Steps:[/bold]\n\n{umrah_steps}",
                    title="Hajj & Umrah Guide",
                    border_style="green"
                ))
            else:
                # Display steps for either Hajj or Umrah
                formatted_steps = "\n\n".join([
                    self.hajj_guide.format_step_info(step)
                    for step in steps.values()
                ])

                rprint(Panel(
                    formatted_steps,
                    title=f"{ritual_type.title()} Guide",
                    border_style="green"
                ))
            return True

        except Exception as e:
            logging.error(f"Error processing Hajj/Umrah guide request: {str(e)}")
            self.console.print("An error occurred while retrieving the guide.", style="red")
            return False

    def handle_islamic_finance(self, query: str) -> bool:
        """Handle Islamic finance queries."""
        try:
            # Extract topic from query
            topic = None
            if "riba" in query.lower():
                topic = "riba"
            elif "investment" in query.lower() or "invest" in query.lower():
                topic = "investment"
            elif "business" in query.lower():
                topic = "business"
            elif "zakat" in query.lower():
                topic = "zakat_management"

            # Get finance advice
            advice_data = self.islamic_finance.get_finance_advice(topic)
            if advice_data:
                formatted_advice = self.islamic_finance.format_advice(advice_data)
                rprint(Panel(
                    formatted_advice,
                    title=f"Islamic Finance: {advice_data['topic']}",
                    border_style="blue"
                ))
                return True
            else:
                self.console.print("Sorry, I couldn't find specific finance advice for your query.", style="yellow")
                return False

        except Exception as e:
            logging.error(f"Error processing finance query: {str(e)}")
            self.console.print("An error occurred while retrieving finance advice.", style="red")
            return False

    def handle_islamic_parenting(self, query: str) -> bool:
        """Handle Islamic parenting queries."""
        try:
            # Extract topic from query
            topic = None
            if "education" in query.lower():
                topic = "education"
            elif "discipline" in query.lower():
                topic = "discipline"
            elif "values" in query.lower():
                topic = "values"

            # Get parenting advice
            advice_data = self.islamic_parenting.get_parenting_advice(topic)
            if advice_data:
                formatted_advice = self.islamic_parenting.format_advice(advice_data)
                rprint(Panel(
                    formatted_advice,
                    title=f"Islamic Parenting: {advice_data['topic']}",
                    border_style="blue"
                ))
                return True
            else:
                self.console.print("Sorry, I couldn't find specific parenting advice for your query.", style="yellow")
                return False

        except Exception as e:
            logging.error(f"Error processing parenting query: {str(e)}")
            self.console.print("An error occurred while retrieving parenting advice.", style="red")
            return False

    def handle_islamic_art(self, query: str) -> bool:
        """Handle Islamic art and calligraphy queries."""
        try:
            # Extract search terms if any
            search_terms = None
            search_match = re.search(r'(?:about|containing|with)\s+([a-z\s]+)', query.lower())
            if search_match:
                search_terms = search_match.group(1).strip()

            if search_terms:
                # Search for specific art pieces
                results = self.islamic_art.search_art(search_terms)
                if results:
                    for result in results:
                        piece = result['piece']
                        formatted_piece = self.islamic_art.format_art_piece(piece)
                        rprint(Panel(
                            formatted_piece,
                            title=f"Islamic {result['category'].title()}",
                            border_style="cyan"
                        ))
                    return True
                else:
                    self.console.print(f"Sorry, I couldn't find any Islamic art matching '{search_terms}'.", style="yellow")
                    return False
            else:
                # Show a random piece
                piece = self.islamic_art.get_random_piece()
                if piece:
                    formatted_piece = self.islamic_art.format_art_piece(piece)
                    rprint(Panel(
                        formatted_piece,
                        title="Islamic Art",
                        border_style="cyan"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't retrieve any Islamic art pieces at this time.", style="red")
                    return False

        except Exception as e:
            logging.error(f"Error processing Islamic art query: {str(e)}")
            self.console.print("An error occurred while retrieving Islamic art.", style="red")
            return False

    def handle_islamic_media(self, query: str) -> bool:
        """Handle Islamic media queries."""
        try:
            # Extract search terms if any
            search_terms = None
            search_match = re.search(r'(?:about|containing|with)\s+([a-z\s]+)', query.lower())
            if search_match:
                search_terms = search_match.group(1).strip()

            if search_terms:
                # Search for specific content
                results = self.islamic_media.search_content(search_terms)
                if results:
                    for result in results:
                        item = result['item']
                        formatted_content = self.islamic_media.format_content(item)
                        rprint(Panel(
                            formatted_content,
                            title=f"Islamic {result['category'].title()}",
                            border_style="purple"
                        ))
                    return True
                else:
                    self.console.print(f"Sorry, I couldn't find any Islamic content matching '{search_terms}'.", style="yellow")
                    return False
            else:
                # Show random content
                content = self.islamic_media.get_random_content()
                if content:
                    formatted_content = self.islamic_media.format_content(content)
                    rprint(Panel(
                        formatted_content,
                        title="Islamic Media Recommendation",
                        border_style="purple"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't retrieve any Islamic content at this time.", style="red")
                    return False

        except Exception as e:
            logging.error(f"Error processing Islamic media query: {str(e)}")
            self.console.print("An error occurred while retrieving Islamic media content.", style="red")
            return False

    def handle_islamic_books(self, query: str) -> bool:
        """Handle Islamic book recommendations."""
        try:
            # Extract search terms if any
            search_terms = None
            search_match = re.search(r'(?:about|on|for)\s+([a-z\s]+)', query.lower())
            if search_match:
                search_terms = search_match.group(1).strip()

            if search_terms:
                # Search for specific books
                results = self.islamic_books.search_books(search_terms)
                if results:
                    for result in results:
                        book = result['book']
                        formatted_book = self.islamic_books.format_book(book)
                        rprint(Panel(
                            formatted_book,
                            title=f"Islamic Book Recommendation ({result['category'].title()})",
                            border_style="green"
                        ))
                    return True
                else:
                    self.console.print(f"Sorry, I couldn't find any Islamic books matching '{search_terms}'.", style="yellow")
                    return False
            else:
                # Show random book
                book = self.islamic_books.get_random_book()
                if book:
                    formatted_book = self.islamic_books.format_book(book)
                    rprint(Panel(
                        formatted_book,
                        title="Islamic Book Recommendation",
                        border_style="green"
                    ))
                    return True
                else:
                    self.console.print("Sorry, I couldn't retrieve any book recommendations at this time.", style="red")
                    return False

        except Exception as e:
            logging.error(f"Error processing book recommendation request: {str(e)}")
            self.console.print("An error occurred while retrieving book recommendations.", style="red")
            return False

    def handle_islamic_counselling(self, query: str) -> bool:
        """Handle Islamic counselling queries."""
        try:
            # Extract topic from query
            topic = None
            for keyword in ['anxiety', 'depression', 'stress', 'relationship']:
                if keyword in query.lower():
                    topic = keyword
                    break

            counselling_data = self.islamic_counselling.get_counselling(topic)
            if counselling_data:
                formatted_response = self.islamic_counselling.format_counselling_response(counselling_data)
                rprint(Panel(
                    formatted_response,
                    title="Islamic Guidance",
                    border_style="blue"
                ))
                return True
            else:
                self.console.print("I apologize, but I couldn't find specific guidance for your concern. Please consider speaking with a qualified counselor.", style="yellow")
                return False

        except Exception as e:
            logging.error(f"Error processing counselling query: {str(e)}")
            self.console.print("An error occurred while providing counselling guidance.", style="red")
            return False

    def handle_islamic_games(self, query: str) -> bool:
        """Handle Islamic games and activities."""
        try:
            # Extract search terms if any
            search_terms = None
            search_match = re.search(r'(?:for|about)\s+([a-z\s]+)', query.lower())
            if search_match:
                searchterms = search_match.group(1).strip()
                logging.info(f"Extracted search terms for games: {search_terms}")

            if search_terms:
                # Search for specific games
                results = self.islamic_games.search_games(search_terms)
                if results:
                    for result in results:
                        game = result['game']
                        formatted_game = self.islamic_games.format_game(game)
                        rprint(Panel(
                            formatted_game,
                            title=f"Islamic {result['category'].title()}",
                            border_style="yellow"
                        ))
                    logging.info(f"Found {len(results)} games matching search terms")
                    return True
                else:
                    self.console.print(f"Sorry, I couldn't find any Islamic games matching '{search_terms}'.", style="yellow")
                    logging.info(f"No games found for search terms: {search_terms}")
                    return False
            else:
                # Show random game
                game = self.islamic_games.get_random_game()
                if game:
                    formatted_game = self.islamic_games.format_game(game)
                    rprint(Panel(
                        formatted_game,
                        title="Islamic Game",
                        border_style="yellow"
                    ))
                    logging.info("Successfully displayed random game")
                    return True
                else:
                    self.console.print("Sorry, I couldn't retrieve any games at this time.", style="red")
                    logging.warning("Failed to retrieve random game")
                    return False

        except Exception as e:
            logging.error(f"Error processing games query: {str(e)}")
            self.console.print("An error occurred while retrieving Islamic games.", style="red")
            return False

    def handle_feedback(self, query: str) -> bool:
        """Handle feedback collection."""
        try:
            # Extract rating if provided
            rating_match = re.search(r'rate.*?(\d+)', query.lower())
            rating = int(rating_match.group(1)) if rating_match else None

            # Determine feedback type
            if 'suggest' in query.lower() or 'improvement' in query.lower():
                feedback_type = 'suggestion'
            else:
                feedback_type = 'response'

            # Get category if mentioned
            category = None
            for cat in ['quran', 'hadith', 'prayer', 'knowledge', 'art', 'games']:
                if cat in query.lower():
                    category = cat
                    break

            # Prompt for feedback
            feedback = Prompt.ask("Please share your feedback")

            if self.feedback_collector.save_feedback(
                feedback_type=feedback_type,
                content=feedback,
                rating=rating,
                query=query,
                category=category
            ):
                self.console.print("Thank you for your feedback!", style="green")
                return True
            else:
                self.console.print("Sorry, I couldn't save your feedback at this time.", style="red")
                return False

        except Exception as e:
            logging.error(f"Error processing feedback: {str(e)}")
            self.console.print("An error occurred while processing your feedback.", style="red")
            return False

    def process_input(self, user_input: str) -> bool:
        """Process a single input and return response status."""
        if user_input.lower() == 'exit':
            return False

        try:
            self.last_query = user_input
            intent = identify_intent(user_input)
            entities = extract_entities(user_input)
            logging.info(f"Identified intent: {intent}, entities: {entities}")

            if intent == 'audio_recitation':
                return self.handle_audio_recitation(entities)
            elif intent == 'islamic_qa':
                return self.handle_islamic_qa(user_input)
            elif intent == 'hajj_guide' or intent == 'hajj_faq':
                return self.handle_hajj_guide(user_input)
            elif intent == 'quran_search':
                return self.handle_quran_search(entities)
            elif intent == 'quran':
                return self.handle_quran_query(entities)
            elif intent == 'hadith':
                return self.handle_hadith_query(entities)
            elif intent == 'prayer_times':
                return self.handle_prayer_query(entities)
            elif intent == 'zakat_calc':
                return self.handle_zakat_calculation()
            elif intent == 'islamic_calendar':
                return self.handle_islamic_calendar()
            elif intent == 'daily_reminder':
                return self.handle_daily_reminder()
            elif intent == 'islamic_history':
                return self.handle_islamic_history(entities.get('topic'))
            elif intent == 'show_history':
                return self.handle_history_query()
            elif intent == 'islamic_finance':
                return self.handle_islamic_finance(user_input)
            elif intent == 'islamic_parenting':
                return self.handle_islamic_parenting(user_input)
            elif intent in ['islamic_art', 'islamic_art_search']:
                return self.handle_islamic_art(user_input)
            elif intent in ['islamic_media', 'islamic_media_search']: #Added Islamic media handling
                return self.handle_islamic_media(user_input)
            elif intent in ['islamic_books', 'islamic_books_search']:
                return self.handle_islamic_books(user_input)
            elif intent == 'islamic_counselling':
                return self.handle_islamic_counselling(user_input)
            elif intent in ['islamic_games', 'islamic_games_search']:
                return self.handle_islamic_games(user_input)
            elif 'feedback' in intent or 'rate' in user_input.lower():
                return self.handle_feedback(user_input)
            else:
                return self.handle_knowledge_query(user_input)

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            self.console.print(f"An error occurred: {str(e)}", style="red")
            return False

    def run_test_sequence(self) -> bool:
        """Run a test sequence to verify functionality."""
        test_queries = [
            "show me surah 1, ayah 1",
            "tell me about Prophet Muhammad",
            "search quran for mercy",
            "show my history",
            "what is zakat?",  # Test Islamic Q&A with references
            "explain wudu",    # Another Q&A test
            "question about halal food",  # Third Q&A test
            "show me Hajj steps",  # Test Hajj guide
            "explain Umrah ritual",  # Test Umrah guide
            "what are Hajj requirements?",  # Test Hajj FAQs
            "tell me about Islamic finance",  # Test finance advice
            "how to avoid riba",  # Test riba guidelines
            "what are halal investments",  # Test investment advice
            "how to raise children Islamically",  # Test parenting advice
            "tell me about Islamic discipline",  # Test discipline tips
            "Islamic education tips",  # Test education advice
            "show me Islamic art", # Test Islamic art
            "tell me about Islamic calligraphy", # Test Islamic art search
            "show me Islamic podcasts",  # Test media recommendations
            "find Islamic videos about Quran",  # Test media search
            "recommend Islamic books",  # Test book recommendations
            "find books about spirituality",  # Test book search
            "I'm feeling anxious, need Islamic guidance",  # Test counselling
            "Help with depression from Islamic perspective",  # Test counselling
            # Add after existing test queries
            "show me Islamic games",  # Test games
            "find games for children",  # Test games search
            "give feedback",  # Test feedback collection
            "rate this response 5",  # Test rating
            "suggest improvement for prayers"  # Test improvement suggestion
        ]

        print("\nRunning test sequence...")
        success = True
        for query in test_queries:
            try:
                print(f"\nTesting query: {query}")
                logging.info(f"Testing query: {query}")
                result = self.process_input(query)
                logging.info(f"Query result: {'success' if result else 'failed'}")

                if not result:
                    logging.error(f"Test failed on query: {query}")
                    success = False
                    break
            except Exception as e:
                logging.error(f"Error during test sequence on query '{query}': {str(e)}")
                success = False
                break

        if success:
            print("\nTest sequence completed successfully.")
            logging.info("Test sequence completed successfully")
        else:
            print("\nTest sequence failed.")
            logging.error("Test sequence failed")

        return success

    def run_feature_test(self, feature: str) -> bool:
        """Run test for a specific feature."""
        logging.info(f"Testing feature: {feature}")
        test_queries = {
            'counselling': [
                "I'm feeling anxious, need Islamic guidance",
                "Help with depression from Islamic perspective"
            ],
            'art': [
                "show me Islamic art",
                "tell me about Islamic calligraphy"
            ],
            'media': [
                "show me Islamic podcasts",
                "find Islamic videos about Quran"
            ],
            'books': [
                "recommend Islamic books",
                "find books about spirituality"
            ],
            'games': [
                "show me Islamic games",
                "find games for children"
            ],
            'feedback': [
                "give feedback",
                "rate this response 5"
            ]
        }

        if feature not in test_queries:
            self.console.print(f"Unknown feature: {feature}", style="red")
            return False

        success = True
        for query in test_queries[feature]:
            self.console.print(f"\nTesting query: {query}", style="blue")
            if not self.process_input(query):
                self.console.print(f"Failed on query: {query}", style="red")
                success = False

        return success

    def run(self, test_input: Optional[str] = None) -> bool:
        """Main chatbot loop."""
        self.display_welcome()

        if test_input:
            return self.process_input(test_input)
        elif self.test_mode:
            return self.run_test_sequence()

        try:
            while True:
                if sys.stdin.isatty():
                    user_input = Prompt.ask("\nAsk me anything").strip()
                else:
                    logging.warning("Non-interactive environment detected, exiting.")
                    return True

                if not self.process_input(user_input):
                    if user_input.lower() == 'exit':
                        self.console.print("Thank you for using DeenAI. Allah Hafiz!", style="green")
                        break
            return True
        except (EOFError, KeyboardInterrupt):
            logging.info("Exiting gracefully")
            return True


def __main__():
    """Main entry point for the chatbot."""
    parser = argparse.ArgumentParser(description='Islamic Chatbot')
    parser.add_argument('--test', action='store_true', help='Run test sequence')
    parser.add_argument('--test-feature', help='Test specific feature (counselling, art, media, books, games, feedback)')
    args = parser.parse_args()

    # Setup logging
    setup_logging()

    chatbot = IslamicChatbot(test_mode=args.test)

    if args.test_feature:
        success = chatbot.run_feature_test(args.test_feature)
        sys.exit(0 if success else 1)
        return

    if args.test:
        success = chatbot.run_test_sequence()
        sys.exit(0 if success else 1)
        return

    # Regular interactive mode
    chatbot.run()

if __name__ == "__main__":
    __main__()
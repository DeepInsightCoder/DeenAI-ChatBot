# API endpoints
QURAN_API_BASE = "https://api.alquran.cloud/v1"
HADITH_API_BASE = "https://api.sunnah.com/v1"
PRAYER_API_BASE = "https://api.aladhan.com/v1"

# Common Islamic questions and answers
ISLAMIC_QA = {
    "zakat": {
        "answer": "Zakat is one of the Five Pillars of Islam. It is a mandatory charitable contribution, typically 2.5% of one's savings, given to those in need.",
        "references": {
            "quran": ["At-Tawbah 9:60", "Al-Baqarah 2:43"],
            "hadith": ["Sahih Bukhari 1395", "Sahih Muslim 16"]
        }
    },
    "hajj": {
        "answer": "Hajj is the annual Islamic pilgrimage to Mecca, Saudi Arabia. It is mandatory for Muslims who are physically and financially capable of undertaking the journey.",
        "references": {
            "quran": ["Ali 'Imran 3:97", "Al-Baqarah 2:196"],
            "hadith": ["Sahih Bukhari 1513"]
        }
    },
    "salah": {
        "answer": "Salah refers to the five daily prayers in Islam: Fajr (dawn), Dhuhr (noon), Asr (afternoon), Maghrib (sunset), and Isha (night).",
        "references": {
            "quran": ["Al-Baqarah 2:43", "An-Nisa 4:103"],
            "hadith": ["Sahih Bukhari 8"]
        }
    },
    "sawm": {
        "answer": "Sawm is fasting during the month of Ramadan from dawn until sunset. It is one of the Five Pillars of Islam.",
        "references": {
            "quran": ["Al-Baqarah 2:183-185"],
            "hadith": ["Sahih Bukhari 1904"]
        }
    },
    "shahada": {
        "answer": "The Shahada is the Islamic declaration of faith: 'There is no god but Allah, and Muhammad is the messenger of Allah.'",
        "references": {
            "quran": ["Muhammad 47:19"],
            "hadith": ["Sahih Muslim 16a"]
        }
    },
    "wudu": {
        "answer": "Wudu is the Islamic ritual washing performed before prayer and handling the Quran. It involves washing specific parts of the body in a particular order.",
        "references": {
            "quran": ["Al-Ma'idah 5:6"],
            "hadith": ["Sahih Bukhari 164"]
        }
    },
    "halal_food": {
        "answer": "Halal food refers to what is permissible to eat in Islam. This includes most vegetables, fruits, grains, and properly slaughtered livestock. Pork and alcohol are prohibited.",
        "references": {
            "quran": ["Al-Ma'idah 5:3", "Al-Baqarah 2:173"],
            "hadith": ["Sahih Muslim 1934"]
        }
    }
}

# NLTK patterns for question matching
QUESTION_PATTERNS = [
    # More specific patterns first
    (r'^(?:(?:what\s+is|tell\s+me)\s+)?(?:today\'?s?\s+)?(?:islamic\s+date|hijri\s+date|current\s+islamic\s+date)[\?\s]*$', 'islamic_calendar'),
    (r'calculate(?:\s+my)?\s+zakat|zakat\s+calculation|how\s+much\s+(?:is\s+)?zakat|compute\s+zakat', 'zakat_calc'),
    (r'(?:search|find).*(?:in\s+)?(?:quran|the\s+quran|quranic verse).*(?:about|for|containing)?\s+\w+', 'quran_search'),
    (r'show me surah|show surah|quran surah', 'quran'),
    (r'prayer times? (in|for|at)', 'prayer_times'),
    (r'hadith about', 'hadith'),
    (r'(?:show|tell|give)?\s*(?:me\s+)?(?:daily|today\'?s?)\s+(?:reminder|islamic reminder|wisdom)', 'daily_reminder'),
    (r'(?:tell|show)\s+(?:me\s+)?(?:about\s+)?(?:islamic\s+history|prophet|prophets?)', 'islamic_history'),
    (r'(?:show|display|list|view)\s+(?:my\s+)?(?:history|surah history|islamic history)', 'show_history'),
    (r'(?:play|recite|listen to)\s+(?:surah|ayah|verse)\s+(\d+)(?:\s*,\s*(?:ayah|verse)\s*(\d+))?', 'audio_recitation'),
    (r'(?:what\s+is|explain|tell\s+me\s+about|question\s+about)\s+(?:islamic\s+)?([a-z\s]+)\??', 'islamic_qa'),
    # New patterns for Hajj/Umrah
    (r'(?:show|tell|explain)(?:\s+me)?\s+(?:about\s+)?(?:hajj|umrah)\s+(?:steps?|guide|ritual)', 'hajj_guide'),
    (r'(?:what\s+are\s+)?(?:hajj|umrah)\s+(?:requirements?|faqs?|preparations?)', 'hajj_faq'),
    # Added Islamic Finance patterns
    (r'(?:tell|show|explain)(?:\s+me)?\s+(?:about\s+)?(?:islamic\s+finance|halal\s+investment|riba|islamic\s+business)', 'islamic_finance'),
    (r'(?:how\s+to|what\s+are)\s+(?:invest|avoid\s+riba|halal\s+business|islamic\s+banking)', 'islamic_finance'),
    # New Islamic parenting patterns
    (r'(?:tell|show|explain)(?:\s+me)?\s+(?:about\s+)?(?:islamic\s+parenting|raising\s+children|child\s+education)', 'islamic_parenting'),
    (r'(?:how\s+to|what\s+are)\s+(?:raise|teach|discipline)\s+(?:children|kids)\s+(?:in\s+islam|islamically)', 'islamic_parenting'),
    # New patterns for Islamic art queries
    (r'(?:show|display|find)\s+(?:me\s+)?(?:islamic\s+)?(?:art|calligraphy|pattern)', 'islamic_art'),
    (r'(?:search|look\s+for)\s+(?:islamic\s+)?art\s+(?:about|containing|with)\s+([a-z\s]+)', 'islamic_art_search'),
    # Add new patterns for media queries
    (r'(?:show|find|recommend)\s+(?:me\s+)?(?:islamic\s+)?(?:podcasts?|videos?|lectures?)', 'islamic_media'),
    (r'(?:search|look\s+for)\s+(?:islamic\s+)?(?:podcasts?|videos?)\s+(?:about|containing|with)\s+([a-z\s]+)', 'islamic_media_search'),
    # Add new patterns for book queries
    (r'(?:show|find|recommend)\s+(?:me\s+)?(?:islamic\s+)?(?:books?|reading)', 'islamic_books'),
    (r'(?:search|look\s+for)\s+(?:islamic\s+)?books?\s+(?:about|on|for)\s+([a-z\s]+)', 'islamic_books_search'),
    # Add counselling patterns
    (r'(?:help|advice|guidance)\s+(?:with|about|for)\s+(?:anxiety|depression|stress|relationship)', 'islamic_counselling'),
    (r'(?:feel(?:ing)?|am)\s+(?:anxious|depressed|stressed|worried|sad)', 'islamic_counselling'),
    (r'(?:islamic|muslim)\s+(?:counselling|therapy|mental\s+health)', 'islamic_counselling'),
    # Add new patterns for game queries
    (r'(?:play|start|show)\s+(?:me\s+)?(?:islamic\s+)?(?:games?|quiz(?:zes)?|activities?)', 'islamic_games'),
    (r'(?:find|search)\s+(?:islamic\s+)?games?\s+(?:for|about)\s+([a-z\s]+)', 'islamic_games_search'),
    # More general patterns last
    (r'what is', 'definition'),
    (r'how to', 'instruction'),
    (r'tell me about', 'information')
]

# Daily Islamic Reminders
DAILY_REMINDERS = [
    {
        'type': 'hadith',
        'text': 'The Prophet (ﷺ) said: "The best of you are those who learn the Quran and teach it to others."',
        'source': 'Sahih Al-Bukhari'
    },
    {
        'type': 'wisdom',
        'text': 'Every act of kindness is charity. - Prophet Muhammad (ﷺ)',
        'source': 'Islamic Wisdom'
    },
    {
        'type': 'quran',
        'text': '"Indeed, with hardship comes ease." (Quran 94:5)',
        'source': 'Surah Ash-Sharh'
    },
    {
        'type': 'dua',
        'text': 'رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ\nRabbana atina fid-dunya hasanatan wa fil-akhirati hasanatan waqina adhaban-nar\n"Our Lord, give us good in this world and good in the Hereafter, and protect us from the torment of the Fire."',
        'source': 'Quran 2:201'
    },
    {
        'type': 'wisdom',
        'text': 'Five before Five: Take benefit of five before five: Your youth before your old age, your health before your sickness, your wealth before your poverty, your free time before your preoccupation, and your life before your death.',
        'source': 'Islamic Teaching'
    }
]

# Zakat calculation constants
ZAKAT_NISAB_GOLD = 87.48  # grams of gold
ZAKAT_NISAB_SILVER = 612.36  # grams of silver
ZAKAT_RATE = 0.025  # 2.5%

# Current gold and silver prices (to be updated regularly)
GOLD_PRICE_PER_GRAM = 85  # USD
SILVER_PRICE_PER_GRAM = 1  # USD

# History of prophets and important Islamic figures
ISLAMIC_HISTORY = {
    "Prophet Muhammad (ﷺ)": "The final messenger of Allah, born in Makkah in 570 CE. He received the first revelation of the Quran at age 40.",
    "Prophet Ibrahim (AS)": "Known as the Friend of Allah (Khalilullah), he rebuilt the Kaaba with his son Ismail.",
    "Prophet Musa (AS)": "Received the Torah and led the Children of Israel out of Egypt.",
    "Prophet Isa (AS)": "Born to Maryam (AS), he was given the Injeel (Gospel) and performed miracles by Allah's permission.",
    "Prophet Yusuf (AS)": "Son of Yaqub (AS), his story is described as the most beautiful of stories in the Quran.",
}
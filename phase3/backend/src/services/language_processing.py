"""
Language Processing Module for Roman Urdu Support
"""

import re
from typing import Dict, List, Tuple

# Dictionary mapping Roman Urdu to English equivalents for common commands
ROMAN_URDU_TO_ENGLISH = {
    # Task creation commands
    'bnana': 'create',
    'banaya': 'create',
    'create': 'create',
    'add': 'add',
    'naya': 'new',
    'new': 'new',
    'kaam': 'task',
    'kam': 'task',
    'task': 'task',
    'todo': 'todo',
    'list': 'list',
    'dikhao': 'show',
    'dikhaye': 'show',
    'dikhaw': 'show',
    'show': 'show',
    'kya': 'what',
    'hai': 'is',
    'ha': 'have',
    'kia': 'what',
    'krna': 'do',
    'kar': 'do',
    'karna': 'do',
    'pending': 'pending',
    'panding': 'pending',
    'khatam': 'complete',
    'khtm': 'complete',
    'band': 'complete',
    'done': 'done',
    'hogya': 'done',
    'ho_gaya': 'done',
    'completed': 'complete',
    'all': 'all',
    'sab': 'all',
    'sb': 'all',
    'sabse': 'all',
    'sbse': 'all',
    'jitni': 'all',
    'kuch': 'some',
    'koi': 'any',
    'konsa': 'which',
    'kon': 'who',
    'koun': 'who',
    'konse': 'which',
    'kon_si': 'which',
    'kon_c': 'which',
    'mera': 'my',
    'meri': 'my',
    'mra': 'my',
    'mri': 'my',
    'tera': 'your',
    'teri': 'your',
    'tra': 'your',
    'tri': 'your',
    'hamara': 'our',
    'hamari': 'our',
    'hmara': 'our',
    'hmari': 'our',
    'iska': 'his',
    'iski': 'his',
    'is': 'this',
    'ye': 'this',
    'wo': 'that',
    'vo': 'that',
    'in': 'these',
    'un': 'those',
    'ye_sab': 'all_these',
    'wo_sab': 'all_those',
    'ab': 'now',
    'just': 'now',
    'phle': 'first',
    'pehle': 'first',
    'last': 'last',
    'akhir': 'last',
    'baad': 'after',
    'agay': 'forward',
    'piche': 'backward',
    'upar': 'above',
    'neeche': 'below',
    'right': 'right',
    'left': 'left',
    'center': 'center',
    'middle': 'middle',
    'finish': 'finish',
    'end': 'end',
    'close': 'close',
    'band': 'close',
    'khtm': 'finish',
    'khatam': 'finish',
    'start': 'start',
    'shuru': 'start',
    'begin': 'start',
    'open': 'open',
    'khul': 'open',
    'khula': 'open',
    'save': 'save',
    'rakh': 'save',
    'rakho': 'save',
    'rakhe': 'save',
    'rakhi': 'save',
    'rakha': 'save',
    'load': 'load',
    'layo': 'load',
    'laye': 'load',
    'layi': 'load',
    'laya': 'load',
    'load_karo': 'load',
    'load_kar': 'load',
    'load_kiya': 'loaded',
    'load_ki': 'loaded',
    'load_hua': 'loaded',
    'load_hui': 'loaded',
    'load_huya': 'loaded',
    'load_huye': 'loaded',
    'delete': 'delete',
    'remove': 'remove',
    'hatana': 'remove',
    'nikal': 'remove',
    'complete': 'complete',
    'ho': 'is',
    'gya': 'done',
    'hogya': 'completed',
    'ho gaya': 'completed',
    'done': 'done',
    'mark': 'mark',
    'as': 'as',
    'krdo': 'mark',
    'kardo': 'mark',
    'help': 'help',
    'madad': 'help',
    'chahiye': 'want',
    'chahta': 'want',
    'chahti': 'want',
    'kaise': 'how',
    'kya': 'what',
    'hai': 'is',
    'koi': 'any',
    'kuch': 'some',
    'sab': 'all',
    'sara': 'all',
    'today': 'today',
    'aj': 'today',
    'kal': 'tomorrow',
    'jitni': 'all',
    'sab': 'all',
    'sabse': 'all',
    'sb': 'all',
    'sbse': 'all',
    'plz': 'please',
    'plx': 'please',
    'krdo': 'please_do',
    'kardo': 'please_do',
    'kijiye': 'please_do',
    'kijiyeh': 'please_do',
    'karni': 'to_do',
    'karna': 'to_do',
    'krni': 'to_do',
    'krna': 'to_do',
    'kr': 'do',
    'kro': 'do',
    'karo': 'do',
    'ker': 'do',
    'kiya': 'did',
    'kiye': 'did',
    'kia': 'did',
    'krke': 'after_doing',
    'kr k': 'after_doing',
    'k jo': 'that_i_will_do',
    'jo': 'that',
    'jis': 'which',
    'jise': 'whom',
    'jb': 'when',
    'jab': 'when',
    'kyun': 'why',
    'kio': 'why',
    'kyn': 'why',
    'kab': 'when',
    'kb': 'when',
    'kaha': 'where',
    'kahan': 'where',
    'konsa': 'which',
    'kon': 'who',
    'koun': 'who',
    'konse': 'which',
    'kon_si': 'which',
    'kon_c': 'which',
    'mera': 'my',
    'meri': 'my',
    'mra': 'my',
    'mri': 'my',
    'tera': 'your',
    'teri': 'your',
    'tra': 'your',
    'tri': 'your',
    'hamara': 'our',
    'hamari': 'our',
    'hmara': 'our',
    'hmari': 'our',
    'iska': 'his',
    'iski': 'his',
    'is': 'this',
    'ye': 'this',
    'wo': 'that',
    'vo': 'that',
    'in': 'these',
    'un': 'those',
    'ye_sab': 'all_these',
    'wo_sab': 'all_those',
    'ab': 'now',
    'just': 'now',
    'phle': 'first',
    'pehle': 'first',
    'last': 'last',
    'akhir': 'last',
    'baad': 'after',
    'agay': 'forward',
    'piche': 'backward',
    'upar': 'above',
    'neeche': 'below',
    'right': 'right',
    'left': 'left',
    'center': 'center',
    'middle': 'middle',
    'finish': 'finish',
    'end': 'end',
    'close': 'close',
    'band': 'close',
    'khtm': 'finish',
    'khatam': 'finish',
    'start': 'start',
    'shuru': 'start',
    'begin': 'start',
    'open': 'open',
    'khul': 'open',
    'khula': 'open',
    'save': 'save',
    'rakh': 'save',
    'rakho': 'save',
    'rakhe': 'save',
    'rakhi': 'save',
    'rakha': 'save',
    'load': 'load',
    'layo': 'load',
    'laye': 'load',
    'layi': 'load',
    'laya': 'load',
    'load_karo': 'load',
    'load_kar': 'load',
    'load_kiya': 'loaded',
    'load_ki': 'loaded',
    'load_hua': 'loaded',
    'load_hui': 'loaded',
    'load_huya': 'loaded',
    'load_huye': 'loaded',
}

def preprocess_roman_urdu(text: str) -> str:
    """
    Preprocess Roman Urdu text to improve intent recognition
    """
    # Convert to lowercase for consistent matching
    text = text.lower()
    
    # Normalize common variations
    text = re.sub(r'[aeiou]+', lambda m: m.group()[0], text)  # Reduce vowel repetition
    text = re.sub(r'[aeiou]{2,}', lambda m: m.group()[0], text)  # Reduce vowel sequences
    
    # Split text into words
    words = text.split()
    
    # Translate Roman Urdu words to English equivalents
    translated_words = []
    for word in words:
        # Remove punctuation for comparison
        clean_word = re.sub(r'[^\w]', '', word)
        if clean_word in ROMAN_URDU_TO_ENGLISH:
            translated_words.append(ROMAN_URDU_TO_ENGLISH[clean_word])
        else:
            translated_words.append(word)
    
    return ' '.join(translated_words)

def detect_language(text: str) -> str:
    """
    Simple language detection based on character patterns
    """
    # Check for common Roman Urdu patterns
    roman_urdu_patterns = [
        r'(kaam|kam|bnana|banaya|kya|hai|krna|kar|karna|ho|gya|hogya|ho_gaya)',
        r'(aj|kal|jitni|sab|sabse|sb|sbse|plz|plx|madad|chahiye|chahta|chahti)'
    ]
    
    text_lower = text.lower()
    for pattern in roman_urdu_patterns:
        if re.search(pattern, text_lower):
            return 'roman_urdu'
    
    return 'english'

def translate_for_intent_classification(text: str) -> str:
    """
    Translate text to English for intent classification
    """
    lang = detect_language(text)
    
    if lang == 'roman_urdu':
        return preprocess_roman_urdu(text)
    else:
        return text
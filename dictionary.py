# dictionary.py
import os
import urllib.request
from pathlib import Path

class Dictionary:
    """Load and manage the dictionary of valid words"""
    
    # Common English words URL (you can also use a local file)
    DEFAULT_WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    
    def __init__(self, wordlist_path=None):
        self.words = set()
        self.wordlist_path = wordlist_path or "words.txt"
        self.load_dictionary()
    
    def load_dictionary(self):
        """Load words from file or download if not exists"""
        if not os.path.exists(self.wordlist_path):
            print(f"📥 Downloading word list...")
            self.download_wordlist()
        
        try:
            with open(self.wordlist_path, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if word.isalpha():  # Only keep alphabetic words
                        self.words.add(word)
            print(f"✅ Loaded {len(self.words):,} words")
        except Exception as e:
            print(f"❌ Error loading dictionary: {e}")
            # Fallback to a small built-in dictionary
            self.words = self.get_fallback_dictionary()
            print(f"✅ Using fallback dictionary with {len(self.words)} words")
    
    def download_wordlist(self):
        """Download a standard English word list"""
        try:
            urllib.request.urlretrieve(self.DEFAULT_WORDLIST_URL, self.wordlist_path)
        except:
            # If download fails, create a basic word list
            self.create_basic_wordlist()
    
    def create_basic_wordlist(self):
        """Create a basic word list if download fails"""
        basic_words = """
        the be to of and a in that have i it for not on with he as you do at
        this but his by from they we say her she or an will my one all would
        there their what so up out if about who get which go me when make can
        like time no just him know take people into year your good some could
        them see other than then now look only come its over think also back
        after use two how our work first well way even new want because any
        these give day most us
        """.split()
        
        with open(self.wordlist_path, 'w') as f:
            for word in basic_words:
                f.write(word + '\n')
    
    def get_fallback_dictionary(self):
        """Return a small built-in dictionary as fallback"""
        return {
            "hello", "world", "python", "programming", "algorithm", "tree",
            "spell", "check", "dictionary", "word", "computer", "science",
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
            "for", "not", "on", "with", "he", "as", "you", "do", "at", "this"
        }
    
    def is_valid(self, word):
        """Check if a word exists in dictionary"""
        return word.lower() in self.words
    
    def get_all_words(self):
        """Return all words in dictionary"""
        return self.words
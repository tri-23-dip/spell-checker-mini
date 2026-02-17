"""
Dictionary management module for loading and accessing valid words.
Supports local files, downloads, and fallback dictionaries.
"""

import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Set, Optional

class Dictionary:
    """Load and manage the dictionary of valid words."""
    
    # Common English words URL
    DEFAULT_WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    
    def __init__(self, wordlist_path: Optional[str] = None):
        """
        Initialize the dictionary.
        
        Args:
            wordlist_path: Path to word list file (default: 'words.txt')
        """
        self.words: Set[str] = set()
        self.wordlist_path = wordlist_path or "words.txt"
        self.load_dictionary()
    
    @property
    def size(self) -> int:
        """Return the number of words in dictionary."""
        return len(self.words)
    
    def load_dictionary(self) -> None:
        """Load words from file or download if not exists."""
        if not os.path.exists(self.wordlist_path):
            print(f"📥 Downloading word list to {self.wordlist_path}...")
            self.download_wordlist()
        
        try:
            # Use UTF-8 encoding and handle different line endings
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    word = line.strip().lower()
                    # Better validation: at least 2 chars, only letters
                    if word and len(word) >= 2 and word.isalpha():
                        self.words.add(word)
                    elif word and word.isalpha() and len(word) == 1:
                        # Allow single letters? (a, I)
                        self.words.add(word)
            
            print(f"✅ Loaded {self.size:,} words from {self.wordlist_path}")
            
        except Exception as e:
            print(f"❌ Error loading dictionary: {e}")
            # Fallback to a small built-in dictionary
            self.words = self.get_fallback_dictionary()
            print(f"✅ Using fallback dictionary with {self.size} words")
    
    def download_wordlist(self) -> None:
        """Download a standard English word list."""
        try:
            # Add user-agent to avoid being blocked
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(self.DEFAULT_WORDLIST_URL, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(self.wordlist_path, 'wb') as f:
                    f.write(response.read())
            print(f"✅ Downloaded word list successfully")
            
        except urllib.error.URLError as e:
            print(f"⚠️  Download failed: {e}")
            self.create_basic_wordlist()
        except Exception as e:
            print(f"⚠️  Unexpected error during download: {e}")
            self.create_basic_wordlist()
    
    def create_basic_wordlist(self) -> None:
        """Create a basic word list if download fails."""
        basic_words = """
        the be to of and a in that have i it for not on with he as you do at
        this but his by from they we say her she or an will my one all would
        there their what so up out if about who get which go me when make can
        like time no just him know take people into year your good some could
        them see other than then now look only come its over think also back
        after use two how our work first well way even new want because any
        these give day most us is was are has had been were said have will
        hello world python programming algorithm tree spell check dictionary
        word computer science data structure function method class object
        """.split()
        
        try:
            with open(self.wordlist_path, 'w', encoding='utf-8') as f:
                for word in sorted(set(basic_words)):
                    f.write(word + '\n')
            print(f"✅ Created basic word list with {len(set(basic_words))} words")
        except Exception as e:
            print(f"⚠️  Could not create word list: {e}")
    
    def get_fallback_dictionary(self) -> Set[str]:
        """Return a small built-in dictionary as fallback."""
        return {
            "a", "an", "the", "and", "or", "but", "if", "then", "else",
            "hello", "world", "python", "programming", "algorithm", "tree",
            "spell", "check", "dictionary", "word", "computer", "science",
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "it",
            "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
            "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
            "will", "my", "one", "all", "would", "there", "their", "what", "so",
            "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
            "make", "can", "like", "time", "no", "just", "him", "know", "take",
            "people", "into", "year", "your", "good", "some", "could", "them",
            "see", "other", "than", "then", "now", "look", "only", "come", "its",
            "over", "think", "also", "back", "after", "use", "two", "how", "our",
            "work", "first", "well", "way", "even", "new", "want", "because",
            "any", "these", "give", "day", "most", "us"
        }
    
    def is_valid(self, word: str) -> bool:
        """Check if a word exists in dictionary."""
        if not word or not isinstance(word, str):
            return False
        return word.lower().strip() in self.words
    
    def add_word(self, word: str) -> bool:
        """Add a new word to the dictionary."""
        word = word.lower().strip()
        
        # Validate word
        if not word or not word.isalpha():
            return False
        
        # Check if already exists
        if word in self.words:
            return False
        
        # Add to set
        self.words.add(word)
        
        # Optionally append to file (silent fail if can't write)
        try:
            with open(self.wordlist_path, 'a', encoding='utf-8') as f:
                f.write(word + '\n')
        except:
            pass  # Don't fail if we can't write to file
        
        return True
    
    def get_all_words(self) -> Set[str]:
        """Return all words in dictionary."""
        return self.words.copy()  # Return a copy to prevent modification
    
    def contains_prefix(self, prefix: str) -> bool:
        """Check if any word starts with the given prefix."""
        prefix = prefix.lower().strip()
        return any(w.startswith(prefix) for w in self.words)
    
    def get_words_by_length(self, length: int) -> Set[str]:
        """Get all words of a specific length."""
        return {w for w in self.words if len(w) == length}
    
    def __contains__(self, word: str) -> bool:
        """Enable 'in' operator support."""
        return self.is_valid(word)
    
    def __len__(self) -> int:
        """Enable len() support."""
        return self.size
    
    def __repr__(self) -> str:
        return f"Dictionary(size={self.size}, file={self.wordlist_path})"

# Quick test if run directly
if __name__ == "__main__":
    print("Testing Dictionary module...")
    d = Dictionary()
    print(f"Dictionary: {d}")
    print(f"Sample words: {list(d.words)[:10]}")
    print(f"Is 'hello' valid? {d.is_valid('hello')}")
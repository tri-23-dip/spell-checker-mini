"""
Dictionary management module.
"""

import os
from typing import Set, Optional


class Dictionary:
    def __init__(self, wordlist_path: Optional[str] = None):
        self.wordlist_path = wordlist_path or "words.txt"
        self.words: Set[str] = set()
        self.load_dictionary()

    @property
    def size(self) -> int:
        return len(self.words)

    def load_dictionary(self):
        if not os.path.exists(self.wordlist_path):
            raise FileNotFoundError(f"{self.wordlist_path} not found.")

        with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip().lower()
                if word.isalpha():
                    self.words.add(word)

    def is_valid(self, word: str) -> bool:
        if not word or not isinstance(word, str):
            return False
        return word.lower().strip() in self.words

    def add_word(self, word: str) -> bool:
        word = word.lower().strip()
        if not word.isalpha():
            return False
        if word in self.words:
            return False

        self.words.add(word)

        try:
            with open(self.wordlist_path, "a", encoding="utf-8") as f:
                f.write(word + "\n")
        except:
            pass

        return True

    def get_all_words(self) -> Set[str]:
        return self.words.copy()

    def __contains__(self, word: str) -> bool:
        return self.is_valid(word)

    def __len__(self) -> int:
        return self.size
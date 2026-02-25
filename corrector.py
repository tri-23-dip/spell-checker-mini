"""
Main spell checker module.
"""

import re
from dictionary import Dictionary
from bktree import BKTree
from distance import levenshtein, damerau_levenshtein


class SpellChecker:
    def __init__(self, use_advanced_distance=True, dictionary_file="words.txt"):
        self.dictionary = Dictionary(wordlist_path=dictionary_file)

        self.use_advanced = use_advanced_distance
        distance_func = (
            damerau_levenshtein if use_advanced_distance else levenshtein
        )

        self.tree = BKTree(distance_func)
        self.tree.build_from_list(self.dictionary.get_all_words())

    def check_word(self, word):
        return self.dictionary.is_valid(word)

    def suggest_corrections(self, word, max_suggestions=5, max_distance=2):
        if not word:
            return []

        word = word.lower().strip()

        if self.check_word(word):
            return [(word, 0)]

        results = self.tree.search(word, max_distance)
        return results[:max_suggestions]

    def check_text(self, text):
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        results = {}

        for word in words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word)
                if suggestions:
                    results[word] = suggestions

        return results

    def auto_correct(self, text, max_distance=2):
        if not text:
            return text

        words = re.findall(r"\b[a-zA-Z]+\b", text)
        corrected = text

        unique_words = sorted(set(words), key=len, reverse=True)

        for word in unique_words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word, max_distance=max_distance)
                if suggestions:
                    best = suggestions[0][0]

                    if word.isupper():
                        best = best.upper()
                    elif word[0].isupper():
                        best = best.capitalize()

                    pattern = r"\b" + re.escape(word) + r"\b"
                    corrected = re.sub(pattern, best, corrected)

        return corrected
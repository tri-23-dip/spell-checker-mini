"""
Main spell checker module that ties together dictionary, BK-tree, and distance algorithms.
"""

import re
from dictionary import Dictionary
from bktree import BKTree
from distance import levenshtein, damerau_levenshtein

class SpellChecker:
    """Main spell checker class that ties everything together."""
    
    def __init__(self, use_advanced_distance=True, dictionary_file='words.txt'):
        """
        Initialize the spell checker.
        
        Args:
            use_advanced_distance: Whether to use Damerau-Levenshtein (True) 
                                  or basic Levenshtein (False)
            dictionary_file: Path to the dictionary file
        """
        self.dictionary = Dictionary()
        self.dictionary.load_dictionary(dictionary_file)
        
        # Choose distance function
        self.use_advanced = use_advanced_distance
        distance_func = damerau_levenshtein if use_advanced_distance else levenshtein
        
        # Initialize BK-tree with chosen distance function
        self.tree = BKTree(distance_func=distance_func)
        
        # Build the BK-tree from dictionary
        print(f"🌳 Building BK-tree with {self.dictionary.size:,} words...")
        self.tree.build_from_list(self.dictionary.get_all_words())
        print(f"✅ BK-tree built with {self.tree.size:,} nodes")
        
        # Common typos and their corrections
        self.common_corrections = {
            "teh": "the",
            "recieve": "receive",
            "wierd": "weird",
            "definately": "definitely",
            "seperate": "separate",
            "occured": "occurred",
            "acommodate": "accommodate",
            "acheive": "achieve",
            "adress": "address",
            "alot": "a lot",
            "begginer": "beginner",
            "beleive": "believe",
            "calender": "calendar",
            "collegue": "colleague",
            "comming": "coming",
            "concious": "conscious",
            "curiousity": "curiosity",
            "decaffination": "decaffeination",
        }
    
    def check_word(self, word):
        """Check if a single word is spelled correctly."""
        return self.dictionary.is_valid(word)
    
    def suggest_corrections(self, word, max_suggestions=5, max_distance=2):
        """
        Suggest corrections for a misspelled word.
        
        Args:
            word: The misspelled word
            max_suggestions: Maximum number of suggestions to return
            max_distance: Maximum edit distance for suggestions
            
        Returns:
            List of (word, distance) tuples, sorted by distance
        """
        if not word or not isinstance(word, str):
            return []
        
        word = word.lower().strip()
        
        # Check if word is already correct
        if self.check_word(word):
            return [(word, 0)]
        
        # Check common typos first
        if word in self.common_corrections:
            correction = self.common_corrections[word]
            return [(correction, 1)]
        
        # Search in BK-tree
        results = self.tree.search(word, max_distance)
        
        # If no results with BK-tree, try manual search with advanced distance
        if not results and self.use_advanced:
            results = self._manual_search(word, max_distance)
        
        # Filter out the original word if it appears
        results = [(w, d) for w, d in results if w != word]
        
        return results[:max_suggestions]
    
    def _manual_search(self, word, max_distance):
        """Fallback manual search through all dictionary words."""
        results = []
        from distance import damerau_levenshtein
        
        for dict_word in self.dictionary.get_all_words():
            dist = damerau_levenshtein(word, dict_word)
            if dist <= max_distance:
                results.append((dict_word, dist))
        
        results.sort(key=lambda x: x[1])
        return results
    
    def check_text(self, text):
        """
        Check an entire text and return misspelled words with suggestions.
        
        Returns:
            Dictionary with misspelled words as keys and suggestions as values
        """
        if not text:
            return {}
        
        # Simple word tokenization
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        results = {}
        
        for word in words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word)
                if suggestions:  # Only include if we have suggestions
                    results[word] = suggestions
        
        return results
    
    def auto_correct(self, text, max_distance=2):
        """
        Automatically correct text using best suggestions.
        
        Args:
            text: Input text to correct
            max_distance: Maximum edit distance for corrections
            
        Returns:
            Corrected text
        """
        if not text:
            return text
        
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        corrected = text
        
        # Sort words by length (longest first) to avoid partial replacements
        unique_words = sorted(set(words), key=len, reverse=True)
        
        for word in unique_words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word, max_distance=max_distance)
                if suggestions:
                    # Use word boundaries to replace only whole words
                    pattern = r'\b' + re.escape(word) + r'\b'
                    corrected = re.sub(pattern, suggestions[0][0], corrected)
        
        return corrected
    
    def add_to_dictionary(self, word):
        """Add a new word to the dictionary."""
        if self.dictionary.add_word(word):
            # Rebuild tree to include new word
            self.tree.insert(word)
            return True
        return False
    
    def get_stats(self):
        """Get statistics about the spell checker."""
        return {
            'dictionary_size': self.dictionary.size,
            'tree_size': self.tree.size,
            'using_advanced_distance': self.use_advanced,
            'common_corrections': len(self.common_corrections)
        }

def demo_mode():
    """Interactive demo of the spell checker."""
    print("\n" + "="*60)
    print("🔤 SPELL CHECKER MINI - DEMO MODE")
    print("="*60)
    
    # Initialize with advanced distance
    checker = SpellChecker(use_advanced_distance=True)
    
    while True:
        print("\n📝 Enter a word or sentence (or 'quit' to exit, 'stats' for info):")
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'stats':
            stats = checker.get_stats()
            print("\n📊 Spell Checker Statistics:")
            for key, value in stats.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
            continue
        
        if ' ' in user_input:
            # Sentence mode
            print("\n🔍 Checking sentence...")
            errors = checker.check_text(user_input)
            
            if not errors:
                print("✅ All words are correct!")
            else:
                print(f"❌ Found {len(errors)} potential error(s):")
                for wrong, suggestions in errors.items():
                    if suggestions:
                        sugg_str = ', '.join([f"'{s[0]}'({s[1]})" for s in suggestions[:3]])
                        print(f"   • '{wrong}' → {sugg_str}")
                    else:
                        print(f"   • '{wrong}' → No suggestions found")
                
                # Show auto-corrected version
                corrected = checker.auto_correct(user_input)
                if corrected != user_input:
                    print(f"\n✨ Auto-corrected: {corrected}")
        else:
            # Single word mode
            if checker.check_word(user_input):
                print(f"✅ '{user_input}' is spelled correctly!")
            else:
                print(f"❌ '{user_input}' might be misspelled")
                suggestions = checker.suggest_corrections(user_input)
                if suggestions:
                    print("💡 Suggestions:")
                    for word, dist in suggestions[:5]:
                        print(f"   → {word} (distance: {dist})")
                else:
                    print("   No suggestions found")

if __name__ == "__main__":
    demo_mode()
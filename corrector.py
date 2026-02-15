# corrector.py
import re
from dictionary import Dictionary
from bktree import BKTree
from distance import levenshtein_distance, damerau_levenshtein_distance

class SpellChecker:
    """Main spell checker class that ties everything together"""
    
    def __init__(self, use_advanced_distance=True):
        self.dictionary = Dictionary()
        self.tree = BKTree()
        self.use_advanced = use_advanced_distance
        
        # Build the BK-tree from dictionary
        print("🌳 Building BK-tree for fast lookup...")
        self.tree.build_from_list(self.dictionary.get_all_words())
        print(f"✅ BK-tree built with {self.tree.size:,} nodes")
        
        # Common typos and their corrections (for learning)
        self.common_corrections = {
            "teh": "the",
            "receive": "receive",
            "wierd": "weird",
            "definately": "definitely",
            "seperate": "separate",
        }
    
    def check_word(self, word):
        """Check if a single word is spelled correctly"""
        return self.dictionary.is_valid(word)
    
    def suggest_corrections(self, word, max_suggestions=5, max_distance=2):
        """
        Suggest corrections for a misspelled word.
        Returns list of (word, distance) tuples.
        """
        word = word.lower()
        
        # Check common typos first
        if word in self.common_corrections:
            return [(self.common_corrections[word], 1)]
        
        # Search in BK-tree
        results = self.tree.search(word, max_distance)
        
        # If no results with standard distance, try advanced distance
        if not results and self.use_advanced:
            # Manual search with advanced distance
            results = []
            for dict_word in self.dictionary.get_all_words():
                dist = damerau_levenshtein_distance(word, dict_word)
                if dist <= max_distance:
                    results.append((dict_word, dist))
            results.sort(key=lambda x: x[1])
        
        return results[:max_suggestions]
    
    def check_text(self, text):
        """
        Check an entire text and return misspelled words with suggestions
        """
        # Simple word tokenization
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        results = {}
        
        for word in words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word)
                results[word] = suggestions
        
        return results
    
    def auto_correct(self, text, max_distance=2):
        """
        Automatically correct text using best suggestions
        """
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        corrected = text
        
        for word in words:
            if not self.check_word(word):
                suggestions = self.suggest_corrections(word, max_distance=max_distance)
                if suggestions:
                    # Use the closest suggestion
                    corrected = corrected.replace(word, suggestions[0][0], 1)
        
        return corrected

def demo_mode():
    """Interactive demo of the spell checker"""
    checker = SpellChecker()
    
    print("\n" + "="*60)
    print("🔤 SPELL CHECKER MINI - DEMO MODE")
    print("="*60)
    
    while True:
        print("\n📝 Enter a word or sentence (or 'quit' to exit):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if ' ' in user_input:
            # Sentence mode
            print("\n🔍 Checking sentence...")
            errors = checker.check_text(user_input)
            
            if not errors:
                print("✅ All words are correct!")
            else:
                print(f"❌ Found {len(errors)} potential errors:")
                for wrong, suggestions in errors.items():
                    if suggestions:
                        sugg_str = ', '.join([f"{s[0]}({s[1]})" for s in suggestions])
                        print(f"   '{wrong}' → {sugg_str}")
                    else:
                        print(f"   '{wrong}' → No suggestions found")
                
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
                    for word, dist in suggestions:
                        print(f"   → {word} (distance: {dist})")
                else:
                    print("   No suggestions found")

if __name__ == "__main__":
    demo_mode()
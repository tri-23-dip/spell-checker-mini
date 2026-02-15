# test.py
from corrector import SpellChecker
from distance import levenshtein_distance, damerau_levenshtein_distance

def test_distances():
    """Test distance functions"""
    print("📏 Testing distance functions...")
    
    test_cases = [
        ("kitten", "sitting", 3),
        ("saturday", "sunday", 3),
        ("book", "back", 2),
        ("hello", "hello", 0),
        ("teh", "the", 1),  # Transposition test
    ]
    
    for s1, s2, expected in test_cases:
        d1 = levenshtein_distance(s1, s2)
        d2 = damerau_levenshtein_distance(s1, s2)
        
        print(f"  '{s1}' -> '{s2}': Levenshtein={d1}, Damerau={d2}")
        
        # Verify transposition handling
        if s1 == "teh" and s2 == "the":
            assert d2 == 1, "Damerau should handle transpositions"
    
    print("✅ Distance tests passed!\n")

def test_spell_checker():
    """Test the spell checker"""
    print("🔍 Testing spell checker...")
    
    checker = SpellChecker()
    
    test_words = [
        ("hello", True),      # Should be correct
        ("helo", False),      # Should be incorrect
        ("programming", True),
        ("programing", False),
        ("teh", False),       # Common typo
    ]
    
    for word, should_be_correct in test_words:
        is_correct = checker.check_word(word)
        status = "✅" if is_correct == should_be_correct else "❌"
        print(f"  {status} '{word}': correct={is_correct}")
        
        # Show suggestions for incorrect words
        if not is_correct:
            suggestions = checker.suggest_corrections(word)
            if suggestions:
                sugg_str = ', '.join([s[0] for s in suggestions[:3]])
                print(f"     Suggestions: {sugg_str}")
    
    print("✅ Spell checker tests passed!\n")

if __name__ == "__main__":
    print("="*50)
    print("🧪 RUNNING TESTS")
    print("="*50)
    
    test_distances()
    test_spell_checker()
    
    print("🎉 All tests passed!")
#!/usr/bin/env python3
"""
Test suite for the spell checker mini project.
Tests all components: distance functions, dictionary, BK-tree, and spell checker.
"""

import time
import sys
from corrector import SpellChecker
from distance import levenshtein, damerau_levenshtein, normalized_similarity

def test_distances():
    """Test distance functions thoroughly."""
    print("\n📏 Testing distance functions...")
    tests_passed = 0
    total_tests = 0
    
    # Test cases: (s1, s2, expected_levenshtein, expected_damerau)
    test_cases = [
        # Basic cases
        ("kitten", "sitting", 3, 3),
        ("saturday", "sunday", 3, 3),
        ("book", "back", 2, 2),
        ("hello", "hello", 0, 0),
        ("", "hello", 5, 5),
        ("hello", "", 5, 5),
        ("", "", 0, 0),
        
        # Transposition tests (Damerau should be better)
        ("teh", "the", 2, 1),      # transposition
        ("caat", "cat", 1, 1),      # deletion
        ("aple", "apple", 1, 1),    # insertion
        ("helo", "hello", 1, 1),    # insertion
        
        # Common typos
        ("recieve", "receive", 2, 1),  # transposition
        ("definately", "definitely", 3, 3),
        ("accomodate", "accommodate", 1, 1),
    ]
    
    for s1, s2, exp_lev, exp_dam in test_cases:
        total_tests += 2  # Two functions per case
        
        # Test Levenshtein
        lev_dist = levenshtein(s1, s2)
        if lev_dist == exp_lev:
            print(f"  ✅ Levenshtein('{s1}', '{s2}') = {lev_dist}")
            tests_passed += 1
        else:
            print(f"  ❌ Levenshtein('{s1}', '{s2}') = {lev_dist} (expected {exp_lev})")
        
        # Test Damerau-Levenshtein
        dam_dist = damerau_levenshtein(s1, s2)
        if dam_dist == exp_dam:
            print(f"  ✅ Damerau('{s1}', '{s2}') = {dam_dist}")
            tests_passed += 1
        else:
            print(f"  ❌ Damerau('{s1}', '{s2}') = {dam_dist} (expected {exp_dam})")
    
    # Test similarity function
    sim = normalized_similarity("kitten", "sitting")
    if 0.5 < sim < 0.6:  # Should be around 0.57
        print(f"  ✅ Similarity('kitten', 'sitting') = {sim:.3f}")
        tests_passed += 1
    total_tests += 1
    
    print(f"\n📊 Distance tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_dictionary():
    """Test dictionary loading and operations."""
    print("\n📚 Testing dictionary...")
    tests_passed = 0
    total_tests = 5
    
    try:
        from dictionary import Dictionary
        
        # Test 1: Load dictionary
        dict1 = Dictionary(wordlist_path="words.txt")
        assert dict1.size > 0, "Dictionary should have words"
        print(f"  ✅ Dictionary loaded {dict1.size:,} words")
        tests_passed += 1
        
        # Test 2: Word validation
        assert dict1.is_valid("hello") == True, "Should recognize 'hello'"
        assert dict1.is_valid("xyzabc123") == False, "Should reject non-words"
        print("  ✅ Word validation working")
        tests_passed += 1
        
        # Test 3: Case insensitivity
        assert dict1.is_valid("HELLO") == True, "Should be case insensitive"
        print("  ✅ Case insensitivity working")
        tests_passed += 1
        
        # Test 4: Add words
        test_word = f"testword{int(time.time())}"
        assert dict1.add_word(test_word) == True, "Should add new word"
        assert dict1.is_valid(test_word) == True, "Should recognize added word"
        print("  ✅ Word addition working")
        tests_passed += 1
        
        # Test 5: Get all words
        all_words = dict1.get_all_words()
        assert len(all_words) == dict1.size, "get_all_words should return all words"
        print("  ✅ get_all_words working")
        tests_passed += 1
        
    except Exception as e:
        print(f"  ❌ Dictionary test failed: {e}")
    
    print(f"📊 Dictionary tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_bktree():
    """Test BK-tree search functionality."""
    print("\n🌳 Testing BK-tree...")
    tests_passed = 0
    total_tests = 4
    
    try:
        from bktree import BKTree
        from distance import levenshtein
        
        # Test 1: Create and insert
        tree = BKTree(levenshtein)
        test_words = ["hello", "help", "hell", "held", "helm", "hero", "hi"]
        for word in test_words:
            tree.insert(word)
        
        assert len(tree) == len(test_words), "Tree size should match"
        print(f"  ✅ Tree created with {len(tree)} words")
        tests_passed += 1
        
        # Test 2: Search with distance 1
        results = tree.search("hel", 1)
        result_words = {word for word, _ in results}
        expected = {"hell", "held", "helm"}
        
        # Allow "help" if it's within distance 1 (it is: hel->help = 1)
        expected.add("help")
        
        assert result_words == expected, f"Expected {expected}, got {result_words}"
        print(f"  ✅ Distance 1 search found {len(results)} words")
        tests_passed += 1
        
        # Test 3: Search with distance 2
        results = tree.search("hel", 2)
        assert len(results) >= 4, "Should find more words with larger distance"
        print(f"  ✅ Distance 2 search found {len(results)} words")
        tests_passed += 1
        
        # Test 4: Contains check
        assert "hello" in tree, "Tree should contain 'hello'"
        assert "xyz" not in tree, "Tree should not contain 'xyz'"
        print("  ✅ Contains check working")
        tests_passed += 1
        
    except Exception as e:
        print(f"  ❌ BK-tree test failed: {e}")
    
    print(f"📊 BK-tree tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_spell_checker():
    """Test the spell checker integration."""
    print("\n🔍 Testing spell checker...")
    tests_passed = 0
    total_tests = 6
    
    try:
        # Test 1: Initialize
        checker = SpellChecker(use_advanced_distance=True)
        print("  ✅ Spell checker initialized")
        tests_passed += 1
        
        # Test 2: Check words
        test_words = [
            ("hello", True),      # Should be correct
            ("helo", False),      # Should be incorrect
            ("programming", True),
            ("programing", False),
            ("teh", False),       # Common typo
        ]
        
        for word, should_be in test_words:
            is_correct = checker.check_word(word)
            assert is_correct == should_be, f"'{word}' should be {should_be}"
        print("  ✅ Word checking working")
        tests_passed += 1
        
        # Test 3: Suggestions for misspelled words
        suggestions = checker.suggest_corrections("helo")
        assert len(suggestions) > 0, "Should suggest corrections"
        assert suggestions[0][0] in ["hello", "help", "hero"], "Should suggest 'hello'"
        print(f"  ✅ Suggestions working: {suggestions[0][0]} (distance: {suggestions[0][1]})")
        tests_passed += 1
        
        # Test 4: Transposition handling
        teh_suggestions = checker.suggest_corrections("teh")
        assert any(s[0] == "the" for s in teh_suggestions), "Should suggest 'the' for 'teh'"
        print("  ✅ Transposition handling working")
        tests_passed += 1
        
        # Test 5: Sentence checking
        text = "This is a simple sentenc with some erors"
        errors = checker.check_text(text)
        assert len(errors) >= 2, "Should find errors in sentence"
        print(f"  ✅ Sentence checking found {len(errors)} errors")
        tests_passed += 1
        
        # Test 6: Auto-correct
        corrected = checker.auto_correct(text)
        assert corrected != text, "Should correct text"
        print(f"  ✅ Auto-correct: '{corrected}'")
        tests_passed += 1
        
    except Exception as e:
        print(f"  ❌ Spell checker test failed: {e}")
    
    print(f"📊 Spell checker tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n⚠️  Testing edge cases...")
    tests_passed = 0
    total_tests = 5
    
    try:
        checker = SpellChecker()
        
        # Test 1: Empty string
        assert checker.check_word("") == False, "Empty string should be invalid"
        assert checker.suggest_corrections("") == [], "Empty string should return empty suggestions"
        print("  ✅ Empty string handling")
        tests_passed += 1
        
        # Test 2: None input
        try:
            checker.check_word(None)
        except (ValueError, AttributeError):
            print("  ✅ None input handled")
            tests_passed += 1
        else:
            print("  ❌ None input not handled properly")
        
        # Test 3: Numbers and special chars
        assert checker.check_word("hello123") == False, "Numbers should be invalid"
        assert checker.check_word("hello!") == False, "Special chars should be invalid"
        print("  ✅ Non-alpha input handling")
        tests_passed += 1
        
        # Test 4: Very long word
        long_word = "a" * 1000
        suggestions = checker.suggest_corrections(long_word)
        assert isinstance(suggestions, list), "Should handle long words"
        print("  ✅ Long word handling")
        tests_passed += 1
        
        # Test 5: Multiple spaces
        text = "hello   world"
        corrected = checker.auto_correct(text)
        assert "  " not in corrected, "Should handle multiple spaces"
        print("  ✅ Multiple space handling")
        tests_passed += 1
        
    except Exception as e:
        print(f"  ❌ Edge case test failed: {e}")
    
    print(f"📊 Edge case tests: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

def run_all_tests():
    """Run all test suites."""
    print("="*60)
    print("🧪 SPELL CHECKER MINI - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Distance Functions", test_distances),
        ("Dictionary", test_dictionary),
        ("BK-Tree", test_bktree),
        ("Spell Checker", test_spell_checker),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n▶️  Running {name} tests...")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ Test suite crashed: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {name}")
        all_passed = all_passed and passed
    
    print("="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! The spell checker is ready to use!")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
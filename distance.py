"""
Distance calculation algorithms for fuzzy string matching.
Provides Levenshtein and Damerau-Levenshtein edit distance functions.
"""

from typing import Dict, Optional

def levenshtein(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to change one word into another.
    
    Uses dynamic programming with O(n*m) time and O(min(n,m)) space.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Integer edit distance (0 = identical strings)
    
    Examples:
        >>> levenshtein("kitten", "sitting")
        3
        >>> levenshtein("hello", "hello")
        0
        >>> levenshtein("", "hello")
        5
    """
    # Handle empty strings
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    
    # Make s1 the shorter string for space optimization
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    
    # Initialize with range of first string length
    previous_row = list(range(len(s1) + 1))
    
    # Iterate through each character of s2
    for i, char2 in enumerate(s2, 1):
        # Start with cost of inserting all previous characters
        current_row = [i]
        
        # Calculate costs for each position
        for j, char1 in enumerate(s1, 1):
            # If characters are equal, cost is diagonal value
            if char1 == char2:
                current_row.append(previous_row[j - 1])
            else:
                # Take minimum of deletion, insertion, substitution
                current_row.append(
                    1 + min(
                        previous_row[j],      # deletion
                        current_row[j - 1],  # insertion
                        previous_row[j - 1]  # substitution
                    )
                )
        
        previous_row = current_row
    
    return previous_row[-1]


def damerau_levenshtein(s1: str, s2: str) -> int:
    """
    Calculate Damerau-Levenshtein distance with transpositions.
    
    Extends Levenshtein distance to include transpositions of adjacent characters,
    which catches common typos like "teh" -> "the".
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Integer edit distance including transpositions
    
    Examples:
        >>> damerau_levenshtein("teh", "the")
        1  # Single transposition
        >>> damerau_levenshtein("caat", "cat")
        1  # Deletion
        >>> damerau_levenshtein("apple", "aple")
        1  # Deletion
    """
    # Handle empty strings
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    
    len1, len2 = len(s1), len(s2)
    
    # Optimize by ensuring s1 is shorter
    if len1 > len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1
    
    # Initialize matrix with extra row/col for transpositions
    INF = len1 + len2
    d = [[INF] * (len2 + 2) for _ in range(len1 + 2)]
    
    # Initialize boundaries
    for i in range(len1 + 1):
        d[i + 1][0] = INF
        d[i + 1][1] = i
    for j in range(len2 + 1):
        d[0][j + 1] = INF
        d[1][j + 1] = j
    
    # Track last positions for transpositions
    last_row: Dict[str, int] = {}
    
    for i in range(1, len1 + 1):
        last_match = 0
        ch1 = s1[i - 1]
        
        for j in range(1, len2 + 1):
            ch2 = s2[j - 1]
            i1 = last_row.get(ch2, 0)
            j1 = last_match
            
            cost = 0 if ch1 == ch2 else 1
            
            # Standard operations
            d[i + 1][j + 1] = min(
                d[i][j + 1] + 1,      # deletion
                d[i + 1][j] + 1,      # insertion
                d[i][j] + cost         # substitution
            )
            
            # Transposition check (adjacent swap)
            if i1 > 0 and j1 > 0:
                # Calculate cost including transposition
                transposition_cost = d[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1)
                d[i + 1][j + 1] = min(d[i + 1][j + 1], transposition_cost)
            
            if ch1 == ch2:
                last_match = j
        
        last_row[ch1] = i
    
    return d[len1 + 1][len2 + 1]


def normalized_similarity(s1: str, s2: str) -> float:
    """
    Return a similarity score between 0.0 and 1.0.
    
    Uses Levenshtein distance normalized by string length.
    1.0 means identical strings, 0.0 means completely different.
    
    Args:
        s1: First string
        s2: Second string
    
    Returns:
        Float between 0 and 1 indicating similarity
    
    Examples:
        >>> normalized_similarity("cat", "cat")
        1.0
        >>> normalized_similarity("cat", "dog")
        0.0
        >>> normalized_similarity("kitten", "sitting")
        0.571...
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = levenshtein(s1, s2)
    return 1.0 - (distance / max_len)


def is_similar(s1: str, s2: str, threshold: float = 0.8) -> bool:
    """
    Check if strings are similar above a threshold.
    
    Args:
        s1: First string
        s2: Second string
        threshold: Similarity threshold (0.0 to 1.0)
    
    Returns:
        True if similarity >= threshold
    
    Examples:
        >>> is_similar("hello", "helo", 0.8)
        True
        >>> is_similar("hello", "world", 0.5)
        False
    """
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1")
    
    return normalized_similarity(s1, s2) >= threshold


def best_match(word: str, candidates: list, use_damerau: bool = True) -> Optional[tuple]:
    """
    Find the best matching word from a list of candidates.
    
    Args:
        word: Word to match
        candidates: List of candidate words
        use_damerau: Whether to use Damerau-Levenshtein (True) or basic Levenshtein (False)
    
    Returns:
        Tuple of (best_word, distance) or None if no candidates
    
    Example:
        >>> best_match("teh", ["the", "tea", "ten"])
        ('the', 1)
    """
    if not candidates:
        return None
    
    distance_func = damerau_levenshtein if use_damerau else levenshtein
    
    best = None
    best_dist = float('inf')
    
    for candidate in candidates:
        dist = distance_func(word, candidate)
        if dist < best_dist:
            best_dist = dist
            best = candidate
            if best_dist == 0:
                break
    
    return (best, best_dist) if best else None


# Aliases for backward compatibility
levenshtein_distance = levenshtein
damerau_levenshtein_distance = damerau_levenshtein

# Quick test if run directly
if __name__ == "__main__":
    print("Testing distance functions:")
    
    test_pairs = [
        ("kitten", "sitting"),
        ("teh", "the"),
        ("hello", "hello"),
        ("", "hello"),
        ("cat", "dog"),
        ("caat", "cat"),
    ]
    
    for s1, s2 in test_pairs:
        ld = levenshtein(s1, s2)
        dld = damerau_levenshtein(s1, s2)
        sim = normalized_similarity(s1, s2)
        print(f"\n'{s1}' -> '{s2}':")
        print(f"  Levenshtein: {ld}")
        print(f"  Damerau-Levenshtein: {dld}")
        print(f"  Similarity: {sim:.3f}")
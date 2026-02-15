# distance.py
def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    Uses dynamic programming with O(n*m) time and O(min(n,m)) space.
    """
    # Make s1 the shorter string for space optimization
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    
    distances = range(len(s1) + 1)
    
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    
    return distances[-1]

def damerau_levenshtein_distance(s1, s2):
    """
    Extended distance that also considers transpositions (swap adjacent chars)
    This catches common typos like "teh" -> "the"
    """
    len1, len2 = len(s1), len(s2)
    inf = len1 + len2
    
    # Initialize matrix
    d = [[0] * (len2 + 2) for _ in range(len1 + 2)]
    
    d[0][0] = inf
    for i in range(0, len1 + 1):
        d[i + 1][0] = inf
        d[i + 1][1] = i
    for j in range(0, len2 + 1):
        d[0][j + 1] = inf
        d[1][j + 1] = j
    
    # Track last positions for transpositions
    last_row = {}
    
    for i in range(1, len1 + 1):
        last_match = 0
        for j in range(1, len2 + 1):
            i1 = last_row.get(s2[j - 1], 0)
            j1 = last_match
            
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            
            if s1[i - 1] == s2[j - 1]:
                last_match = j
            
            # Standard operations + transposition
            d[i + 1][j + 1] = min(
                d[i][j + 1] + 1,      # deletion
                d[i + 1][j] + 1,      # insertion
                d[i][j] + cost,        # substitution
                d[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1)  # transposition
            )
        
        last_row[s1[i - 1]] = i
    
    return d[len1 + 1][len2 + 1]
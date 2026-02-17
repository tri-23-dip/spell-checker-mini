"""
BK-Tree implementation for fuzzy string matching.
Used as the core data structure for the spell checker.
"""

from distance import levenshtein

class BKTree:
    """
    Burkhard-Keller Tree: A metric tree for fast fuzzy string matching.
    
    Properties:
    - root: Root node of the tree
    - distance: Distance function to use (default: Levenshtein)
    - size: Number of words in the tree
    """
    
    class Node:
        """Tree node containing a word and its child nodes."""
        __slots__ = ('word', 'children')  # Memory optimization
        
        def __init__(self, word):
            self.word = word
            self.children = {}  # distance -> child node
    
    def __init__(self, distance_func=levenshtein):
        self.root = None
        self.distance = distance_func
        self.size = 0
    
    def insert(self, word):
        """Insert a word into the BK-Tree."""
        # Input validation
        if not word or not isinstance(word, str):
            raise ValueError("Word must be a non-empty string")
        
        word = word.lower().strip()
        
        if self.root is None:
            self.root = self.Node(word)
            self.size = 1
            return
        
        node = self.root
        while True:
            dist = self.distance(word, node.word)
            if dist == 0:
                return  # Word already exists
            
            if dist in node.children:
                node = node.children[dist]
            else:
                node.children[dist] = self.Node(word)
                self.size += 1
                break
    
    def search(self, word, max_distance):
        """
        Find all words within max_distance of the given word.
        
        Args:
            word: The word to search for
            max_distance: Maximum edit distance allowed
            
        Returns:
            List of (word, distance) tuples, sorted by distance
        """
        # Input validation
        if max_distance < 0:
            raise ValueError("max_distance must be non-negative")
        if not isinstance(word, str):
            raise ValueError("Word must be a string")
        
        word = word.lower().strip()
        if self.root is None or not word:
            return []
        
        results = []
        stack = [self.root]
        
        while stack:
            node = stack.pop()
            dist = self.distance(word, node.word)
            
            if dist <= max_distance:
                results.append((node.word, dist))
            
            # Only traverse children within the distance range
            min_child_dist = max(0, dist - max_distance)
            max_child_dist = dist + max_distance
            
            for child_dist, child_node in node.children.items():
                if min_child_dist <= child_dist <= max_child_dist:
                    stack.append(child_node)
        
        # Remove duplicates and sort
        seen = set()
        unique_results = []
        for word, dist in results:
            if word not in seen:
                seen.add(word)
                unique_results.append((word, dist))
        
        unique_results.sort(key=lambda x: x[1])
        return unique_results
    
    def build_from_list(self, words):
        """Build tree from a list of words."""
        if not isinstance(words, (list, tuple, set)):
            raise ValueError("words must be a list, tuple, or set")
        
        for word in words:
            self.insert(word)
    
    def __len__(self):
        """Return the number of words in the tree."""
        return self.size
    
    def __contains__(self, word):
        """Check if a word exists in the tree (fast lookup)."""
        if self.root is None:
            return False
        
        word = word.lower().strip()
        node = self.root
        
        while True:
            dist = self.distance(word, node.word)
            if dist == 0:
                return True
            
            if dist in node.children:
                node = node.children[dist]
            else:
                return False
    
    def get_all_words(self):
        """Return all words in the tree (for debugging)."""
        words = []
        if self.root:
            stack = [self.root]
            while stack:
                node = stack.pop()
                words.append(node.word)
                stack.extend(node.children.values())
        return sorted(words)
    
    def __repr__(self):
        return f"BKTree(size={self.size})"
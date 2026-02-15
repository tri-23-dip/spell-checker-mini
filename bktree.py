# bktree.py
from distance import levenshtein_distance

class BKTree:
    """
    Burkhard-Keller Tree: A metric tree for fast fuzzy string matching.
    Perfect for spell checking because it quickly finds words within
    a certain edit distance.
    """
    
    class Node:
        def __init__(self, word):
            self.word = word
            self.children = {}  # distance -> child node
    
    def __init__(self, distance_func=levenshtein_distance):
        self.root = None
        self.distance = distance_func
        self.size = 0
    
    def insert(self, word):
        """Insert a word into the BK-Tree"""
        word = word.lower()
        
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
        Returns list of (word, distance) tuples.
        """
        word = word.lower()
        if self.root is None:
            return []
        
        results = []
        stack = [self.root]
        
        while stack:
            node = stack.pop()
            dist = self.distance(word, node.word)
            
            if dist <= max_distance:
                results.append((node.word, dist))
            
            # Check all children where distance is in range [dist-max, dist+max]
            for child_dist, child_node in node.children.items():
                if abs(dist - child_dist) <= max_distance:
                    stack.append(child_node)
        
        # Sort by distance
        results.sort(key=lambda x: x[1])
        return results
    
    def build_from_list(self, words):
        """Build tree from a list of words"""
        for word in words:
            self.insert(word)

# For very large dictionaries, we could implement a PersistentBKTree
# that saves to disk, but this in-memory version is perfect for demo
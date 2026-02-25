"""
BK-Tree implementation for fuzzy string matching.
"""

from distance import levenshtein


class BKTree:
    class Node:
        __slots__ = ("word", "children")

        def __init__(self, word):
            self.word = word
            self.children = {}

    def __init__(self, distance_func=levenshtein):
        self.root = None
        self.distance = distance_func
        self.size = 0

    def insert(self, word):
        if not word or not isinstance(word, str):
            return

        word = word.lower().strip()

        if self.root is None:
            self.root = self.Node(word)
            self.size = 1
            return

        node = self.root
        while True:
            dist = self.distance(word, node.word)
            if dist == 0:
                return

            if dist in node.children:
                node = node.children[dist]
            else:
                node.children[dist] = self.Node(word)
                self.size += 1
                break

    def search(self, word, max_distance):
        if self.root is None:
            return []

        word = word.lower().strip()
        results = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            dist = self.distance(word, node.word)

            if dist <= max_distance:
                results.append((node.word, dist))

            min_child = max(0, dist - max_distance)
            max_child = dist + max_distance

            for child_dist, child_node in node.children.items():
                if min_child <= child_dist <= max_child:
                    stack.append(child_node)

        results.sort(key=lambda x: (x[1], abs(len(x[0]) - len(word)), x[0]))
        return results

    def build_from_list(self, words):
        for word in words:
            self.insert(word)

    def __len__(self):
        return self.size

    def __contains__(self, word):
        return any(w == word for w, _ in self.search(word, 0))
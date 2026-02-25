"""
Distance calculation algorithms for fuzzy string matching.
Optimized with LRU caching for performance.
"""

from typing import Dict, Optional
from functools import lru_cache


@lru_cache(maxsize=20000)
def levenshtein(s1: str, s2: str) -> int:
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    if len(s1) > len(s2):
        s1, s2 = s2, s1

    previous_row = list(range(len(s1) + 1))

    for i, char2 in enumerate(s2, 1):
        current_row = [i]
        for j, char1 in enumerate(s1, 1):
            if char1 == char2:
                current_row.append(previous_row[j - 1])
            else:
                current_row.append(
                    1 + min(
                        previous_row[j],
                        current_row[j - 1],
                        previous_row[j - 1],
                    )
                )
        previous_row = current_row

    return previous_row[-1]


@lru_cache(maxsize=20000)
def damerau_levenshtein(s1: str, s2: str) -> int:
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    len1, len2 = len(s1), len(s2)
    INF = len1 + len2

    d = [[INF] * (len2 + 2) for _ in range(len1 + 2)]

    for i in range(len1 + 1):
        d[i + 1][1] = i
        d[i + 1][0] = INF
    for j in range(len2 + 1):
        d[1][j + 1] = j
        d[0][j + 1] = INF

    last_row: Dict[str, int] = {}

    for i in range(1, len1 + 1):
        last_match = 0
        ch1 = s1[i - 1]

        for j in range(1, len2 + 1):
            ch2 = s2[j - 1]
            i1 = last_row.get(ch2, 0)
            j1 = last_match

            cost = 0 if ch1 == ch2 else 1

            d[i + 1][j + 1] = min(
                d[i][j + 1] + 1,
                d[i + 1][j] + 1,
                d[i][j] + cost,
            )

            if i1 > 0 and j1 > 0:
                d[i + 1][j + 1] = min(
                    d[i + 1][j + 1],
                    d[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
                )

            if ch1 == ch2:
                last_match = j

        last_row[ch1] = i

    return d[len1 + 1][len2 + 1]
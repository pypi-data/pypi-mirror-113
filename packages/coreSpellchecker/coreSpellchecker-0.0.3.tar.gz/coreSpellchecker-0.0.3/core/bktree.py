from collections import deque
from core.functions import distance_functionLV
from core.functions import distance_functionHM
from core.functions import distance_functionJC


class BKTree(object):
    def __init__(self, items_list=[], items_dict={}):
        self.tree = None

        _add = self.add
        for item in items_list:
            _add(item)

        for item in items_dict:
            _add(item)

    def add(self, item):
        node = self.tree
        if node is None:
            self.tree = (item, {})
            return

        while True:
            parent, children = node
            distance = distance_functionLV(item, parent)
            node = children.get(distance)
            if node is None:
                children[distance] = (item, {})
                break

    def findLV(self, item, n):
        if self.tree is None:
            return []

        candidates = deque([self.tree])
        found = []

        while candidates:
            candidate, children = candidates.popleft()
            candidate = candidate.lower()                                               # Change all letters to lower case
            distanceLV = distance_functionLV(candidate, item)                               # Ganti here so LV, HM and JC included
            #distance = distance_functionHM(candidate, item)                               # Ganti here so LV, HM and JC included
            #distance = distance_functionJC(candidate, item)                               # Ganti here so LV, HM and JC included

            if distanceLV <= n:
                found.append((distanceLV, candidate))

            if children:
                lower = distanceLV - n
                upper = distanceLV + n
                candidates.extend(c for d, c in children.items() if lower <= d <= upper)

        found.sort()
        return found
    
    def findHM(self, item, n):
        if self.tree is None:
            return []

        candidates = deque([self.tree])
        found = []

        while candidates:
            candidate, children = candidates.popleft()
            candidate = candidate.lower()                                               # Change all letters to lower case
            #distanceLV = distance_functionLV(candidate, item)                               # Ganti here so LV, HM and JC included
            distanceHM = distance_functionHM(candidate, item)                               # Ganti here so LV, HM and JC included
            #distanceJC = distance_functionJC(candidate, item)                               # Ganti here so LV, HM and JC included

            if distanceHM <= n:
                found.append((distanceHM, candidate))

            if children:
                lower = distanceHM - n
                upper = distanceHM + n
                candidates.extend(c for d, c in children.items() if lower <= d <= upper)

        found.sort()
        return found


    def __iter__(self):
        if self.tree is None:
            return

        candidates = deque([self.tree])

        while candidates:
            candidate, children = candidates.popleft()
            yield candidate
            candidates.extend(children.values())
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1_map = [0] * 26
        s2_map = [0] * 26

        n = len(s1)
        for i in range(n):
            index = ord(s1[i]) - ord("a")
            s1_map[index] += 1

            index = ord(s2[i]) - ord("a")
            s2_map[index] += 1

        # check the first window
        if s1_map == s2_map:
            return True

        l = 0
        for r in range(len(s1), len(s2)):
            # move left pointer forward
            s2_map[ord(s2[l]) - ord('a')] -= 1
            l += 1

            # move right pointer forware
            s2_map[ord(s2[r]) - ord('a')] += 1
            if s1_map == s2_map:
                return True

        return False
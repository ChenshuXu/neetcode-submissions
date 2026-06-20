class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        sliding window
        
        Then we slide the index j to the right. If it is not in the HashSet, we slide j further. Doing so until s[j] is already in the HashSet. At this point, we found the maximum size of substrings without duplicate characters start with index ii. Then slide i to the right until no duplicate.
        time: O(n)
        space: O(n)
        """
        chars = collections.defaultdict(int)
        left = 0

        result = 0
        for right in range(len(s)):
            chars[s[right]] += 1
            # keep moving left point until no duplicates with right pointer
            while chars[s[right]] > 1:
                chars[s[left]] -= 1
                left += 1
                
            result = max(result, right - left + 1)
        return result
import collections

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """
        Sliding window

        For each window, check whether it can become a repeating character substring.

        A window is valid if:
        window length - count of most frequent char <= k

        If valid, expand right.
        If invalid, shrink left.

        Time: O(26 * n) = O(n)
        Space: O(26) = O(1)
        """
        count = collections.defaultdict(int)
        left = 0
        result = 0

        for right in range(len(s)):
            count[s[right]] += 1

            # current window length
            window_len = right - left + 1

            # most frequent char count in current window
            max_freq = max(count.values())

            # if we need to replace more than k chars, shrink from left
            while window_len - max_freq > k:
                count[s[left]] -= 1
                left += 1

                window_len = right - left + 1
                max_freq = max(count.values())

            result = max(result, right - left + 1)

        return result
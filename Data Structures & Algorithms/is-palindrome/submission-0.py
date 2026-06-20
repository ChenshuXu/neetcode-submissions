class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        Set two pointers, one at each end of the input string
        If the input is palindromic, both the pointers should point to equivalent characters, at all times
        If this condition is not met at any point of time, we break and return early
        We can simply ignore non-alphanumeric characters by continuing to traverse further.
        Continue traversing inwards until the pointers meet in the middle.
        Time complexity: O(n)
        space O(1)
        """
        l, r = 0, len(s) - 1
        while l < r:
            # or use string.isalnum()
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True

    # Could write own alpha-numeric function
    # or use string.isalnum()
    def alphanum(self, c):
        return (
            ord("A") <= ord(c) <= ord("Z")
            or ord("a") <= ord(c) <= ord("z")
            or ord("0") <= ord(c) <= ord("9")
        )
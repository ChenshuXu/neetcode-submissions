class Solution:
    def maxArea(self, heights: List[int]) -> int:
        # two pointers, move the pointer with the smaller height inward, 
        # because the water level is limited by the shorter bar. 
        # Keep updating the maximum area until the two pointers meet.
        l, r = 0, len(heights) - 1
        res = 0
        
        while l < r:
            area = min(heights[l], heights[r]) * (r - l)
            res = max(res, area)
            if heights[l] < heights[r]:
                l += 1
            elif heights[r] <= heights[l]:
                r -= 1
            
        return res
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        input check: duplicates? there is exactly one solution?

        sort to elimate duplicates
        then the problem become two sum II, choose the first number, then use two pointers,
        increase left when total is too small, decrease right when total is too big

        time: O(n^2), two sum 2 is O(n), called n times
        space: O(logN) to O(N), depends on sort
        """
        res = []
        nums.sort()

        for i, a in enumerate(nums):
            # we don't want to use the same first value twice
            if i > 0 and a == nums[i - 1]:
                continue

            # two sum II
            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = a + nums[l] + nums[r]
                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    """
                    skip duplicates
                    we only need to update one pointer, the other will be updated in the next loop
                    [-2,-2,0,0,2,2]
                    each value(at left) only has one corresponding value(at right)
                    so the duplicated right value will be updated(skipped) in next loop
                    """
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
                        
        return res
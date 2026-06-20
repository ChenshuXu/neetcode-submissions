class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        data = set()
        for n in nums:
            data.add(n)
        
        max_length = 0
        for n in data:
            local_max_length = 1
            while n + 1 in data:
                local_max_length += 1
                n += 1
            if local_max_length > max_length:
                max_length = local_max_length

        return max_length
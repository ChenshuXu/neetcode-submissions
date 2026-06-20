class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # output[i] = nums[i] 左边所有数的乘积 * nums[i] 右边所有数的乘积
        # example: [1,2,3,4]
        # left to right product
        # [1,1,1*2,1*2*3]
        # right to left product
        # [4*3*2,4*3,4,1]
        # ans=left[i]*right[i]
        if not nums:
            return [1]

        n = len(nums)
        product = 1
        leftProduct = [1 for _ in range(n)]
        for i in range(1, n):
            product = product * nums[i - 1]
            leftProduct[i] = product

        product = 1
        rightProduct = [1 for _ in range(n)]
        for i in range(n - 2, -1, -1):
            product = product * nums[i + 1]
            rightProduct[i] = product

        result = [0 for _ in range(n)]
        for i in range(n):
            result[i] = leftProduct[i] * rightProduct[i]

        return result

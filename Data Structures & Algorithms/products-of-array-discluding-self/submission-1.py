class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # output[i] = nums[i] 左边所有数的乘积 * nums[i] 右边所有数的乘积
        # example: [1,2,3,4]
        # left to right product
        # [1,1,1*2,1*2*3]
        # right to left product
        # [4*3*2,4*3,4,1]
        # ans=left[i]*right[i]
        n = len(nums)

        output = [1] * n

        prefix = 1
        for i in range(n):
            output[i] = prefix
            prefix *= nums[i]

        suffix = 1
        for i in range(n - 1, -1, -1):
            output[i] *= suffix
            suffix *= nums[i]

        return output

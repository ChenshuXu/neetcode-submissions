func productExceptSelf(nums []int) []int {
    // example: [1,2,3,4]
    // left to right product
    // [1,1,1*2,1*2*3]
    // right to left product
    // [4*3*2,4*3,4,1]

    // ans=left[i]*right[i]
    
    n := len(nums)
    output := make([]int, n)

    prefix := 1
    for i := 0; i < n; i++ {
        output[i] = prefix
        prefix *= nums[i]
    }

    suffix := 1
    for i := n - 1; i >= 0; i-- {
        output[i] *= suffix
        suffix *= nums[i]
    }

    return output
}

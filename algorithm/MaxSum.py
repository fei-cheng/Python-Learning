def maxSum(items):
    maxSum = curSum = 0
    for num in items:
        curSum = max(curSum + num, 0)
        maxSum = max(maxSum, curSum)
    return maxSum

if __name__ == '__main__':
    print maxSum([31,-41,59,26,-53,58,97,-93,-23,84])

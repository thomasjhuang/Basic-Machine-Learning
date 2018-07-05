
def findMaxSubArray(low, high, A):
    if low == high:
        return low,high,A[low]
    else:
        mid = (high + low) // 2
        leftlow, lefthigh, leftmax = findMaxSubArray(low,mid, A)
        rightlow, righthigh, rightmax = findMaxSubArray(mid+1, high, A)
        crosslow, crosshigh, crossmax = findCrossingArray(low, high, A)
        if leftmax >= rightmax and leftmax >= crossmax:
            return leftlow, lefthigh, leftmax
        elif rightmax >= leftmax and rightmax >= crossmax:
            return rightlow, righthigh, rightmax
        else:
            return crosslow, crosshigh, crossmax

def findCrossingArray(low, high, A):
    mid = (high + low) // 2
    leftmaxind = -1
    leftmax = -9000
    sum = 0
    for i in range(mid, low, -1):
        sum = sum + A[i]
        if sum > leftmax:
            leftmax = sum
            leftmaxind = i
    rightmaxind = -1
    rightmax = -9000
    sum = 0
    for j in range(mid+1, high):
        sum = sum + A[j]
        if sum > rightmax:
            rightmax = sum
            rightmaxind = j
    return leftmaxind, rightmaxind, leftmax + rightmax

def main():
    a = [3, -4, 5, 6, -7, 8, 9, -1000]
    low, high, sum = findMaxSubArray(0, len(a)-1, a)
    print('low: ' + str(low))
    print('high: ' + str(high))
    print('sum: ' + str(sum))

if __name__ == '__main__':
    main()

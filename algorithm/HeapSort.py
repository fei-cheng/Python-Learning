def SiftUp(T, n):
    while n > 1:
        idx = n / 2
        if T[idx] > T[n]:
            T[idx], T[n] = T[n], T[idx]
            n = idx
        else:
            break

def SiftDown(T, n):
    idx = 1
    while 2 * idx <= n:
        son = 2 * idx
        if (son + 1 <= n) and (T[son] > T[son + 1]):
            son += 1
        if T[idx] > T[son]:
            T[idx], T[son] = T[son], T[idx]
            idx = son
        else:
            break

def HeapSort(Values):
    length = len(Values)
    ArrayList = [length] + Values
    for i in range(2, length+1):
	SiftUp(ArrayList, i)
    for j in range(length, 1, -1):
	ArrayList[1], ArrayList[j] = ArrayList[j], ArrayList[1]
	SiftDown(ArrayList, j-1)
    return ArrayList[1:]


def test():
    Values = [8, 9, 7, 1, 5, 6, 2, 4, 3, 0]
    print HeapSort(Values)

if __name__ == '__main__':
    test()


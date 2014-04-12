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
    ArrayList = [len(Values)] + Values
    for
    

    return ArrayList[1:]



def test():
    Values = [1, 2, 3]
    print HeapSort(Values)

if __name__ == '__main__':
    test()

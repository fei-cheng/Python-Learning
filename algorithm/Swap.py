__author__ = 'fei.cheng'

def swap(a, b):
    return b, a

def main():
    a = 'hello'
    b = 'world'

    a, b = swap(a, b)

    print b, a


if __name__ == '__main__':
    main()

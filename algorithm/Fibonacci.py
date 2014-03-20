known = {0:0, 1:1}

def fibonacci(n):
    if n not in known:
        known[n] = fibonacci(n-1) + fibonacci(n-2)
    return known[n]

if __name__ == '__main__':
    print fibonacci(7)

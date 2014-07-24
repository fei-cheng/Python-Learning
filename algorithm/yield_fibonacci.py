def fibonacci(max):
    first, second = 0, 1
    while first < max:
        yield first
        first, second = second, first + second

class Fibonacci:
    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.first = 0
        self.second = 1
        return self

    def next(self):
        result = self.first
        if self.first > self.max:
            raise StopIteration
        self.first, self.second = self.second, self.first + self.second
        return result
        
        

if __name__ == '__main__':
    
    # test generator
    for i in fibonacci(100):
        print i,

    print ''
    
    # test class
    for j in Fibonacci(100):
        print j,

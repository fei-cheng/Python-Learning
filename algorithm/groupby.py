from operator import itemgetter

class groupby:
    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    def __iter__(self):
        return self
    def next(self):
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey))
    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)

if __name__ == '__main__':
    
    things = [('2009-09-02', 11),
              ('2009-09-02', 3),
              ('2009-09-03', 10),
              ('2009-09-03', 4),
              ('2009-09-03', 22),
              ('2009-09-06', 33)]

    for key, items in groupby(things, itemgetter(0)):
        print key
        for subitem in items:
            print subitem
        print '------' * 4

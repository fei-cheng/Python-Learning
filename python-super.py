'''
class FooParent(object):
    def __init__(self):
        self.parent = 'I am the parent.'
        print 'Parent'

    def bar(self, message):
        print message,'from Parent'

class FooChild(FooParent):
    def __init__(self):
        FooParent.__init__(self)
        print 'Child'

    def bar(self, message):
        FooParent.bar(self, message)
        print 'Child bar function.'
        print self.parent

if __name__ == '__main__':
    fooChild = FooChild()
    print '----------------------'
    fooChild.bar('HelloWorld')

'''

class FooParent(object):
    def __init__(self):
        self.parent = 'I am the parent.'
        print 'Parent'

    def bar(self, message):
        print message,'from Parent'

class FooChild(FooParent):
    def __init__(self):
        super(FooChild, self).__init__()
        print 'Child'

    def bar(self, message):
        super(FooChild, self).bar(message)
        print 'Child bar function.'
        print self.parent

if __name__ == '__main__':
    fooChild = FooChild()
    print '----------------------'
    fooChild.bar('HelloWorld')

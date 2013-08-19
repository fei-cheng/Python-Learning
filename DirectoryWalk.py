import os

def Walk(dirname=None):
    if not dirname:
        dirname = os.getcwd()
    for name in os.listdir(dirname):
        item = os.path.join(dirname, name)
        if os.path.isfile(item):
            print item
        else:
            Walk(item)

if __name__ == '__main__':
    Walk()

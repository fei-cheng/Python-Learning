from point import Point

class KMeans:

    def __init__(self, K, indata):
        self.k = K
        self.indata = indata
        self.cluster = []
        
        if len(indata) < K:
            print 'K is too large!'
            return
            
        for i in range(0, K):
            self.cluster.append([])
        for i in range(0, len(indata)):
            idx = i % K
            self.cluster[idx].append(indata[i])

    def adjust(self):
        adjust = 0
        centers = []
        
        for sublist in self.cluster:
            cp = Point((0,0,))
            for p in sublist:
                cp = cp + p
            cp = cp / len(sublist)
            centers.append(cp)
            
        for k, sublist in enumerate(self.cluster):
            for p in sublist:
                min_idx = 0
                min_dst = centers[0].distance(p)
                for idx in range(1, self.k):
                    dist = centers[idx].distance(p)
                    if dist < min_dst:
                        min_idx = idx
                        min_dst = dist
                if min_idx != k:
                    sublist.remove(p)
                    self.cluster[min_idx].append(p)
                    adjust += 1
        return adjust

    def kmeans(self):
        times = 0
        while True:
            adjust = self.adjust()
            if not adjust:
                break
            times += 1
        return times


if __name__ == '__main__':
    file = open('points.in','r')
    indata = []
    while True:
        s = file.readline()
        if len(s)==0:
            break
        points = s.split()
        indata.append(Point(tuple([int(i) for i in points])))
    km = KMeans(4, indata)
    km.kmeans()
    for i in range(len(km.cluster)):
        print 'kind ', i
        for p in km.cluster[i]:
            print p.point

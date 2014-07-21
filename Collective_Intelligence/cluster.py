import random
from math import sqrt
import Image,ImageDraw

def readfile(filename):
    """
        In the file, the first row is title and the first column is name.
    """
    delt = '\t'
    lines = [line for line in file(filename)]
    
    data = []
    rownames = []
    colnames = lines[0].strip().split(delt)[1:]
    for line in lines[1:]:
        p = line.strip().split(delt)
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
        
    return rownames, colnames, data
    
    
def pearson(v1, v2):
    """
        The more similar the items are, the smaller the result is.
    """
    sum1 = sum(v1)
    sum2 = sum(v2)
    
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    
    pSum = sum( [v1[i]*v2[i] for i in range(len(v1))] )
    
    # Calculate r (Pearson score)
    n = len(v1)
    num = n * pSum - sum1 * sum2
    den = sqrt( (n * sum1Sq - pow(sum1, 2)) * (n * sum2Sq - pow(sum2, 2)) )
    
    if den == 0:
        return 0
    return 1.0 - num / den
    
    
class bicluster:
  def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
    """
        The "distance" here means the distance between its left child and right child.
    """
    self.id = id
    self.vec = vec
    self.left = left
    self.right = right
    self.distance = distance
    
    
def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1
    
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]
    
    while len(clust) > 1:
        length = len(clust)
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        
        vec_len = len(clust[0].vec)
        for i in range(length):
            for j in range(i+1, length):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                dist = distances[(clust[i].id, clust[j].id)]
                
                if dist < closest:
                    closest = dist
                    lowestpair = (i, j)
        left_child = clust[lowestpair[0]]
        right_child = clust[lowestpair[1]]
        merge_vec = [ (left_child.vec[i] + right_child.vec[i]) / 2.0 for i in range(vec_len)]
                
        # create the new cluster
        new_cluster = bicluster(merge_vec, left=left_child, right=right_child, distance=closest, id=currentclustid)
                
        # cluster id is negative if it is not in the original set
        currentclustid -= 1
        # the order below can't be reversed, the item has bigger id should be deleted first
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(new_cluster)

    return clust[0]
    
    
    
def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for i in range(n):
        print ' ',
        
    if clust.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels is None:
            print clust.id
        else:
            print labels[clust.id]

    # now print the right and left branches
    if clust.left is not None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right is not None:
        printclust(clust.right, labels=labels, n=n+1)
        
        
def getheight(clust):
    if clust is None:
        return 0    # It is not necessary here because "clust" is always a full binary tree.
    if (clust.left is None) and (clust.right is None):
        return 1
    return getheight(clust.left) + getheight(clust.right)

    
def getdepth(clust):
    if (clust.left is None) and (clust.right is None):
        return 0
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    width = 2048
    height = getheight(clust) * 20
    depth  = getdepth(clust)

    scaling = float(width - 150) / depth
    
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.line((0, height/2, 10, height/2), fill=(255, 0, 0))
    
    drawnode(draw, clust, 10, height/2, scaling, labels)
    img.save(jpeg, 'JPEG')

    
    
def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y -(h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children    
        draw.line((x, top + h1/2, x, bottom - h2/2), fill=(255,0,0))    
    
        # Horizontal line to left item
        draw.line((x, top + h1/2, x + ll, top + h1/2), fill=(255,0,0))    

        # Horizontal line to right item
        draw.line((x, bottom - h2/2, x + ll, bottom - h2/2), fill=(255,0,0))        

        # Call the function to draw the left and right nodes    
        drawnode(draw, clust.left, x + ll, top + h1/2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2/2, scaling, labels)
    else:   
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def rotatematrix(data):
    return map(list, zip(*data)) # list transposition 
    
    
def kcluster(rows, distance=pearson, k=4):
    depth = len(rows[0])
    # Determine the minimum and maximum values for each point
    ranges = [( min([row[i] for row in rows]), max([row[i] for row in rows]) ) for i in range(depth)]
    # Create k randomly placed centroids
    clusters = [[random.random()*(ranges[i][1]-ranges[i][0]) + ranges[i][0]  for i in range(depth)] for j in range(k)]
    
    lastmatches = None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]
        
        for j in range(len(rows)):
            bestmatch = 0
            shortestdist = distance(clusters[bestmatch], rows[j])
            for i in range(k):
                d = distance(clusters[i], rows[j])
                if d < shortestdist:
                    bestmatch = i
                    shortestdist = d
            bestmatches[bestmatch].append(j)
        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches
        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * depth
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(depth):
                        avgs[m] += rows[rowid][m]
                for j in range(depth):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs
                
    return bestmatches
        
    
def tanamoto(v1, v2):
    c1, c2, shr = 0, 0, 0
    for i in range(len(v1)):
        if v1[i] != 0:
            c1 += 1       # in v1
        if v2[i] != 0:
            c2 += 1       # in v2
        if v1[i] != 0 and v2[i] != 0:
            shr += 1      # in both
    return 1.0 - (float(shr) / (c1+c2-shr))
  
  
def scaledown(data, distance=pearson, rate=0.01):
    n = len(data)
    outersum = 0.0
    
    fakedist = [[0.0 for j in range(n)] for i in range(n)]
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    
    loc = [[random.random(), random.random()] for i in range(n)]
    
    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(i, n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][idx] - loc[j][idx], 2) for idx in range(len(loc[i]))]))
                fakedist[j][i] = fakedist[i][j]
        # Move points
        grad = [[0.0, 0.0] for i in range(n)]
        
        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]
                
                grad[k][0] += ( (loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                grad[k][1] += ( (loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm
                
                totalerror += abs(errorterm)
        print totalerror
        
        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror:
            break
            
        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    
    return loc
  
  
def draw2d(data, labels, jpeg='mds2d.jpg'):
    img = Image.new('RGB', (2000,2000), (255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x,y), labels[i], (0,0,0))
    img.save(jpeg, 'JPEG')

  
if __name__ == '__main__':
    blognames, words, data = readfile('blogdata.txt')
    coords = scaledown(data)
    draw2d(coords, blognames, jpeg='blogs2d.jpg')

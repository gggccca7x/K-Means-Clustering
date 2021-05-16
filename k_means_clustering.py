# K Means clustering algorithm
# a single iteration:
## 1 - get closest cluster for each data point
## 2 - average each cluster
## 3 - if any cluster changed then repeat

# understanding limitations of pythons floating points:
#https://docs.python.org/3/tutorial/floatingpoint.html

import matplotlib.pyplot as plt
import random

### CHANGE ON DIMENSIONS
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def reset_x_y(self):
        self.x = 0.0
        self.y = 0.0

class Cluster:
    def __init__(self, val: Point, tot: Point, count):
        self.val = val # 2D
        self.tot = tot # 2D
        self.count = count
        self.changed = False

    def reset(self):
        self.n = 0
        self.tot.reset_x_y()
        self.count = 0
        self.changed = False

    ### CHANGE ON DIMENSIONS
    def add_new(self, v):
        self.tot.x += v.x
        self.tot.y += v.y
        self.count += 1

    def calculate_val(self):
        if(self.count > 0):
            new_val = Point(self.tot.x / self.count, self.tot.y / self.count)
            if not checkPointsEqual(new_val, self.val):
                self.changed = True
            self.val = new_val
        else:
            print("something has gone horribly wrong")

    def printVal(self):
        print(f'val x : {self.val.x} , val y : {self.val.y}')

### CHANGE ON DIMENSIONS
def checkPointsEqual(lhs: Point, rhs: Point):
    return round(lhs.x, 7) == round(rhs.x, 7) and round(lhs.y, 7) == round(rhs.y, 7)

def closest(num : Point, clusters: Cluster):
    ### CHANGE ON DIMENSIONS
    diff = abs(clusters[0].val.x - num.x) + abs(clusters[0].val.y - num.y)
    index = 0
    i = 1
    for c in clusters[1:]:
        ### CHANGE ON DIMENSIONS
        new_diff = abs(c.val.x - num.x) + abs(c.val.y - num.y)
        if new_diff < diff:
            diff = new_diff
            index = i
        i += 1
    return index

def single_iteration(data, clusters: Cluster):
    for c in clusters:
        c.reset()
    for val in data:
        idx = closest(val, clusters)
        clusters[idx].add_new(val)
    cluster_val_changed = False
    for c in clusters:
        c.calculate_val()
        if c.changed:
            cluster_val_changed = True
    if cluster_val_changed:
        return single_iteration(data, clusters)
    else:
        return clusters

# sum(x-avX)^2 / n-1
def calculateVariance(data, clusters: Cluster):
    ### CHANGE ON DIMENSIONS
    variance = Point(0.0, 0.0)
    for d in data:
        i = closest(d, clusters)
        variance.x += abs(d.x - clusters[i].val.x)
        variance.y += abs(d.y - clusters[i].val.y)
    return (variance.x / (len(data) - 1) + variance.y / (len(data) - 1))

# get random indexes to create random starting points
def getRandomIndexes(k, length_data):
    my_list = list(range(0,length_data))
    random.shuffle(my_list)
    return my_list[:k]
    
myData = [Point(0,1), Point(0.1, 0.9), Point(2.2, 5), Point(2.6, 5), Point(8,8), Point(7.9, 8.2), Point(6.7, 0.2), Point(6.5, 0.2), Point(6.51, 0.19), Point(2.2, 4.98)]

# clusters = []
# clusters.append(Cluster(myData[0], Point(0.0, 0.0), 0))
# clusters.append(Cluster(myData[1], Point(0.0, 0.0), 0))
# clusters.append(Cluster(myData[2], Point(0.0, 0.0), 0))
# clusters.append(Cluster(myData[3], Point(0.0, 0.0), 0))
# clusters.append(Cluster(myData[4], Point(0.0, 0.0), 0))
# clusters = single_iteration(myData, clusters)
# for c in clusters:
#     c.printVal()


variances = []
# for each k
for k in range(1,len(myData)):
    # create list of clusters
    clusters = []

    # for n in range(0, k):
        # clusters.append(Cluster(myData[n], 0, 0))
    indexes = getRandomIndexes(k, len(myData))
    for n in range(0, k):
        x_val = myData[indexes[n]].x
        y_val = myData[indexes[n]].y
        clusters.append(Cluster(Point(x_val, y_val), Point(0.0, 0.0) ,0))

    # pass through recursive single iteration method
    clusters = single_iteration(myData, clusters)

    # calculate variance
    v = calculateVariance(myData, clusters) 
    variances.append((k,v))

# determine best k with elbow method
for v in variances:
    print(v)
plt.plot(*zip(*variances))
plt.show()

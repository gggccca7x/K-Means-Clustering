# K Means clustering algorithm
# a single iteration:
## 1 - get closest cluster for each data point
## 2 - average each cluster
## 3 - if any cluster changed then repeat

import matplotlib.pyplot as plt
import random

class Cluster :
    def __init__(self, val, tot, count):
        self.val = val
        self.tot = tot
        self.count = count
        self.changed = False

    def reset(self):
        self.n = 0
        self.tot = 0.0
        self.count = 0
        self.changed = False

    def add_new(self, v):
        self.tot += v
        self.count += 1

    def calculate_val(self):
        if(self.count > 0):
            new_val = self.tot / self.count
            if new_val != self.val:
                self.changed = True
            self.val = new_val
        else:
            print("something has gone horribly wrong")


def closest(num, clusters: Cluster):
    diff = abs(clusters[0].val - num)
    index = 0
    i = 1
    for c in clusters[1:]:
        new_diff = abs(c.val - num)
        if new_diff < diff:
            diff = new_diff
            index = i
        i += 1
    return index

def single_iteration(data, clusters: Cluster):
    for c in clusters:
        c.reset()
    for val in data:
        index = closest(val, clusters)
        clusters[index].add_new(val)
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
    variance = 0.0
    for d in data:
        i = closest(d, clusters)
        variance += abs(d - clusters[i].val)
    return variance / (len(data) - 1)

# get random indexes to create random starting points
def getRandomIndexes(k, length_data):
    my_list = list(range(0,length_data))
    random.shuffle(my_list)
    return my_list[:k]
    
myData = [5, 6, 7, 20, 21, 27, 28, 29]
variances = []
# for each k
for k in range(1,len(myData)):
    # create list of clusters
    clusters = []

    # for n in range(0, k):
        # clusters.append(Cluster(myData[n], 0, 0))
    indexes = getRandomIndexes(k, len(myData))
    for n in range(0, k):
        clusters.append(Cluster(myData[indexes[n]], 0, 0))

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

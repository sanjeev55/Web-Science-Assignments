import pandas as pd
import numpy as np
import math as m
import random
import matplotlib.pylab as plt
from collections import Counter
import operator

def plotGraph(finalList1,finalList2):
    lists1 = sorted(finalList1.items())
    x1, y1 = zip(*lists1)

    lists2 = sorted(finalList2.items())
    x2, y2 = zip(*lists2)

    plt.scatter(np.log(x1), np.log(y1),color='red')
    plt.scatter(np.log(x2),np.log(y2),color='blue')
    plt.ylabel("Log of Fraction of the Frequency")
    plt.xlabel("Lof of Degree")
    plt.title("Log Log Plot of Degree Distribution")
    plt.legend(labels=['with equal probability', 'with preferential attachment'])
    plt.show()


def calculateEntropy(degreeDist):
    entropy = 0
    for key, value in degreeDist.items():
        entropy = -(value * m.log(value,2))
    return  entropy

def calculateDegreeDist(nodeDegree):
    degreeList = list(nodeDegree.values())
    uniqueDegree = np.unique(degreeList)
    totalNodes = degreeList.__len__()
    degreeDistList = {}
    degreeCount = Counter(degreeList)
    for deg in uniqueDegree:
        count = degreeCount[deg]
        pDeg = count / totalNodes
        degreeDistList.update({deg:pDeg})

    print("--------------Degree Distribution-----------")
    print(degreeDistList)
    return degreeDistList

# #for nodes with equal probability
nodeDegree = {1:2}
timestamp = 1
while timestamp < 10000:

    newNode = nodeDegree.__len__() + 1

    #choosing random node from all the available node since all the node has equal probability
    key, value = random.choice(list(nodeDegree.items()))
    value = value + 1

    #updating the value of selected node and adding the new node
    nodeDegree.update({key:value})
    nodeDegree.update({newNode:1})
    timestamp = timestamp + 1


#List of final nodes with its degree
print("------Total nodes with its respective degrees---------")
print(nodeDegree)

#calculating the degree distribution
degreeDistList = calculateDegreeDist(nodeDegree)

#calculating the entropy of degree distribution
entropyNormal = calculateEntropy(degreeDistList)
print("Entropy with equal probability:",entropyNormal)

# with preferrential attachment

nodeDegree = {1:2}
timestamp = 1
nodeProbList = {}
cumulativeProbList = {}

while timestamp <= 10000:
    cSum = 0
    newNode = nodeDegree.__len__() + 1
    totalDegree = sum(nodeDegree.values())

    #calculating the probability of each node
    for key, value in nodeDegree.items():
        nodeProb = value/totalDegree
        nodeProbList.update({key:nodeProb})

    #calulating the cumulative sum
    for key, value in nodeProbList.items():
        cSum = cSum + value
        cumulativeProbList.update({key:cSum})

    randomNum = random.uniform(0,1)

    #selecting node with just higher value than the random number
    newList = dict((key, value) for key, value in cumulativeProbList.items() if value > randomNum)
    linkNode = min(newList.items(), key=operator.itemgetter(1))[0]

    #adding the value to the degree in the selected node
    nodeDegree[linkNode] = nodeDegree[linkNode] + 1

    #updating the value of the selected node and adding new node
    nodeDegree.update({linkNode:nodeDegree[linkNode]})
    nodeDegree.update({newNode:1})

    timestamp = timestamp + 1

print("------Total nodes with its respective degrees---------")
print(nodeDegree)

#calculating degree distribution
degreeDistListPreferential = calculateDegreeDist(nodeDegree)

#calculating entropy
entropyPreferential = calculateEntropy(degreeDistListPreferential)
print("Entropy with Preferential Attachment:",entropyPreferential)

#plotting the scatter plot
plotGraph(degreeDistList,degreeDistListPreferential)

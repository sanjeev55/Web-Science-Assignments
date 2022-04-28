import random as rd

nameList = ['Bidish','Eunhye','Prajwal','Sanjeev']
final = {}

for name in nameList:
    q = rd.randint(1,4)
    while q in final.keys():
        q = rd.randint(1,4)
    final.update({q:name})

print(final)



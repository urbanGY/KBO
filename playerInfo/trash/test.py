# import numpy as np
# li = np.array([])
# tmp = [0,0,0]
# tmp2 = [0,0,1]
# a = []
# li = np.append(tmp,tmp2)
# a.append(li)
# li = np.append(tmp2,tmp)
# a.append(li)
#
# print(a)
mon = '04'
for i in range(int(mon)):
    print(i)

def a(list):
    for i in range(4):
        list.append(i)
    return list

def b(list):
    for i in range(4,8):
        list.append(i)
    return list

list = []
list = a(list)
list = b(list)
print(list)

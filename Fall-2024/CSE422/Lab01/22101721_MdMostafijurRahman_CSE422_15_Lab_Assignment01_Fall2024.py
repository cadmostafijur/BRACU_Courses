#22101721_MdMostafijurRahman_CSE422_15_Lab_Assignment01_Fall2024.py
import heapq
inp = open('input.txt')
ln_list = inp.readlines()
child_path_dic = {} #store nodes children , dis
gl = None
st = None
for line in ln_list:
    parts = line.split()
    if len(parts) < 2:
        continue
    k = parts[0]  #pt node
    heru = int(parts[1])  #ht valu
    
    if heru == 0:
        gl = k  #goalnode == h(0)
    if st is None:
        st = k  #firstnode== st node
    child_path_dic[k] = [heru]

    for i in range(2, len(parts), 2): #childnodewith dis value
        child = parts[i]
        distvalu = int(parts[i + 1])
        child_path_dic[k].append((child, distvalu))

def algo_astar(st, gl, child_path_dic):
    if st not in child_path_dic or gl not in child_path_dic:
        return None  # st or gl chck  graph

    pqueue = []  #priorityqueue
    pdic = {}  #store gvalus, pts
    h = child_path_dic[st][0]  #heurvalu st node
    g_value = 0
    heapq.heappush(pqueue, (h, st))#push stnode itto prioqueue
    pdic[st] = (g_value, None)

    while pqueue:
        par_value, k = heapq.heappop(pqueue)#popnode low f valu
        g_value = par_value - child_path_dic[k][0]
        if k == gl:
            return pdic

        for i in range(1, len(child_path_dic[k])):
            child, distvalu = child_path_dic[k][i]
            f_value = g_value + distvalu + child_path_dic[child][0]
            heapq.heappush(pqueue, (f_value, child))#chidenode push prioqueue
            if child not in pdic or pdic[child][0] > g_value + distvalu:#checkparent dic, shortpath found
                pdic[child] = (g_value + distvalu, k)


pdic = algo_astar(st, gl, child_path_dic)
if pdic is None: #check path 
    print("No Path Found")
else:
    dis = pdic[gl][0]
    k = gl
    pth = ''
    while k is not None:
        pth = '->' + k + pth
        k = pdic[k][1]
    print("Path:",pth[2:])
    print("Total distance:", dis,'km')


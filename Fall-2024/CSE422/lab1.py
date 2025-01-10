inp=open('input.txt')
out=open('output.txt')
ln_list=inp.readlines()
#print(ln) #list line
for i in range(len(ln_list)):
    ln_list[i]=ln_list[i].split()
# print(ln_list)
child_path_dic={}
for j in ln_list:
    k=j[0]
    heru=int(j[1])
    h_value=0
    if heru==h_value:
        g=k
    child_path_dic[k]=[int(heru)]
    count=2
    for i in range(count,len(j),2):
        child_path_dic[k].append((j[i],int(j[i+1])))
# print(child_path_dic)
import heapq
def algosearch_astar(g,child_path_dic):
    pqueue=[]
    pdic={}
    k=list(child_path_dic.keys())[0]
    # print()
    h=child_path_dic[k][0] #set value startpoint from graph node
    gp=0
    heapq.heappush(pqueue,(h,k)) #push start node
    pdic[k]=(gp,None)
    while True:
        parvalu,k=heapq.heappop(pqueue) #popqueue
        gvalue=parvalu-child_path_dic[k][0]
        for i in range(1,len(child_path_dic[k])):
            ch,gp=child_path_dic[k][i]
            out=gvalue+gp+child_path_dic[ch][0]
            heapq.heappush(pqueue,(out,ch)) #push child of par node
            if ch not in pdic.keys():
                pdic[ch]=(gp+gvalue,k)
            else:
                if pdic[ch][0]>=gp+gvalue:
                    pdic[ch]=(gp+gvalue,k)
        if k==g:
            if parvalu<=pqueue[0][0]:
                break
    return pdic

pdic=algosearch_astar(g,child_path_dic)
# print(pdic)
dis=pdic[g][0]
k=g
pth=''
while True:
    pth='->'+pdic[k][1]+pth
    k=pdic[k][1]
    if pdic[k][1]==None:
        break
pth+='->'+g
print("path:",pth[2:])
import random
def gen_intial_popula(po_size,chrom_len):
    population=[]
    for i in range(po_size):
        chromsom=[random.randint(0,1) for i in range(chrom_len)]
        population.append(chromsom)
    return population
def cross_two_points(p1,p2):
    leng=len(p1)
    pt1=random.randint(1,leng-2)
    pt2=random.randint(pt1+1,leng-1)
    ofspr1=p1[:pt1]+p2[pt1:pt2] +p1[pt2:]
    ofspr2=p2[:pt1]+p1[pt1:pt2] +p2[pt2:]
    return ofspr1, ofspr2

inp = open('input.txt')
inp_line = inp.readlines()
num_cor, num_time = map(int, inp_line[0].split())
courses = [i.strip() for i in inp_line[1:]]
# print(courses)
chrom_len=num_cor* num_time
po_size=9
population=gen_intial_popula(po_size,chrom_len)
p1,p2=random.sample(population,2)
ofspr1,ofspr2=cross_two_points(p1,p2)
parentt1=''.join(map(str,p1))
parentt2=''.join(map(str,p2))
off_spr1=''.join(map(str,ofspr1))
off_spr2=''.join(map(str,ofspr2))
print(f"parents are: {parentt1},{parentt2} and \nresult offspring after crossover:  {off_spr1},{off_spr2}")
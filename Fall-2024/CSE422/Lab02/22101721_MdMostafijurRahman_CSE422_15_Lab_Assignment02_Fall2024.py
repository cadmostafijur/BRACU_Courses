import random

inp = open('input.txt')
inp_line = inp.readlines()
num_cor, num_time = map(int, inp_line[0].split())
courses = [i.strip() for i in inp_line[1:]]
# print(courses)
if num_time < num_cor:
    print("num_time is greate than or equal to num_cor")

chrom_len = num_cor * num_time

def fitness(chromosome):
    ov_penalty = 0
    consi_penalty = 0
    time_segm = []
    st = 0
    for i in range(num_time):
        end = st + num_cor
        time_segm.append(chromosome[st:end])
        st = end

    for segment in time_segm:
        ov_penalty += max(0, sum(segment) - 1)

    cor_cts = [0] * num_cor
    for segment in time_segm:
        for i in range(num_cor):
            if segment[i] == 1:
                cor_cts[i] += 1
    consi_penalty += sum(abs(ct - 1) for ct in cor_cts)  #penalty
    total_penalty = ov_penalty + consi_penalty
    return -total_penalty

def mutate(chromosome):
    mutation_rate = 0.01
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

def genrate_int_population(po_size):
    population = []
    for i in range(po_size):
        chromosome = [0] * chrom_len
        for j in range(num_cor):
            timeslot = random.randint(0, num_time - 1)
            chromosome[timeslot * num_cor + j] = 1
        population.append(chromosome)
    return population

def sel_parent(population, fit):
    parents = []
    for i in range(2):
        #random
        indices = random.sample(range(len(population)), 3)  
        tournament = [(population[i], fit[i]) for i in indices]
        best_individual = max(tournament, key=lambda x: x[1])
        parents.append(best_individual[0])
    return parents

def ck_crossover(p1, p2):
    point = random.randint(1, chrom_len - 1)
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

def genetic_algo(po_size, gen_max):
    mutation_rate=0.01
    population = genrate_int_population(po_size)
    bt_fitt = float('-inf')
    bt_chromsom = None

    for generation in range(gen_max):
        fit = [fitness(chrom) for chrom in population]
        new_population = []

        for _ in range(po_size // 2):
            p1, p2 = sel_parent(population, fit)
            c1, c2 = ck_crossover(p1, p2)
            mutate(c1)
            mutate(c2)
            new_population.extend([c1, c2])

        population = new_population
        fit = [fitness(chrom) for chrom in population]
        rec_best_fitt = max(fit)
        current_bt_chromsom = population[fit.index(rec_best_fitt)]

        if rec_best_fitt > bt_fitt:
            bt_fitt = rec_best_fitt
            bt_chromsom = current_bt_chromsom

    return bt_chromsom, bt_fitt

po_size = 100
# mutation_rate = 0.01
gen_max = 1000

bt_result, bt_fitt = genetic_algo(po_size, gen_max)

print("best solution:", ''.join(map(str, bt_result)))
print("best fitness:", bt_fitt)








####when run part1 comment
####the  part 2 otherwise variable name clash
##########part 2

# import random
# def gen_intial_popula(po_size,chrom_len):
#     population=[]
#     for i in range(po_size):
#         chromsom=[random.randint(0,1) for i in range(chrom_len)]
#         population.append(chromsom)
#     return population
# def cross_two_points(p1,p2):
#     leng=len(p1)
#     pt1=random.randint(1,leng-2)
#     pt2=random.randint(pt1+1,leng-1)
#     ofspr1=p1[:pt1]+p2[pt1:pt2] +p1[pt2:]
#     ofspr2=p2[:pt1]+p1[pt1:pt2] +p2[pt2:]
#     return ofspr1, ofspr2

# inp = open('input.txt')
# inp_line = inp.readlines()
# num_cor, num_time = map(int, inp_line[0].split())
# courses = [i.strip() for i in inp_line[1:]]
# # print(courses)
# chrom_len=num_cor* num_time
# po_size=9
# population=gen_intial_popula(po_size,chrom_len)
# p1,p2=random.sample(population,2)
# ofspr1,ofspr2=cross_two_points(p1,p2)
# parentt1=''.join(map(str,p1))
# parentt2=''.join(map(str,p2))
# off_spr1=''.join(map(str,ofspr1))
# off_spr2=''.join(map(str,ofspr2))
# print(f"parents are: {parentt1},{parentt2} and \nresult offspring after crossover:  {off_spr1},{off_spr2}")
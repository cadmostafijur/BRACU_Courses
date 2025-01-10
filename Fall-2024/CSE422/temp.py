import random

# Read input data from file
with open('input.txt', 'r') as inp:
    inp_lines = inp.readlines()

# Parse input values
num_cor, num_time = map(int, inp_lines[0].split())
courses = [line.strip() for line in inp_lines[1:]]
if num_time < num_cor:
    raise ValueError("Error: The number of timeslots (T) must be greater than or equal to the number of courses (N).")

chrom_len = num_cor * num_time

# Fitness function to calculate penalties
def fitness(chromosome):
    ov_penalty = 0
    consi_penalty = 0

    # Split chromosome into timeslot segments
    time_segm = [chromosome[i * num_cor:(i + 1) * num_cor] for i in range(num_time)]

    # Calculate overlap penalty
    for segment in time_segm:
        ov_penalty += max(0, sum(segment) - 1)

    # Calculate consistency penalty
    cor_cts = [0] * num_cor
    for segment in time_segm:
        for i in range(num_cor):
            if segment[i] == 1:
                cor_cts[i] += 1

    # Total penalty is the sum of overlap and consistency penalties
    consi_penalty += sum(abs(ct - 1) for ct in cor_cts)
    total_penalty = ov_penalty + consi_penalty
    return -total_penalty

# Generate the initial population
def generate_initial_population(pop_size):
    population = []
    for _ in range(pop_size):
        chromosome = [0] * chrom_len
        for j in range(num_cor):
            timeslot = random.randint(0, num_time - 1)
            chromosome[timeslot * num_cor + j] = 1
        population.append(chromosome)
    return population

# Select parents using tournament selection
def select_parents(population, fitnesses):
    parents = []
    for _ in range(2):
        indices = random.sample(range(len(population)), 3)  # Randomly sample 3 individuals
        tournament = [(population[i], fitnesses[i]) for i in indices]
        best_individual = max(tournament, key=lambda x: x[1])
        parents.append(best_individual[0])
    return parents

# Perform crossover between two parents
def crossover(parent1, parent2):
    point = random.randint(1, chrom_len - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutate a chromosome with a given mutation rate
def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

# Main genetic algorithm function
def genetic_algorithm(pop_size, mutation_rate, max_generations):
    population = generate_initial_population(pop_size)
    best_fitness = float('-inf')
    best_chromosome = None

    for generation in range(max_generations):
        fitnesses = [fitness(chrom) for chrom in population]
        new_population = []

        for _ in range(pop_size // 2):
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
        fitnesses = [fitness(chrom) for chrom in population]
        current_best_fitness = max(fitnesses)
        current_best_chromosome = population[fitnesses.index(current_best_fitness)]

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_chromosome = current_best_chromosome

        # Print progress
        # print(f"Generation {generation + 1}: Best Fitness = {current_best_fitness}")

    return best_chromosome, best_fitness

# Parameters
pop_size = 100
mutation_rate = 0.01
max_generations = 1000

# Run the genetic algorithm
best_solution, best_fitness = genetic_algorithm(pop_size, mutation_rate, max_generations)

# Print the best solution and fitness
print("Best Solution:", ''.join(map(str, best_solution)))
print("Best Fitness:", best_fitness)

# Write the output to a file
with open('output.txt', 'w') as out_file:
    out_file.write(''.join(map(str, best_solution)) + '\n')
    out_file.write(str(best_fitness) + '\n')

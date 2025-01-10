#Part 2

import random

def generate_initial_population(pop_size, chromosome_length):
    population = []
    for _ in range(pop_size):
        chromosome = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(chromosome)
    return population

def two_point_crossover(parent1, parent2):
    length = len(parent1)
    point1 = random.randint(1, length - 2)
    point2 = random.randint(point1 + 1, length - 1)

    offs1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offs2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return offs1, offs2

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    N = int(lines[0].split()[0])
    T = int(lines[0].split()[1])
    courses = [line.strip() for line in lines[1:]]
    return N, T, courses

def write_output_file(filename, parent1, parent2, offs1, offs2):
    with open(filename, 'w') as file:
        file.write("Parent 1: " + ''.join(map(str, parent1)) + "\n")
        file.write("Parent 2: " + ''.join(map(str, parent2)) + "\n")
        file.write("Offspring 1:  " + ''.join(map(str, offs1)) + "\n")
        file.write("Offspring 2:  " + ''.join(map(str, offs2)) + "\n")

def main():
    input_filename = "input.txt"
    output_filename = "output2.txt"

    N, T, courses = read_input_file(input_filename)
    chromosome_length = N * T
    pop_size = 10

    population = generate_initial_population(pop_size, chromosome_length)

    parent1, parent2 = random.sample(population, 2)

    offs1, offs2 = two_point_crossover(parent1, parent2)

    write_output_file(output_filename, parent1, parent2, offs1, offs2)

if __name__ == "__main__":
    main()

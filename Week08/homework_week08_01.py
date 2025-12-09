import random

target_sentence = "Hello, world!" 
gene_pool = " ,!.?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

population_size = 100 
mutation_rate = 0.5

def generate_chromosome(length):
    genes = []
    while len(genes) < length:
        genes.append(gene_pool[random.randrange(0, len(gene_pool))])
    return ''.join(genes)

def calculate_fitness(chromosome):
    fitness = 0
    for i in range(len(chromosome)):
        if chromosome[i] == target_sentence[i]:
            fitness += 1
    return fitness

def crossover(parent1, parent2):
    split_point = random.randint(0, len(parent1) - 1)
    child_genes = parent1[:split_point] + parent2[split_point:]
    return child_genes

def mutate(chromosome):
    if random.random() > mutation_rate:
        return chromosome
    index_to_mutate = random.randrange(0, len(chromosome))
    gene_list = list(chromosome)
    new_gene = gene_pool[random.randrange(0, len(gene_pool))]
    gene_list[index_to_mutate] = new_gene
    
    return ''.join(gene_list)

print(f"Target Sentence: '{target_sentence}'")
print("- Start -")

population = []
for i in range(population_size):
    population.append(generate_chromosome(len(target_sentence)))

for generation in range(50000):
    population_fitness = []
    for chromosome in population:
        population_fitness.append(calculate_fitness(chromosome))
    
    parent1_index = population_fitness.index(max(population_fitness))
    parent1 = population[parent1_index]
    
    temp_fitness = population_fitness[:]
    temp_fitness[parent1_index] = -1
    parent2_index = temp_fitness.index(max(temp_fitness))
    parent2 = population[parent2_index]

    child = crossover(parent1, parent2)
    child = mutate(child)
    child_fitness = calculate_fitness(child)

    min_fitness_index = population_fitness.index(min(population_fitness))
    
    del population[min_fitness_index]
    population.append(child)

    current_best_fitness = max(population_fitness)
    current_best_one = population[population_fitness.index(current_best_fitness)]

    if generation % 100 == 0:
        print(f"Generation now {generation}: Best now: '{current_best_one}' (Score: {current_best_fitness})")

    if current_best_one == target_sentence:
        print("\n---")
        print(f"Solution found at Generation {generation}")
        print(f"Final Solution: {current_best_one}")
        print("---")
        break

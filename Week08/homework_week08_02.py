import random
import time

gene_pool = " ,!.?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_chromosome(length):
    genes = []
    while len(genes) < length:
        genes.append(gene_pool[random.randrange(0, len(gene_pool))])
    return ''.join(genes)

def calculate_fitness(chromosome, target):
    fitness = 0
    for i in range(len(chromosome)):
        if chromosome[i] == target[i]:
            fitness += 1
    return fitness

def crossover(parent1, parent2):
    split_point = random.randint(0, len(parent1) - 1)
    return parent1[:split_point] + parent2[split_point:]

def mutate(chromosome, rate):
    if random.random() > rate:
        return chromosome
    
    index_to_mutate = random.randrange(0, len(chromosome))
    gene_list = list(chromosome)
    new_gene = gene_pool[random.randrange(0, len(gene_pool))]
    gene_list[index_to_mutate] = new_gene
    return ''.join(gene_list)

def run_experiment(exp_id, target_sentence, population_size, max_generations, mutation_rate):

    print(f"\n- Start -")
    print(f"Target Sentence: '{target_sentence}'")
    print(f"Population Size: {population_size}")
    print(f"Mutation Rate: {mutation_rate}")
    
    start_time = time.time()

    population = []
    for _ in range(population_size):
        population.append(generate_chromosome(len(target_sentence)))

    found = False
    best_chromosome = ""

    for generation in range(max_generations):
        population_fitness = [calculate_fitness(c, target_sentence) for c in population]
        
        current_best_fitness = max(population_fitness)
        best_chromosome = population[population_fitness.index(current_best_fitness)]
        
        if best_chromosome == target_sentence:
            end_time = time.time()
            print(f"Solution found at Generation {generation}")
            print(f"time: {end_time - start_time:.4f}s")
            found = True
            break
    
        if generation % 500 == 0 or generation == 0:
            print(f"Generation now {generation}: Best now='{best_chromosome}' (Score: {current_best_fitness}/{len(target_sentence)})")

        parent1 = population[population_fitness.index(max(population_fitness))]
        
        temp_fitness = population_fitness[:]
        temp_fitness[population_fitness.index(max(population_fitness))] = -1
        parent2 = population[temp_fitness.index(max(temp_fitness))]

        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate)

        min_fitness_idx = population_fitness.index(min(population_fitness))
        del population[min_fitness_idx]
        population.append(child)
    
    if not found:
        print(f"Unable to find correct solution")
        print(f"Final Result: '{best_chromosome}'")
    
    print(f"Final Solution: '{best_chromosome}'")
    print(f"{exp_id} Finish\n")

if __name__ == "__main__":

    # Test 1 short sentence
    run_experiment(
        exp_id="Test 1",
        target_sentence="Jedi",
        population_size=20,
        max_generations=5000,
        mutation_rate=0.5
    )

    # Test 2 medium sentence
    run_experiment(
        exp_id="Test 2",
        target_sentence="Star Wars",
        population_size=100,
        max_generations=20000,
        mutation_rate=0.4
    )

    # Test 3 long sentence
    run_experiment(
        exp_id="Test 3",
        target_sentence="May the force be with you, young Skywalker.",
        population_size=200,
        max_generations=50000,
        mutation_rate=0.3
    )

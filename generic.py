import copy
import random
import statistics
import csv

from loader import read_input_data
from pprint import pprint
from datetime import datetime


def proceed_genetic_algorithm(path, file_name, selection_type, tournament_size, population_size, generation_number, cross_chance, mut_chance):
    result = list()  # [avg_fitness, [min_fitness, bag_structure], [man_fitness, bag_structure], population]

    # Read data from the file
    bag_size, items, known_solution = read_input_data(path, file_name)

    # start population creation
    population = generate_start_population(items, bag_size, population_size)

    # go through generation
    for generation_id in range(0, generation_number):
        # counting fitness of each element of population
        population = update_fitness(items, population, bag_size)
        # add stats about population to results
        result.append(copy.deepcopy(evaluate_population(population)))
        # select new population
        population = do_selection(population, selection_type, tournament_size)

        # cross new population
        population = do_crossover(copy.deepcopy(population), cross_chance)
        # mutate new population
        population = do_mutation(population.copy(), mut_chance)
    print_result(result)
    return result


# This method print best result to console
def print_result(result):
    #pprint(result)
    print("Average fitnesses")
    pprint(list(map(lambda r: r[0], result)))
    print("Best values")
    pprint(list(map(lambda r: r[2][0], result)))
    best = 0
    for i in range(0, len(result)):
        if result[i][2][0] >= result[best][2][0]:
            best = i
    print("Best result", result[best][2])


# This is main method for selection part
def do_selection(population, selection_type, tournament_size):
    if selection_type == 'r':
        return roulette_selection(population)
    elif selection_type == 't':
        return tournament_selection(population, tournament_size)


# This is main method for crossing individuals
def do_crossover(population, cross_chance):
    pair_number = int(len(population) / 2)
    bag_length = len(population[0][1])
    for i in range(0, pair_number):
        if random.random() <= cross_chance:
            cut_point = random.randint(0, bag_length - 1)
            bag1 = population[i * 2][1][:cut_point] + population[i * 2 + 1][1][cut_point:]
            bag2 = population[i * 2 + 1][1][:cut_point] + population[i * 2][1][cut_point:]
            population[i * 2][1] = bag1
            population[i * 2 + 1][1] = bag2

    return population


# This is main method for mutating each chromosome
def do_mutation(population, mut_chance):
    for i in range(0, len(population)):
        for item in range(0, len(population[i][1])):
            random_value = random.random()
            if random_value <= mut_chance:
                if population[i][1][item] == 0:
                    population[i][1][item] = 1
                else:
                    population[i][1][item] = 0

    return population


# This is tournament selection
def tournament_selection(population, size):
    new_population = list()
    if size > 1:
        print("ERROR: tournament size > 1, should be in range (0, 1)")
    else:
        tournament_size = int(len(population) * size)

        # if tournament size less then 1 then we choose 1
        if tournament_size < 1:
            tournament_size = 1
        # if tournament size more then size of population we get population size as tournament size
        if tournament_size > len(population):
            tournament_size = len(population)

        # Creating new population
        while len(new_population) < len(population):
            # filling tournament team
            best_bag = [-1]
            for i in range(0, tournament_size):
                position = random.randint(0, len(population) - 1)
                if best_bag[0] < population[position][0]:
                    best_bag = population[position]
            new_population.append(copy.deepcopy(best_bag))

    return new_population


# This is roulette selection method
def roulette_selection(population):
    new_population = list()
    sum_value = sum(list(map(lambda bag: bag[0], population)))
    probability_array = list()

    # create list ot probabilities
    for i in range(0, len(population)):
        if i == 0:
            probability_array.append(population[i][0] / sum_value)
        else:
            probability_array.append((population[i][0] / sum_value) + probability_array[i - 1])

    while len(new_population) < len(population):
        probability = random.random()
        index = 0

        while probability > probability_array[index] and index < len(probability_array):
            index = index + 1
        new_population.append(copy.deepcopy(population[index]))

    '''if new_population[0][1][0] == 0:
        new_population[0][1][0] = 1
    else:
        new_population[0][1][0] = 0'''
    return new_population


# This method judge population, found min/max/average
def evaluate_population(population):
    avg_fitness = statistics.mean(list(map(lambda bag: bag[0], population)))
    min_fitness = min(list(map(lambda bag: bag[0], population)))
    max_fitness = max(list(map(lambda bag: bag[0], population)))

    min_bag_structure = list(filter(lambda bag: bag[0] == min_fitness, population))[0]
    max_bag_structure = list(filter(lambda bag: bag[0] == max_fitness, population))[0]

    return [avg_fitness, min_bag_structure, max_bag_structure, population]


# This method generates first population for genetic algorithm
def generate_start_population(items, bag_size, population_size):
    population = list()
    '''for i in range(0, population_size):
        bag_structure = [0] * len(items)
        actual_size = 0
        number_of_items = random.randint(0, len(items) - 1)
        n = 0

        # adding items to bag until filled it up
        while n < number_of_items:
            position = random.randint(0, len(items) - 1)

            # if item is not taken already we are taking it other wise nothing is happened
            if bag_structure[position] == 0:
                bag_structure[position] = 1
                actual_size = actual_size + items[position][1]
                n = n + 1

        # add prepared bag structure and it fitness's value (has 0 value at this moment) to population
        population.append([0, bag_structure])'''

    #avg_item_weight = statistics.mean(list(map(lambda item: item[1], items)))
    avg_item_weight = 0

    # create as much bags as size of population
    for i in range(0, population_size):
        bag_structure = [0] * len(items)
        actual_size = 0

        # adding items to bag until filled it up
        while (actual_size + avg_item_weight) < bag_size:
            position = random.randint(0, len(items) - 1)

            # if item is not taken already we are taking it other wise nothing is happened
            if bag_structure[position] == 0:
                bag_structure[position] = 1
                actual_size = actual_size + items[position][1]

        # add prepared bag structure and it fitness's value (has 0 value at this moment) to population
        population.append([0, bag_structure])

    pprint(population)
    return population


# This method update fitness of each bag in population
def update_fitness(items, population, bag_size):
    pop = copy.deepcopy(population)
    for bag in pop:
        bag[0] = count_fitness(items, bag[1], bag_size)
    return pop


# This method return fitness of the bag
def count_fitness(items, bag_structure, bag_size):
    value = 0
    weight = 0

    for i in range(0, len(bag_structure)):
        if bag_structure[i] == 1:
            value = value + items[i][0]
            weight = weight + items[i][1]

    # return 10% of fitness value if back weight cross bag size
    if weight > bag_size:
        return value / 10
    else:
        return value


# Save to CSV
def save_to_CSV(input_file_name, result, selection_type, tournament_size, population_number, generation_number, crossing_chance, mutation_chance):
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    if selection_type =='r':
        new_file = input_file_name + "_" + dt_string + "_" + selection_type + "_" + str(population_number) \
                   + "_" + str(generation_number) + "_" + str(crossing_chance) + "_" + str(mutation_chance)
    else:
        new_file = input_file_name + "_" + dt_string + "_" + selection_type + "_" + str(tournament_size) + "_" \
                   + str(population_number) + "_" + str(generation_number) + "_" + str(crossing_chance) + "_" \
                   + str(mutation_chance)

    new_file = new_file.replace('.', '')
    new_file = new_file.replace(':', '')
    new_file = new_file + '.csv'

    with open(new_file, mode='w') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['nr_pokolenia', 'najlepsza_ocena', 'średnia_ocen', 'najgorsza_ocena'])
        for r in range(0, len(result)):
            writer.writerow([r, result[r][2][0], result[r][0], result[r][1][0]])


# This method find solutions for ranges of each parameter
def auto_find_solution():
    file_name = "p07.csv"
    population_range = [10]
    generation_range = [100]
    crossing_chance = [0.7]
    mutation_chance = [0.01, 0.015, 0.02, 0.025]
    selection_type = ['t']  # 't' or 'r'
    tournament_size = [0.6]  # range (0, 1)

    for pr in population_range:
        for gr in generation_range:
            for cc in crossing_chance:
                for mc in mutation_chance:
                    for st in selection_type:
                        if st == 't':
                            for ts in tournament_size:
                                result = proceed_genetic_algorithm("/data/single/", file_name, st, ts, pr, gr, cc, mc)
                                save_to_CSV(file_name, result, st, ts, pr, gr, cc, mc)
                        else:
                            ts = '-'
                            result = proceed_genetic_algorithm("/data/single/", file_name, st, ts, pr, gr, cc, mc)
                            save_to_CSV(file_name, result, st, ts, pr, gr, cc, mc)


# enter to the program
if __name__ == '__main__':
    #auto_find_solution()
    file_name = "p08.csv"
    population_number = 100
    generation_number = 100
    crossing_chance = 0.7
    mutation_chance = 0.02
    selection_type = 't'  # 't' or 'r'
    tournament_size = 0.4  # range (0, 1)

    result = proceed_genetic_algorithm("/data/single/", file_name, selection_type, tournament_size, population_number, generation_number,
                                       crossing_chance, mutation_chance)
    save_to_CSV(file_name, result, selection_type, tournament_size, population_number, generation_number, crossing_chance, mutation_chance)
from map import Map
from map import generate_new_map_filename
from random import randint
from os.path import isfile
from random import sample
from copy import deepcopy
from copy import copy
import sys

POPULATION_SIZE = 15
SUNLIGHT_REQUIREMENT = 4
WATER_REQUIREMENT = 9
TREE_SURVIVAL_SCORE_INCREMENT = 1
COMPETITION_SCORE_INCREMENT = 1
OUT_OF_BOUNDS_WATER_ASSUMPTION = 2
CROSSOVER_FREQUENCY = 0.33
MUTATION_FREQUENCY = 0.05
MAX_GENERATIONS = 500


def generate_initial_population(height, width, size):
    population = []
    for i in range(0, size):
        population.append({'configuration': [[randint(0, 1) for i in range(0, width)] for j in range(0, height)]})

    return population


def fitness(configuration, resource_layout):
    competition = 1
    tree_survival_score = 0

    for i, row in enumerate(configuration):
        for j, space in enumerate(row):
            if space == 1:
                if resource_layout[i][j]['soil'] == 1 and resource_layout[i][j]['sunlight'] >= SUNLIGHT_REQUIREMENT:
                    water_availability_sum = 0
                    coords = ((i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1))
                    for coord in coords:
                        water_availability_sum += resource_layout[coord[0]][coord[1]]['water']\
                            if 0 <= coord[0] < len(configuration) and 0 <= coord[1] < len(row)\
                            else OUT_OF_BOUNDS_WATER_ASSUMPTION
                    if water_availability_sum >= WATER_REQUIREMENT:
                        tree_survival_score += TREE_SURVIVAL_SCORE_INCREMENT

    config_copy = deepcopy(configuration)
    for i in range(0, len(config_copy)):
        for j in range(0, len(config_copy[i])):
            if config_copy[i][j] == 1:
                coords = ((i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1))
                for coord in coords:
                    if 0 <= coord[0] < len(config_copy) and 0 <= coord[1] < len(config_copy[i]) and config_copy[coord[0]][coord[1]] == 1:
                        competition += COMPETITION_SCORE_INCREMENT
                config_copy[i][j] = 0

    return float(tree_survival_score) / float(competition)


def selection(pop, m):  # using the technique known as Fitness Proportionate Selection
    fitness_score_sum = 0
    highest_fitness_score_seen = 0
    best_solution = None
    for ind in pop:
        fit_score = fitness(ind['configuration'], m.get_layout())
        ind['fitness'] = fit_score
        fitness_score_sum += fit_score
        if fit_score > highest_fitness_score_seen or highest_fitness_score_seen is None:
            highest_fitness_score_seen = fit_score
            best_solution = deepcopy(ind)

    for ind in pop:
        ind['selection_fitness'] = ind['fitness'] / fitness_score_sum

    pop.sort(key=lambda x: x['selection_fitness'], reverse=True)
    accumulated_value = 0
    for ind in pop:
        accumulated_value += ind['selection_fitness']
        ind['accumulated_value'] = accumulated_value

    num_crossovers = int(round(CROSSOVER_FREQUENCY * len(pop)))
    to_crossover = []
    partners = []
    to_continue = []
    while len(to_crossover) + len(to_continue) < len(pop):
        last_accumulated_value = 0
        selection_pivot = float(randint(0, 100)) / 100
        selected_individual = None
        for ind in pop:
            if last_accumulated_value <= selection_pivot < ind['accumulated_value']:
                selected_individual = ind
                break
            last_accumulated_value = ind['accumulated_value']
        if selected_individual is not None:
            if len(to_crossover) < num_crossovers:
                partners.append(deepcopy(selected_individual))
                if len(partners) == 2:
                    to_crossover.append(tuple(partners))
                    partners = []
            else:
                to_continue.append(deepcopy(selected_individual))

    return best_solution, to_continue, to_crossover


def crossover(to_crossover):
    new_individuals = []
    for (partner_1, partner_2) in to_crossover:
        crossover_on = randint(0, len(partner_1) - 1)
        new_individual_layout = []
        for i in range(0, crossover_on):
            new_individual_layout.append(deepcopy(partner_1['configuration'][i]))
        for i in range(crossover_on, len(partner_2)):
            new_individual_layout.append(deepcopy(partner_2['configuration'][i]))
        new_individuals.append({'configuration': new_individual_layout})

    return new_individuals


def mutation(pop):
    num_mutations = int(round(MUTATION_FREQUENCY * len(pop)))
    to_mutate = sample(pop, num_mutations)
    for ind in to_mutate:
        mutate = True
        while mutate:
            mutated_gene = [randint(0, 1) for i in range(0, len(ind['configuration'][0]))]
            ind['configuration'][randint(0, len(ind['configuration']) - 1)] = mutated_gene
            mutate = True if randint(0, 100) <= int(MUTATION_FREQUENCY * 100) else False


def main():
    m = None
    if len(sys.argv) == 2:
        if isfile('./' + sys.argv[1]):
            m = Map(filename=sys.argv[1])
        else:
            print('The file ' + sys.argv[1] + ' does not exist in the root directory.')
            sys.exit()
    elif len(sys.argv) == 3:
        try:
            height = int(sys.argv[1])
            width = int(sys.argv[2])
            m = Map(height, width)
            m.write_to_file(generate_new_map_filename())
        except ValueError:
            print('An error occurred when parsing the provided arguments; the two arguments provided must be integers.')
    else:
        print('The correct number of arguments was not provided. Provide either one filename to read a map from'
              + ' or two integers to generate a new map.')

    if m is None:
        sys.exit()

    if m.get_height() == 0:
        print('The provided map is empty.')
        sys.exit()

    best_solution = None

    pop = generate_initial_population(m.get_height(), m.get_width(), POPULATION_SIZE)

    for i in range(MAX_GENERATIONS):
        best_solution_in_population, to_continue, to_crossover = selection(pop, m)
        print('Best in population: ' + str(best_solution_in_population['fitness']))
        if best_solution is None or best_solution_in_population['fitness'] > best_solution['fitness']:
            best_solution = best_solution_in_population

        print('Best overall: ' + str(best_solution['fitness']))
        pop = to_continue + crossover(to_crossover)
        mutation(pop)


if __name__ == '__main__':
    main()
    sys.exit()

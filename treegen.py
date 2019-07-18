from map import Map
from map import generate_new_map_filename
from random import randint
from copy import deepcopy
import sys

POPULATION_SIZE = 10
SUNLIGHT_REQUIREMENT = 4
WATER_REQUIREMENT = 9
TREE_SURVIVAL_SCORE_INCREMENT = 1
COMPETITION_SCORE_INCREMENT = 1
OUT_OF_BOUNDS_WATER_ASSUMPTION = 2


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

    return tree_survival_score / float(competition)


def crossover():
    return None


def mutation():
    return None


def main():
    m = None
    if len(sys.argv) == 2:
        m = Map(filename=sys.argv[1])
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

    highest_fitness_score_seen = None
    pop = generate_initial_population(m.get_height(), m.get_width(), POPULATION_SIZE)
    for ind in pop:
        fit_score = fitness(ind['configuration'], m.get_layout())
        ind['fitness'] = fit_score
        if fit_score > highest_fitness_score_seen or highest_fitness_score_seen is None:
            highest_fitness_score_seen = fit_score


if __name__ == '__main__':
    main()
    sys.exit()

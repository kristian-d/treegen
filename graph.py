from treegen import generate_initial_population
from treegen import selection
from treegen import crossover
from treegen import mutation
from treegen import getMAX_GENERATIONS
from treegen import getPOPULATION_SIZE
from random import randint
from os.path import isfile
from datetime import datetime
from map import Map
from map import generate_new_map_filename
import sys
import matplotlib.pyplot as plt
import csv



def generate_new_stats_filename():
    return 'GraphData_' + datetime.now().strftime('%m_%d_%H_%M') + '.txt'

def createGraph(bestList):
    generationNumberList = range(1, getMAX_GENERATIONS() + 1)
    plt.plot(generationNumberList, bestList, linewidth=0.2, c='r')
    plt.ylabel('Fitness Scores')
    plt.xlabel('Generation Number')
    plt.show()


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
    listOfBest_solutions = []

    pop = generate_initial_population(m.get_height(), m.get_width(), getPOPULATION_SIZE())

    for i in range(getMAX_GENERATIONS()):

        print('Generation number: ' + str(i + 1))
        best_solution_in_population, to_continue, to_crossover = selection(pop, m)
        listOfBest_solutions.append(best_solution_in_population['fitness'])
        print('Best in population: ' + str(best_solution_in_population['fitness']))
        if best_solution is None or best_solution_in_population['fitness'] > best_solution['fitness']:
            best_solution = best_solution_in_population

        print('Best overall: ' + str(best_solution['fitness']))
        pop = to_continue + crossover(to_crossover)
        mutation(pop)
        print('')
    
    fn = generate_new_stats_filename()
    with open(fn, 'ab') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(listOfBest_solutions)
    createGraph(listOfBest_solutions)
    


if __name__ == '__main__':
    main()
    sys.exit()
from treegen import generate_initial_population
from treegen import selection
from treegen import crossover
from treegen import mutation
from random import randint
from os.path import isfile
from datetime import datetime
from map import Map
from multiprocessing import Pool
import sys


def generate_new_stats_filename():
    return 'stats_' + datetime.now().strftime('%m_%d_%H_%M') + '.txt'


def run_trial(max_gens, m, trial_num, num_trial):
    print('Running trial number ' + str(trial_num) + ' of ' + str(num_trial) + '.')

    pop_size = randint(10, 100)
    crossover_freq = randint(1, 99) / 100.0
    mutation_freq = randint(1, 99) / 100.0

    best_solution = None

    pop = generate_initial_population(m.get_height(), m.get_width(), pop_size)

    for i in range(max_gens):
        best_solution_in_population, to_continue, to_crossover = selection(pop, m, crossover_freq)
        if best_solution is None or best_solution_in_population['fitness'] > best_solution['fitness']:
            best_solution = best_solution_in_population

        pop = to_continue + crossover(to_crossover)
        mutation(pop, mutation_freq)

    return '(' + str(pop_size) + ', ' + str(crossover_freq) + ', ' + str(mutation_freq) + ', ' \
           + str(best_solution['fitness']) + ')'


def main():
    if not len(sys.argv) == 4 and not len(sys.argv) == 5:
        print('The maximum number of generations must be provided in integer form, followed by the number of trials '
              + 'to run in integer form, followed by the file name containing the map to be tested with, followed by '
              + ' the optional integer argument determining the number of parallel trials running at any given time.')
        sys.exit()

    process_count = 1
    try:
        max_generations = int(sys.argv[1])
        num_trials = int(sys.argv[2])
        if len(sys.argv) == 5:
            process_count = int(sys.argv[4])
    except ValueError:
        print('The maximum generations, number of trials, and optional number of processes arguments must be integers.')
        sys.exit()

    if process_count == 0:
        print('The number of processes used to run trials cannot be 0.')
        sys.exit()

    p_str = 'process' if process_count == 1 else 'processes'
    print('Using ' + str(process_count) + ' ' + p_str + ' to run trials.')

    if isfile('./' + sys.argv[3]):
        m = Map(filename=sys.argv[3])
    else:
        print('The file ' + sys.argv[3] + ' does not exist in the root directory.')
        sys.exit()

    pool = Pool(processes=process_count)
    process_results = [
        pool.apply_async(run_trial, (max_generations, m, trial_number + 1, num_trials))
        for trial_number in range(num_trials)
    ]
    stats = [res.get() for res in process_results]
    fn = generate_new_stats_filename()
    f = open(fn, 'w+')
    try:
        f.write('\n'.join(stats))
    except IOError:
        print('An error occurred when writing statistics to file ' + fn)
    f.close()
    print('Successfully wrote ' + str(num_trials) + ' run statistics to file ' + fn)


if __name__ == '__main__':
    main()
    sys.exit()

To simply generate a map, run in the command line 'python map.py __ __' where the blanks are integer arguments for the height and width of the map.
The generated map will be saved in a text file in the root directory of the project.

To run the algorithm on a new map entirely, enter 'python treegen.py __ __' where the blanks are integer arguments for the height and width of the map.
Again, the generated map will be saved in a text file as above.

To run the algorithm on an existing map (from a text file), run 'python treegen.py ____' where the blank is the filename containing the map you wish to use.

Be careful not to commit any map text files to the repository. They can stay on your local machine.

Any variables controlling the creation of a map are currently placed as globals at the top of map.py. Change them if you'd like.

Any variables controlling the genetic algorithm are currently placed as globals at the top of treegen.py. These can and
should be changed for different trials on the same maps to see how the outputs compare.

To test variables such as population size, mutation frequency, and crossover frequency on a provided map, 
enter 'python run_for_statistics.py __ __ _____ __' into the command line. The first argument is the  
number of generations each trial run of the algorithm will complete before returning a fitness score. The 
second argument is the number of trials to run. The third argument is the file name of the file containing the map 
configuration to be tested. The fourth argument is optional and determines how many parallel processes to use for 
running trials; the default value is 1 process.

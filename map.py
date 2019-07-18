from random import randint, choice
from os.path import isfile
from datetime import datetime
from ast import literal_eval
import sys

WATER_RANGE = 5
SUNLIGHT_RANGE = 5
SOIL_PROBABILITY_TUP = (1, 1, 1, 0)


class Map:
    def __init__(self, *args, **kwargs):
        try:
            print('Reading map from file...')
            self.__filename = kwargs['filename']
            self.__map = self.__read_from_file(self.get_filename())
        except KeyError:
            if len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
                print('Generating a new map...')
                self.__map = self.__generate_map(args[0], args[1])
            else:
                print('No filename for pre-existing map or height and width for new map was provided. Map could not be generated.')

    @staticmethod
    def __generate_resources():
        w = randint(0, WATER_RANGE + 1)
        sn = randint(0, SUNLIGHT_RANGE + 1)
        sl = choice(SOIL_PROBABILITY_TUP)
        return {'water': w, 'sunlight': sn, 'soil': sl}

    def __generate_map(self, height, width):
        return [[self.__generate_resources() for i in range(0, width)] for j in range(0, height)]

    def get_map(self):
        return self.__map

    def get_filename(self):
        return self.__filename

    @staticmethod
    def __stringify_location(loc):
        return '(w=' + str(loc['water']) + ',sn=' + str(loc['sunlight']) + ',sl=' + str(loc['soil']) + ')'

    def write_to_file(self, fn=''):
        try:
            if isfile('./' + fn):
                print('The filename provided, ' + fn +
                      ', already exists in the immediate directory. Choose a new filename to write to.')
            else:
                f = open(fn, 'w+')
                f.write(str(self.get_map()))
                f.close()
        except IOError:
            print('An error occurred when writing map to file ' + fn)

        print('Successfully wrote map to file ' + fn)

    @staticmethod
    def __read_from_file(fn):
        contents = None
        try:
            f = open(fn, 'r')
            contents = f.read()
        except IOError:
            print('An error occurred when reading from file ' + fn)

        mx = None
        try:
            mx = literal_eval(contents)
        except SyntaxError:
            print('An error occurred when parsing text from file ' + fn + ' into a map.')

        return mx

    def __str__(self):
        return '\n'.join(
            [', '.join([self.__stringify_location(loc) for loc in row]) for row in self.get_map()])


def generate_new_filename():
    fn = None
    datetime_str = datetime.now().strftime('%m_%d_%H_%M')
    new_fn = 'map_' + datetime_str + '.txt'
    if not isfile('./' + new_fn):
        fn = new_fn

    return fn


def main():
    if not len(sys.argv) == 3:
        print('The correct amount of arguments was not provided. Provide two integer arguments to generate a map.')

    try:
        height = int(sys.argv[1])
        width = int(sys.argv[2])
        m = Map(height, width)
        m.write_to_file(generate_new_filename())
    except ValueError:
        print('An error occurred when parsing the provided arguments; the two arguments provided must be integers.')


if __name__ == '__main__':
    main()
    sys.exit()



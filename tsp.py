from email import parser
from black import main
import sys
from argparse import ArgumentParser
from rand import rand_num


def read_distance_matrix(filename):
    with open(filename, 'r') as f:
        l = [[float(num) for num in line.split('  ')] for line in f]
    return l


if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    m = read_distance_matrix(args.file)
    print(m)

import sys

from email import parser
from utils import read_distance_matrix
from argparse import ArgumentParser
from rand import rand_num

def initial_point(data):
    total_city = len(data)
    return rand_num(total_city)

def ranking_closest(distance_matrix, tour):
    closest = 9999
    if len(tour) == 0:
        last_city = 1
        tour.append(1)
    else:
        last_city = tour[-1]

    for idx, i in enumerate(distance_matrix[last_city - 1]):
        if (idx + 1) not in tour and i != 0:
            if i < closest:
                closest = i
                next_city = idx
    try:
        tour.append(next_city + 1)
    except:
        print('---- fim')
    return tour

def grasp(distance_matrix):
    tour = []
    print('---- Montando solução')
    for i in range(0,5):
        print('---- Tour atual{}'.format(tour))
        tour = ranking_closest(distance_matrix,tour)



if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    m = read_distance_matrix(args.file)
    grasp(m)
    #initial_city = initial_point(m)
    #print(initial_city)

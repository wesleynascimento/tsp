import sys
import copy
from email import parser
from utils import *
from argparse import ArgumentParser
from rand import rand_num

def greedy_closest(distance_matrix, tour):
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

def localsearch_2opt(distance_matrix, city_tour):
    tour = copy.deepcopy(city_tour)
    best_route = copy.deepcopy(tour)
    seed = copy.deepcopy(tour)  
    for i in range(0, len(tour[0])-2):
        for j in range(i+1, len(tour[0])-1):
            best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))
            #best_route[0][-1] = best_route[0][0]
            best_route[1] = get_total_distance(distance_matrix,best_route[0])
            if(best_route[1] < tour[1]):
                tour[1] = copy.deepcopy(best_route[1])
                for n in range(0, len(tour[0])): 
                    tour[0][n] = best_route[0][n]
            best_route = copy.deepcopy(seed)
    return tour

def grasp(distance_matrix, n):
    tour = []
    city_tour = []
    print('---- Montando solução')
    for i in range(0,n):
        print('---- Tour atual{}'.format(tour))
        tour = greedy_closest(distance_matrix,tour)
    city_tour.append(tour)
    city_tour.append(0)
    city_tour[1] = (get_total_distance(distance_matrix,city_tour[0]))
    best_route = localsearch_2opt(distance_matrix,city_tour)
    print(best_route)



if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    m = read_distance_matrix(args.file)
    grasp(m, 5)

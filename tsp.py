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
def cheapestInsertion(distance_matrix):
    dista = distance_matrix
    tour = []
    dTour = 0
    t1, t2, t3, dTour = tInicial(dista)
    tour.append(t1)
    tour.append(t2)
    tour.append(t3)
    listaMenor = []
    l=[]
    while len(tour) != len(dista):
        tab = caminho(tour)
        for x in range(len(dista)):
            if x not in tour and x not in listaMenor:
                for i in tab:
                    id, res = distanciaCheapest(i[0], i[1], x, dista)
                    l.append(i[0])
                    l.append(id)
                    l.append(i[1])
                    l.append(res)
                    if len(l)!=0:
                        listaMenor.append(l)
                        l=[]
        n,m,id,dis=menorDistanciaVet(listaMenor)
        tour=inserirTour(n,m,id,tour)
        dTour+=dis
        listaMenor=[]
    return tour

def hillClimbing(distaMatriz):
    atualSolucao = cheapestInsertion(distaMatriz)
    atualTamanhoRota = get_total_distance(distaMatriz, atualSolucao)
    vizinhos = funcVizinhos(atualSolucao)
    melhorVizinho, melhorVizinhoTamanhoRota = funcMelhorVizinho(distaMatriz, vizinhos)

    while melhorVizinhoTamanhoRota < atualTamanhoRota:
        atualSolucao = melhorVizinho
        atualTamanhoRota = melhorVizinhoTamanhoRota
        vizinhos = funcVizinhos(atualSolucao)
        melhorVizinho, melhorVizinhoTamanhoRota = funcMelhorVizinho(distaMatriz, vizinhos)

    return atualSolucao, atualTamanhoRota

def heuristicaCriada(distaMatriz,n):
    melhorDis=99999990
    melhorRota=[]
    rotas=[]
    tour=[]
    for i in range(n):
        cam,dis=hillClimbing(distaMatriz)
        tour.append(cam)
        tour.append(dis)
        rotas.append(tour)
        if dis<melhorDis:
            melhorDis=dis
            melhorRota=cam
        tour=[]
        print("iteracao =", i, "| distancia total =", melhorDis)
    print(melhorRota)


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

def grasp2(distance_matrix, n):
    tour = []
    city_tour = []
    print('---- Montando solução')
    for i in range(0,n):
        #print('---- Tour atual{}'.format(tour))
        tour = cheapestInsertion(distance_matrix)
    city_tour.append(tour)
    city_tour.append(get_total_distance(distance_matrix,tour))
    print(city_tour)
    best_route = hillClimbing(distance_matrix,tour)
    #print(best_route)

if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    #m = read_distance_matrix(args.file)
    #grasp(m, 5)
    mat=pegaMatriz(args.file)
    #cheapestInsertion(mat)
    #grasp2(mat, 5)
    #print(hillClimbing(mat))
    heuristicaCriada(mat,1000)
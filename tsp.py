import sys
import copy
import random
from email import parser
from utils import *
from argparse import ArgumentParser
from rand import rand_num

def ranking(distance_matrix, city_tour, city=1, rcl=25):
    distance_list = copy.deepcopy(distance_matrix[city-1])
    tour_ = copy.deepcopy(city_tour)
    tour_.sort(reverse=True)
    for item in tour_:
        distance_list.pop(item-1)
    distance_list.sort()
    if 0 in distance_list:
        distance_list.remove(0)
    return distance_list[:rcl]

def seed_function(distance_matrix, tour, rcl_limiter=25):
    closest = 9999
    if len(tour) == 0:
        #last_city = rand_num(len(distance_matrix[0]))
        last_city = 1
        tour.append(last_city)
    else:
        last_city = tour[-1]
    rcl = ranking(distance_matrix, tour, tour[-1], rcl_limiter)
    for k in range(0,len(distance_matrix[0])):
        if len(rcl) != 0:
            next_city_d = random.choice(rcl)
            for idx,item in enumerate(distance_matrix[last_city - 1]):
                if item == next_city_d and (idx + 1) not in tour:
                    next_city = idx + 1
            try:
                tour.append(next_city)
                rcl = ranking(distance_matrix, tour, tour[-1], rcl_limiter)
                last_city = tour[-1]
            except:
                pass
        else:
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
                    #print(i[0],"--",x,"--",i[1],)
                    id, res = distanciaCheapest(i[0], i[1], x, dista)

                    l.append(i[0])
                    l.append(id)
                    l.append(i[1])
                    l.append(res)
                    if len(l)!=0:
                        #print(l)
                        listaMenor.append(l)
                        l=[]
        #print(listaMenor)
        n,m,id,dis=menorDistanciaVet(listaMenor)
        #print(n,m,id,"-----",dis)
        tour=inserirTour(n,m,id,tour)
        dTour+=dis
        listaMenor=[]
        #print(tour)
        #print(dTour)
        #print("------")
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
            best_route[1] = get_total_distance(distance_matrix,best_route[0])
            if(best_route[1] < tour[1]):
                tour[1] = copy.deepcopy(best_route[1])
                for n in range(0, len(tour[0])): 
                    tour[0][n] = best_route[0][n]
            best_route = copy.deepcopy(seed)
    return tour

def grasp(distance_matrix, iterations= 50, rcl=10):
    seed = []
    city_tour = []
    best_route = [[9999],9999] # estrutura é [[lista de cidades], distancia total]
    best_iteration = 0
    print('---- Montando solução')
    for count in range(0,iterations): # Multistart
        # construtor
        seed = seed_function(distance_matrix,seed,rcl)
        city_tour.append(seed)
        city_tour.append((get_total_distance(distance_matrix,city_tour[0])))
        actual_best_route = localsearch_2opt(distance_matrix,city_tour)
        if actual_best_route[1] < best_route[1]:
            best_route = copy.deepcopy(actual_best_route)
            best_iteration = count
        #reset tour
        print("iteracao =", count, "| distancia total =", best_route[1])
        #print(best_route[0])
        city_tour = []
        actual_best_route = []
        seed = []
    return best_iteration, best_route



if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    m = read_distance_matrix(args.file)
    it, route = grasp(m, 7000, 3)
    print('Melhor iteração foi em -> {}'.format(it))
    #mat=pegaMatriz(args.file)
    #grasp2(mat, 6)
    #m = read_distance_matrix(args.file)
    #grasp(m, 5)
    mat=pegaMatriz(args.file)
    #cheapestInsertion(mat)
    #grasp2(mat, 5)
    #print(hillClimbing(mat))
    heuristicaCriada(mat,5000)
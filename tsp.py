import sys
import copy
from email import parser
from utils import *
from argparse import ArgumentParser
from rand import rand_num

def greedy_closest(distance_matrix, tour):
    closest = 9999
    if len(tour) == 0:
        #last_city = rand_num(len(distance_matrix[0]))
        last_city = 1
        tour.append(last_city)
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
        pass
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
        print(tour)
        print(dTour)
        print("------")
    return tour

def hillClimbing(distMatriz,solucao):
    atualSolucao = solucao
    atualRotaTamanho = tamanhoRota(distMatriz, atualSolucao)
    vizinhos = criandoVizinhos(atualSolucao)
    mVizinho, mVizinhoTamanhoRota = melhorVizinho(distMatriz, vizinhos)

    while mVizinhoTamanhoRota < atualRotaTamanho:
        atualSolucao = mVizinho
        atualRotaTamanho = mVizinhoTamanhoRota
        vizinhos = criandoVizinhos(atualSolucao)
        mVizinho, mVizinhoTamanhoRota = melhorVizinho(distMatriz, vizinhos)

    return atualSolucao, atualRotaTamanho


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

def grasp(distance_matrix, n, iterations= 50):
    seed = []
    city_tour = []
    best_route = [[9999],9999] # estrutura é [[lista de cidades], distancia total]
    
    print('---- Montando solução')
    for count in range(0,iterations): # Multistart
        # construtor
        for i in range(0,n):
            seed = greedy_closest(distance_matrix,seed)
        city_tour.append(seed)
        city_tour.append((get_total_distance(distance_matrix,city_tour[0])))
        actual_best_route = localsearch_2opt(distance_matrix,city_tour)
        if actual_best_route[1] < best_route[1]:
            best_route = copy.deepcopy(actual_best_route)
        #reset tour
        print("iteracao =", count, "| distancia total =", best_route[1])
        actual_best_route = []
        seed = []

def grasp2(distance_matrix, n):
    tour = []
    city_tour = []
    print('---- Montando solução')
    for i in range(0,n):
        print('---- Tour atual{}'.format(tour))
        tour = cheapestInsertion(distance_matrix)
    city_tour.append(tour)
    city_tour.append(0)
    city_tour[1] = (get_total_distance(distance_matrix,city_tour[0]))
    best_route = hillClimbing(distance_matrix,city_tour)
    print(best_route)

if __name__ == '__main__':
    #arg parser
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='path to file of distance matrix', metavar='PATH', required=True)
    args = parser.parse_args()

    m = read_distance_matrix(args.file)
    n = len(m[0])
    grasp(m, n)
    #mat=pegaMatriz(args.file)
    #grasp2(mat, 6)
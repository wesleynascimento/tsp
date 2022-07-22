from rand import rand_num

def read_distance_matrix(filename):
    with open(filename, 'r') as f:
        l = [[float(num) for num in line.split()] for line in f]
    return l

def initial_point(data):
    total_city = len(data)
    return rand_num(total_city)

def get_total_distance(distance_matrix, city_tour):
    total_distance = 0
    for idx, i in enumerate(city_tour):
        try:
            total_distance += distance_matrix[i-1][city_tour[idx+1]-1]
        except:
            pass
    return total_distance

def distanciaCheapest(i,j,k,mat):
    dist=mat[i][k]+mat[k][j]-mat[i][j]
    return k,dist

def caminho(tour):
    lista = []
    l = []
    for i in range(len(tour) - 1):
        l.append(tour[i])
        l.append(tour[i + 1])
        lista.append(l)
        l = []
    l.append(tour[-1])
    l.append(tour[0])
    lista.append(l)
    l = []
    return lista
def menorDistanciaVet(vet):
    aux=1000000
    id=-1
    for i in range(len(vet)):
        if vet[i][3]<aux:
            n = vet[i][0]
            id = vet[i][1]
            m = vet[i][2]
            aux = vet[i][3]


    return n,m, id,aux

def inserirTour(i,j,k,tour):
    corte1 = tour.index(i)
    l1 = tour[:corte1 + 1]
    l2 = tour[corte1 + 1:]
    l3 = []
    l3 = l1
    l3.append(k)
    l3 += l2
    return l3

def tInicial(mat):
    dis=0
    esc=[]
    tam=len(mat)-1

    while len(esc)!=3:
        x = rand_num(tam)
        if x not in esc:
            esc.append(x)
    ini = esc[0]
    mid=esc[1]
    fim=esc[2]
    dis=mat[0][1]+mat[1][2]+mat[2][0]
    return ini,mid,fim,dis

def pegaMatriz(nome):
    vet=[]
    mat=[]
    lin=[]
    num=""
    arq=open(nome,"r")
    for x in arq:
        lin=x.strip("\n")
        lin=x.split(" ")
        vet.append(lin)
    for i in vet:
        lin=[]
        for j in i:
            if j!=" " or j!="" or j!='"':
                num+=j
            if j=='"':
                num=""
            elif j!="":
                numInt=int(float(num))
                lin.append(numInt)
                num=""
        mat.append(lin)
    return mat

def funcVizinhos(solucao):
    vizinhos = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinho = solucao.copy()
            vizinho[i] = solucao[j]
            vizinho[j] = solucao[i]
            vizinhos.append(vizinho)
    return vizinhos

def funcMelhorVizinho(distMatriz, vizinhos):
    melhorRotaTamanho = get_total_distance(distMatriz, vizinhos[0])
    melhorVizinho = vizinhos[0]
    for vizinho in vizinhos:
        atualTamanhoRota = get_total_distance(distMatriz, vizinho)
        if atualTamanhoRota < melhorRotaTamanho:
            melhorRotaTamanho = atualTamanhoRota
            melhorVizinho = vizinho
    return melhorVizinho, melhorRotaTamanho
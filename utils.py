from rand import rand_num

def read_distance_matrix(filename):
    with open(filename, 'r') as f:
        l = [[float(num) for num in line.split('  ')] for line in f]
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
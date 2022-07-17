def read_distance_matrix(filename):
    with open(filename, 'r') as f:
        l = [[float(num) for num in line.split('  ')] for line in f]
    return l
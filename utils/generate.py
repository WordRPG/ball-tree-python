import random

generator = random.Random(1234)

def generate_random_point(dims): 
    return [generator.random() - generator.random() for i in range(dims)]

def generate_random_points(n, dims): 
    return [generate_random_point(dims) for i in range(n)]
import math 

def squared_euclidean_distance(A, B):
    total = sum((A[i] - B[i]) ** 2 for i in range(len(A)))
    return total

def euclidean_distance(A, B):
    total = sum((A[i] - B[i]) ** 2 for i in range(len(A)))
    return math.sqrt(total) 

def magnitude(A): 
    return math.sqrt(sum(A[i] ** 2 for i in range(len(A))))

def cosine_distance(A, B):
    dot_product = sum(A[i] * B[i] for i in range(len(A)))
    cosine = dot_product / (magnitude(A) * magnitude(B))
    return cosine
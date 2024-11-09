from utils.metrics import euclidean_distance 

def brute_force_nearest_neighbors(points, target, k, metric_fn = euclidean_distance): 
    neighbors = []
    for i in range(len(points)): 
        other_point = points[i]
        distance = metric_fn(target, other_point) 
        record = { 
            "index" : i, 
            "point" : other_point, 
            "distance" : distance 
        }
        neighbors.append(record) 
    neighbors.sort(key=lambda x: x["distance"])
    neighbors = [[x["index"], x["distance"]] for x in neighbors]
    neighbors = neighbors[0:k]
    return neighbors
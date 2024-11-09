from ball_tree import BallTree 
from utils.generate import generate_random_points
from utils.neighbors import brute_force_nearest_neighbors

print("Generating random points.")
points = generate_random_points(100, 300)
target = points[50]
query_count = 10

print("Brute forcing random points with nearest neighbors search.")
nearest_bf = brute_force_nearest_neighbors(points, target, query_count)
for item in nearest_bf:
    print("\t", item[0], "|", item[1])

print("Initializing tree.")
tree = BallTree()

print("Building tree.")
visits = tree.build(points)

print(tree.size)

# print("Querying tree.") 
# nearest = tree.nearest(target)
# print(nearest)
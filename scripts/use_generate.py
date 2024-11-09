from utils.generate import generate_random_point, generate_random_points

point = generate_random_point(3)
print(point)

print("-----")

points = generate_random_points(100, 3)
print(len(points))
print(points[0])
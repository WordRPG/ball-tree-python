from utils.metrics import euclidean_distance
from utils.project_point import project_to_line


class Point: 
    def __init__(self, value, id_): 
        self.value = value 
        self.id = id_ 

class ProjectedPoint(Point): 
    def __init__(self, value, id_):
        Point.__init__(self, value, id_)

class Centroid(Point): 
    def __init__(self, value, id_):
        Point.__init__(self, value, id_)

class BallTree:
    def __init__(self, metric_fn = euclidean_distance): 
        self.metric_fn = metric_fn
        self.root = None
        self.size = 0
        self.threshold = 1
        
        self.leaf_ids = []
        self.leaf_depths = []

    def metric(self, A, B):
        return self.metric_fn(A.value, B.value)

    def prepare_points(self, points):
        self.points = [Point(points[i], i) for i in range(len(points))] 

    def build(self, points, verbose = False): 
        self.prepare_points(points)
        state = {
            "visit_count" : 0,
            "verbose" : verbose
        }
        self.root = self.buildFor(self.points, 0, state)
        self.balance_info = self.get_balance_info()
        return state["visit_count"]
        
    def buildFor(self, points, depth, state): 
        state["visit_count"] += 1

        if state["verbose"]:
            print("Visit Count :", state["visit_count"])

        # --- base conditions --- # 
        if len(points) <= self.threshold:
            self.size += len(points)
            return {
                "points" : [point.id for point in points], 
                "left" : None, 
                "right" : None,
                "sub_leaf" : True
            }  

        if len(points) == 0:
            return None  

        # --- specify key point --- # 
        key_point = points[len(points) // 2]

        # --- build line --- #
        farthest_index_a = self.find_farthest(key_point, points)
        farthest_point_a = points[farthest_index_a] 
        farthest_index_b = self.find_farthest(farthest_point_a, points)
        farthest_point_b = points[farthest_index_b]
        line = (farthest_point_a, farthest_point_b)

        # --- project points to line --- # 
        projections = self.project_points(line, points) 
        
        # --- get median of points --- # 
        median, left, right = self.get_median_data(line, projections)
        
        centroid = self.centroid(points, median.id)
        radius = self.radius(centroid, points) 

        node = {}

        print("  " * depth, len(left), len(right))

        if len(left) <= self.threshold or len(right) <= self.threshold:
            node["is_leaf"] = True
            self.leaf_depths.append(depth) 
            self.leaf_ids.append(median.id)

        # --- build node --- # 
        node = {
            "id" : median.id, 
            "centroid" : centroid,
        }

        node["left"] = self.buildFor(left, depth + 1, state), 
        node["right"] = self.buildFor(right, depth + 1, state)
    
        # --- build left and right subtree --- #
        return node

    def find_farthest(self, key_point, points):
        farthest_index = -1
        farthest_distance = float("-inf")
        for i in range(len(points)):
            other_point = points[i]
            distance = self.metric(key_point, other_point) 
            if distance > farthest_distance: 
                farthest_index = i 
                farthest_distance = distance 
        return farthest_index

    def project_points(self, line, points):
        projections = [] 
        A = line[0]
        B = line[1]
        for i in range(len(points)):
            C = points[i]
            projection = project_to_line(A.value, B.value, C.value)
            projection = ProjectedPoint(projection, points[i].id)
            projections.append(projection)
        return projections

    def get_median_data(self, line, projections): 
        A = line[0]
        B = line[1]

        # --- compute distances and then sort --- #
        distances = [] 
        for i in range(len(projections)):
            C = projections[i] 
            record = {
                "point" : C, 
                "distance" : self.metric(A, C)
            }
            distances.append(record)
        distances.sort(key=lambda x: x["distance"]) 

        # --- get items to the left and right --- # 
        median_index = len(projections) // 2
        median = projections[median_index]

        left = [x["point"] for x in distances[0:median_index]]
        right = [x["point"] for x in distances[median_index:]]

        return median, left, right

    def get_balance_info(self):
        X = self.leaf_depths
        count = len(X)
        min_  = min(X)
        max_  = max(X)
        ave   = sum(X) / len(self.leaf_depths) 
        std   = (sum((X[i] - ave) ** 2 for i in range(len(X))) / count) ** 1/2 
        dist  = {} 
        for item in self.leaf_depths:
            if item not in dist:
                dist[item] = 0
            dist[item] += 1 

        return {
            "count" : count,
            "min" : min_,
            "max" : max_, 
            "ave" : ave, 
            "std" : std, 
            "dist" : dist 
        }   
        

    def centroid(self, points, id_): 
        n = len(points)
        dims = len(points[0].value)
        centroid = [0 for i in range(dims)]
        for i in range(n):
            point = points[i]
            coords = point.value
            for j in range(dims):
                centroid[j] += coords[j]
        centroid = [x / n for x in centroid]
        return Centroid(centroid, id_) 

    def radius(self, centroid, points):
        farthest_index = self.find_farthest(centroid, points)
        farthest_point = points[farthest_index]
        radius = self.metric(centroid, farthest_point)
        return radius

    def nearest(self, target, verbose = True): 
        state = {
            "visit_count" : 0, 
            "verbose" : verbose
        }
        return self.nearest_search_in(self.root, target, None, state) 

    def nearest_search_in(self, node, target, parent, state):   
        if state["verbose"]: 
            print("Visit Count :", state["visit_count"])
        
        if "is_leaf" in node:
            return None

        centroid_a = node["left"]["centroid"]
        centroid_b = node["right"]["centroid"]

        dist_centroid_a = self.metric(target, centroid_a) 
        dist_centroid_b = self.metric(target, centroid_b) 

        if dist_centroid_a < dist_centroid_b: 
            return self.nearest_search_in(node["left"], target, node, state) 
        else: 
            return self.nearest_search_in(node["right"], target, node, state)

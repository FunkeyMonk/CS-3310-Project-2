import random
import time
import heapq

def create_rand_graph():
    vertices_list = [10,20,30] #can add more if necessary
    vertices = random.choice(vertices_list) #grabs random value from vertices list
    density = round(random.uniform(0.1, 0.9), 2) #provides random density
    #density = 0.9 #fixed density for consistent testing
    
    #create graph using the random vertices and density
    graph = {i: {} for i in range(vertices)}
    for i in range(vertices):
        for j in range(vertices):
            if i!=j and random.random() < density:
                graph[i][j] = random.randint(1, 10) #weights range from 1 to 10, can change
    
    #prints the graph values and the graph
    print(f"Graph: {vertices} vertices, density={density}")
    for u, neighbors in graph.items():
        print(f"{u}: {neighbors}")
    return graph

def repeated_dijkstra(graph):
    map = {
        vertex: list() for vertex in graph
    }
    for vertex in graph:
        map[vertex] = dijkstra(graph, vertex)
    return map

def dijkstra(graph, source):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        #skip if on worse path
        if current_distance > distances[current_vertex]:
            continue

        #explore neighbors, update distances, add to priority queue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def floyd_warshal(graph):
    INF = float('infinity')
    vertices = list(graph.keys())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    # Initialize distance matrix
    dist = [[INF] * n for _ in range(n)]
    for v in vertices:
        i = index[v]
        dist[i][i] = 0

    # Set initial edge weights
    for u, neighbors in graph.items():
        i = index[u]
        for v, w in neighbors.items():
            j = index[v]
            if w < dist[i][j]:
                dist[i][j] = w

    # Floyd–Warshall algorithm
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist

    # Convert back to dict-of-dicts: {source: {target: distance}}
    result = {}
    for i, u in enumerate(vertices):
        inner = {}
        for j, v in enumerate(vertices):
            inner[v] = dist[i][j]
        result[u] = inner

    return result

def find_all_paths(graph, start, end, path=None):
        if path is None:
            path = [start]
        
        if start == end:
            return [path]
        
        if start not in graph:
            return []
        
        paths = []
        for neighbor in graph[start]:
            if neighbor not in path: # Avoid cycles
                new_path = path + [neighbor]
                new_paths = find_all_paths(graph, neighbor, end, new_path)
                for p in new_paths:
                    paths.append(p)
        return paths

#goes through found path and adds weights
def calculate_path_weight(graph, path):
    total_weight = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        total_weight += graph[u][v]
    return total_weight
    
# Validation Function (brute-force comparison)
def validate_algorithms(graph):
    
    dijkstra_results = repeated_dijkstra(graph)
    fw_results = floyd_warshal(graph)
    
    vertices = list(graph.keys())
    all_tests_passed = True

    for start in vertices: #go through every pair
        for end in vertices:
            if start == end:
                continue
            
            all_paths = find_all_paths(graph, start, end) #Result of brute force paths
            
            path_weights = []
            if not all_paths: # No path exists
                true_min = float('infinity')
            else:
                for p in all_paths: #calculate weights for each path
                    w = calculate_path_weight(graph, p)
                    path_weights.append(w)
                true_min = min(path_weights) #get minimum weight from all paths of the pair

            #get results of pair from both algorithms
            d_res = dijkstra_results[start][end]
            fw_res = fw_results[start][end]
            
            #compares the results to the bruteforce
            match_dijkstra = (d_res == true_min)
            match_fw = (fw_res == true_min)
            
            if not match_dijkstra or not match_fw:
                all_tests_passed = False
            
    print("Result:")
    if all_tests_passed:
        print("All pairs match\n")
    else:
        print("Pairs do not match\n")
        
def rand_graph_testing(counter):
    print("Graph: ", counter+1)
    graph = create_rand_graph()

    start = time.perf_counter()
    res = repeated_dijkstra(graph)
    end = time.perf_counter()
    
    for(key, value) in res.items():
        print(f"From vertex {key}: {value}")

    print("\nRepeated Dijkstra's Algorithm")
    print("Runtime: ", end-start, " seconds")

    start = time.perf_counter()
    res = floyd_warshal(graph)
    end = time.perf_counter()

    print("\nFloyd-Warshal Algorithm")
    print("Runtime: ", end-start, " seconds\n")
    return graph

def fixed_graph_testing(counter):
    print("Graph: ", counter+1)
    graph = {
        0: {1: 3, 2: 8, 4: 4},
        1: {3: 1, 4: 7},
        2: {1: 4},
        3: {0: 2, 2: 5},
        4: {3: 6}
    }

    start = time.perf_counter()
    res = repeated_dijkstra(graph)
    end = time.perf_counter()
    
    for(key, value) in res.items():
        print(f"From vertex {key}: {value}")

    print("\nRepeated Dijkstra's Algorithm")
    print("Runtime: ", end-start, " seconds\n")
    
    start = time.perf_counter()
    res = floyd_warshal(graph)
    end = time.perf_counter()
    
    for(key, value) in res.items():
        print(f"From vertex {key}: {value}")

    print("\nFloyd-Warshal Algorithm")
    print("Runtime: ", end-start, " seconds\n")
    return graph

def main():
    currentTest = 0 #0 for fixed graph, 1 for random graphs
    graph = None
    if currentTest == 0:
        print("Fixed Graph Testing:\n")
        graph = fixed_graph_testing(0)
        
        print("Validation Testing")     #Validation of both algorithms for fixed graph
        validate_algorithms(graph)      #has a time complexity of O(V*V!) so only use for small graphs unless you want to blow up your computer
    else:
        print("Random Graph Testing:\n")
        for i in range(5):
            graph = rand_graph_testing(i)

if __name__ == "__main__":
    main()

import random
import time
import heapq

def create_rand_graph():
    vertices_list = [30,40,50] #can add more if necessary
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
    print("Runtime: ", end-start, " seconds")
    print("\n\n")

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
    print("Runtime: ", end-start, " seconds")
    print("\n\n")

def main():
    #for i in range(5):
    #    rand_graph_testing(i)'
    fixed_graph_testing(0)

if __name__ == "__main__":
    main()

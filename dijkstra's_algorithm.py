print("\n[hw] week09: Dijkstra's Algorithm")
import numpy as np

def dijkstra(graph, start):
    inf = 1000
    n = len(graph)
    distance = [inf] * n    # distance
    visited = [False] * n   # flag
    distance[start] = 0     # start node
    path = [[] for _ in range(n)]   # list to save 'path'

    for _ in range(n):
        min_dist = inf  # minimum distance
        min_index = -1  # minimum index
        for i in range(n):
            if (not visited[i]) and (distance[i] < min_dist):   # update
                min_dist = distance[i]
                min_index = i
        
        if (min_index != -1):
            visited[min_index] = True   # flag
            for j in range(n):
                if (not visited[j]) and (graph[min_index][j] != inf):
                    new_dist = distance[min_index] + graph[min_index][j]
                    if new_dist < distance[j]:  # update
                        distance[j] = new_dist
                        path[j] = path[min_index] + [min_index]

    return distance, path

# directed graph
inf = 1000
graph = np.array([
    [0, 3, 2, 8, inf, inf],     # start from node 'a'
    [inf, 0, 1, inf, 5, inf],
    [inf, inf, 0, 5, 3, inf],
    [inf, inf, inf, 0, 3, 2],
    [inf, inf, inf, inf, 0, 1],
    [inf, inf, inf, inf, inf, 0]
])

start_node = 0      # start from node 'a' (index = 0)
distances, paths = dijkstra(graph, start_node)

nodes = ['a', 'b', 'c', 'd', 'e', 'f']  # node labels

print("\n(1) Shortest Path from node 'a' by Dijkstra's Algorithm")
for i in range(1, len(distances)):  # repeat -- except for start node
    node_label = nodes[i]
    shortest_distance = distances[i]
    shortest_path = [nodes[node] for node in paths[i] + [i]]
    shortest_path_str = ' -> '.join(shortest_path)
    print("[path to " + node_label + "] " + shortest_path_str
          + " (distance: " + str(shortest_distance) + ")")


print("\n(2) Shortest & Longest Distance:")
shortest_distance = min(distances[1:])          # distance
longest_distance = max(distances[1:])           # distance

shortest_node_index = np.argmin(distances[1:])  # distance -> index
longest_node_index = np.argmax(distances[1:])   # distance -> index

shortest_node = nodes[shortest_node_index]      # index -> node label
longest_node = nodes[longest_node_index]        # index -> node label

print("Shortest: node '", shortest_node, "' (distance: ", shortest_distance, ")", sep='')
print("Longest: node '", longest_node, "' (distance: ", longest_distance, ")", sep='')
print()
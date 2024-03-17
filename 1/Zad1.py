import pandas as pd
import matplotlib.pyplot as plt
import time
import sys
import graph as G

def splitTime(date):
    splitDate = date.split(":")
    return int(splitDate[0])*60+int(splitDate[1])

def compileTime(time):
    return str(int(time/60))+":"+str(time%60)

# Tworzenie DataFrame z danymi
df = pd.read_csv('c1.csv')
# df = pd.read_csv('connection_graph.csv')



# Tworzenie grafu ważonego
graph = G.Graph()

# Dodawanie krawędzi i wag do grafu
for index, row in df.iterrows():
    edge = (row['start_stop'], row['end_stop'])
    graph.add_edge(row['start_stop'], row['end_stop'],row['line'],row["departure_time"],row["arrival_time"],row["start_stop_lat"],row["start_stop_lon"],row["end_stop_lat"],row["end_stop_lon"])


# Algorytm Dijkstry
# start_node = 'Babimojska'  # Początkowy wierzchołek
# end_node = 'Biegasa'  # Wierzchołek docelowy
# start_time = "16:58:00"


start_node = 'Pola'  # Początkowy wierzchołek
end_node = 'Przybyszewskiego'  # Wierzchołek docelowy
start_time = "20:05:00"

# path, total_distance = graph.dijkstra_algorithm(start_node, end_node, start_time)
# print(path)
# print(total_distance)


# print(graph.a_star(start_node, end_node, start_time))
# print(graph.a_star_line(start_node, end_node, start_time))



def toString(self):
    print(self.start_node.name,self.end_node.name,self.line,self.departure_time,self.arrival_time)

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    stops = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        stops.append(previous_nodes[node][1])
        node = previous_nodes[node][0]
 
    # Add the start node manually
    path.append(start_node)
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))
    for stop in stops:
        toString(stop)

def print_a_star(start_node,target_node,path):
    paths = []
    stops = []
    node = target_node
    while node != start_node:
        paths.append(node)
        print(path[node].end_node.name)
        stops.append(path[node])
        node = path[node].start_node.name
    
    paths.append(start_node)
    print("We found the following best path with a value of {}.".format(path[target_node]))
    print(" -> ".join(reversed(paths)))
    for stop in stops:
        toString(stop)
print_a_star(start_node,end_node,graph.a_star_test(start_node, end_node, start_time))
# print_a_star(start_node,end_node,graph.a_star(start_node, end_node, start_time))
# print(graph.a_star(start_node, end_node, start_time))

# print_result(path,total_distance,start_node,end_node)
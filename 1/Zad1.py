import pandas as pd
import graph as G

def splitTime(date):
    splitDate = date.split(":")
    return int(splitDate[0])*60+int(splitDate[1])

def compileTime(time):
    return str(int(time/60))+":"+str(time%60)

# Tworzenie DataFrame z danymi
# df = pd.read_csv('c1.csv')
df = pd.read_csv('connection_graph.csv')



# Tworzenie grafu ważonego
graph = G.Graph()

# Dodawanie krawędzi i wag do grafu
for index, row in df.iterrows():
    edge = (row['start_stop'], row['end_stop'])
    graph.add_edge(row['start_stop'], row['end_stop'],row['line'],row["departure_time"],row["arrival_time"],row["start_stop_lat"],row["start_stop_lon"],row["end_stop_lat"],row["end_stop_lon"])


# Algorytm Dijkstry
start_node = 'Piastowska'  # Początkowy wierzchołek
end_node = 'FAT'  # Wierzchołek docelowy
start_time = "12:00:00"


# start_node = 'Pola'  # Początkowy wierzchołek
# end_node = 'Rondo'  # Wierzchołek docelowy
# start_time = "20:05:00"

# print(path)
# print(total_distance)




# print_a_star(start_node,end_node,graph.a_star_test(start_node, end_node, start_time))
# print_a_star(start_node,end_node,graph.a_star(start_node, end_node, start_time))
# print(graph.a_star(start_node, end_node, start_time))
        
graph.djikstra(start_node, end_node, start_time)
graph.a_star_algorithm(start_node,end_node,"t",start_time)
graph.a_star_algorithm(start_node,end_node,"p",start_time)

# print_result(path,total_distance,start_node,end_node)
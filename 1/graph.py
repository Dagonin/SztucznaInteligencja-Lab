from geopy.distance import geodesic
import time
import math

SPEED = 19

def splitTime(date):
    splitDate = date.split(":")
    return int(splitDate[0])*60+int(splitDate[1])

def joinTime(time):
    hours = math.floor(time/60)
    minutes = time%60
    return f"{hours}:{minutes}:00"

    

class Node:
    def __init__(self, name,coordinates):
        self.name = name
        self.coordinates = coordinates
        self.edges = []

class Edge:
    def __init__(self, start_node, end_node, line, departure_time, arrival_time):
        self.start_node = start_node
        self.end_node = end_node
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def getWeight(self,currentTime):
        if(self.departure_time>=currentTime):
            return 1 + self.departure_time - currentTime
        else:
            return float('inf')
        
    def getWeight_line(self,currentLine,currentTime):
        if(self.departure_time>=currentTime):
            if(self.line==currentLine):
                return 0 + (self.departure_time - currentTime)/10000
            else:
                return 1 + (self.departure_time - currentTime)/10000
        else:
            return float('inf')
                


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name,coordinates):
        node = Node(name,coordinates)
        self.nodes[name] = node

    def add_edge(self, start_node_name, end_node_name, line, departure_time, arrival_time,start_lat,start_lon,end_lat,end_lon):
        if start_node_name not in self.nodes:
            self.add_node(start_node_name,(start_lat,start_lon))
        if end_node_name not in self.nodes:
            self.add_node(end_node_name,(end_lat,end_lon))

        start_node = self.nodes[start_node_name]
        end_node = self.nodes[end_node_name]

        edge = Edge(start_node, end_node, line, splitTime(departure_time), splitTime(arrival_time))
        self.nodes[start_node.name].edges.append(edge)
        self.edges.append(edge)

    def getHeuristic(self,start_node,end_node):
        distance1 = math.sqrt(pow(start_node.coordinates[0] - end_node.coordinates[0],2) + pow(start_node.coordinates[1] - end_node.coordinates[1],2))
        return distance1

    def getNeighbors(self, start_node):
        return self.nodes[start_node].edges
    

    def djikstra(self,start_node,end_node,start_time):
        test_numer = 0
        algorithm_start_time = time.time()
        visited = {}
        unvisited = {}
        for node in self.nodes:
            unvisited[node] = [float('inf'),None]
        unvisited[start_node] = [splitTime(start_time),None]
        finished = False
        while finished == False:
            test_numer+=1
            if(len(unvisited)==0):
                finished = True
            else:
                current_min_node = None
                for node in unvisited:
                    if current_min_node == None:
                        current_min_node = node
                    elif unvisited[node][0] < unvisited[current_min_node][0]:
                        current_min_node = node
                current_time = unvisited[current_min_node][0]
                neighbors = self.getNeighbors(current_min_node)       
                for neighbor in neighbors:
                    if(neighbor.end_node.name not in visited):
                        if(unvisited[current_min_node][1]==None):
                            new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight(current_time))
                        else:
                            new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight(unvisited[current_min_node][1].arrival_time))
                        if(new_g_score<unvisited[neighbor.end_node.name][0]):
                            unvisited[neighbor.end_node.name][0] = new_g_score
                            unvisited[neighbor.end_node.name][1] = neighbor
                visited[current_min_node] = unvisited[current_min_node][1]
                del unvisited[current_min_node]
        algorithm_end_time = time.time()
        elapsed_time = algorithm_end_time - algorithm_start_time
        print(f"Algorytm djikstra zajął: {elapsed_time}")
        print(test_numer)
        self.print_a_star(start_node,end_node,visited)
        return visited

    def a_star(self,start_node,end_node,start_time):
        test_numer = 0
        algorithm_start_time = time.time()
        visited = {}
        unvisited = {}
        f_score = 10
        current_time = splitTime(start_time)
        for node in self.nodes:
            unvisited[node] = [float('inf'),float('inf'),None]
        unvisited[start_node] = [0,f_score,None]
        finished = False
        while finished == False:
            test_numer+=1
            if(len(unvisited)==0):
                finished = True
            else:
                current_min_node = None
                for node in unvisited:
                    if current_min_node == None:
                        current_min_node = node
                    elif unvisited[node][1] < unvisited[current_min_node][1]:
                        current_min_node = node
                if(current_min_node==end_node):
                    finished = True
                    visited[current_min_node] = unvisited[current_min_node][2]
                else:
                    neighbors = self.getNeighbors(current_min_node)
                    for neighbor in neighbors:
                        if(neighbor.end_node.name not in visited):
                            if(unvisited[current_min_node][2]==None):
                                new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight(current_time))
                            else:
                                new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight(unvisited[current_min_node][2].arrival_time))
                            if(new_g_score<unvisited[neighbor.end_node.name][0]):
                                unvisited[neighbor.end_node.name][0] = new_g_score
                                unvisited[neighbor.end_node.name][1] = new_g_score + self.getHeuristic(neighbor.start_node,neighbor.end_node)
                                unvisited[neighbor.end_node.name][2] = neighbor

                    visited[current_min_node] = unvisited[current_min_node][2]
                    del unvisited[current_min_node]
        algorithm_end_time = time.time()
        elapsed_time = algorithm_end_time - algorithm_start_time
        print(f"Algorytm A* od czasu zajął: {elapsed_time}")
        print(test_numer)
        return visited



    

    def a_star_line(self,start_node,end_node,start_time):
        test_numer = 0
        algorithm_start_time = time.time()
        visited = {}
        unvisited = {}
        f_score = 10
        current_time = splitTime(start_time)
        for node in self.nodes:
            unvisited[node] = [float('inf'),float('inf'),None]
        unvisited[start_node] = [0,f_score,None]
        finished = False
        while finished == False:
            test_numer+=1
            if(len(unvisited)==0):
                finished = True
            else:
                current_min_node = None
                for node in unvisited:
                    if current_min_node == None:
                        current_min_node = node
                    elif unvisited[node][1] < unvisited[current_min_node][1]:
                        current_min_node = node
                if(current_min_node==end_node):
                    finished = True
                    visited[current_min_node] = unvisited[current_min_node][2]
                else:
                    neighbors = self.getNeighbors(current_min_node)
                    for neighbor in neighbors:
                        if(neighbor.end_node.name not in visited):
                            if(unvisited[current_min_node][2]==None):
                                new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight_line(None,current_time))
                            else:
                                new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight_line(unvisited[current_min_node][2].line,unvisited[current_min_node][2].arrival_time))
                            if(new_g_score<unvisited[neighbor.end_node.name][0]):
                                unvisited[neighbor.end_node.name][0] = new_g_score
                                unvisited[neighbor.end_node.name][1] = new_g_score + self.getHeuristic(neighbor.start_node,neighbor.end_node)
                                unvisited[neighbor.end_node.name][2] = neighbor

                    visited[current_min_node] = unvisited[current_min_node][2]
                    del unvisited[current_min_node]
        algorithm_end_time = time.time()
        elapsed_time = algorithm_end_time - algorithm_start_time
        print(f"Algorytm A* od liczby przesiadek zajął: {elapsed_time}")
        print(test_numer)
        return visited  


    def a_star_algorithm(self,start_node,end_node,type,start_time):
        
        if(type == "t"):
            self.print_a_star(start_node,end_node,self.a_star(start_node,end_node,start_time))
        if(type == "p"):
            self.print_a_star(start_node,end_node,self.a_star_line(start_node,end_node,start_time))
        else:
            return "Wybrales zly typ"
    

    def print_a_star(self, start_node, target_node, path):
        paths = {}

        node = target_node
        while node != start_node:
            current_line = path[node].line
            if current_line not in paths:
                paths[current_line] = [path[node]]
            else:
                paths[current_line].append(path[node])
            node = path[node].start_node.name

        for line, line_paths in paths.items():
            print("Linia", line)
            first_stop = line_paths[-1]  # Pierwszy przystanek na linii
            last_stop = line_paths[0]    # Ostatni przystanek na linii
            print(f"Przystanek start: {first_stop.start_node.name} | Przystanek koniec: {last_stop.end_node.name} | Czas odjazdu: {joinTime(first_stop.departure_time)} | Czas przyjazdu: {joinTime(last_stop.arrival_time)}")


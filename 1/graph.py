from datetime import datetime
import heapq
import sys
from geopy.distance import geodesic



SPEED = 19

def splitTime(date):
    splitDate = date.split(":")
    return int(splitDate[0])*60+int(splitDate[1])


    

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
            return self.departure_time - currentTime
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
        distance = geodesic(start_node.coordinates,end_node.coordinates).kilometers
        return distance/SPEED

    def getNeighbors(self, start_node):
        return self.nodes[start_node].edges

    def dijkstra_algorithm(self, start_node, end_node, start_time):
        unvisited_nodes = list(self.nodes)
    
        shortest_path = {}
        current_time = splitTime(start_time)
        previous_nodes = {}
     
        for node in unvisited_nodes:
            shortest_path[node] = float('inf') 
        shortest_path[start_node] = splitTime(start_time)

        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes: 
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
            neighbors = self.getNeighbors(current_min_node)
            current_time = shortest_path[current_min_node]
            for neighbor in neighbors:
                tentative_value = float(shortest_path[current_min_node]) + float(neighbor.getWeight(current_time))
                if tentative_value < shortest_path[neighbor.end_node.name]:
                    shortest_path[neighbor.end_node.name] = tentative_value
                    previous_nodes[neighbor.end_node.name] = (current_min_node,neighbor)
            unvisited_nodes.remove(current_min_node)

        return previous_nodes, shortest_path
    

    def a_star(self,start_node,end_node,start_time):
        visited = {}
        unvisited = {}
        for node in self.nodes:
            unvisited[node] = [float('inf'),float('inf'),None]
        f_score = 10
        unvisited[start_node] = [splitTime(start_time),f_score,None]
        finished = False
        while finished == False:
            if(len(unvisited)==0):
                finished == True
            else:
                current_min_node = None
                for node in unvisited:
                    if current_min_node == None:
                        current_min_node = node
                    elif unvisited[node][1] < unvisited[current_min_node][1]:
                        current_min_node = node
                current_time = unvisited[current_min_node][0]

                if(current_min_node==end_node):
                    finished = True
                    visited[current_min_node] = unvisited[current_min_node][2]
                else:
                    neighbors = self.getNeighbors(current_min_node)       
                    for neighbor in neighbors:
                        if(neighbor.end_node.name not in visited):
                            new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight(current_time))
                            if(new_g_score<unvisited[neighbor.end_node.name][0]):
                                unvisited[neighbor.end_node.name][0] = new_g_score
                                unvisited[neighbor.end_node.name][1] = new_g_score + self.getHeuristic(neighbor.start_node,neighbor.end_node)
                                unvisited[neighbor.end_node.name][2] = neighbor
                    visited[current_min_node] = unvisited[current_min_node][2]
                    del unvisited[current_min_node]
        return visited



    

    def a_star_test(self,start_node,end_node,start_time):
        visited = {}
        unvisited = {}
        f_score = 10
        current_time = splitTime(start_time)
        for node in self.nodes:
            # [waga,waga z heurystyka,przystanek,linia, czas]
            unvisited[node] = [float('inf'),float('inf'),None,None,0]
        unvisited[start_node] = [0,f_score,None,None,current_time]
        finished = False
        while finished == False:
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
                            new_g_score = float(unvisited[current_min_node][0]) + float(neighbor.getWeight_line(unvisited[current_min_node][3],unvisited[current_min_node][4]))
                            if(new_g_score<unvisited[neighbor.end_node.name][0]):
                                unvisited[neighbor.end_node.name][0] = new_g_score
                                unvisited[neighbor.end_node.name][1] = new_g_score + self.getHeuristic(neighbor.start_node,neighbor.end_node)
                                unvisited[neighbor.end_node.name][2] = neighbor
                                unvisited[neighbor.end_node.name][3] = neighbor.line
                                unvisited[neighbor.end_node.name][4] = neighbor.arrival_time

                    visited[current_min_node] = unvisited[current_min_node][2]
                    del unvisited[current_min_node]
        return visited  


    # https://adacomputerscience.org/concepts/path_a_star?examBoard=all&stage=all
    # jako heurestyke chyba najlepiej obliczanie czasu na podstawie odleglosci
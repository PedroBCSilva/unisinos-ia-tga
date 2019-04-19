# COMO USAR python simple_cvrp.py --file "CVRP/test.txt"

import random, sys, copy, math
from optparse import OptionParser
from random import randint

#          truck,node1,node2,node3,node4
solution = [[1,1,2,3,4,5,6,7,8,9,10]]

class cvrp:
    def __init__(self, filename, truck_count):
        self.filename = filename
        self.nodes = []
        self.nodes_count = 0
        self.capacity = 0
        self.deposit = None
        self.init_data(self.filename)
        self.truck_count = truck_count
        self.trucks = []
        self.init_trucks()
        self.solution = self.init_solution()
        self.total_distance = self.calc_total_distance()

    def init_data(self,filename):
        node_coord = False
        node_demand = False
        nodes_count = 0
        with open (filename, 'rt') as file:
            for line in file:
                if "NODE_COORD_SECTION" in line:
                    node_demand = False
                    node_coord = True
                    # do something
                    continue
                elif "DEMAND_SECTION" in line:
                    node_demand = True
                    node_coord = False
                    # do something
                    continue
                elif "CAPACITY" in line:
                    self.capacity = line[9:-1] #-1 para remover o \n
                    continue
                else:
                    if node_coord == True:
                        nodes_count = nodes_count + 1
                        (deposit, x, y) = line.split()
                        self.nodes.append([deposit, int(x), int(y), 0])
                        # print(self.nodes)
                    elif node_demand == True:
                        self.nodes_count = nodes_count
                        (deposit, quantity) = line.split()
                        self.nodes[int(deposit)-1] = [self.nodes[int(deposit)-1][0], self.nodes[int(deposit)-1][1], self.nodes[int(deposit)-1][2], int(quantity)]
                        continue
                    continue
        self.deposit = self.nodes[0]
        self.nodes.pop(0)

    def retrieve_data(self,index):
        return self.nodes[int(index)][1],self.nodes[int(index)][2]

    def printStatus(self):
        print("STATUS")
        print("======")
        print("Capacidade = ", self.capacity)
        print("Deposito = ", self.deposit)
        print("Distancia total = ", self.total_distance)
        print("Trucks = ", self.trucks)
        # print("Nós:")
        total = 0
        for i in range(len(self.nodes)):
            if len(self.nodes[i]) == 5:
                total += 1
        print("Quantidade Depositos = ", len(self.nodes))
        print("Nós percorridos =", total)

    def init_trucks(self):
        for i in range(self.truck_count):
            self.trucks.append(int(self.capacity))

    def get_first_not_flagged_node(self):
        pos = 0
        for node in self.nodes:
            if len(node) != 5:
                return pos
            pos = pos + 1
    
    def count_available_nodes(self):
        count = 0
        for node in self.nodes:
            if len(node) != 5:
                count += 1
        return count

    def find_random_node(self, truck):
        node = None
        has_node = self.count_available_nodes() > 0
        smallest_node = self.get_lowest_available_node()
        while node is None and has_node and truck >= smallest_node[3]:
            pos = randint(0, len(self.nodes)-1)
            if len(self.nodes[pos]) != 5 and truck-self.nodes[pos][3] >= 0:
                self.nodes[pos].append(False)
                return pos
        return None

    def get_lowest_available_node(self):
        smallest_pos = self.get_first_not_flagged_node()
        if smallest_pos is None:
            return None

        smallest_node = self.nodes[smallest_pos]
        pos = 0
        for node in self.nodes:
            if node[3] < smallest_node[3] and len(node) != 5:
                smallest_node = node
                smallest_pos = pos
            pos += 1

        return smallest_node

    def init_solution(self):
        all_solutions = []
        for i in range(len(self.trucks)):
            current_solution = []
            truck = self.trucks[i]
            has_nodes = True
            while has_nodes:
                node = self.find_random_node(truck)
                if node is None:
                    has_nodes = False # has no more close nodes with enough capacity to supply
                else:
                    current_solution.append(node)
                    truck = truck - int(self.get_cost(node)) # update truck capacity
            self.trucks[i] = truck # update truck capacity
            all_solutions.append(current_solution)
        return all_solutions

    def hill_climbing(self):
        all_solutions = self.init_solution()

        # generate neighborhood
        # running through neighbor until there is no other change
            # look for the best change
            # execute change

        return 0

    def calc_cost_route(self, nodes):
        total = 0
        for i in range(len(nodes)):
            node = self.nodes[i]
            if i == 0:
                total += self.calc_cost(self.deposit[1], node[1], self.deposit[2], node[2])
                if i+1 < len(nodes):
                    total += self.calc_cost(node[1], self.nodes[i+1][1], node[2], self.nodes[i+1][2])
            elif i == len(nodes)-1:
                total += self.calc_cost(node[1], self.deposit[1], node[2], self.deposit[2])
            else:
                total += self.calc_cost(node[1], self.nodes[i+1][1], node[2], self.nodes[i+1][2])
        return total

    def calc_total_distance(self):
        total = 0
        for solution in self.solution:
            total += self.calc_cost_route(solution)
        return total

    def calc_cost(self, xa, xb, ya, yb):
        return math.sqrt(((xa-xb) * (xa-xb))+((ya-yb) * (ya-yb)))

    def get_cost(self, pos):
        if not self.nodes:
            return None
        else:
            return self.nodes[pos][3]

    def check_quantity(self):
        qtyOk = 0
        count = 0
        truckQty = int(self.capacity)
        for trip in solution:
            node_length = len(trip)-1
            for node in range(0, node_length):
                print(int(self.nodes[int(node)][3]))
                truckQty = truckQty - int(self.nodes[int(node)][3])
                if truckQty < 0:
                    qtyOk = qtyOk -1
                print("current quantity", truckQty)
        if qtyOk == 0:
            qtyOk = qtyOk+1
        return qtyOk

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("--file", dest="filename", help="Path of file", default="CVRP/eil33.vrp.txt",
                     type="string")
    parser.add_option("--trucks", dest="truck_count", help="Quantity of trucks", default="4",
                     type="int")

    (options, args) = parser.parse_args()

    CVRP = cvrp(options.filename, options.truck_count)
    CVRP.printStatus()
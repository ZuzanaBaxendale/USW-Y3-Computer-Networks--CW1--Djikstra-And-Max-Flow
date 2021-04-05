infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False

class Dijkstra:

    def __init__(self):
        '''initialise class'''
        self.startnode = 0
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []     
        self.route_populated = False
        self.currentnode = 0

    def populate_network(self, filename):
        ''' iterates through a .txt filefilled with the network '''

        self.network_populated = False      # network starts off as unpopulated

        try:
            file = open(filename, "r")      # open the file for reading
        except IOError:     # catches an error if file does not exist
            print ("Network file does not exist")
            return      # early return if population fails
        for line in file:
            self.network.append(list(map(int, line.strip().split(','))))       # fills the network with comma seperated values using the split method

        self.network_populated = True       # network gets set to populated
        file.close

    def populate_node_table(self):
        ''' populate the node table with the values presented in the network '''

        self.nodetable = []     # clears node table so it can be repopulated
        self.nodetable_populated = False        # sets the node table to unpopulated

        if not self.network_populated:      # checks network has contents
            print ("Network is empty")
            return      # early return

        for node in self.network:       # for loop iterating through network
            self.nodetable.append(Node())           # populates node table with nodes in the network

        self.nodetable[self.startnode].distfromsource = 0       # start node set to have 0 for a distance
        self.nodetable[self.startnode].visited = True       # start node set to visited algorithm starts here
        self.nodetable_populated = True     # sets node table to populated


    def parse_route(self, filename):
        ''' Reads characters in the file and sets the start and end node to the correct values '''
        try:
            with open(filename, 'r') as line:       # opens file for reading
                path = line.readline()      # reads characters from the file stores into a list
                self.startnode = ord(path[0]) - 65      # set the start node to the int values using ASCII conversion
                self.endnode = ord(path[2]) - 65        # set the end node to the int values using ASCII conversion
                self.route_populated = True     # route is populated set true
                
        except IOError:     # try block to check if the file exists
            print ("Route file does not exist")
            self.route_populated = False        # route not populated set false

    def return_near_neighbour(self):
        ''' return all of the nodes with weight > 0 and unvisited and next to current node in the network '''

        nearestnodes = []      # holds nearest nodes
        for index, edge in enumerate(self.network[self.currentnode]):       # iterate through finding the current node in the network
            
            if edge > 0 and not self.nodetable[index].visited:      # check possible to visit
                nearestnodes.append(index)     # vallid node found will be added to list of available nodes
                
        return nearestnodes        # returns possible nodes connected to current node

    def calculate_tentative(self):
        ''' calculate distances for each of the nodes without marking as visited, determine the shortest distances in network '''

        nearest_neighbours = self.return_near_neighbour()       # use near neighbour meathod to find nodes to look at

        for neighboursindex in nearest_neighbours:      # iterates through nearest neighbours
            tentative_distance = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][neighboursindex]       # current tentative distance is sum of the current nodes distance from source
                                                                                                                                         #  and distance of neighbours to the current node
            if tentative_distance < self.nodetable[neighboursindex].distfromsource:      # if current tentative < one of the neighbours distances from source
                self.nodetable[neighboursindex].distfromsource = tentative_distance      # that distance will then be set to the tentative distance
                self.nodetable[neighboursindex].previous = self.currentnode     #connect its previous to the current node

    def determine_next_node(self):
        ''' determine next node that has shortest distance from source '''

        dist_compare = infinity     # set to infinity to start
        
        self.currentnode = invalid_node         # can't visit current node

        for index, node in enumerate(self.nodetable):       # iterates through node table looking at all the nodes distances from source

            if (node.distfromsource < dist_compare) and node.visited is False:      # if node has the shortest distance and is unvisited it will become next node
                dist_compare = node.distfromsource      # keep changing comparative until shortest distance has been found
                self.currentnode = index        # sets new current node to new found shortest distance node

    def calculate_shortest_path(self):
        ''' calculate the shortest path from the start node '''

        self.populate_node_table()      # populates the node table using populate function
        
        self.currentnode = self.startnode       # sets the current node to starting node

        while self.currentnode is not self.endnode and self.currentnode is not invalid_node:    # while the current node is not at the end of the path and it is not an invalid node
            
            self.calculate_tentative()      # the tentative distance will be calculated through the network
            self.determine_next_node()      # and the next node will be determined for the path
            self.nodetable[self.currentnode].visited = True

    def return_shortest_path(self):
        ''' this method will be used to display the final shortest path of the network '''

        self.calculate_shortest_path()      # calculates the shortest path
        curnode = self.endnode      # initially starts a the end node to reverse back through the path
        while curnode is not self.startnode:        # will run until start node is reached (end of path)
            if curnode is invalid_node:     # if the current node is invalid node, an empty path and distance will be returned
                return self.route, 0
            self.route.append(chr(curnode + 65))        # appends the next node in the shortest path to a list
            curnode = self.nodetable[curnode].previous      # and cycles to the next previous node in the path

        self.route.append(chr(self.startnode + 65))     # adds the starting node to the end of the list
        self.route.reverse()    # reverses the list as the list will be in reverse because it started at the end node

        distance = self.nodetable[self.endnode].distfromsource      # the end nodes distance from source will be the overall path distance
        print(("Distance from source: " + str(distance)))
        return self.route, distance     # returns the required values

class MaxFlow(Dijkstra):    # Max flow class inherits from Dijkstra class so it can use their methods
    def __init__(self): # initialise dijkstra
        '''initialise class'''
        Dijkstra.__init__(self)     # constructor class
        self.original_network = []      # holds a copy of the network

    def populate_network(self, filename):
        ''' populate the network list from "network.txt" '''

        Dijkstra.populate_network(self, filename)   # uses the Dijkstras populate network method
        self.original_network = [newlist[:] for newlist in self.network]    # uses slice operation to create a copy of the original network

    def return_near_neighbour(self):
        ''' return the next neighbour in the network '''

        nearnodes = [] # holds near nodes
        
        for index, edge in enumerate(self.network[self.currentnode]):       # iterate through the current node in the network
            if edge > 0 and not self.nodetable[index].visited:      # checks possible to visit and it hasn't been visited yet
                nearnodes.append(index)     # valid node found will be added to list of available nodes
        return nearnodes        # returns possible nodes connected to current node

    def return_the_bottleneck_flow(self):
        ''' cycle through the shortest path presented to find the bottleneck value in the path '''

        bottleneck = 0  # initially the bottleneck is set to 0
        
        for index, node in enumerate(self.route):   # for loop to iterate through the shortest path
            if (index + 1) != len(self.route):    # if end of path
                if bottleneck == 0: # set the bottleneck to infinity if it is a new path (allows initial bottleneck to be set)
                    bottleneck = infinity
                    
                cur_node_path = (ord(self.route[index]) - 65) # assigns the current node to a variable
                next_node_path = (ord(self.route[index + 1]) - 65)    # assigns the next node to a variable
                flow = self.network[cur_node_path][next_node_path]  # assigns the current bottlenecks in the network to flow

                if flow < bottleneck:   # if capacity is less than the bottleneck (see if it can fit through the pipe)
                    bottleneck = flow   # if so sets the new bottleneck
        return bottleneck # returns overall final bottleneck

    def remove_the_flow_capacity(self):
        '''remove flow from network and return both the path and the amount removed'''

        bottleneck = self.return_the_bottleneck_flow()      # set bottleneck from previouse method
        flows = ""
        if bottleneck > 0:
            print(("Current Path: " + str(self.route)))

        for index, node in enumerate(self.route):       # enumerates through the shortest path in the network
            if index + 1 != len(self.route):        # checks if the position is at the end of the path
                cur_node_path = (ord(self.route[index]) - 65)       # assigns current node in the path to a variable
                next_node_path = (ord(self.route[index + 1]) - 65)      # assigns next node in the path to a variable
                flows += str(self.route[index]) + " --> " + str(self.route[index + 1]) + " Original Flow: (" + str(
                    self.network[cur_node_path][next_node_path]) + "), New Flow: ("    # string is used to print the current flow
                self.network[cur_node_path][next_node_path] -= bottleneck       # takes bottleneck off of networks available capacity for the node
                self.network[next_node_path][cur_node_path] += bottleneck       # puts bottleneck in the opposite direction to allow reverse flow
                flows += str(self.network[cur_node_path][next_node_path]) + ") \n"      # updates flow string
        print(("Path Bottleneck: " + str(bottleneck)))      # prints bottleneck
        print (flows)       # prints flows
        return self.route, bottleneck       # return route and bottleneck

    def return_the_max_flow(self):
        ''' determine the max flow of the network by running the various methods to calculate it and print the max flow of the entire network '''
        distance = infinity         # set to infinity for comparison
        maxflow = 0         # set to 0 because we have yet to start finding max flow

        while distance != 0:    # while there is a path to visit
            route, distance = Dijkstra.return_shortest_path(self)   # find the current shortest path using dijkstra method
            path, bottleneck = self.remove_the_flow_capacity()      # finds bottleneck of that path
            maxflow += bottleneck       # add current flow to max flow and determine overall max flow

            print(("Currnet maxflow: ", maxflow))       # print maxflow

            for index in range(0, len(self.nodetable)): # for loop iterastes through node table to reset all of the nodes to their initial states
                self.nodetable[index].visited = False       # initial state
                self.nodetable[index].distfromsource = infinity         # initial state
                self.nodetable[index].previous = invalid_node       # initial state
            self.nodetable[self.startnode].distfromsource = 0       # It does the same for the start node
            self.nodetable[self.startnode].visited = True       # initial state
            self.route = [] # and then clears the current path 

        print(("Max Flow: ", maxflow))      # prints the final max flow
        return maxflow      # and returns it

if __name__ == '__main__':
    ''' to change the network and route change the name of the textfiles being passed'''
    
    ''' MAX FLOW '''
    maxFlow = MaxFlow()
    maxFlow.populate_network("network.txt")
    maxFlow.parse_route("route.txt")
    maxFlow.return_the_max_flow()
    ''' DIJKSTRA '''
    dijkstra = Dijkstra()
    dijkstra.populate_network("network.txt")
    dijkstra.parse_route("route.txt")
    print("The shortest path found using Dijkstra is: " + str(dijkstra.return_shortest_path()))
    

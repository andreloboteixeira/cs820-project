"""
Description
-----------

1. This program stores in a networkx graph the information imported from a .txt file created by the generator. The file name is passed using the paramenter 'input-dot-graph'.

2. The truck load capacity should be informed, as well as the initial conditions: 

'truck-cap-max': an integer which represents the truck load capacity
'truck-initial-load': an integer with the number of goods already in the truck
'truck-start-node': an integer which is the node id where the truck starts 

3. The algorithm proposed tries to return a path in the graph which represents the sequence of nodes the truck visited. 

The algorithm seeks to decide if the truck either goes to a warehouse or a store. 

This decision is based on a threshold(load-threshold-factor) for the current truck load. If it is above the threshold, the decision is to go to the store with the COSTLESS path and which still have demand.

On the other hand, if the current truck load is bellow the threshold, the decision is to go to the warehouse with the COSTLESS path and which still have goods to supply.


# Example to run:

>>> python run_truck_path_search --name goto_warehouse_or_store --input_dot_graph graph --truck_cap_max 6 --truck-start-node 0 --truck-initial-load 0 --load-threshold-factor 0.5

"""

import networkx as nx
from graph import import_graph_from, get_stores, get_warehouses
from utilities import TicTac

import copy 

import datetime
import argparse

INF = 9999999999999999999

# # Execution arguments
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str,
                    help="A name for the experiment.")

# Input Graph from .txt file
parser.add_argument('--input_dot_graph', type=str,
                    help="The .txt file in dot format containig the graph.")

# --- Specific problem parameters
parser.add_argument('--truck_cap_max', type=int, default=1,
                    help="truck load max capacity.")

# --- Initial state parameters
parser.add_argument('--truck-start-node', type=int,
                    help="Truck start node.")                    
parser.add_argument('--truck-initial-load', type=int, default=0,
                    help="Truck initial load.")

# --- Algorithms parameters
parser.add_argument('--load-threshold-factor', type=float, default=0.5,
                    help="For the greedy algorithm which decides to either go to a warehouse or a store, the load threshold factor.")           
args = parser.parse_args()
_exp_name = args.name
_truck_cap_max = args.truck_cap_max
_load_threshold_factor = args.load_threshold_factor
_truck_initial_load = args.truck_initial_load
_truck_start_node = args.truck_start_node
_input_dot_graph = args.input_dot_graph
_load_threshold = _load_threshold_factor* _truck_cap_max

# EXPERIMENT SETUP
timers = TicTac()
# Start global timer
timers.tic()

graph = nx.Graph()

# --- Import graph from text file created by the generator
import_graph_from(graph=graph, path="../graph-generator/{}.txt".format(_input_dot_graph))

# Logging the algorithm 
save_path_algo = open("{:%Y_%m_%d__%H_%M}_alg_log.txt".format(datetime.datetime.now()),"w+")

# START
truck_curr_node = _truck_start_node
truck_curr_load = _truck_initial_load

list_paths = []
_, store_demand_list = get_stores(graph)
while sum(store_demand_list) != 0:
    path_to_go = []

    # go to the costless warehouse
    if truck_curr_load < _load_threshold:
        save_path_algo.write("The load is bellow the threshold: GOTO A WAREHOUSE >>>>\n")
        
        warehouses_ids_list, warehouses_supplies_list = get_warehouses(graph)
        
        save_path_algo.write("Searching the costless warehouse >>>\n")
        costless_warehouse_id = None
        costless_warehouse_cost = INF
        for curr_id in range(len(warehouses_ids_list)):
            warehouse_id = warehouses_ids_list[curr_id]
            warehouse_supply = warehouses_supplies_list[curr_id]
            # print(warehouse_id, " ", warehouse_supply)
            
            if warehouse_supply > 0:
        
                save_path_algo.write("--- current W id: {}\n".format(warehouse_id))
                curr_path = nx.shortest_path(graph,source=truck_curr_node,target=warehouse_id, weight="cost")
                save_path_algo.write("--- path to current W: {}\n".format(curr_path))
                curr_path_length = nx.shortest_path_length(graph,source=truck_curr_node,target=warehouse_id, weight="cost")
                save_path_algo.write("--- path cost: {}\n".format(curr_path_length))
                if curr_path_length < costless_warehouse_cost:
                    costless_warehouse_cost = curr_path_length
                    costless_warehouse_id = warehouse_id
                    path_to_go = curr_path
                save_path_algo.write("--- GOTO: costless warehouse to go: {}\n".format(costless_warehouse_id))
        
        # update suply of the store
        if not costless_warehouse_id == None:
            # @TODO: update the supply
            # Try to load the truck at its maximum capacity
            graph.nodes[costless_warehouse_id]["supply"] = 0
            truck_curr_load = 6
            truck_curr_node = costless_warehouse_id
            
    # go to the costless store
    elif truck_curr_load >= _load_threshold:
        save_path_algo.write("The load is above the threshold: GOTO A STORE >>>>\n")

        store_ids_list, store_demand_list = get_stores(graph)
        
        save_path_algo.write("Searching the costless store >>>\n")
        costless_store_id = None
        costless_store_cost = INF
        for curr_id in range(len(store_ids_list)):
            store_id = store_ids_list[curr_id]
            store_demand = store_demand_list[curr_id]
            # save_path_algo.write(store_id, " ", store_demand)
            
            # the store demand should be > 0
            if store_demand > 0:

                save_path_algo.write("--- current S id: {}\n".format(store_id))
                curr_path = nx.shortest_path(graph,source=truck_curr_node,target=store_id, weight="cost")
                save_path_algo.write("--- path to current S: {}\n".format(curr_path))
                curr_path_length = nx.shortest_path_length(graph,source=truck_curr_node,target=store_id, weight="cost")
                save_path_algo.write("--- path cost: {}\n".format(curr_path_length))
                if curr_path_length < costless_store_cost:
                    costless_store_cost = curr_path_length
                    costless_store_id = store_id
                    path_to_go = curr_path
                    
                save_path_algo.write("--- GOTO: costless store to go: {}\n".format(costless_store_id))


        # update demand of the store
        if not costless_store_id == None:
            # @TODO: update the demand
            graph.nodes[costless_store_id]["demand"] = 0
            truck_curr_load = 0
            truck_curr_node = costless_store_id

    # if a path from current node to a next one was found
    if path_to_go:
        list_paths.append(path_to_go)
    
    # get stores demand list to check if there is still demand
    _, store_demand_list = get_stores(graph)

exp_total_time = timers.tac()
save_path_algo.write("\nTotal time of the experiment:{}\n\n".format(exp_total_time))
save_path_algo.write("\nTruck started at node ({}) with initial load of ({}), and capacity of ({})\n".format(_truck_start_node,_truck_initial_load, _truck_cap_max))
save_path_algo.write("\nThe algorithm used a threshold factor of ({})\n".format(_load_threshold_factor))

save_path_algo.write("\nThe imported graph file name is '{}'\n".format(_input_dot_graph))
save_path_algo.write("\nThe list of paths is '{}'\n".format(_input_dot_graph))
for path in list_paths:
    save_path_algo.write(str(path) + "\n")

# Closing file to log the algorithm
save_path_algo.close()


# --- Result path >>>>>>>>>>>>>>>
print("\n\nTruck path: \n{}\n\n".format(list_paths))
print("Experiment time: {} s".format(exp_total_time))

# --- Save path to .txt file
save_folder = "{:%Y_%m_%d__%H_%M}_{}.txt".format(datetime.datetime.now(), _exp_name)
save_path_found = open(save_folder,"w+")
print("Path saved to text file: ", save_folder)

save_path_found.write("Truck started at no: " + str(_truck_start_node) + "\n")
for path in list_paths:
    save_path_found.write(str(path) + "\n")
save_path_found.close()

# --- Save .dot file with truck path
node_counter = 0
graph_to_save = copy.copy(graph)
for path in list_paths:
    for node_id in path:
        graph_to_save.nodes[node_id]["label"] += "{}, ".format(node_counter)
        node_counter+=1

nx.drawing.nx_pydot.write_dot(graph_to_save, "{}.dot".format(save_folder.replace(".txt","")))
print("Generated graph .dot file with the sequence of nodes the truck should go: \n {}".format(save_folder))
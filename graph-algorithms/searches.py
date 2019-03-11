import networkx as nx
from graph import *
import copy 

INF = 9999999999999999999

def heuristics_():
    pass

if __name__ == "__main__":
    graph = nx.Graph()

    import_graph_from(graph=graph, path="../graph-generator/graph1.txt")
    
    # write_graph(graph)

    # user input
    # truck_cap = input(">>> input truck capacity: ")
    truck_cap = 6
    
    # load_threshold = input(">>> input load threshold: ")
    load_threshold = (truck_cap/2)
    
    # truck_cap = input(">>> input truck starting load: ")
    truck_load = 0

    # truck_cap = input(">>> input the starting node: ")
    start_node = 0


    # START
    curr_node = start_node
    list_paths = []

    _, store_demand_list = get_stores(graph)
    while sum(store_demand_list) != 0:
        path_to_go = []

        # go to the costless warehouse
        if truck_load < load_threshold:
            print("GOTO WAREHOUSE >>>>")
            
            warehouses_ids_list, warehouses_supplies_list = get_warehouses(graph)
            
            costless_warehouse_id = None
            costless_warehouse_cost = INF
            for curr_id in range(len(warehouses_ids_list)):
                warehouse_id = warehouses_ids_list[curr_id]
                warehouse_supply = warehouses_supplies_list[curr_id]
                # print(warehouse_id, " ", warehouse_supply)
                
                # the store demand should be > 0
                if warehouse_supply > 0:
            
                    print("W id: ", warehouse_id)
                    curr_path = nx.shortest_path(graph,source=curr_node,target=warehouse_id, weight="cost")
                    print("curr_path", curr_path)
                    curr_path_length = nx.shortest_path_length(graph,source=curr_node,target=warehouse_id, weight="cost")
                    print("curr length: ", curr_path_length)
                    if curr_path_length < costless_warehouse_cost:
                        costless_warehouse_cost = curr_path_length
                        costless_warehouse_id = warehouse_id
                        path_to_go = curr_path
                print("costless warehouse to go: ", costless_warehouse_id)
            
            # update suply of the store
            if not costless_warehouse_id == None:
                # @TODO: update the supply
                graph.nodes[costless_warehouse_id]["supply"] = 0
                truck_load = 6
                curr_node = costless_warehouse_id
                
        # go to the costless store
        elif truck_load >= load_threshold:
            print("GOTO STORE >>>>")

            store_ids_list, store_demand_list = get_stores(graph)
            
            costless_store_id = None
            costless_store_cost = INF
            for curr_id in range(len(store_ids_list)):
                store_id = store_ids_list[curr_id]
                store_demand = store_demand_list[curr_id]
                # print(store_id, " ", store_demand)
                
                # the store demand should be > 0
                if store_demand > 0:

                    print("S id: ", store_id)
                    curr_path = nx.shortest_path(graph,source=curr_node,target=store_id, weight="cost")
                    print("curr_path", curr_path)
                    curr_path_length = nx.shortest_path_length(graph,source=curr_node,target=store_id, weight="cost")
                    print("curr length: ", curr_path_length)
                    if curr_path_length < costless_store_cost:
                        costless_store_cost = curr_path_length
                        costless_store_id = store_id
                        path_to_go = curr_path
                        
                    print("costless store to go: ", costless_store_id)

            # update demand of the store
            if not costless_store_id == None:
                # @TODO: update the demand
                graph.nodes[costless_store_id]["demand"] = 0
                truck_load = 0
                curr_node = costless_store_id

        # if a path from current node to a next one was found
        if path_to_go:
            list_paths.append(path_to_go)
        
        # get stores demand list to check if there is still demand
        _, store_demand_list = get_stores(graph)
    

    print("Truck path: ")
    print(list_paths)
    
    
    print("Saving to text file >>> ")
    save_path_found = open("path.txt","w+")
    
    save_path_found.write("Truck started at: " + str(start_node) + "\n")
    for path in list_paths:
        save_path_found.write(str(path) + "\n")
    
    save_path_found.close()
    # raise Exception

    # print("truck path: ")
    # graph_to_save = copy.copy(graph)
    # for path in list_paths:
    #     print(path)
    #     for node_id in path:
    #         print(graph.nodes[node_id]["label"])
    #         print(graph.nodes[node_id]["label"])

    # nx.drawing.nx_pydot.write_dot(graph, "g.dot")
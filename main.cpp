#include <vector>
#include <string>
#include <time.h>
#include <iostream>
#include <fstream>
#include <random>


using namespace std;

// seed the PRNG
random_device rd;
mt19937 mt(rd());
uniform_real_distribution<double> dist(0.0, RAND_MAX);

// a custom function to generate pseudorandom floats between MIN and MAX
// note: this can be easily type-casted like "(int)rnd_num(x,y)" to integers with float part truncated
float rnd_num(float MIN, float MAX){
	return MIN + (float)(dist(mt)) /( (float) (RAND_MAX/(MAX - MIN))); // pseurandom enough to work, lol
}

// function to do a flip of the coin - yes or no? - one or zero will know
bool coinflip(){
	if (rnd_num(0.0,1.0) > 0.5) {
		return true;
	} else {
		return false;
	}
}

// movement graph data structures
struct edge { 
int dest_id; // edge destination node id
int distance; // distance to travel
int time; // time to spend on travel
};

struct node {
int id;
int type; // 0 - joint; 1 - store; 2 - warehouse
vector<edge> edges; // storage for edges of the node
bool hasSpreadEdges; // flag to check if the node yet tried to edges
};

vector<node> nodes;

int main() {
	cout << "Shipping roadmap graph generator v0.1a by Mikhail Shchukin." << endl;

	cout << "Please enter the number of nodes to generate: " ;
	int max_nodes;
	cin >> max_nodes;

	if (max_nodes < 2) { // quick check if the user is a complete retard
		cout << "Hey, you will then have a useless graph with no edges. You're fucked up!" << endl;
		return 1; // stop the program and go cry		
	}

	cout << "Please enter the maximum number of edges per node: " ;
	int max_edges_per_node;
	cin >> max_edges_per_node;

	if (max_edges_per_node < 1) { // quick check if the user is a complete retard who doesn't know about graph theory
		cout << "Hey, you will then have no edges at all. You're fucked up!" << endl;
		return 1; // stop the program and go cry		
	}

	if (max_edges_per_node > max_nodes - 1) { // quick check if the user is a complete retard who doesn't know about graph theory
		cout << "Hey, you will then have too many edges. You're fucked up!" << endl;
		return 1; // stop the program and go cry		
	}

	cout << "How many stores would you like to have on the map?: " ;
	int max_stores;
	cin >> max_stores;

	if (max_stores < 1) { // quick check if the user is a complete retard
		cout << "Hey, will then have no stores at all. You're fucked up!" << endl;
		return 1; // stop the program and go cry		
	}

	cout << "How many warehouses would you like to have on the map?: " ;
	int max_warehouses;
	cin >> max_warehouses;

	if (max_warehouses < 1) { // quick check if the user is a complete retard
		cout << "Hey, will then have no warehouses at all. You're fucked up!" << endl;
		return 1; // stop the program and go cry		
	}

	if (max_stores + max_warehouses > max_nodes) { // quick check if the user is a complete retard who cannot count
		cout << "Hey, you want more warehouses/stores than the number of nodes to be generated. You're fucked up!" << endl;
		return 1; // stop the program and go cry
	}
	cout << "Okay, I am going to generate the shipping roadmap graph now. Hold on tight." << endl;

	// create the requested number of nodes
	for (int i=0; i<max_nodes; i++){
		node n; //dummy node for reusage in loop
		n.id = i; // assign node id
		n.type = 0; // during initial placement - all nodes are type 0, joints. may be converted into stores/warehouses later
		n.hasSpreadEdges = false; // all new-born nodes will have to produce edges
		nodes.push_back(n); // load the created node into the global storage
	}

	// now turn random joint nodes into stores and warehouses
	// create stores
	for (int i=0; i<max_stores; i++){
		int replacement_node_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id
		int dummy = 0;
		do {
			replacement_node_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id again
		} while (nodes[replacement_node_id].type > 0); // re-roll the loop if a non-joint node was selected for replacement
		nodes[replacement_node_id].type = 1; // replace this joint with a store
	}
	// create warehouses
	for (int i=0; i<max_warehouses; i++){
		int replacement_node_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id
		int dummy = 0;
		do {
			replacement_node_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id again
		} while (nodes[replacement_node_id].type > 0); // re-roll the loop if a non-joint node was selected for replacement
		nodes[replacement_node_id].type = 2; // replace this joint with a warehouse
	}

	// once the nodes have been created, let's create the edges between them
	// ACHTUNG - THIS AREA WILL BE UNDER ACTIVE DEVELOPMENT - EXPECT FUCKED-UP RESULTS STARTING FROM HERE
	for (unsigned int i=0; i<nodes.size(); i++){
		for (int e=0; e<max_edges_per_node; e++){
			if (coinflip()) {
				edge e; //dummy edge for reusage in loop
				// pick the destination node
				while (true) {
					e.dest_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id
					if (e.dest_id != i){ // for any edge: destination != source
						break;
					}
				} // re-roll the loop if edge source and destination nodes are the same
				// generate edge distance
				// TODO: make these distances real and somewhat related to time - consider the velocity of the truck maybe?
				e.distance = (int)rnd_num(1.0,200.0);
				// generate edge time
				// TODO: make these times reasonable - consider minutes, hours?
				e.time = (int)rnd_num(30.0,120.0); // for now - let it be minutes of transition
				nodes[i].edges.push_back(e); // record the edge to the node
			}
		}
		if (nodes[i].edges.size() == 0) { // if the loop above generated no edges - just generate at least one to keep graph connected
			edge e; //dummy edge for reusage in loop
			// pick the destination node
			while (true) {
				e.dest_id = (int)rnd_num(0.0,(float)nodes.size()); // pick any node id
				if (e.dest_id != i){ // for any edge: destination != source
					break;
				}
			} // re-roll the loop if edge source and destination nodes are the same
			// generate edge distance
			// TODO: make these distances real and somewhat related to time - consider the velocity of the truck maybe?
			e.distance = (int)rnd_num(1.0,200.0);
			// generate edge time
			// TODO: make these times reasonable - consider minutes, hours?
			e.time = (int)rnd_num(30.0,120.0); // for now - let it be minutes of transition
			nodes[i].edges.push_back(e); // record the edge to the node
		}
		nodes[i].hasSpreadEdges = true; // this node has produced nodes, toggle the flag
	}

	// display the results
	// TODO: write results to text file while displaying them in the same loop.
	cout << "The shipping roadmap graph has been constructed. Details follow below." << endl;
	for (unsigned int i=0; i<nodes.size(); i++){
		cout << "Node [" << nodes[i].id << "]";
		switch(nodes[i].type){
		case 0:
			cout << " is a JOINT" << endl;
			break;
		case 1:
			cout << " is a STORE" << endl;
			break;
		case 2:
			cout << " is a WAREHOUSE" << endl;
			break;
		}
		for (unsigned int k=0; k<nodes[i].edges.size(); k++){
			cout << "> Edge between nodes [" << nodes[i].id << "] and [" << nodes[i].edges[k].dest_id << "]" << endl;
			cout << ">> Distance: " << nodes[i].edges[k].distance << "; Time to traverse: " << nodes[i].edges[k].time << endl;
		}
	}


}

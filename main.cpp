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

// generates pseudorandom floats between MIN and MAX
float rnd_num(float MIN, float MAX){
	return MIN + (float)(dist(mt)) /( (float) (RAND_MAX/(MAX - MIN))); // pseurandom enough to work, lol
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
vector<edge> edges;
};

vector<node> nodes;

int main() {
	cout << rnd_num(5.0, 123.0) << endl;
	cout << "Shipping roadmap graph generator v0.1a by Mikhail Shchukin." << endl;
	cout << "Please enter the maximum number of nodes to generate:" ;
	int max_nodes;
	cin >> max_nodes;
	cout << "Please enter the maximum number of edges per node:" ;
	int max_edges_per_node;
	cin >> max_edges_per_node;
}

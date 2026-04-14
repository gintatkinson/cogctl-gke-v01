/*
 * Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef _PATHCOMP_TOOLS_H
#define _PATHCOMP_TOOLS_H

#include <glib.h>
#include <glib/gstdio.h>
#include <glib-2.0/glib/gtypes.h>
#include <uuid/uuid.h>

// External variables
extern GList* contextSet;
extern GList* linkList;
extern GList* deviceList;
extern GList* serviceList;
extern GList* activeServList;

//////////////////////////////////////////////////////////
// Optimization computation argument 
//////////////////////////////////////////////////////////
#define NO_OPTIMIZATION_ARGUMENT		0x00000000
#define ENERGY_EFFICIENT_ARGUMENT		0x00000001

#define INFINITY_COST                   0xFFFFFFFF
#define MAX_NUM_PRED					100

#define MAX_KSP_VALUE					5

// HTTP RETURN CODES
#define HTTP_CODE_OK					200
#define HTTP_CODE_CREATED 				201
#define HTTP_CODE_BAD_REQUEST    		400
#define HTTP_CODE_UNAUTHORIZED   		401
#define HTTP_CODE_FORBIDDEN      		403
#define HTTP_CODE_NOT_FOUND				404
#define HTTP_CODE_NOT_ACCEPTABLE		406

#define MAX_NODE_ID_SIZE				37 // UUID 128 Bits - In hexadecimal requires 36 char
#define MAX_CONTEXT_ID					37
//#define UUID_CHAR_LENGTH				37
#define UUID_CHAR_LENGTH				100
struct nodes_t {
	gchar nodeId[UUID_CHAR_LENGTH];
};

struct nodeItem_t {
    struct nodes_t node;
    gdouble distance; // traversed distance
	gdouble latency; // incured latency
	gdouble power; //consumed power
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Structures for collecting the RL topology including: intra WAN topology and inter-WAN links
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
#define MAX_INTER_DOMAIN_PLUG_IN_SIZE					128
struct edges_t {	
	//aNodeId/Device Id
	struct nodes_t aNodeId;	
	//zNodeId/Device Id
	struct nodes_t zNodeId;	
	
	// UUID of the endPointIds
	gchar aEndPointId[UUID_CHAR_LENGTH];
	gchar zEndPointId[UUID_CHAR_LENGTH];

	// UUID of the link
	gchar linkId[UUID_CHAR_LENGTH];

	// Potential(total) and available capacity
	gint unit;
	gdouble totalCap, availCap;
	
	gdouble cost;	
	gdouble delay;
	gdouble energy;

	// inter-domain local and remote Ids
	gchar interDomain_localId[MAX_INTER_DOMAIN_PLUG_IN_SIZE];
	gchar interDomain_remoteId[MAX_INTER_DOMAIN_PLUG_IN_SIZE];

	gchar aTopologyId[UUID_CHAR_LENGTH];
	gchar zTopologyId[UUID_CHAR_LENGTH];
};

// Structure to handle the path computation
struct pred_comp_t {
	struct nodes_t v;
	struct edges_t e;	
};

struct pred_t {
    struct pred_comp_t predComp[MAX_NUM_PRED];
    gint numPredComp;
};

// Structures for the managing the path computation algorithm
struct map_t {
	struct nodes_t verticeId;
	struct edges_t predecessor;
	gdouble distance;
	gdouble avaiBandwidth;
	gdouble latency;
	gdouble power;
};

#define MAX_MAP_NODE_SIZE				100
struct map_nodes_t {
    struct map_t map[MAX_MAP_NODE_SIZE];
    gint numMapNodes;
};

#define MAX_NUM_VERTICES				100 // 100 # LGR: reduced from 100 to 20 to divide by 5 the memory used
#define MAX_NUM_EDGES					5 // 100 # LGR: reduced from 100 to 5 to divide by 20 the memory used

// Structures for the graph composition
struct targetNodes_t {
	// remote / targeted node
	struct nodes_t tVertice;
	// edge conencting a pair of vertices
	struct edges_t edges[MAX_NUM_EDGES];	
	gint numEdges; 
};

struct vertices_t {
	struct targetNodes_t targetedVertices[MAX_NUM_VERTICES];
	gint numTargetedVertices;
    struct nodes_t verticeId;
	gdouble power_idle; // power idle of the device (due to the fans, etc.)
};

struct graph_t {
	struct vertices_t vertices[MAX_NUM_VERTICES];
	gint numVertices;	
};

////////////////////////////////////////////////////
// Structure for the Set of Contexts
///////////////////////////////////////////////////
struct context_t {
	gchar contextId[UUID_CHAR_LENGTH]; // UUID char format 36 chars
	// conext Id has a graph associated
	struct graph_t g;
};

#define MAX_ALG_ID_LENGTH		10
////////////////////////////////////////////////////
// External Variables
///////////////////////////////////////////////////
extern gchar algId[MAX_ALG_ID_LENGTH];

////////////////////////////////////////////////////
// Structure for the Requested Transport Connectivity Services
///////////////////////////////////////////////////
#define SERVICE_TYPE_UNKNOWN			0
#define SERVICE_TYPE_L3NM				1
#define SERVICE_TYPE_L2NM				2
#define SERVICE_TYPE_TAPI				3

///////////////////////////////////////////////////////////////////
// Structure for the topology_id
///////////////////////////////////////////////////////////////////
struct topology_id_t {
	gchar contextId[UUID_CHAR_LENGTH];
	gchar topology_uuid[UUID_CHAR_LENGTH];
};

struct inter_domain_plug_in_t {
	gchar inter_domain_plug_in_local_id[MAX_INTER_DOMAIN_PLUG_IN_SIZE];
	gchar inter_domain_plug_in_remote_id[MAX_INTER_DOMAIN_PLUG_IN_SIZE];
};

///////////////////////////////////////////////////////////////////
// Structure for the endPointId
///////////////////////////////////////////////////////////////////
struct endPointId_t {
	struct topology_id_t topology_id;
	gchar device_id[UUID_CHAR_LENGTH];
	gchar endpoint_uuid[UUID_CHAR_LENGTH];
};

///////////////////////////////////////////////////////////////////
// Structure for the endPoint
///////////////////////////////////////////////////////////////////
#define CAPACITY_UNIT_TB									0
#define CAPACITY_UNIT_TBPS									1
#define CAPACITY_UNIT_GB									2
#define CAPACITY_UNIT_GBPS									3
#define CAPACITY_UNIT_MB									4
#define CAPACITY_UNIT_MBPS									5
#define CAPACITY_UNIT_KB									6
#define CAPACITY_UNIT_KBPS									7
#define CAPACITY_UNIT_GHZ									8
#define CAPACITY_UNIT_MHZ									9
struct capacity_t {
	gdouble value;
	gint unit;
};

///////////////////////////////////////////////////////////////////
// Structure for the endPoint
///////////////////////////////////////////////////////////////////
#define MAX_ENDPOINT_TYPE_SIZE								128
// Link Port Direction
#define LINK_PORT_DIRECTION_BIDIRECTIONAL					0
#define LINK_PORT_DIRECTION_INPUT							1
#define LINK_PORT_DIRECTION_OUTPUT							2
#define LINK_PORT_DIRECTION_UNKNOWN							3
// Termination Direction
#define TERMINATION_DIRECTION_BIDIRECTIONAL					0
#define TERMINATION_DIRECTION_SINK							1
#define TERMINATION_DIRECTION_SOURCE						2
#define TERMINATION_DIRECTION_UNKNOWN						3
// Termination State
#define TERMINATION_STATE_CAN_NEVER_TERMINATE				0
#define TERMINATION_STATE_NOT_TERMINATED					1
#define TERMINATION_STATE_TERMINATED_SERVER_TO_CLIENT_FLOW	2
#define TERMINATION_STATE_TERMINATED_CLIENT_TO_SERVER_FLOW	3
#define TERMINATION_STATE_TERMINATED_BIDIRECTIONAL			4

struct endPoint_t {
	struct endPointId_t endPointId;
	gchar endpointType[MAX_ENDPOINT_TYPE_SIZE];
	guint link_port_direction;
	guint termination_direction;
	guint termination_state;
	struct capacity_t potential_capacity;
	struct capacity_t available_capacity;
	// inter-domain identifiers
	struct inter_domain_plug_in_t inter_domain_plug_in;
	gfloat energyConsumption; // in nJ/bit
	gint operational_status; // 0 Undefined, 1 Disabled, 2 Enabled
};

///////////////////////////////////////////////////////////////////
// Structure for the device contents
///////////////////////////////////////////////////////////////////
#define MAX_DEV_TYPE_SIZE				128
#define MAX_DEV_ENDPOINT_LENGTH			100	// 10 # LGR: controllers might have large number of endpoints
struct device_t {
	gdouble power_idle; // power idle (baseline) of the switch in Watts
	gint operational_status; // 0 - Undefined, 1 - Disabled, 2 - Enabled
	gchar deviceId[UUID_CHAR_LENGTH]; // device ID using UUID (128 bits)
	gchar deviceType[MAX_DEV_TYPE_SIZE]; // Specifies the device type
	// define the endpoints attached to the device
	gint numEndPoints;
	struct endPoint_t endPoints[MAX_DEV_ENDPOINT_LENGTH];
};

///////////////////////////////////////////////////////////////////
// Structure for the link EndPoint Id
///////////////////////////////////////////////////////////////////
struct link_endpointId_t {
	struct topology_id_t topology_id;
	gchar deviceId[UUID_CHAR_LENGTH];  // Device UUID
	gchar endPointId[UUID_CHAR_LENGTH];	// Link EndPoint UUID
};

///////////////////////////////////////////////////////////////////
// Structure for the link cost characteristics
///////////////////////////////////////////////////////////////////
#define LINK_COST_NAME_SIZE								128
struct cost_characteristics_t {
	gchar cost_name[LINK_COST_NAME_SIZE];
	gdouble cost_value;
	gdouble cost_algorithm;
};

///////////////////////////////////////////////////////////////////
// Structure for the latency characteristics of the link
///////////////////////////////////////////////////////////////////
struct latency_characteristics_t {
	gdouble fixed_latency;
};

///////////////////////////////////////////////////////////////////
// Structure for the latency characteristics of the link
///////////////////////////////////////////////////////////////////
struct power_characteristics_t {
	gdouble power;
};

///////////////////////////////////////////////////////////////////
// Structure for the link 
///////////////////////////////////////////////////////////////////
#define MAX_NUM_LINK_ENDPOINT_IDS								2

#define LINK_FORWARDING_DIRECTION_BIDIRECTIONAL					0
#define LINK_FORWARDING_DIRECTION_UNIDIRECTIONAL				1
#define LINK_FORWARDING_DIRECTION_UNKNOWN						2
struct link_t {
	gchar linkId[UUID_CHAR_LENGTH]; // link Id using UUID (128 bits)
	//gdouble energy_link; // in nJ/bit
	//gint operational_status; // 0 Undefined, 1 Disabled, 2 Enabled
	gint numLinkEndPointIds;
	struct link_endpointId_t linkEndPointId[MAX_NUM_LINK_ENDPOINT_IDS];
	guint forwarding_direction;
	struct capacity_t potential_capacity;
	struct capacity_t available_capacity;
	struct cost_characteristics_t cost_characteristics;
	struct latency_characteristics_t latency_characteristics;
};

////////////////////////////////////////////////////
// Structure for service Identifier
///////////////////////////////////////////////////
struct serviceId_t {
	gchar contextId[UUID_CHAR_LENGTH];
	gchar service_uuid[UUID_CHAR_LENGTH];
};

////////////////////////////////////////////////////
// Structure the service endpoint ids
///////////////////////////////////////////////////
struct service_endpoints_id_t {
	struct topology_id_t topology_id;
	gchar device_uuid[UUID_CHAR_LENGTH];
	gchar endpoint_uuid[UUID_CHAR_LENGTH];
};

////////////////////////////////////////////////////
// Structure for handling generic targeted service constraints
////////////////////////////////////////////////////
#define MAX_CONSTRAINT_SIZE					128
// Constraint Type: bandwidth, latency, energy, cost
struct constraint_t {
	gchar constraint_type[MAX_CONSTRAINT_SIZE];
	gchar constraint_value[MAX_CONSTRAINT_SIZE];
};

////////////////////////////////////////////////////
// Structure for individual service request
////////////////////////////////////////////////////
#define SERVICE_TYPE_UNKNOWN					0
#define SERVICE_TYPE_L3NM						1
#define SERVICE_TYPE_L2NM						2
#define SERVICE_TYPE_TAPI						3

#define MAX_NUM_SERVICE_ENPOINTS_ID				2

#define MAX_NUM_SERVICE_CONSTRAINTS				10
struct service_t {	
	gchar algId[MAX_ALG_ID_LENGTH]; // Indentifier used to determine the used Algorithm Id, e.g., KSP	
	guint kPaths_inspected; // PATHS expected to be inspected
	guint kPaths_returned; // Maximum number of PATHS to be returned
	
	struct serviceId_t serviceId;
	guint service_type;	 // unknown, l2nm, l3nm, tapi

	// endpoints of the network connectivity service, assumed p2p
	// the 1st one assumed to be the source (ingress) and the 2nd one is the sink (egress)
	struct service_endpoints_id_t service_endpoints_id[MAX_NUM_SERVICE_ENPOINTS_ID];
	guint num_service_endpoints_id;

	// Service Constraints
	struct constraint_t constraints[MAX_NUM_SERVICE_CONSTRAINTS];
	guint num_service_constraints;
};

////////////////////////////////////////////////////
// Structure to handle path constraints during computation
////////////////////////////////////////////////////
struct path_constraints_t {
	gdouble bwConstraint;
	gboolean bw;

	gdouble costConstraint;
	gboolean cost;

	gdouble latencyConstraint;
	gboolean latency;

	gdouble energyConstraint;
	gboolean energy;
};

////////////////////////////////////////////////////
// Structure for the handling the service requests
///////////////////////////////////////////////////
//#define MAX_SERVICE_LIST						100
//struct serviceList_t {
//	struct service_t services[MAX_SERVICE_LIST];
//	gint numServiceList;	
//};

////////////////////////////////////////////////////
// Structure for the handling the active services 
///////////////////////////////////////////////////
struct activeServPath_t {
	struct topology_id_t topology_id;
	gchar deviceId[UUID_CHAR_LENGTH];
	gchar endPointId[UUID_CHAR_LENGTH];
};

struct activeService_t {
	struct serviceId_t serviceId;
	guint service_type;	 // unknown, l2nm, l3nm, tapi
	struct service_endpoints_id_t service_endpoints_id[MAX_NUM_SERVICE_ENPOINTS_ID];
	guint num_service_endpoints_id;
	GList* activeServPath;
};

////////////////////////////////////////////////////////////////////////////////////////////
// Structure describing the links forming a computed path
////////////////////////////////////////////////////////////////////////////////////////////
struct linkTopology_t {
	gchar topologyId[UUID_CHAR_LENGTH];
};

struct pathLink_t {
	gchar linkId[UUID_CHAR_LENGTH]; // link id UUID in char format

	gchar aDeviceId[UUID_CHAR_LENGTH];
	gchar zDeviceId[UUID_CHAR_LENGTH];
	gchar aEndPointId[UUID_CHAR_LENGTH];
	gchar zEndPointId[UUID_CHAR_LENGTH];

	struct topology_id_t topologyId;
	struct linkTopology_t linkTopologies[2]; // A p2p link (at most) can connect to devices (endpoints) attached to 2 different topologies
	gint numLinkTopologies;
};

////////////////////////////////////////////////////////////////////////////////////////////
// Structure describing a computed path
////////////////////////////////////////////////////////////////////////////////////////////
#define MAX_ROUTE_ELEMENTS  50
struct routeElement_t {
	//aNodeId/Device Id
	struct nodes_t aNodeId;
	//zNodeId/Device Id
	struct nodes_t zNodeId;

	// UUID of the endPointIds
	gchar aEndPointId[UUID_CHAR_LENGTH];
	gchar zEndPointId[UUID_CHAR_LENGTH];

	// UUID of the link
	gchar linkId[UUID_CHAR_LENGTH];

	gchar aTopologyId[UUID_CHAR_LENGTH];
	gchar zTopologyId[UUID_CHAR_LENGTH];

	// contextId
	gchar contextId[UUID_CHAR_LENGTH];
};

struct compRouteOutputItem_t {	
	gint unit;
	gdouble totalCap, availCap;

	gdouble cost;
	gdouble delay;
	gdouble power;

	struct routeElement_t routeElement[MAX_ROUTE_ELEMENTS];
	gint numRouteElements;
};

#define MAX_NUM_PATHS		30
struct path_set_t {
	struct compRouteOutputItem_t paths[MAX_NUM_PATHS];
	gint numPaths;
};

#define MAX_NUM_PATH_LINKS						20
struct path_t {
	struct capacity_t path_capacity;
	struct latency_characteristics_t path_latency;
	struct cost_characteristics_t path_cost;
	struct power_characteristics_t path_power;

	struct pathLink_t pathLinks[MAX_NUM_PATH_LINKS];
	guint numPathLinks;
};

#define NO_PATH_CONS_ISSUE								1	 // No path due to a constraint issue
#define MAX_NUM_COMPUTED_PATHS							10
struct compRouteOutput_t {
	// object describing the service identifier: serviceId and contextId
	struct serviceId_t serviceId;
	// array describing the service endpoints ids
	struct service_endpoints_id_t service_endpoints_id[MAX_NUM_SERVICE_ENPOINTS_ID];
	guint num_service_endpoints_id;
	struct path_t paths[MAX_NUM_COMPUTED_PATHS];
	gint numPaths;	
	// if the transport connectivity service cannot be computed, this value is set to 0 determining the constraints were not fulfilled
	gint noPathIssue;
};

////////////////////////////////////////////////////////////////////////////////////////////
// Structure to handle the response list with all the computed network connectivity services
////////////////////////////////////////////////////////////////////////////////////////////
#define MAX_COMP_CONN_LIST		100
struct compRouteOutputList_t {
	struct compRouteOutput_t compRouteConnection[MAX_COMP_CONN_LIST];
	gint numCompRouteConnList;

	///////////////// Metrics //////////////////////////////////////////
	// Number of total succesfully computed connections, i.e., at least 1 feasible path exists
	// for every connection in the list
	gint compRouteOK;
	// For the succesfully newly computed/recovered/re-allocated/re-optimized connections, this 
	// metric determines the average allocable bandwidth over all the (re-)computed paths for the succesfully 
	// (i.e., feasible path) connections
	gdouble compRouteConnAvBandwidth;
	// For the succesfully newly computed/recovered/re-allocated/re-optimized connections, this 
	// metric determines the average path length (in terms of number of hops) over the computed path for the
	// succesfully (i.e., feasible path) connections
	gdouble compRouteConnAvPathLength;
};

// Prototype of external declaration of functions
void print_path (struct compRouteOutputItem_t *);
void print_path_t(struct path_t*);
struct path_t* create_path();

void duplicate_string(gchar *, gchar *);

gchar* get_uuid_char(uuid_t);
void copy_service_id(struct serviceId_t*, struct serviceId_t *);
void copy_service_endpoint_id(struct service_endpoints_id_t *, struct service_endpoints_id_t *);

struct graph_t* get_graph_by_contextId(GList*, gchar *);

struct pred_t * create_predecessors ();
struct edges_t* create_edge();
void print_predecessors (struct pred_t *);
void build_predecessors (struct pred_t *, struct service_t *, struct map_nodes_t *);
struct nodes_t * create_node ();
struct routeElement_t * create_routeElement ();

void duplicate_node_id (struct nodes_t *, struct nodes_t *);
gint compare_node_id (struct nodes_t *, struct nodes_t *);
void duplicate_routeElement (struct routeElement_t *, struct routeElement_t *);
void duplicate_edge (struct edges_t *, struct edges_t *);
void duplicate_path (struct compRouteOutputItem_t *, struct compRouteOutputItem_t *);
void duplicate_path_t(struct compRouteOutputItem_t *, struct path_t *);
gint get_map_index_by_nodeId (gchar *, struct map_nodes_t *);
void get_edge_from_map_by_node (struct edges_t *, struct nodes_t*, struct map_nodes_t *);
void get_edge_from_predecessors (struct edges_t *, struct nodes_t*, struct pred_t *);
void build_path (struct compRouteOutputItem_t *, struct pred_t *, struct service_t *);
void print_graph (struct graph_t *);

gint graph_vertice_lookup (gchar *, struct graph_t *);
gint graph_targeted_vertice_lookup (gint, gchar *, struct graph_t *);
gint graph_targeted_vertice_add (gint, gchar *, struct graph_t *);

void remove_edge_from_graph (struct graph_t *, struct edges_t *);

struct path_set_t * create_path_set ();
void sort_path_set (struct path_set_t *, guint);
void pop_front_path_set (struct path_set_t *);
void remove_path_set(struct path_set_t*);

void build_map_node(struct map_nodes_t *, struct graph_t *);
struct compRouteOutputList_t * create_route_list();
void duplicate_route_list(struct compRouteOutputList_t *, struct compRouteOutputList_t *);
struct compRouteOutputItem_t * create_path_item (); 
void add_routeElement_path_back (struct routeElement_t *, struct compRouteOutputItem_t *);
gboolean matching_path_rootPath (struct compRouteOutputItem_t *, struct compRouteOutputItem_t *, struct nodes_t *, struct edges_t *);
void modify_targeted_graph (struct graph_t *, struct path_set_t *, struct compRouteOutputItem_t *, struct nodes_t *);
gint find_nodeId (gconstpointer, gconstpointer);
gint check_link (struct nodeItem_t *, gint, gint, struct graph_t *, struct service_t *, GList **, GList **, struct map_nodes_t *, guint arg);
gboolean check_computed_path_feasibility (struct service_t *, struct compRouteOutputItem_t * );

gint sort_by_distance (gconstpointer, gconstpointer);
gint sort_by_energy(gconstpointer, gconstpointer);

struct graph_t * create_graph ();
struct map_nodes_t * create_map_node ();

struct service_t * get_service_for_computed_path(gchar *);

void print_service_type(guint);
void print_link_port_direction(guint);
void print_termination_direction(guint);
void print_termination_state(guint);
void print_capacity_unit(guint);
void print_link_forwarding_direction(guint);

void build_contextSet(GList **);
void build_contextSet_active(GList **);
void print_contextSet(GList *);

gint same_src_dst_pe_nodeid (struct service_t *);
void comp_route_connection_issue_handler (struct compRouteOutput_t *, struct service_t *);

void destroy_compRouteOutputList (struct compRouteOutputList_t *);
void duplicate_graph (struct graph_t *, struct graph_t *);

void allocate_graph_resources (struct path_t *, struct service_t *, struct graph_t *);
void allocate_graph_reverse_resources(struct path_t*, struct service_t *, struct graph_t *);
void print_route_solution_list (GList *);
struct timeval tv_adjust(struct timeval);

void print_path_connection_list(struct compRouteOutputList_t*);
void update_stats_path_comp(struct compRouteOutputList_t*, struct timeval, gint, gint);
void destroy_active_service(struct activeService_t*);
void destroy_requested_service(struct service_t*);
void destroy_device(struct device_t*);
void destroy_link(struct link_t*);
void destroy_context(struct context_t*);
void dijkstra(gint, gint, struct graph_t*, struct service_t*, struct map_nodes_t*, struct nodes_t*, struct compRouteOutputItem_t*, guint);
void set_path_attributes(struct compRouteOutputItem_t*, struct map_t*);
void alg_comp(struct service_t*, struct compRouteOutput_t*, struct graph_t*, guint);
#endif

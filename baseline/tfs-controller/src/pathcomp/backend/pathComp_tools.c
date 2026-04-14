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

#include <stdio.h>
#include <stdlib.h> 
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <glib.h>
#include <sys/time.h>
#include <ctype.h>
#include <strings.h>
#include <time.h>
#include <math.h>
#include <fcntl.h>
#include <uuid/uuid.h>
#include <errno.h>

#include "pathComp_log.h"
#include "pathComp.h"
#include "pathComp_tools.h"

gint numPathCompIntents = 0;  // number of events triggering the path computation
//gint numSuccesPathComp = 0; // number of events resulting in succesfully path computations fulfilling the constraints
struct timeval total_path_comp_time;
gdouble totalReqBw = 0.0;
gdouble totalServedBw = 0.0;

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function for time processing
 *
 * 	@param a
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 ////////////////////////////////////////////////////////////////////////////////////////
struct timeval tv_adjust (struct timeval a) {
	while (a.tv_usec >= 1000000) {
		a.tv_usec -= 1000000;
		a.tv_sec++;
	}
	while (a.tv_usec < 0) {
		a.tv_usec += 1000000;
		a.tv_sec--;
	}
	return a;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief friendly function to copy safely strings
 *
 * 	@param dst
 *  @param src
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 ////////////////////////////////////////////////////////////////////////////////////////
void duplicate_string(gchar* dst, gchar* src) {
	g_assert(dst); g_assert(src);
	strcpy(dst, src);
	dst[strlen(dst)] = '\0';
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to print the computed the path
 *
 *	@param path
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void print_path (struct compRouteOutputItem_t *p) {
	g_assert(p);	
	DEBUG_PC ("=========== COMPUTED PATH =======================");
	DEBUG_PC ("E2E Avail. Bw: %f, Latency: %f, Cost: %f, Consumed Power (in W): %f", p->availCap, p->delay, p->cost, p->power);
	for (gint k = 0; k < p->numRouteElements; k++) {
		DEBUG_PC ("%s[%s] --> %s[%s]", p->routeElement[k].aNodeId.nodeId, p->routeElement[k].aEndPointId,
																p->routeElement[k].zNodeId.nodeId, p->routeElement[k].zEndPointId);
		DEBUG_PC("\t linkId: %s", p->routeElement[k].linkId);
		DEBUG_PC("\t aTopologyId: %s", p->routeElement[k].aTopologyId);
		DEBUG_PC("\t zTopologyId: %s", p->routeElement[k].zTopologyId);
	}
	DEBUG_PC ("==================================================================");		
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to print the output path formed by link Ids
 *
 *	@param p
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_path_t(struct path_t* p) {
	g_assert(p);
	DEBUG_PC(" ============ COMPUTED OUTPUT PATH =================");
	DEBUG_PC("Path AvailBw: %f, Cost: %f, Latency: %f, Power: %f", p->path_capacity.value,
			p->path_cost.cost_value, p->path_latency.fixed_latency, p->path_power.power);
	DEBUG_PC("number of links of path %d", p->numPathLinks);
	for (gint k = 0; k < p->numPathLinks; k++) {
		DEBUG_PC("Link: %s", p->pathLinks[k].linkId);
		for (gint l = 0; l < p->pathLinks[k].numLinkTopologies; l++) {
			DEBUG_PC("end Link [%d] TopologyId: %s", l, p->pathLinks[k].linkTopologies[l].topologyId);
		}
		DEBUG_PC(" ContextId: %s", p->pathLinks[k].topologyId.contextId);
		DEBUG_PC(" TopologyUUid: %s", p->pathLinks[k].topologyId.topology_uuid);
		DEBUG_PC(" aDeviceId: %s", p->pathLinks[k].aDeviceId);
		DEBUG_PC(" aEndpointId: %s", p->pathLinks[k].aEndPointId);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used allocate memory for struct path_t
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 ////////////////////////////////////////////////////////////////////////////////////////
struct path_t* create_path() {
	struct path_t* p = g_malloc0(sizeof(struct path_t));
	if (p == NULL) {
		DEBUG_PC("Memory allocation failure");
		exit(-1);
	}
	return(p);
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Returns the char (36 bytes) format of a uuid
 *
 *	@param uuid
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gchar* get_uuid_char(uuid_t uuid) {
	gchar* uuidChar = g_malloc0(16); // uuid has 36 chars
	if (uuidChar == NULL) {
		DEBUG_PC("Memory Allocation failure");
		exit(-1);
	}
	uuid_unparse(uuid, (char *)uuidChar);
	return uuidChar;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Makes a copy of the service identifier (including the context)
 *
 *	@param o
 *  @param i
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void copy_service_id(struct serviceId_t* o, struct serviceId_t* i) {
	g_assert(o); g_assert(i);
	memcpy(o->contextId, i->contextId, sizeof(i->contextId));
	memcpy(o->service_uuid, i->service_uuid, sizeof(i->service_uuid));
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Makes a copy of the service endpoint identifier (including the topology (contect and topology id), device and endpoint (port))
 *
 *	@param oEp
 *  @param iEp
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void copy_service_endpoint_id(struct service_endpoints_id_t* oEp, struct service_endpoints_id_t* iEp) {
	g_assert(oEp); g_assert(iEp);

	// copy topology information
	memcpy(oEp->topology_id.contextId, iEp->topology_id.contextId, sizeof(iEp->topology_id.contextId));
	memcpy(oEp->topology_id.topology_uuid, iEp->topology_id.topology_uuid, sizeof(iEp->topology_id.topology_uuid));

	// copy the endpoint
	memcpy(oEp->device_uuid, iEp->device_uuid, sizeof(iEp->device_uuid));
	memcpy(oEp->endpoint_uuid, iEp->endpoint_uuid, sizeof(iEp->endpoint_uuid));
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief From the set of contexts, it is returned the graph associated to that context matching
 *	with the passed contextId.
 *
 *	@param Set
 *  @param contextId
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct graph_t* get_graph_by_contextId(GList* set, gchar* contextId) {
	g_assert(contextId);

	// iterate over the set of context. Pick the one matching with contextId, and return the graph.
	// If not found, return NULL
	struct graph_t* g = NULL;
	for (GList *ln = g_list_first(set);
		ln;
		ln = g_list_next(ln)){
		struct context_t* context = (struct context_t*)(ln->data);
		if (strcmp(context->contextId, contextId) == 0) {
			g = &(context->g);
			return g;
		}
	}
	return NULL;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Process the service constraint and maps them into the path constraints
 * to be fulfilled
 *
 *  @param path_constraints
 *  @param s
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct path_constraints_t * get_path_constraints(struct service_t* s) {
	g_assert(s);
	
	struct path_constraints_t* path_constraints = g_malloc0(sizeof(struct path_constraints_t));
	if (path_constraints == NULL) {
		DEBUG_PC("Memory Allocation Failure");
		exit(-1);
	}

	char* eptr;
	for (gint i = 0; i < s->num_service_constraints; i++) {
		struct constraint_t* constraint = &(s->constraints[i]);;
		if (strncmp((const char*)constraint->constraint_type, "bandwidth", 9) == 0) {
			path_constraints->bwConstraint = (gdouble)(strtod((char*)constraint->constraint_value, &eptr));
			path_constraints->bw = TRUE;
			//DEBUG_PC("Path Constraint Bw: %f", path_constraints->bwConstraint);
		}
		if (strncmp((const char*)constraint->constraint_type, "cost", 4) == 0) {
			path_constraints->costConstraint = (gdouble)(strtod((char*)constraint->constraint_value, &eptr));
			path_constraints->cost = TRUE;
			//DEBUG_PC("Path Constraint Cost: %f", path_constraints->costConstraint);
		}
		if (strncmp((const char*)constraint->constraint_type, "latency", 7) == 0) {
			path_constraints->latencyConstraint = (gdouble)(strtod((char*)constraint->constraint_value, &eptr));
			path_constraints->latency = TRUE;
			//DEBUG_PC("Path Constraint Latency: %f", path_constraints->latencyConstraint);
		}
		if (strncmp((const char*)constraint->constraint_type, "energy", 6) == 0) {
			path_constraints->energyConstraint = (gdouble)(strtod((char*)constraint->constraint_value, &eptr));
			path_constraints->energy = TRUE;
			//DEBUG_PC("Path Constraint Energy: %f", path_constraints->energyConstraint);
		}
	}
	return path_constraints;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Creates the predecessors to keep the computed path
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct pred_t * create_predecessors () {
	struct pred_t *predecessors = g_malloc0 (sizeof (struct pred_t));
	if (predecessors == NULL) {
		DEBUG_PC ("memory allocation failed\n");
		exit (-1);
	}   
	return predecessors;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief create edge
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct edges_t* create_edge() {
	struct edges_t* e = g_malloc0(sizeof(struct edges_t));
	if (e == NULL) {
		DEBUG_PC("Memory allocation failed\n");
		exit(-1);
	}
	return e;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Prints the list of the predecessors for a given computed Shortest Path
 *
 *	@param p 
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void print_predecessors (struct pred_t *p)
{
	g_assert (p);
	DEBUG_PC ("Number of Predecessors: %d", p->numPredComp);
	for (gint i = 0; i < p->numPredComp; i++) {
		struct pred_comp_t *pComp = &(p->predComp[i]);
		DEBUG_PC ("deviceId: %s", pComp->v.nodeId);		
		struct edges_t *e = &(pComp->e);
		DEBUG_PC("Edge[#%d] (linkId): %s", i, e->linkId);
		DEBUG_PC ("\t %s[%s] ===>", e->aNodeId.nodeId, e->aEndPointId);
		DEBUG_PC("\t %s[%s]", e->zNodeId.nodeId, e->zEndPointId);
		DEBUG_PC("\t aTopologyId: %s", e->aTopologyId);
		DEBUG_PC("\t zTopologyId: %s", e->zTopologyId);
	}	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Builds the list of predecessors for the request destination using the computed Shortest Path
 *	being stored in map
 *
 *	@param p 
 *	@param s
 *	@param map
 *	
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void build_predecessors (struct pred_t *p, struct service_t *s, struct map_nodes_t *map) {
	g_assert (p); g_assert (s); g_assert (map);
	
	struct nodes_t *v = create_node();
	duplicate_string(v->nodeId, s->service_endpoints_id[1].device_uuid);
	
	struct edges_t *e = create_edge();	
	get_edge_from_map_by_node (e, v, map);
			
	// Get u (being source of edge e)
	struct nodes_t u;	
	duplicate_node_id (&e->aNodeId, &u);
		
	// Add to the predecessors list
	struct pred_comp_t *pred = &(p->predComp[p->numPredComp]);
	duplicate_node_id (&u, &pred->v);	
	struct edges_t *e1 = &(pred->e);	
	duplicate_edge (e1, e);
	p->numPredComp++;	
	// Back-trace edges till reaching the srcPEId
	struct nodes_t* srcNode = create_node();
	duplicate_string(srcNode->nodeId, s->service_endpoints_id[0].device_uuid);

	while (compare_node_id (&u, srcNode) != 0) 	{		
		duplicate_node_id (&u, v);
		get_edge_from_map_by_node (e, v, map);		
		// Get the u (being source of edge e)		
		duplicate_node_id (&e->aNodeId, &u);		
		// Get the new predecessor
		struct pred_comp_t *pred = &p->predComp[p->numPredComp];			
		// Add to the predecessors list					
		duplicate_node_id (&u, &pred->v);		
		struct edges_t *e1 = &(pred->e);
		duplicate_edge (e1, e);
		p->numPredComp++;		
	}
	print_predecessors (p);
    g_free (e); g_free(v); g_free(srcNode);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief It creates a struct nodes_t
 *
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct nodes_t * create_node ()
{
	struct nodes_t *n = g_malloc0 (sizeof (struct nodes_t));
	if (n == NULL) {
		DEBUG_PC ("memory allocation problem");
		exit (-1);
	}
	return n;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief It creates a routeElement_t
 *
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct routeElement_t * create_routeElement () {
	struct routeElement_t *rE = g_malloc0 (sizeof (struct routeElement_t));
	if (rE == NULL)	{
		DEBUG_PC ("memory allocation problem");
		exit (-1);		
	}
	return rE;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief copy node ids
 *
 *	@param src
 *  @param dst
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void duplicate_node_id (struct nodes_t *src, struct nodes_t *dst) {	
	g_assert (src);
	g_assert (dst);	
	//DEBUG_PC ("Duplicate nodeId for %s", src->nodeId);	
	strcpy (dst->nodeId, src->nodeId);	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief compares a pair of node Ids
 *
 *	@param a
 *  @param b
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint compare_node_id (struct nodes_t *a, struct nodes_t *b) {
	g_assert (a);
	g_assert (b);	
	return (memcmp (&a->nodeId, b->nodeId, strlen (b->nodeId)));	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief duplicate two routeElement_t
 *
 *	@param src
 *  @param dst
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void duplicate_routeElement (struct routeElement_t *src, struct routeElement_t *dst)
{
	g_assert (src);
	g_assert (dst);
	
	duplicate_node_id (&(src->aNodeId), &(dst->aNodeId));
	duplicate_node_id (&(src->zNodeId), &(dst->zNodeId));
	duplicate_string(dst->aEndPointId, src->aEndPointId);
	duplicate_string(dst->zEndPointId, src->zEndPointId);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief duplicate two edges
 *
 *	@param e1 (destination)
 *  @param e2 (source)
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void duplicate_edge (struct edges_t *e1, struct edges_t *e2) {
	g_assert (e1); g_assert (e2);
		
	duplicate_node_id (&e2->aNodeId, &e1->aNodeId);
	duplicate_node_id (&e2->zNodeId, &e1->zNodeId);
	//DEBUG_PC ("e->aNodeId: %s --->  e->zNodeId: %s", e1->aNodeId.nodeId, e1->zNodeId.nodeId);
	duplicate_string(e1->aEndPointId, e2->aEndPointId);
	duplicate_string(e1->zEndPointId, e2->zEndPointId);
	duplicate_string(e1->linkId, e2->linkId);
	duplicate_string(e1->interDomain_localId, e2->interDomain_localId);
	duplicate_string(e1->interDomain_remoteId, e2->interDomain_remoteId);
	duplicate_string(e1->aTopologyId, e2->aTopologyId);
	duplicate_string(e1->zTopologyId, e2->zTopologyId);
	
	e1->unit = e2->unit;
	memcpy(&e1->totalCap, &e2->totalCap, sizeof(gdouble));
	memcpy(&e1->availCap, &e2->availCap, sizeof(gdouble));

	memcpy (&e1->cost, &e2->cost, sizeof (gdouble));
    memcpy (&e1->delay, &e2->delay, sizeof (gdouble));
	memcpy(&e1->energy, &e2->energy, sizeof(gdouble));
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Duplicate path 
 *
 *	@param a - original
 *  @param b - copy
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void duplicate_path (struct compRouteOutputItem_t *a, struct compRouteOutputItem_t *b) {		
	g_assert (a); 	g_assert (b);
	memcpy(&b->availCap, &a->availCap, sizeof (gdouble));		
	memcpy(&b->cost, &a->cost, sizeof(gdouble));	
	memcpy(&b->delay, &a->delay, sizeof (gdouble));
	memcpy(&b->power, &a->power, sizeof(gdouble));
	b->numRouteElements = a->numRouteElements;
	for (gint k = 0; k < a->numRouteElements; k++) {			
		//DEBUG_PC ("aNodeId: %s // zNodeId: %s", a->routeElement[k].aNodeId.nodeId, a->routeElement[k].zNodeId.nodeId);
		// aNodeId duplication
		struct nodes_t *n1 = &(a->routeElement[k].aNodeId);
		struct nodes_t *n2 = &(b->routeElement[k].aNodeId);			
		duplicate_node_id (n1, n2);					
		//zNodeId duplication
		n1 = &(a->routeElement[k].zNodeId);
		n2 = &(b->routeElement[k].zNodeId);			
		duplicate_node_id (n1, n2);
		duplicate_string(b->routeElement[k].aEndPointId, a->routeElement[k].aEndPointId);
		duplicate_string(b->routeElement[k].zEndPointId, a->routeElement[k].zEndPointId);
		duplicate_string(b->routeElement[k].linkId, a->routeElement[k].linkId);
		duplicate_string(b->routeElement[k].aTopologyId, a->routeElement[k].aTopologyId);
		duplicate_string(b->routeElement[k].zTopologyId, a->routeElement[k].zTopologyId);
	}	
	return;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Duplicate path from compRouteOutputItem_t to path_t
 *
 *	@param a - original
 *  @param b - copy
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void duplicate_path_t(struct compRouteOutputItem_t* a, struct path_t* b) {
	g_assert(a); g_assert(b);

	// transfer path characteristics ...
	memcpy(&b->path_capacity.value, &a->availCap, sizeof(gdouble));
	memcpy(&b->path_cost.cost_value, &a->cost, sizeof(gdouble));
	memcpy(&b->path_latency.fixed_latency, &a->delay, sizeof(gdouble));
	memcpy(&b->path_power.power, &a->power, sizeof(gdouble));

	b->numPathLinks = a->numRouteElements;

	for (gint k = 0; k < a->numRouteElements; k++) {
		struct routeElement_t* rE = &(a->routeElement[k]);
		struct pathLink_t* pL = &(b->pathLinks[k]);

		// copy the aDeviceId and aEndpointId, zDeviceId and zEndPointId
		duplicate_string(pL->aDeviceId, rE->aNodeId.nodeId);
		duplicate_string(pL->zDeviceId, rE->zNodeId.nodeId);
		duplicate_string(pL->aEndPointId, rE->aEndPointId);
		duplicate_string(pL->zEndPointId, rE->zEndPointId);

		duplicate_string(pL->topologyId.topology_uuid, rE->aTopologyId);
		duplicate_string(pL->topologyId.contextId, rE->contextId);

		//copy the linkId
		duplicate_string(pL->linkId, rE->linkId);
		pL->numLinkTopologies++;
		duplicate_string(pL->linkTopologies[pL->numLinkTopologies - 1].topologyId, rE->aTopologyId);
		pL->numLinkTopologies++;
		duplicate_string(pL->linkTopologies[pL->numLinkTopologies - 1].topologyId, rE->zTopologyId);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Return the index into mapN related nodeId
 * 
 *  @param nodeId
 *  @para mapN
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint get_map_index_by_nodeId (gchar *nodeId, struct map_nodes_t * mapN) {
    gint i = 0;    
    for (i = 0; i < mapN->numMapNodes; i++) {
		//DEBUG_PC ("i: %d; current: %s // targeted: %s", i, mapN->map[i].verticeId.nodeId, nodeId);
        if (memcmp (mapN->map[i].verticeId.nodeId, nodeId, strlen (nodeId)) == 0) {
			//DEBUG_PC ("Index: %d", i);
			return i;            
        }
    }
	//DEBUG_PC ("Index: %d", index);
    return -1;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Get the edge e enabling reaching the computed v in mapNodes
 * 
 *  @param e
 *  @param v
 *  @param mapN
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void get_edge_from_map_by_node (struct edges_t *e, struct nodes_t* v, struct map_nodes_t *mapN) {	
	//DEBUG_PC ("Get the Edge into map from node v: %s", v.nodeId);	
	// Get the edge reaching the node v from mapNodes
	gint map_vIndex = get_map_index_by_nodeId (v->nodeId, mapN);	
	//DEBUG_PC ("aNodeId: %s --> zNodeId: %s", mapN->map[map_vIndex].predecessor.aNodeId.nodeId, mapN->map[map_vIndex].predecessor.zNodeId.nodeId);	
	struct edges_t *te = &(mapN->map[map_vIndex].predecessor);	
	duplicate_edge (e, te);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Get the edge from the predecessors array for a given node n
 * 
 *  @param e
 *  @param n
 *  @param predecessors
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void get_edge_from_predecessors (struct edges_t *e, struct nodes_t* n, struct pred_t *predecessors) {
	g_assert(predecessors);
	DEBUG_PC ("Get edge outgoing node %s from predecessors list", n->nodeId);
	//print_predecessors (predecessors);
	for (gint i = 0; i < predecessors->numPredComp; i++) {
		struct pred_comp_t *pred = &(predecessors->predComp[i]);
		if (compare_node_id (n, &pred->v) == 0) {
			// Add to the predecessors list
			struct edges_t *te = &(pred->e);
			DEBUG_PC("add e (linkId): %s", te->linkId);
			duplicate_edge (e, te);
			return;
		}	
	}	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Construct the path using the predecessors list
 * 
 *  @param path
 *  @param predecessors
 *	@param s
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void build_path (struct compRouteOutputItem_t *p, struct pred_t *predecessors, struct service_t *s) {
	// Get the source device Id	of the network connectivity service
	struct nodes_t *v = create_node();
	// Src Node of the Service set to v
	duplicate_string(v->nodeId, s->service_endpoints_id[0].device_uuid);
								  	
	// Get the edge for v in predecessors
	struct edges_t* e = create_edge();
	get_edge_from_predecessors (e, v, predecessors);	
	// Get the target for e
	struct nodes_t u;	
	duplicate_node_id (&e->zNodeId, &u);
	//DEBUG_PC ("u: %s", u.nodeId);
	struct path_constraints_t* pathCons = get_path_constraints(s);		

	// Add route element to the path being constructed
	gint k = 0;
	duplicate_node_id (&e->aNodeId, &p->routeElement[k].aNodeId);
	duplicate_node_id (&e->zNodeId, &p->routeElement[k].zNodeId);
	duplicate_string(p->routeElement[k].aEndPointId, e->aEndPointId);
	duplicate_string(p->routeElement[k].zEndPointId, e->zEndPointId);
	duplicate_string(p->routeElement[k].linkId, e->linkId);
	duplicate_string(p->routeElement[k].aTopologyId, e->aTopologyId);
	duplicate_string(p->routeElement[k].zTopologyId, e->zTopologyId);
	duplicate_string(p->routeElement[k].contextId, s->serviceId.contextId);
	p->numRouteElements++;

	// Get Dst Node of connectivity service
	struct nodes_t* dst = create_node();
	duplicate_string(dst->nodeId, s->service_endpoints_id[1].device_uuid);
	while (compare_node_id (&u, dst) != 0) {
		k++; 
		p->numRouteElements++;			
		duplicate_node_id (&u, v);
		get_edge_from_predecessors (e, v, predecessors);
		// Get the target u		
		duplicate_node_id (&e->zNodeId, &u);
		// Add route element to the path being constructed		
		duplicate_node_id (&e->aNodeId, &p->routeElement[k].aNodeId);
		duplicate_node_id (&e->zNodeId, &p->routeElement[k].zNodeId);
		duplicate_string(p->routeElement[k].aEndPointId, e->aEndPointId);
		duplicate_string(p->routeElement[k].zEndPointId, e->zEndPointId);
		duplicate_string(p->routeElement[k].linkId, e->linkId);
		duplicate_string(p->routeElement[k].aTopologyId, e->aTopologyId);
		duplicate_string(p->routeElement[k].zTopologyId, e->zTopologyId);
		duplicate_string(p->routeElement[k].contextId, s->serviceId.contextId);		
	}		
	g_free(e); g_free(v); g_free(pathCons);
	//DEBUG_PC ("Path is constructed");	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Print the graph for DEBUG_PCging purposes
 * 
 *  @param g
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void print_graph (struct graph_t *g) {
	g_assert(g);
    DEBUG_PC ("================================================================");
    DEBUG_PC ("===========================   GRAPH   ==========================");
    DEBUG_PC ("================================================================");
	DEBUG_PC("Graph Num Vertices: %d", g->numVertices);    
    
    for (gint i = 0; i < g->numVertices; i++) {
        DEBUG_PC ("Head Vertice [%s]", g->vertices[i].verticeId.nodeId);
        for (gint j = 0; j < g->vertices[i].numTargetedVertices; j++)
        {
            DEBUG_PC ("  Tail Vertice: %s", g->vertices[i].targetedVertices[j].tVertice.nodeId);
            for (gint k = 0; k < g->vertices[i].targetedVertices[j].numEdges; k++)
            {
                struct edges_t *e = &(g->vertices[i].targetedVertices[j].edges[k]);
				DEBUG_PC ("%s(%s) --> %s(%s) [C: %f, Bw: %f b/s, Delay: %f ms]", e->aNodeId.nodeId, e->aEndPointId, e->zNodeId.nodeId, 
								e->zEndPointId, e->cost, e->availCap, e->delay);				
           }
        }       
    }     
    return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Look for a given edge into the graph
 *
 *  @param verticeIndex
 *	@param targetedVerticeIndex
 *  @param e
 *  @param g
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint graph_edge_lookup (gint verticeIndex, gint targetedVerticeIndex, struct edges_t *e, struct graph_t *g)	{
	gint indexEdge = -1;
	
	for (gint j = 0; j < g->vertices[verticeIndex].targetedVertices[targetedVerticeIndex].numEdges; j++) {
		struct edges_t *e2 = &(g->vertices[verticeIndex].targetedVertices[targetedVerticeIndex].edges[j]);
		if ((compare_node_id (&e->aNodeId, &e2->aNodeId) == 0) &&
			(compare_node_id (&e->zNodeId, &e2->zNodeId) == 0) &&
			(strcmp (e->aEndPointId, e2->aEndPointId) == 0) &&
			(strcmp (e->zEndPointId, e2->zEndPointId) == 0) &&
			(strcmp(e->linkId, e2->linkId) == 0)) {
			DEBUG_PC ("%s (%s) --> %s (%s) [linkId: %s] FOUND in the Graph at index: %d", e->aNodeId.nodeId, e->aEndPointId, e->zNodeId.nodeId, 
							e->zEndPointId, e->linkId, j);
			indexEdge = j;
			return indexEdge;
		}		
	}	
	return indexEdge;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Look for a given vertice within the graph using the nodeId
 *
 *  @param nodeId
 *	@param g
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint graph_vertice_lookup (gchar *nodeId, struct graph_t *g)
{
    gint index = -1; 
	//DEBUG_PC("Searching Node: %s", nodeId);
    for (gint i = 0; i < g->numVertices; i++) {
		//DEBUG_PC("Checked Graph Node: %s", g->vertices[i].verticeId.nodeId);
		if (memcmp (g->vertices[i].verticeId.nodeId, nodeId, strlen (nodeId)) == 0)
        {
            index = i;
            //DEBUG_PC ("%s is found in the graph vertice [%d]", nodeId, index);
            break;
        }     
    }  
    return (index);
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Check if a nodeId is already considered into the set of targeted vertices from a given vertice
 *
 *  @param nodeId
 *  @param vIndex
 *  @param g
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint graph_targeted_vertice_lookup (gint vIndex, gchar *nodeId, struct graph_t *g)
{
    gint addedTargetedVerticeIndex = -1;
    gint i = 0;
    
    if (g->vertices[vIndex].numTargetedVertices == 0)
    {
        return (addedTargetedVerticeIndex);
    }
    
    for (i = 0; i < g->vertices[vIndex].numTargetedVertices; i++)
    {
        if (memcmp (g->vertices[vIndex].targetedVertices[i].tVertice.nodeId, nodeId, strlen (nodeId)) == 0)
        {
            DEBUG_PC ("Targeted %s reachable from %s", nodeId, g->vertices[vIndex].verticeId.nodeId);
            addedTargetedVerticeIndex = i;
            return (addedTargetedVerticeIndex);
        }        
    }    
    // not found ...    
    return (addedTargetedVerticeIndex);
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Check if a nodeId is already considered into the set of targeted vertices from a given vertice, if not to be added
 *
 *  @param nodeId
 *  @param vIndex
 *  @param g
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint graph_targeted_vertice_add (gint vIndex, gchar *nodeId, struct graph_t *g)
{
    gint addedTargetedVerticeIndex = -1;
    gint i = 0;
    
    if (g->vertices[vIndex].numTargetedVertices == 0)
    {
        //DEBUG_PC ("targeted vertice %s being reachable from vertice %s", nodeId, g->vertices[vIndex].verticeId.nodeId);        
        addedTargetedVerticeIndex = 0;
        return (addedTargetedVerticeIndex);
    }
    
    for (i = 0; i < g->vertices[vIndex].numTargetedVertices; i++)
    {        
		if (memcmp (g->vertices[vIndex].targetedVertices[i].tVertice.nodeId, nodeId, strlen (nodeId)) == 0)
        {
            //DEBUG_PC ("Targeted vertice %s is already considered in the reachable from vertice %s", nodeId, g->vertices[vIndex].verticeId.nodeId);
            addedTargetedVerticeIndex = -1;
            return (addedTargetedVerticeIndex);
        }        
    }    
    // It is not found, next to be added at i position
    addedTargetedVerticeIndex = i;
    return (addedTargetedVerticeIndex);
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Remove edge from the graph
 *
 *  @param g
 *  @param e
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
void remove_edge_from_graph (struct graph_t *g, struct edges_t *e) {
	// Find the ingress vertice into the graph
	DEBUG_PC ("Removing from Graph %s[%s]) ---> %s[%s] (linkId: %s)", e->aNodeId.nodeId, e->aEndPointId, e->zNodeId.nodeId, e->aEndPointId, e->linkId);
	gint verticeIndex = -1;		
	verticeIndex = graph_vertice_lookup (e->aNodeId.nodeId, g);
	if (verticeIndex == -1)	{
		DEBUG_PC ("Edge w/ %s is NOT in the Graph!!", e->aNodeId.nodeId);
		return;
	}
	
	// Find the targeted vertice from vertice Id
	gint targetedVerticeIndex = -1;
	targetedVerticeIndex = graph_targeted_vertice_lookup (verticeIndex, e->zNodeId.nodeId, g);
	if (targetedVerticeIndex == -1)	{
		DEBUG_PC ("%s --> %s NOT in the Graph!!", e->aNodeId.nodeId, e->zNodeId.nodeId);
		return;
	}	
	//DEBUG_PC ("%s --> %s found in the Graph", e->aNodeId.nodeId, e->zNodeId.nodeId);
	
	// Get the edge position
	gint edgeIndex = -1;
	edgeIndex = graph_edge_lookup (verticeIndex, targetedVerticeIndex, e, g);
	if (edgeIndex == -1) {
		DEBUG_PC ("%s --> %s NOT in the Graph!!", e->aNodeId.nodeId, e->zNodeId.nodeId);
		return;
	}
	
	//DEBUG_PC ("%s --> %s FOUND in Graph w/ edgeIndex: %d", e->aNodeId.nodeId, e->zNodeId.nodeId, edgeIndex);
	
	// Remove the edge
	//DEBUG_PC ("Start Removing %s --> %s from Graph", e->aNodeId.nodeId, e->zNodeId.nodeId);	
	struct targetNodes_t *v = &(g->vertices[verticeIndex].targetedVertices[targetedVerticeIndex]);	
	for (gint j = edgeIndex; j < v->numEdges; j++) {	
		struct edges_t *e1 = &(v->edges[j]);
		struct edges_t *e2 = &(v->edges[j+1]);		
		duplicate_edge (e1, e2);
	}
	v->numEdges --;
	DEBUG_PC ("Number of Edges between %s and %s is %d", e->aNodeId.nodeId, e->zNodeId.nodeId, v->numEdges);	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief create the pointer for keeping a set of the paths (struct compRouteOutput_t)
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct path_set_t * create_path_set () {
	struct path_set_t * p = g_malloc0 (sizeof (struct path_set_t));
	if (p == NULL) {
		DEBUG_PC ("Memory allocation problem");
		exit (-1);		
	}
	return p;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Remove the path set
 *
 * @param p
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2021
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void remove_path_set(struct path_set_t* p) {
	g_assert(p); g_free(p);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Create map of nodes to handle the path computation
 *
 * 	@param mapN
 *  @param g
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void build_map_node (struct map_nodes_t *mapN, struct graph_t *g) {
	//DEBUG_PC ("Construction of the Map of Nodes");               
    for (gint i = 0; i < g->numVertices; i++) {	
		duplicate_node_id (&g->vertices[i].verticeId, &mapN->map[i].verticeId);
        mapN->map[i].distance = INFINITY_COST;
        mapN->map[i].avaiBandwidth = 0.0;
        mapN->map[i].latency = INFINITY_COST;
		mapN->map[i].power = INFINITY_COST;
        mapN->numMapNodes++;
    }
    //DEBUG_PC ("mapNodes formed by %d Nodes", mapN->numMapNodes);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Allocate memory for path of struct compRouteOutputList_t *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct compRouteOutputList_t * create_route_list () {
	struct compRouteOutputList_t *p = g_malloc0 (sizeof (struct compRouteOutputList_t));
	if (p == NULL) {
		DEBUG_PC ("Memory Allocation Problem");
		exit (-1);
	}
	return p;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Copy all the attributes defining a path
 *
 * @param dst_path
 * @param src_path
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void copy_path(struct path_t* dst_path, struct path_t* src_path) {
	g_assert(dst_path);
	g_assert(src_path);

	// Path capacity
	dst_path->path_capacity.unit = src_path->path_capacity.unit;
	memcpy(&dst_path->path_capacity.value, &src_path->path_capacity.value, sizeof(gdouble));

	// Path latency
	memcpy(&dst_path->path_latency.fixed_latency, &src_path->path_latency.fixed_latency, sizeof(gdouble));

	// Path cost
	duplicate_string(dst_path->path_cost.cost_name, src_path->path_cost.cost_name);
	memcpy(&dst_path->path_cost.cost_value, &src_path->path_cost.cost_value, sizeof(gdouble));
	memcpy(&dst_path->path_cost.cost_algorithm, &src_path->path_cost.cost_algorithm, sizeof(gdouble));

	// Path links
	dst_path->numPathLinks = src_path->numPathLinks;
	for (gint i = 0; i < dst_path->numPathLinks; i++) {
		struct pathLink_t* dPathLink = &(dst_path->pathLinks[i]);
		struct pathLink_t* sPathLink = &(src_path->pathLinks[i]);

		duplicate_string(dPathLink->linkId, sPathLink->linkId);
		duplicate_string(dPathLink->aDeviceId, sPathLink->aDeviceId);
		duplicate_string(dPathLink->zDeviceId, sPathLink->zDeviceId);
		duplicate_string(dPathLink->aEndPointId, sPathLink->aEndPointId);
		duplicate_string(dPathLink->zEndPointId, sPathLink->zEndPointId);

		duplicate_string(dPathLink->topologyId.contextId, sPathLink->topologyId.contextId);
		duplicate_string(dPathLink->topologyId.topology_uuid, sPathLink->topologyId.topology_uuid);

		dPathLink->numLinkTopologies = sPathLink->numLinkTopologies;
		for (gint j = 0; j < dPathLink->numLinkTopologies; j++) {
			struct linkTopology_t* dLinkTop = &(dPathLink->linkTopologies[j]);
			struct linkTopology_t* sLinkTop = &(sPathLink->linkTopologies[j]);

			duplicate_string(dLinkTop->topologyId, sLinkTop->topologyId);
		}
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Duplicate the route output instance
 *
 * @param dst_ro
 * @param src_ro
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void duplicate_compRouteOuput(struct compRouteOutput_t* dst_ro, struct compRouteOutput_t* src_ro) {
	g_assert(dst_ro); g_assert(src_ro); 
		
	// Copy the serviceId
	copy_service_id(&dst_ro->serviceId, &src_ro->serviceId);
	dst_ro->num_service_endpoints_id = src_ro->num_service_endpoints_id;

	for (gint j = 0; j < dst_ro->num_service_endpoints_id; j++) {
		struct service_endpoints_id_t* iEp = &(src_ro->service_endpoints_id[j]);
		struct service_endpoints_id_t* oEp = &(dst_ro->service_endpoints_id[j]);
		copy_service_endpoint_id(oEp, iEp);
	}

	// Copy paths
	dst_ro->numPaths = src_ro->numPaths;
	for (gint j = 0; j < dst_ro->numPaths; j++) {
		struct path_t* dst_path = &(dst_ro->paths[j]);
		struct path_t* src_path = &(src_ro->paths[j]);
		copy_path(dst_path, src_path);
	}
	// copy no path issue value
	dst_ro->noPathIssue = src_ro->noPathIssue;
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Duplicate the computation route output list
 * 
 * @param dst
 * @param src
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void duplicate_route_list(struct compRouteOutputList_t* dst, struct compRouteOutputList_t* src) {
	g_assert(src); g_assert(dst);

	dst->numCompRouteConnList = src->numCompRouteConnList;
	dst->compRouteOK = src->compRouteOK;
	memcpy(&dst->compRouteConnAvBandwidth, &src->compRouteConnAvBandwidth, sizeof(gdouble));
	memcpy(&dst->compRouteConnAvPathLength, &src->compRouteConnAvPathLength, sizeof(gdouble));
	for (gint i = 0; i < src->numCompRouteConnList; i++) {
		struct compRouteOutput_t* src_ro = &(src->compRouteConnection[i]);
		struct compRouteOutput_t* dst_ro = &(dst->compRouteConnection[i]);
		duplicate_compRouteOuput(dst_ro, src_ro);
	}	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Allocate memory for path of struct compRouteOutputItem_t *
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct compRouteOutputItem_t *create_path_item () {
	struct compRouteOutputItem_t *p = g_malloc0 (sizeof (struct compRouteOutputItem_t));
	if (p == NULL) 	{
		DEBUG_PC ("Memory Allocation Problem");
		exit (-1);
	}
	return p;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Sort the set of paths the AvailBw, Cost and Delay
 *
 *	@params setP
 *  @params args
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void sort_path_set(struct path_set_t* setP, guint args) {
	g_assert(setP);
	// Sort the paths contained in setP by:
	// 1st Criteria: The path cost (maybe bound to link distance)
	// 2nd Criteria: The consumed path power 
	// 3nd Criteria: The path latency
	// 3rd Criteria: The available Bw
	float epsilon = 0.1;

	for (gint i = 0; i < setP->numPaths; i++) {
		for (gint j = 0; j < (setP->numPaths - i - 1); j++)	{
			struct compRouteOutputItem_t* path1 = &setP->paths[j];
			struct compRouteOutputItem_t* path2 = &setP->paths[j + 1];			
			struct compRouteOutputItem_t* pathTmp = create_path_item();
			//////////////////////// Criterias ////////////////////////////////////////
			// 1st Criteria (Cost)
			if (path2->cost < path1->cost) {
				duplicate_path(path1, pathTmp);
				duplicate_path(path2, path1);
				duplicate_path(pathTmp, path2);
				g_free(pathTmp);
				continue;
			}
			if (path2->cost == path1->cost) {
				// 2nd Criteria (Energy)
				if (args & ENERGY_EFFICIENT_ARGUMENT) {
					if (path2->power < path1->power) {
						duplicate_path(path1, pathTmp);
						duplicate_path(path2, path1);
						duplicate_path(pathTmp, path2);
						g_free(pathTmp);
						continue;
					}
					else {	  // path1->power < path2->power
						g_free(pathTmp);
						continue;
					}
				}
				else { // No enery efficient argument
					// 3rd Criteria (latency)
					if (path2->delay < path1->delay) {
						duplicate_path(path1, pathTmp);
						duplicate_path(path2, path1);
						duplicate_path(pathTmp, path2);
						g_free(pathTmp);
						continue;
					}
					else if (path1->delay < path2->delay) {
						g_free(pathTmp);
						continue;
					}
					else { // path1->delay == path2->delay
						// 4th Criteria (available bw)
						if (path2->availCap > path1->availCap) {
							duplicate_path(path1, pathTmp);
							duplicate_path(path2, path1);
							duplicate_path(pathTmp, path2);
							g_free(pathTmp);
							continue;
						}
						else {
							g_free(pathTmp);
							continue;
						}
					}
				}
			}
			else {	// path1->cost < path2->cost
				g_free(pathTmp);
				continue;
			}				
		}
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Remove first element from the path sets 
 *
 *	@params setP
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void pop_front_path_set (struct path_set_t *setP) {
	for (gint j = 0; j < setP->numPaths - 1; j++) {
		struct compRouteOutputItem_t *path1 = &setP->paths[j];
		struct compRouteOutputItem_t *path2 = &setP->paths[j+1];		
		duplicate_path (path2, path1);		
	}
	setP->numPaths--;	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Add routeElement to the back of the path
 *
 * 	@param rE
 * 	@param p
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void add_routeElement_path_back (struct routeElement_t *rE, struct compRouteOutputItem_t *p) {
	//DEBUG_PC ("p->numRouteElements: %d", p->numRouteElements);
	p->numRouteElements++;
	gint index = p->numRouteElements - 1;
	
	struct nodes_t *pn = &(p->routeElement[index].aNodeId);
	struct nodes_t *rEn = &(rE->aNodeId);
	
	// duplicate aNodeId
	duplicate_node_id (rEn, pn);	
	pn = &(p->routeElement[index].zNodeId);
	rEn = &(rE->zNodeId);
	duplicate_node_id (rEn, pn);
	duplicate_string(p->routeElement[index].aEndPointId, rE->aEndPointId);
	duplicate_string(p->routeElement[index].zEndPointId, rE->zEndPointId);
	duplicate_string(p->routeElement[index].linkId, rE->linkId);
	duplicate_string(p->routeElement[index].aTopologyId, rE->aTopologyId);
	duplicate_string(p->routeElement[index].zTopologyId, rE->zTopologyId);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief This function compares ap and rootPath. If all the links are equal between both ap and rootPath till the sN, then the link from sN to next node 
 * 	ap is returned
 * 
 * @params ap
 * @params p
 * @params sN
 * @params e
 * 
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gboolean matching_path_rootPath (struct compRouteOutputItem_t *ap, struct compRouteOutputItem_t *rootPath, struct nodes_t *sN, struct edges_t *e) {
	gint j = 0;
	gboolean ret = FALSE;
	while ((j < ap->numRouteElements) && (j < rootPath->numRouteElements)) {
		if ((memcmp (ap->routeElement[j].aNodeId.nodeId, rootPath->routeElement[j].aNodeId.nodeId, sizeof (ap->routeElement[j].aNodeId.nodeId)) == 0) &&
			//(memcmp (ap->routeElement[j].zNodeId.nodeId, rootPath->routeElement[j].zNodeId.nodeId, sizeof (ap->routeElement[j].zNodeId.nodeId)) != 0) &&
			(memcmp (sN->nodeId, rootPath->routeElement[j].aNodeId.nodeId, sizeof (ap->routeElement[j].aNodeId.nodeId)) == 0)) {						
			duplicate_node_id (&ap->routeElement[j].aNodeId, &e->aNodeId);
			duplicate_node_id (&ap->routeElement[j].zNodeId, &e->zNodeId);
			duplicate_string(e->aEndPointId, ap->routeElement[j].aEndPointId);
			duplicate_string(e->zEndPointId, ap->routeElement[j].zEndPointId);
			duplicate_string(e->linkId, ap->routeElement[j].linkId);
			return TRUE;			
		}		
		if ((memcmp (ap->routeElement[j].aNodeId.nodeId, rootPath->routeElement[j].aNodeId.nodeId, sizeof (ap->routeElement[j].aNodeId.nodeId)) == 0) && 
			(memcmp (ap->routeElement[j].zNodeId.nodeId, rootPath->routeElement[j].zNodeId.nodeId, sizeof (ap->routeElement[j].zNodeId.nodeId)) == 0)) {
			j++;			
			continue;			
		}
		
		if ((memcmp (ap->routeElement[j].aNodeId.nodeId, rootPath->routeElement[j].aNodeId.nodeId, sizeof (ap->routeElement[j].aNodeId.nodeId)) != 0) || 
			(memcmp (ap->routeElement[j].zNodeId.nodeId, rootPath->routeElement[j].zNodeId.nodeId, sizeof (ap->routeElement[j].zNodeId.nodeId)) != 0)) {
			//DEBUG_PC ("ap and rootPath not in the same path");
			return ret;
		}
	}	
	return ret;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief This function is used to modify the graph to be used for running the subsequent SP computations acording to the YEN algorithm principles
 * 
 * @params g
 * @params A
 * @params rootPath
 * @params spurNode
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void modify_targeted_graph (struct graph_t *g, struct path_set_t *A, struct compRouteOutputItem_t * rootPath, struct nodes_t * spurNode) {
	//DEBUG_PC ("Modify the Targeted graph according to the Yen algorithm principles");
	for (gint j = 0; j < A->numPaths; j++) {
		struct compRouteOutputItem_t *ap = &A->paths[j];
		struct edges_t *e = create_edge();
		gboolean ret =  FALSE;
		ret = matching_path_rootPath (ap, rootPath, spurNode, e);		
		if (ret == TRUE) {
			DEBUG_PC ("Removal %s[%s] --> %s[%s] from the graph", e->aNodeId.nodeId, e->aEndPointId, e->zNodeId.nodeId, e->aEndPointId);
			remove_edge_from_graph (g, e);
			//DEBUG_PC ("Print Resulting Graph");
			print_graph (g);
			g_free (e);			
		}
		if (ret == FALSE) {
			g_free (e);
			continue;
		}						
	}	
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Supporting fucntion to Check if a nodeId is already in the items of a given GList
 * 
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint find_nodeId (gconstpointer data, gconstpointer userdata) {
     /** check values */
     g_assert(data != NULL);
     g_assert(userdata != NULL);
 
     struct nodeItem_t *SNodeId = (struct nodeItem_t *)data;
     guchar * nodeId = (guchar *)userdata; 
     
     //DEBUG_PC ("SNodeId (%s) nodeId (%s)", SNodeId->node.nodeId, nodeId);   
        
     if (!memcmp(SNodeId->node.nodeId, nodeId, strlen (SNodeId->node.nodeId))) {
		return (0);
     }
    return -1;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Explores the link between u and v
 * 
 *  @param u
 *  @param v 
 *	@param g
 *	@param s
 *  @param S
 *  @param Q
 *	@param mapNodes
 * 
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint check_link (struct nodeItem_t *u, gint indexGraphU, gint indexGraphV, struct graph_t *g, 
				struct service_t *s, GList **S, GList **Q, struct map_nodes_t *mapNodes, 
				guint arg) { 
	g_assert(g); g_assert(s); g_assert(mapNodes);

	struct targetNodes_t *v = &(g->vertices[indexGraphU].targetedVertices[indexGraphV]);	
    DEBUG_PC("=======================CHECK Edge %s => %s =================================", u->node.nodeId, v->tVertice.nodeId);
	//DEBUG_PC("\t %s => %s", u->node.nodeId, v->tVertice.nodeId);	
    
    // v already explored in S? then, discard it
    GList *found = g_list_find_custom (*S, v->tVertice.nodeId, find_nodeId);
    if (found != NULL) {
        DEBUG_PC ("%s in S, DISCARD", v->tVertice.nodeId);        
        return 0;
    }

	// Get the set of constraints imposed by the service
	struct path_constraints_t* path_constraints = get_path_constraints(s);
    gdouble distance_through_u = INFINITY_COST ,latency_through_u = INFINITY_COST, power_through_u = INFINITY_COST;
	gint i = 0, foundAvailBw = 0;
    // BANDWIDTH requirement to be fulfilled on EDGE u->v        
    gdouble edgeAvailBw = 0.0, edgeTotalBw = 0.0;
    for (i = 0; i < v->numEdges; i++) {        
        struct edges_t *e = &(v->edges[i]);
		memcpy (&edgeAvailBw, &(e->availCap), sizeof (gdouble));
		memcpy(&edgeTotalBw, &(e->totalCap), sizeof(gdouble));
		DEBUG_PC("EDGE %s[%s] => %s[%s]", u->node.nodeId, e->aEndPointId, v->tVertice.nodeId, e->zEndPointId);
        //DEBUG_PC ("\t %s[%s] =>", u->node.nodeId, e->aEndPointId);
		//DEBUG_PC("\t => %s[%s]", v->tVertice.nodeId, e->zEndPointId);
		DEBUG_PC("\t Edge Att: AvailBw: %f, TotalBw: %f", edgeAvailBw, edgeTotalBw);
        // Check Service Bw constraint
		if ((path_constraints->bw == TRUE) && (edgeAvailBw < path_constraints->bwConstraint)) {
			continue;
		}
		else {
			foundAvailBw = 1;
			break;
		}		
    }
	// BW constraint NOT MET, then DISCARD edge
    if ((path_constraints->bw == TRUE) && (foundAvailBw == 0)) {
       	DEBUG_PC ("Edge AvailBw: %f < path_constraint: %f -- DISCARD Edge", edgeAvailBw, path_constraints->bwConstraint);
		g_free(path_constraints);
        return 0;    
    } 

    gint indexEdge = i; // get the index for the explored edge
    // Update distance, latency and availBw through u to reach v
    gint map_uIndex = get_map_index_by_nodeId (u->node.nodeId, mapNodes);
	struct map_t *u_map = &mapNodes->map[map_uIndex];
    distance_through_u = u_map->distance + v->edges[indexEdge].cost;
    latency_through_u = u_map->latency + v->edges[indexEdge].delay;
	// Consumed power at v through u is the sum
	// 1. Power from src to u
	// 2. Power-idle at node u
	// 3. power consumed over the edge between u and v, i.e. energy*usedBw
	power_through_u = u_map->power + g->vertices[indexGraphU].power_idle + ((edgeTotalBw - edgeAvailBw + path_constraints->bwConstraint) * (v->edges[indexEdge].energy));
    gdouble availBw_through_u = 0.0;

	// ingress endpoint (u) is the src of the request
    if (strcmp (u->node.nodeId, s->service_endpoints_id[0].device_uuid) == 0) {
        //DEBUG_PC ("AvailBw %f on %s --> %s", edgeAvailBw, u->node.nodeId, v->tVertice.nodeId);        
        memcpy (&availBw_through_u, &edgeAvailBw, sizeof (gdouble));        
    }
    else {
        // Get the minimum available bandwidth between the src-->u and the new added edge u-->v
        //DEBUG_PC ("Current AvailBw: %f from src to %s", u_map->avaiBandwidth, u->node.nodeId);
        //DEBUG_PC ("AvailBw: %f %s --> %s", edgeAvailBw, u->node.nodeId, v->tVertice.nodeId);
        if (u_map->avaiBandwidth <= edgeAvailBw) {
            memcpy (&availBw_through_u, &u_map->avaiBandwidth, sizeof (gdouble));    
		}
		else {
			memcpy (&availBw_through_u, &edgeAvailBw, sizeof (gdouble));
		} 
    }     
    // Relax the link according to the pathCost, latency, and energy
    gint map_vIndex = get_map_index_by_nodeId (v->tVertice.nodeId, mapNodes);
	struct map_t *v_map = &mapNodes->map[map_vIndex];
    // If cost dist (u, v) > dist (src, v) relax the link
    if (distance_through_u > v_map->distance) {
        //DEBUG_PC ("dist(src, u) + dist(u, v): %f > dist (src, v): %f --> Discard Link", distance_through_u, v_map->distance);  
        return 0;
    }
	// If energy consumption optimization is requested
	if (arg & ENERGY_EFFICIENT_ARGUMENT) {
		if (distance_through_u == v_map->distance) {
			if (power_through_u > v_map->power) {
				DEBUG_PC("Energy (src -> u + u -> v: %f (Watts) > Energy (src, v): %f (Watts) --> DISCARD EDGE", power_through_u, v_map->power);
				return 0;
			}
			// same energy consumption, consider latency
			if ((power_through_u == v_map->power) && (latency_through_u > v_map->latency)) {
				return 0;
			}
			// same energy, same latency, criteria: choose the one having the largest available bw
			if ((power_through_u == v_map->power) && (latency_through_u == v_map->latency) && (availBw_through_u < v_map->avaiBandwidth)) {
				return 0;
			}
		}
	} // No optimization, rely on latency and available e2e bandwidth
	else {
		// If dist (src, u) + dist (u, v) = current dist(src, v), then use the latency as discarding criteria
		if ((distance_through_u == v_map->distance) && (latency_through_u > v_map->latency)) {
			//DEBUG_PC ("dist(src, u) + dist(u,v) = current dist(src, v), but latency (src,u) + latency (u, v) > current latency (src, v)");          
			return 0;
		}
		// If dist (src, u) + dist (u,v) == current dist(src, v) AND latency (src, u) + latency (u, v) == current latency (src, v), the available bandwidth is the criteria
		if ((distance_through_u == v_map->distance) && (latency_through_u == v_map->latency) && (availBw_through_u < v_map->avaiBandwidth)) {
			return 0;
		}
	}
   	DEBUG_PC ("Edge %s --> %s [RELAXED]", u->node.nodeId, v->tVertice.nodeId);
    DEBUG_PC ("\t path till %s: AvailBw: %f Mb/s | Cost: %f | Latency: %f ms | Energy: %f Watts", v->tVertice.nodeId, availBw_through_u, distance_through_u,
																latency_through_u, power_through_u);
    
    // Update Q list -- 
    struct nodeItem_t *nodeItem = g_malloc0 (sizeof (struct nodeItem_t));
    if (nodeItem == NULL) {
		DEBUG_PC ("memory allocation failed\n");
		exit (-1);    
    }    
    nodeItem->distance = distance_through_u;
	memcpy(&nodeItem->distance, &distance_through_u, sizeof(gdouble));		     
	memcpy(&nodeItem->latency, &latency_through_u, sizeof(gdouble));
	memcpy(&nodeItem->power, &power_through_u, sizeof(gdouble));
	duplicate_node_id (&v->tVertice, &nodeItem->node);	
	// add node to the Q list
	if (arg & ENERGY_EFFICIENT_ARGUMENT) {
		*Q = g_list_insert_sorted(*Q, nodeItem, sort_by_energy);
	}
	else {
		*Q = g_list_insert_sorted (*Q, nodeItem, sort_by_distance);
	}
    
	// Update the mapNodes for the specific reached tv   
    v_map->distance = distance_through_u;
	memcpy(&v_map->distance, &distance_through_u, sizeof(gdouble));
    memcpy (&v_map->avaiBandwidth, &availBw_through_u, sizeof (gdouble));
    memcpy (&v_map->latency, &latency_through_u, sizeof (gdouble));
	memcpy(&v_map->power, &power_through_u, sizeof(gdouble));
    // Duplicate the predecessor edge into the mapNodes 
	struct edges_t *e1 = &(v_map->predecessor);
	struct edges_t *e2 = &(v->edges[indexEdge]);
	duplicate_edge(e1, e2);	
	//DEBUG_PC ("u->v Edge: %s(%s) --> %s(%s)", e2->aNodeId.nodeId, e2->aEndPointId, e2->zNodeId.nodeId, e2->zEndPointId);
	//DEBUG_PC("v-pred aTopology: %s", e2->aTopologyId);
	//DEBUG_PC("v-pred zTopology: %s", e2->zTopologyId);

    // Check whether v is dstPEId
	//DEBUG_PC ("Targeted dstId: %s", s->service_endpoints_id[1].device_uuid);
	//DEBUG_PC ("nodeId added to the map: %s", v_map->verticeId.nodeId);
	//DEBUG_PC ("Q Length: %d", g_list_length(*Q));
	g_free(path_constraints);
    return 0;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Check the feasability of a path wrt the constraints imposed by the request in terms of latency
 * 
 *  @param s
 *	@param p
 * 
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gboolean check_computed_path_feasibility (struct service_t *s, struct compRouteOutputItem_t* p) {	
	float epsilon = 0.0000001;
	struct path_constraints_t* pathCons = get_path_constraints(s);
	gboolean ret = TRUE;
	if (pathCons->latency == TRUE) {
		if ((pathCons->latencyConstraint - p->delay > 0.0) || (fabs(pathCons->latencyConstraint - p->delay) < epsilon)) {
			DEBUG_PC("Computed Path (latency: %f) is feasible wrt Connection Demand: %f", p->delay, pathCons->latencyConstraint);
		}
		else {
			DEBUG_PC("Computed Path (latency: %f) is NOT feasible wrt Connection Demand: %f", p->delay, pathCons->latencyConstraint);
			g_free(pathCons);
			return FALSE;
		}
	}
	// Other constraints...		
	g_free(pathCons);
	return ret;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Sorting the GList Q items by distance 
 * 
 * @param a
 * @param b
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint sort_by_distance (gconstpointer a, gconstpointer b) {
	//DEBUG_PC ("sort by distance a and b");	
	g_assert(a != NULL);
	g_assert(b != NULL);
	
	//DEBUG_PC ("sort by distance a and b");	  
	struct nodeItem_t *node1 = (struct nodeItem_t *)a;
	struct nodeItem_t *node2 = (struct nodeItem_t *)b;
	g_assert (node1);
	g_assert (node2);
	 
	//DEBUG_PC ("a->distance %u; b->distance %u", node1->distance, node2->distance);
	//DEBUG_PC("a->latency: %f; b->latency: %f", node1->latency, node2->latency);
	//1st criteria, sorting by lowest distance
	if (node1->distance > node2->distance)
		return 1;
	else if (node1->distance < node2->distance)
		return 0;
	if (node1->distance == node2->distance) {
		if (node1->latency > node2->latency)
			return 1;
		else if (node1->latency <= node2->latency)
			return 0;
	}
	return 0;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Sorting the GList Q items by distance
 * 
 * @param a
 * @param b
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint sort_by_energy(gconstpointer a, gconstpointer b) {	
	g_assert(a != NULL);
	g_assert(b != NULL);

	//DEBUG_PC ("sort by distance a and b");	  
	struct nodeItem_t* node1 = (struct nodeItem_t*)a;
	struct nodeItem_t* node2 = (struct nodeItem_t*)b;
	g_assert(node1);
	g_assert(node2);
	
	//1st criteria: sorting by lowest distance
	if (node1->distance > node2->distance)
		return 1;
	if (node1->distance < node2->distance)
		return 0;

	// 2nd Criteria: sorting by the lowest energy
	if (node1->power > node2->power)
		return 1;
	if (node1->power < node1->power)
		return 0;

	// 3rd Criteria: by the latency 
	if (node1->latency > node2->latency)
		return 1;
	if (node1->latency <= node2->latency)
		return 0;
	return 0;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Allocate memory for graph
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct graph_t * create_graph () {
	struct graph_t * g = g_malloc0 (sizeof (struct graph_t));
	if (g == NULL) {
		DEBUG_PC ("Memory Allocation Problem");
		exit (-1);
	}
	return g;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Allocate memory for mapNodes
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct map_nodes_t * create_map_node ()	 {
	struct map_nodes_t * mN = g_malloc0 (sizeof (struct map_nodes_t));
	if (mN == NULL) {
		DEBUG_PC ("Memory allocation failed");
		exit (-1);
	}
	return mN;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Look up for the service in the servieList bound to a serviceUUID
 * 
 * @params serviceUUID
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct service_t* get_service_for_computed_path(gchar* serviceUUID) {
	gint i = 0;
	for(GList *listnode = g_list_first(serviceList);
		listnode;
		listnode = g_list_next(listnode), i++) {
			struct service_t* s = (struct service_t*)(listnode->data);
			if (strcmp(s->serviceId.service_uuid, serviceUUID) == 0)
				return s;
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the service type
 * 
 * @param type
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_service_type(guint type) {
	switch (type) {
	case SERVICE_TYPE_UNKNOWN:
			DEBUG_PC("Service Type UNKNOWN");
			break;
		case SERVICE_TYPE_L3NM:
			DEBUG_PC("Service Type L3NM");
			break;
		case SERVICE_TYPE_L2NM:
			DEBUG_PC("Service Type L2NM");
			break;
		case SERVICE_TYPE_TAPI:
			DEBUG_PC("Service Type L2NM");
			break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the port direction
 *
 * @param direction
 *
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_link_port_direction(guint direction) {
	switch (direction) {
		case LINK_PORT_DIRECTION_BIDIRECTIONAL:
			//DEBUG_PC("Bidirectional Port Direction");
			break;
		case LINK_PORT_DIRECTION_INPUT:
			//DEBUG_PC("Input Port Direction");
			break;
		case LINK_PORT_DIRECTION_OUTPUT:
			//DEBUG_PC("Output Port Direction");
			break;
		case LINK_PORT_DIRECTION_UNKNOWN:
			//DEBUG_PC("Unknown Port Direction");
			break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the port termination direction
 *
 * @param direction
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_termination_direction(guint direction) {
	switch (direction) {
	case TERMINATION_DIRECTION_BIDIRECTIONAL:
		//DEBUG_PC("Bidirectional Termination Direction");
		break;
	case TERMINATION_DIRECTION_SINK:
		//DEBUG_PC("Input Termination Direction");
		break;
	case TERMINATION_DIRECTION_SOURCE:
		//DEBUG_PC("Output Termination Direction");
		break;
	case TERMINATION_DIRECTION_UNKNOWN:
		//DEBUG_PC("Unknown Termination Direction");
		break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the termination state
 *
 * @param state 
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_termination_state(guint state)
{
	switch (state) {
	case TERMINATION_STATE_CAN_NEVER_TERMINATE:
		//DEBUG_PC("Can never Terminate");
		break;
	case TERMINATION_STATE_NOT_TERMINATED:
		DEBUG_PC("Not terminated");
		break;
	case TERMINATION_STATE_TERMINATED_SERVER_TO_CLIENT_FLOW:
		DEBUG_PC("Terminated server to client flow");
		break;
	case TERMINATION_STATE_TERMINATED_CLIENT_TO_SERVER_FLOW:
		DEBUG_PC("Terminated client to server flow");
		break;
	case TERMINATION_STATE_TERMINATED_BIDIRECTIONAL:
		//DEBUG_PC("Terminated bidirectional");
		break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the capacity unit
 *
 * @param unit
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_capacity_unit(guint unit) {

	switch (unit) {
		case CAPACITY_UNIT_TB:
			DEBUG_PC("Unit in TB");
			break;
		case CAPACITY_UNIT_TBPS:
			DEBUG_PC("Unit in TB/s");
			break;
		case CAPACITY_UNIT_GB:
			DEBUG_PC("Unit in GB");
			break;
		case CAPACITY_UNIT_GBPS:
			DEBUG_PC("Unit in GB/s");
			break;
		case CAPACITY_UNIT_MB:
			DEBUG_PC("Unit in MB");
			break;
		case CAPACITY_UNIT_MBPS:
			//DEBUG_PC("Unit in MB/s");
			break;
		case CAPACITY_UNIT_KB:
			DEBUG_PC("Unit in KB");
			break;
		case CAPACITY_UNIT_KBPS:
			DEBUG_PC("Unit in KB/s");
			break;
		case CAPACITY_UNIT_GHZ: 
			DEBUG_PC("Unit in GHz");
			break;
		case CAPACITY_UNIT_MHZ:
			DEBUG_PC("Unit in MHz");
			break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Friendly function to log the link forwarding direction
 *
 * @param linkFwDir
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_link_forwarding_direction(guint linkFwDir) {
	switch (linkFwDir) {
		case LINK_FORWARDING_DIRECTION_BIDIRECTIONAL:
			DEBUG_PC("BIDIRECTIONAL LINK FORWARDING DIRECTION");
			break;
		case LINK_FORWARDING_DIRECTION_UNIDIRECTIONAL:
			DEBUG_PC("UNIDIRECTIONAL LINK FORWARDING DIRECTION");
			break;
		case  LINK_FORWARDING_DIRECTION_UNKNOWN:
			DEBUG_PC("UNKNOWN LINK FORWARDING DIRECTION");
			break;
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Search a specific contextUuid element into the contextSet
 *
 * @param contextUuid
 * @param set
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct context_t* find_contextId_in_set(gchar* contextUuid, GList** set) {
	//DEBUG_PC("Checking if contextId: %s in in the ContextSet??", contextUuid);
	gint i = 0;
	for (GList *ln = g_list_first(*set);
		ln;
		ln = g_list_next(ln)){
		struct context_t* c = (struct context_t*)(ln->data);
		//DEBUG_PC("Context Item [%d] Id: %s", i, c->contextId);
		if (strcmp(contextUuid, c->contextId) == 0) {
			//DEBUG_PC("contextId: %s is FOUND in the ContextSet_List", contextUuid);
			return c;
		}
		i++;
	}
	//DEBUG_PC("contextId: %s NOT FOUND in the ContextSet_List", contextUuid);
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Add a specific context uuid into the context set
 *
 * @param contextUuid
 * @param set
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct context_t* add_contextId_in_set(gchar *contextUuid, GList** set) {

	struct context_t* c = g_malloc0(sizeof(struct context_t));
	if (c == NULL) {
		DEBUG_PC("Memory Allocation Failure");
		exit(-1);
	}
	duplicate_string(c->contextId, contextUuid);
	// Add the context into the context set
	//DEBUG_PC("Adding ContextId: %s", contextUuid);
	//DEBUG_PC(" (BEFORE ADDING) Context Set Length: %d", g_list_length(*set));
	*set = g_list_append(*set, c);
	//DEBUG_PC(" (AFTER ADDING) Context Set Length: %d", g_list_length(*set));
	return c;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Find a vertex in a specific graph
 *
 * @param contextUuid
 * @param set
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct vertices_t* find_vertex_in_graph_context(struct graph_t *g, gchar* deviceId) {
	for (gint i = 0; i < g->numVertices; i++) {
		struct vertices_t* v = &(g->vertices[i]);
		if (strcmp(v->verticeId.nodeId, deviceId) == 0) {
			return v;
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Adding a deviceId into a graph
 *
 * @param g
 * @param deviceId
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct vertices_t* add_vertex_in_graph(struct graph_t* g, struct device_t *d) {
	g->numVertices++;
	struct vertices_t* v = &(g->vertices[g->numVertices - 1]);
	duplicate_string(v->verticeId.nodeId, d->deviceId);
	memcpy(&v->power_idle, &d->power_idle, sizeof(gdouble));
	return v;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Construct the graphs (vertices and edges) bound to every individual context
 *
 * @param cSet
 * @param activeFlag
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void build_contextSet_deviceList(GList** cSet, gint activeFlag) {
	// Check every device their endpoints	
	for (GList* listnode = g_list_first(deviceList); 
		listnode; 
		listnode = g_list_next(listnode)) {	
		struct device_t* d = (struct device_t*)(listnode->data);
		//DEBUG_PC("Exploring DeviceId: %s", d->deviceId);

		if ((activeFlag == 1) && (d->operational_status != 2)) {
			// it is only considered devices with operational status enabled, i.e., set to 2
			continue;
		}
		// Check the associated endPoints
		for (gint j = 0; j < d->numEndPoints; j++) {
			struct endPoint_t* eP = &(d->endPoints[j]);
			// Get endPointId (topology, context, device Id and endpoint uuid)
			struct endPointId_t* ePid = &(eP->endPointId);  //end point id
			//DEBUG_PC("   EndPointId: %s || Type: %s", eP->endPointId.endpoint_uuid, d->deviceType);
			//DEBUG_PC("   TopologyId: %s || ContextId: %s", eP->endPointId.topology_id.topology_uuid, eP->endPointId.topology_id.contextId);
			// Add contextId in ContextSet and the deviceId (+endpoint) into the vertex set
			struct context_t *c = find_contextId_in_set(eP->endPointId.topology_id.contextId, cSet);
			if (c == NULL) {
				DEBUG_PC("   contextUuid: %s MUST BE ADDED to ContextSet", eP->endPointId.topology_id.contextId);
				c = add_contextId_in_set(eP->endPointId.topology_id.contextId, cSet);
			}
			// Check if the deviceId and endPointUuid are already considered in the graph of the context c
			struct vertices_t* v = find_vertex_in_graph_context(&c->g, d->deviceId);
			if (v == NULL) {
				//DEBUG_PC("  deviceId: %s MUST BE ADDED to the Context Graph", d->deviceId);
				v = add_vertex_in_graph(&c->g, d);
			}
		}
	}
	//print_contextSet(cSet);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Determine whether a deviceId is in the targetNode list of a specific vertex v
 *
 * @param v
 * @param deviceId
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct targetNodes_t* find_targeted_vertex_in_graph_context(struct vertices_t* v, gchar *deviceId) {
	for (gint k = 0; k < v->numTargetedVertices; k++) {
		struct targetNodes_t* w = &(v->targetedVertices[k]);
		if (strcmp(w->tVertice.nodeId, deviceId) == 0) {
			return w;
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Add a deviceId a targetNode of a specific vertex v
 *
 * @param v
 * @param deviceId
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct targetNodes_t* add_targeted_vertex_in_graph_context(struct vertices_t* v, gchar* bDeviceId) {
	v->numTargetedVertices++;
	struct targetNodes_t* w = &(v->targetedVertices[v->numTargetedVertices - 1]);
	duplicate_string(w->tVertice.nodeId, bDeviceId);
	return w;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Returns the structure of a device endpoint bound to a specific deviceId and endPointId
 *
 * @param devId
 * @param endPointUuid
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct endPoint_t* find_device_tied_endpoint(gchar* devId, gchar* endPointUuid) {
	//DEBUG_PC("devId: %s ePId: %s", devId, endPointUuid);
	for (GList* ln = g_list_first(deviceList);
		ln;
		ln = g_list_next(ln)) {
		struct device_t* d = (struct device_t*)(ln->data);
		if (strcmp(d->deviceId, devId) != 0) {
			continue;
		}
		// Iterate over the endpoints tied to the deviceId
		for (gint j = 0; j < d->numEndPoints; j++) {
			struct endPoint_t* eP = &(d->endPoints[j]);
			//DEBUG_PC("looked endPointId: %s", eP->endPointId.endpoint_uuid);
			if (strcmp(eP->endPointId.endpoint_uuid, endPointUuid) == 0) {
				return eP;
			}
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Adding the edge/linnk in the targetedNodes w list
 *
 * @param w
 * @param l
 * @param activeFlag
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void add_edge_in_targetedVertice_set(struct targetNodes_t* w, struct link_t* l, gint activeFlag) {
	//DEBUG_PC("\t targetedVertex: %s", w->tVertice.nodeId);

	// Check if the activeFlag is 1. If YES, it is only added to the edges as long as the 
	// associated endPoint is in status ENABLED, i.e., with operational status set to 2
	// Get the endpoints (A and Z) of the link l (assumed P2P)
	struct link_endpointId_t* aEndpointId = &(l->linkEndPointId[0]);
	struct link_endpointId_t* zEndpointId = &(l->linkEndPointId[1]);
	// Get the endPoint Information tied to the device bound to aEndPointId
	struct endPoint_t* eP = find_device_tied_endpoint(aEndpointId->deviceId, aEndpointId->endPointId);
	if (eP == NULL) {
		DEBUG_PC("devId: %s endPointUuid: %s NOT in Device List!!--- Weird", aEndpointId->deviceId, aEndpointId->endPointId);
		exit(-1);
	}
	// Check whether the port in that endPoint (eP) is Active upon the activeFlag being SET
	if (activeFlag == 1) {
		if (eP->operational_status != 2) // NOT ENABLED, then discard this link
			return;
	}

	// Add the edge into the graph
	w->numEdges++;
	struct edges_t* e = &(w->edges[w->numEdges - 1]);
	// Copy the link Id UUID
	duplicate_string(e->linkId, l->linkId);
	duplicate_string(e->aNodeId.nodeId, aEndpointId->deviceId);
	duplicate_string(e->aEndPointId, aEndpointId->endPointId);
	duplicate_string(e->aTopologyId, aEndpointId->topology_id.topology_uuid);	
	duplicate_string(e->zNodeId.nodeId, zEndpointId->deviceId);
	duplicate_string(e->zEndPointId, zEndpointId->endPointId);
	duplicate_string(e->zTopologyId, zEndpointId->topology_id.topology_uuid);
	
	//Potential(total) and available capacity
	e->unit = eP->potential_capacity.unit;
	memcpy(&e->totalCap, &eP->potential_capacity.value, sizeof(gdouble));
	memcpy(&e->availCap, &eP->available_capacity.value, sizeof(gdouble));
	// Copy interdomain local/remote Ids
	memcpy(e->interDomain_localId, eP->inter_domain_plug_in.inter_domain_plug_in_local_id, 
		strlen(eP->inter_domain_plug_in.inter_domain_plug_in_local_id));
	memcpy(e->interDomain_remoteId, eP->inter_domain_plug_in.inter_domain_plug_in_remote_id,
		strlen(eP->inter_domain_plug_in.inter_domain_plug_in_remote_id));
	// cost value
	memcpy(&e->cost, &l->cost_characteristics.cost_value, sizeof(gdouble));
	// latency ms
	memcpy(&e->delay, &l->latency_characteristics.fixed_latency, sizeof(gdouble));
	// energy J/bits ~ power
	memcpy(&e->energy, &eP->energyConsumption, sizeof(gfloat));
	
	//DEBUG_PC("Edge - Total/Available Capacity: %f/%f; Cost: %f; Delay: %f, Energy: %f", eP->potential_capacity.value, eP->available_capacity.value,
	//	l->cost_characteristics.cost_value, l->latency_characteristics.fixed_latency, l->energy_link);

	//DEBUG_PC("Graph Edge - Total/Available Capacity: %f/%f; Cost: %f; Delay: %f, Energy: %f", e->totalCap, e->availCap,
	//	e->cost, e->delay, e->energy);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Searching a specific edge/link by the linkId(UUID)
 *
 * @param w
 * @param l
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct edges_t* find_edge_in_targetedVertice_set(struct targetNodes_t* w, struct link_t* l) {		
	for (gint i = 0; i < w->numEdges; i++) {
		struct edges_t* e = &(w->edges[i]);
		if (strcmp(e->linkId, l->linkId) == 0) {
			return e;
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief supporting the construction of the graph per context using the explicit
 * contents/info of the link list
 *
 * @param set
 * @param activeFlag
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void build_contextSet_linklList(GList** set, gint activeFlag) {	
	// for each link in linkList:
	// 1st- Retrieve endpoints A --> B feauture (context Id, device Id, endpoint Id)
	// 2st - In the graph associated to the contextId, check wheter A (deviceId) is in the vertices list
	// o No, this is weird ... exit
	// o Yes, get the other link endpoint (i.e., B) and check whether it exists. If NOT add it, considering
	// all the attributes; Otherwise, check whether the link is different from existing edges between A and B
	gdouble epsilon = 0.1;
	gint j = 0;
	for (GList* ln = g_list_first(linkList);
		ln;
		ln = g_list_next(ln)) {
		struct link_t* l = (struct link_t*)(ln->data);
		j++;

		// link assumed to be P2P A --> B; i.e. 2 endPoints; 1st specifies A and 2nd specifie B
		struct link_endpointId_t* aEndpointId = &(l->linkEndPointId[0]);
		struct topology_id_t* topologyId = &(aEndpointId->topology_id);
		// get the contextId
		gchar contextUuid[UUID_CHAR_LENGTH];
		duplicate_string(contextUuid, topologyId->contextId);
		DEBUG_PC("Link: %s in ContextId: %s", l->linkId, contextUuid);

		// Check first contextUuid exists in the cSet
		//DEBUG_PC("Length of Context: %d", g_list_length(set));
		struct context_t* c = find_contextId_in_set(contextUuid, set);
		if (c == NULL) {
			DEBUG_PC("ContextId: %s does NOT exist... weird", contextUuid);
			exit(-1);
		}

		// get the device ID of A
		gchar aDeviceId[UUID_CHAR_LENGTH];
		duplicate_string(aDeviceId, aEndpointId->deviceId);

		struct graph_t* g = &(c->g); // get the graph associated to the context c
		struct vertices_t* v = find_vertex_in_graph_context(g, aDeviceId);
		if (v == NULL) {
			DEBUG_PC("%s NOT a VERTEX of contextId: %s ... WEIRD", aDeviceId, contextUuid);
			exit(-1);
		}		
		// get the bEndpointId
		struct link_endpointId_t* bEndpointId = &(l->linkEndPointId[1]);
		gchar bDeviceId[UUID_CHAR_LENGTH];
		duplicate_string(bDeviceId, bEndpointId->deviceId);
		DEBUG_PC("[%d] -- Link: %s [%s ==> %s]", j-1, l->linkId, aDeviceId, bDeviceId);
		// Check whether device B is in the targeted Vertices from A (i.e., v)?
		// If not, add B in the targeted vertices B + create the edge and add it
		// If B exist, check whether the explored link/edge is already in the list of edges
		struct targetNodes_t* w = find_targeted_vertex_in_graph_context(v, bDeviceId);
		if (w == NULL) {
			DEBUG_PC("[%s] is PEER of [%s]", bDeviceId, v->verticeId.nodeId);
			w = add_targeted_vertex_in_graph_context(v, bDeviceId);
			add_edge_in_targetedVertice_set(w, l, activeFlag);
		}
		else {
			// w exists, it is needed to check whether the edge (link) should be added
			struct edges_t* e = find_edge_in_targetedVertice_set(w, l);
			if (e == NULL) {
				// Add the link into the list
				add_edge_in_targetedVertice_set(w, l, activeFlag);
			}
			else {
				DEBUG_PC("The link already exists ...");
				continue;
			}
		}
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Create the set of (distinct) contexts with the deviceList and linkList
 *
 * @param cSet
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void build_contextSet(GList** cSet) {
	gint activeFlag = 0; // this means that all the devices/links (regardless they are active or not) are considered

	// devices are tied to contexts, i.e. depending on the contextId of the devices
	build_contextSet_deviceList(cSet, activeFlag);

	DEBUG_PC("Length for the Context Set: %d", g_list_length(*cSet));

	// Once the diverse contexts are created and the devices/endpoints asigned to the 
	// respective graph tied to each context, it is needed to create the edges
	build_contextSet_linklList(cSet, activeFlag);

	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Create the set of (distinct) contexts with the deviceList and linkList with
 * operational status active
 *
 * @param cSet
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void build_contextSet_active(GList** cSet) {
	gint activeFlag = 1; // this means that all the devices (regardless they are active or not) are considered

	// devices are tied to contexts, i.e. depending on the contextId of the devices
	build_contextSet_deviceList(cSet, activeFlag);

	DEBUG_PC("Length for the Context Set: %d", g_list_length(*cSet));

	// Once the diverse contexts are created and the devices/endpoints asigned to the 
	// respective graph tied to each context, it is needed to create the edges
	build_contextSet_linklList(cSet, activeFlag);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Print the contents of the ContextIds
 *
 * @param set
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_contextSet(GList* set) {

	DEBUG_PC("Printing the ContextSet w/ number of Elements: %d", g_list_length(set));

	for (GList* ln = g_list_first(set);
		ln;
		ln = g_list_next(ln)) {
		struct context_t* c = (struct context_t*)(ln->data);
		DEBUG_PC("-------------------------------------------------------------");
		DEBUG_PC(" Context Id: %s", c->contextId);
		DEBUG_PC("-------------------------------------------------------------");

		struct graph_t* g = &(c->g);
		for (gint j = 0; j < g->numVertices; j++) {
			struct vertices_t* v = &(g->vertices[j]);
			DEBUG_PC("  Head Device Id: %s", v->verticeId.nodeId);
			for (gint k = 0; k < v->numTargetedVertices; k++) {
				struct targetNodes_t* w = &(v->targetedVertices[k]);
				DEBUG_PC("  [%d] --- Peer Device Id: %s", k, w->tVertice.nodeId);
				for (gint l = 0; l < w->numEdges; l++) {
					struct edges_t* e = &(w->edges[l]);
					DEBUG_PC("   \t link Id: %s", e->linkId);
					DEBUG_PC("   \t aEndPointId: %s", e->aEndPointId);
					DEBUG_PC("   \t zEndPointId: %s", e->zEndPointId);
					DEBUG_PC("   \t Available Capacity: %f, Latency: %f, Cost: %f", e->availCap, e->delay, e->cost);
					DEBUG_PC("   \t aTopologyId: %s", e->aTopologyId);
					DEBUG_PC("   \t zTopologyId: %s", e->zTopologyId);
				}
			}
		}
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Check whether src and dst PE nodeId of the req are the same
 *
 *	@param r
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint same_src_dst_pe_nodeid(struct service_t* s)
{
	// Check that source PE and dst PE are NOT the same, i.e., different ingress and egress endpoints (iEp, eEp)
	struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[0]);
	struct service_endpoints_id_t* eEp = &(s->service_endpoints_id[1]);

	gchar* iEpUUID = iEp->endpoint_uuid;
	gchar* eEpUUID = eEp->endpoint_uuid;
	gchar* iDevUUID = iEp->device_uuid;
	gchar* eDevUUID = eEp->device_uuid;

	// Compare the device uuids
	if (strcmp(iDevUUID, eDevUUID) != 0) {
		DEBUG_PC("DIFFERENT --- iDevId: %s and eDevId: %s", iDevUUID, eDevUUID);
		return 1;
	}
	// Compare the endpoints (ports)
	if (strcmp(iEpUUID, eEpUUID) != 0) {
		DEBUG_PC("DIFFERENT --- iEpUUID: %s and eEpUUID: %s", iEpUUID, eEpUUID);
		return 1;
	}
	return 0;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Handles issues with the route computation
 *
 *	@param route
 *	@param s
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void comp_route_connection_issue_handler (struct compRouteOutput_t *path, struct service_t *s)
{
	g_assert(path); g_assert(s);

	// Increase the number of computed routes/paths despite there was an issue to be reported		
	path->numPaths++;	
	// Copy the serviceId
	copy_service_id(&(path->serviceId), &(s->serviceId));

	// copy the service endpoints, in general, there will be 2 (point-to-point network connectivity services)
	for (gint i = 0; i < s->num_service_endpoints_id; i++) {
		struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[i]);
		struct service_endpoints_id_t* oEp = &(path->service_endpoints_id[i]);
		copy_service_endpoint_id(oEp, iEp);
	}
	path->num_service_endpoints_id = s->num_service_endpoints_id;
	path->noPathIssue = NO_PATH_CONS_ISSUE;
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief released the allocated memory fo compRouteOutputList_t
 *
 *	@param ro
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void destroy_compRouteOutputList (struct compRouteOutputList_t *ro)
{
	g_assert (ro);	
	g_free (ro);	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief creates a copy of the underlying graph
 *
 *	@param originalGraph
 *	@param destGraph
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void duplicate_graph (struct graph_t *originalGraph, struct graph_t *destGraph)	{
	g_assert (originalGraph); g_assert (destGraph);
	
	destGraph->numVertices = originalGraph->numVertices;
	for (gint i = 0; i < originalGraph->numVertices; i++) {
		struct vertices_t *oVertex = &(originalGraph->vertices[i]);
		struct vertices_t *dVertex = &(destGraph->vertices[i]);
		dVertex->numTargetedVertices = oVertex->numTargetedVertices;		
		duplicate_node_id (&oVertex->verticeId, &dVertex->verticeId);
		memcpy(&dVertex->power_idle, &oVertex->power_idle, sizeof(gdouble));
		
		for (gint j = 0; j < oVertex->numTargetedVertices; j++)	{
			struct targetNodes_t *oTargetedVertex = &(oVertex->targetedVertices[j]);
			struct targetNodes_t *dTargetedVertex = &(dVertex->targetedVertices[j]);
			duplicate_node_id (&oTargetedVertex->tVertice, &dTargetedVertex->tVertice);
			dTargetedVertex->numEdges = oTargetedVertex->numEdges;
			
			for (gint k = 0; k < oTargetedVertex->numEdges; k++) {
				struct edges_t *oEdge = &(oTargetedVertex->edges[k]);
				struct edges_t *dEdge = &(dTargetedVertex->edges[k]);
				duplicate_edge (dEdge, oEdge);						
			}
		}	
	}	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to retrieve from the graph the edge instance associated to the
 * pathLink (pL)
 *
 *	@param pL
 *	@parma g
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct edges_t* get_edge_from_graph_by_linkId(struct pathLink_t* pL, struct graph_t* g) {
	g_assert(pL);
	g_assert(g);

	for (gint i = 0; i < g->numVertices; i++) {
		struct vertices_t* v = &(g->vertices[i]);
		for (gint j = 0; j < v->numTargetedVertices; j++) {
			struct targetNodes_t* tv = &(v->targetedVertices[j]);
			for (gint k = 0; k < tv->numEdges; k++) {
				struct edges_t* e = &(tv->edges[k]);
				if (strcmp(e->linkId, pL->linkId) == 0) {
					return e;
				}
			}		
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to retrieve from the graph the reverse edge (rev_e) associated to an edge (e)
 *
 *	@param e
 *	@parma g
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
struct edges_t* get_reverse_edge_from_the_graph(struct edges_t* e, struct graph_t* g) {
	g_assert(e);
	g_assert(g);

	for (gint i = 0; i < g->numVertices; i++) {
		struct vertices_t* v = &(g->vertices[i]);
		// Check Route Element zNodeId with the v->verticeId
		if (compare_node_id(&e->zNodeId, &v->verticeId) != 0)
			continue;
		// Check Route Element zNodeis with any of reachable targeted vertices from v
		gboolean foundTargVert = FALSE;
		gint indexTargVert = -1;
		for (gint j = 0; j < v->numTargetedVertices; j++) {
			struct targetNodes_t* tv = &(v->targetedVertices[j]);
			if (compare_node_id(&e->aNodeId, &tv->tVertice) == 0)
			{
				foundTargVert = TRUE;
				indexTargVert = j;
				break;
			}
		}
		if (foundTargVert == FALSE) {
			 continue;
		}			

		// The targeted vertice is found, then check matching with the endpoints
		struct targetNodes_t* tv = &(v->targetedVertices[indexTargVert]);
		for (gint k = 0; k < tv->numEdges; k++) {
			struct edges_t* rev_e = &(tv->edges[k]);
			if ((strcmp(rev_e->aEndPointId, e->zEndPointId) == 0) &&
				(strcmp(rev_e->zEndPointId, e->aEndPointId) == 0)) {
				return rev_e;
			}				
		}
	}
	return NULL;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to reflect in the graph the assigned/allocated resources contained in the path p
 * 	considering the needs (e.g., bandwidth) of service s
 *
 *	@param p
 *	@param s
 *	@parma g
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void allocate_graph_resources (struct path_t *p, struct service_t *s, struct graph_t *g)
{
	g_assert (p); g_assert (s); g_assert (g);
	// Retrieve the requested bw by the service
	struct path_constraints_t* pathCons = get_path_constraints(s);

	for (gint i = 0; i < p->numPathLinks; i++) {
		struct pathLink_t* pL = &(p->pathLinks[i]);
		// get the edge associated to the linkId in the graph
		struct edges_t* e = get_edge_from_graph_by_linkId(pL, g);
		if (e == NULL) {
			DEBUG_PC("The linkId: %s is NOT found in the Graph!!!", pL->linkId);
			exit(-1);
		}
		//Update the availBw in the edge
		gdouble resBw = e->availCap - pathCons->bwConstraint;
		DEBUG_PC("Updating the Avail Bw @ edge/link: %s", e->linkId);
		DEBUG_PC("Initial avaiCap @ e/link: %f, demanded Bw: %f, resulting Avail Bw: %f", e->availCap, pathCons->bwConstraint, resBw);
		memcpy(&e->availCap, &resBw, sizeof(gdouble));
		DEBUG_PC("Final e/link avail Bw: %f", e->availCap);	
	}
	g_free(pathCons);	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to reflect in the graph the assigned/allocated resources contained in the reverse direction of the path p
 * 	considering the needs (e.g., bandwidth) of service s
 *
 *	@param p
 *	@param s
 *	@parma g
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void allocate_graph_reverse_resources(struct path_t* p, struct service_t * s, struct graph_t* g)
{
	g_assert(p); g_assert(s); g_assert(g);

	struct path_constraints_t* pathCons = get_path_constraints(s);
	for (gint i = 0; i < p->numPathLinks; i++) {
		struct pathLink_t* pL = &(p->pathLinks[i]);
		struct edges_t* e = get_edge_from_graph_by_linkId(pL, g);
		if (e == NULL) {
			DEBUG_PC("The linkId: %s is NOT found in the Graph!!!", pL->linkId);
			exit(-1);
		}
		struct edges_t* rev_e = get_reverse_edge_from_the_graph(e, g);
		if (rev_e == NULL) {
			DEBUG_PC("the reverse edge of linkId: %s is NOT found in the Graph!!!", pL->linkId);
			exit(-1);
		}
		//Update the availBw in the edge
		gdouble resBw = rev_e->availCap - pathCons->bwConstraint;
		DEBUG_PC("Updating the Avail Bw @ reverse edge/link: %s", rev_e->linkId);
		DEBUG_PC("Initial avaiCap @ reverse edge e/link: %f, demanded Bw: %f, resulting Avail Bw: %f", rev_e->availCap, pathCons->bwConstraint, resBw);
		memcpy(&rev_e->availCap, &resBw, sizeof(gdouble));
		DEBUG_PC("Final reverse edge e/link avail Bw: %f", rev_e->availCap);
	}
	g_free(pathCons);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Function used to printall the computed paths for the requested network connectivity services
 *
 *	@param routeList
 *
 * 	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void print_path_connection_list(struct compRouteOutputList_t* routeList) {
	g_assert(routeList);
	for (gint i = 0; i < routeList->numCompRouteConnList; i++) {
		DEBUG_PC("==================== Service instance: %d ===================", i);
		struct compRouteOutput_t* rO = &(routeList->compRouteConnection[i]);
		DEBUG_PC("num service endpoints: %d", rO->num_service_endpoints_id);
		struct serviceId_t* s = &(rO->serviceId);
		DEBUG_PC("ContextId: %s, ServiceId: %s", s->contextId, s->service_uuid);
		DEBUG_PC("ingress - %s[%s]", rO->service_endpoints_id[0].device_uuid, 
			rO->service_endpoints_id[0].endpoint_uuid);
		DEBUG_PC("egress - %s [%s]", rO->service_endpoints_id[1].device_uuid,
			rO->service_endpoints_id[1].endpoint_uuid);

		if (rO->noPathIssue == NO_PATH_CONS_ISSUE) {
			DEBUG_PC("NO PATH SUCCESSFULLY COMPUTED");
			continue;
		}
		// Path
		DEBUG_PC("Number of paths: %d", rO->numPaths);
		for (gint j = 0; j < rO->numPaths; j++) {
			struct path_t* p = &(rO->paths[j]);
			print_path_t(p);
		}
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief update statistics for the path computation operations
 *
 *  @param routeConnList
 *	@param d
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void update_stats_path_comp(struct compRouteOutputList_t* routeConnList, struct timeval d, gint numSuccesPathComp, gint numPathCompIntents) {
	g_assert(routeConnList);

	total_path_comp_time.tv_sec = total_path_comp_time.tv_sec + d.tv_sec;
	total_path_comp_time.tv_usec = total_path_comp_time.tv_usec + d.tv_usec;
	total_path_comp_time = tv_adjust(total_path_comp_time);

	gdouble path_comp_time_msec = (((total_path_comp_time.tv_sec) * 1000) + ((total_path_comp_time.tv_usec) / 1000));
	gdouble av_alg_comp_time = ((path_comp_time_msec / numSuccesPathComp));
	DEBUG_PC("\t --- STATS PATH COMP ----");
	DEBUG_PC("Succesfully Comp: %d | Path Comp Requests: %d", numSuccesPathComp, numPathCompIntents);
	DEBUG_PC("AV. PATH COMP ALG. TIME: %f ms", av_alg_comp_time);

	gint i = 0;
	for (GList* listnode = g_list_first(serviceList);
		listnode;
		listnode = g_list_next(listnode), i++) {
		struct service_t* s = (struct service_t*)(listnode->data);
		char* eptr;
		for (gint j = 0; j < s->num_service_constraints; j++) {
			struct constraint_t* constraints = &(s->constraints[j]);
			if (strncmp((const char*)(constraints->constraint_type), "bandwidth", 9) == 0) {
				totalReqBw += (gdouble)(strtod((char*)constraints->constraint_value, &eptr));
			}
		}
	}

	for (gint k = 0; k < routeConnList->numCompRouteConnList; k++) {
		struct compRouteOutput_t* rO = &(routeConnList->compRouteConnection[k]);
		if (rO->noPathIssue == NO_PATH_CONS_ISSUE) {
			continue;
		}
		// Get the requested service bw bound to that computed path
		struct path_t* p = &(rO->paths[0]);
		struct service_t* s = get_service_for_computed_path(rO->serviceId.service_uuid);
		if (s == NULL) {
			DEBUG_PC("Weird the service associated to a path is not found");
			exit(-1);
		}
		for (gint l = 0; l < s->num_service_constraints; l++) {
			struct constraint_t* constraints = &(s->constraints[l]);
			char* eptr;
			if (strncmp((const char*)(constraints->constraint_type), "bandwidth", 9) == 0) {
				totalServedBw += (gdouble)(strtod((char*)constraints->constraint_value, &eptr));
			}
		}
	}
	gdouble avServedRatio = totalServedBw / totalReqBw;
	DEBUG_PC("AV. Served Ratio: %f", avServedRatio);
	gdouble avBlockedBwRatio = (gdouble)(1.0 - avServedRatio);
	DEBUG_PC("AV. BBE: %f", avBlockedBwRatio);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate active service	path
 *
 *  @param actServPath
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_active_service_path(struct activeServPath_t* actServPath) {
	g_assert(actServPath);
	g_free(actServPath);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate active service
 *
 *  @param actService
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_active_service(struct activeService_t* actService) {
	g_assert(actService);
	g_list_free_full(g_steal_pointer(&actService->activeServPath), (GDestroyNotify)destroy_active_service_path);
	g_free(actService);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate a requested service 
 *
 *  @param s
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_requested_service(struct service_t* s) {
	g_assert(s);
	g_free(s);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate a device
 *
 *  @param d
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_device(struct device_t* d) {
	g_assert(d);
	g_free(d);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate a link	from the linkList
 *
 *  @param d
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_link(struct link_t* l) {
	g_assert(l);
	g_free(l);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Eliminate a context from the contextSet
 *
 *  @param d
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void destroy_context(struct context_t* c) {
	g_assert(c);
	g_free(c);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief Excecution Dijkstra algorithm
 *
 *  @param srcMapIndex
 *  @param dstMapIndex
 *	@param g
 *	@param s
 *  @param mapNodes
 *  @param SN
 *  @param RP
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void dijkstra(gint srcMapIndex, gint dstMapIndex, struct graph_t* g, struct service_t* s, 
	struct map_nodes_t* mapNodes, struct nodes_t* SN, struct compRouteOutputItem_t* RP,
	guint arg) {
	g_assert(s);g_assert(g);

	// Set params into mapNodes related to the source nodes of the request
	mapNodes->map[srcMapIndex].distance = 0.0;
	mapNodes->map[srcMapIndex].latency = 0.0;
	mapNodes->map[srcMapIndex].avaiBandwidth = 0.0;
	mapNodes->map[srcMapIndex].power = 0.0;

	// Initialize the set Q and S
	GList *S = NULL, *Q = NULL;
	gint indexVertice = -1;

	//  Add the source into the Q
	struct nodeItem_t* nodeItem = g_malloc0(sizeof(struct nodeItem_t));
	if (nodeItem == NULL) {
		DEBUG_PC("memory allocation failed\n");
		exit(-1);
	}
	// initialize some nodeItem attributes
	nodeItem->distance = 0.0;
	nodeItem->latency = 0.0;
	nodeItem->power = 0.0;
	duplicate_node_id(&mapNodes->map[srcMapIndex].verticeId, &nodeItem->node);

	// Select the optimization process
	if (arg & ENERGY_EFFICIENT_ARGUMENT)
		Q = g_list_insert_sorted(Q, nodeItem, sort_by_energy);
	// more "if" according to different optimization criteria ...
	else
		Q = g_list_insert_sorted(Q, nodeItem, sort_by_distance);

	// Check whether there is spurNode (SN) and rootPath (RP)
	if (SN != NULL && RP != NULL) {
		struct routeElement_t* re;
		for (gint j = 0; j < RP->numRouteElements; j++) {
			// Get the source and target Nodes of the routeElement within the rootPath
			re = &RP->routeElement[j];
			DEBUG_PC("root Link: aNodeId: %s (%s) --> zNodeiId: %s (%s)", re->aNodeId.nodeId, re->aEndPointId, re->zNodeId.nodeId, re->zEndPointId);

			// if ingress of the root link (aNodeId) is the spurNode, then stops
			if (compare_node_id(&re->aNodeId, SN) == 0) {
				DEBUG_PC("Ingress Node rootLink %s = spurNode %s; STOP exploring rootPath (RP)", re->aNodeId.nodeId, SN->nodeId);
				break;
			}
			// Extract from Q
			GList* listnode = g_list_first(Q);
			struct nodeItem_t* node = (struct nodeItem_t*)(listnode->data);
			Q = g_list_remove(Q, node);

			indexVertice = graph_vertice_lookup(node->node.nodeId, g);
			g_assert(indexVertice >= 0);

			// Get the indexTargetedVertice
			gint indexTVertice = -1;
			indexTVertice = graph_targeted_vertice_lookup(indexVertice, re->zNodeId.nodeId, g);
			gint done = check_link(node, indexVertice, indexTVertice, g, s, &S, &Q, mapNodes, arg);
			(void)done;
			// Add to the S list
			S = g_list_append(S, node);
		}
		// Check that the first node in Q set is SpurNode, otherwise something went wrong ...
		if (compare_node_id(&re->aNodeId, SN) != 0) {
			DEBUG_PC ("root Link: aNodeId: %s is NOT the spurNode: %s -- something wrong", re->aNodeId.nodeId, SN->nodeId);
			g_list_free_full(g_steal_pointer(&S), g_free);
			g_list_free_full(g_steal_pointer(&Q), g_free);
			return;
		}
	}
	while (g_list_length(Q) > 0) {
		//Extract from Q set
		GList* listnode = g_list_first(Q);
		struct nodeItem_t* node = (struct nodeItem_t*)(listnode->data);
		Q = g_list_remove(Q, node);
		DEBUG_PC("Q length: %d", g_list_length(Q));
		DEBUG_PC("Explored DeviceId: %s", node->node.nodeId);

		// scan all the links from u within the graph
		indexVertice = graph_vertice_lookup(node->node.nodeId, g);
		g_assert(indexVertice >= 0);

		// Check the targeted vertices from u
		for (gint i = 0; i < g->vertices[indexVertice].numTargetedVertices; i++) {
			gint done = check_link(node, indexVertice, i, g, s, &S, &Q, mapNodes, arg);
			(void)done;
		}
		// Add node into the S Set
		S = g_list_append(S, node);
		//DEBUG_PC ("S length: %d", g_list_length (S));              
	}
	g_list_free_full(g_steal_pointer(&S), g_free);
	g_list_free_full(g_steal_pointer(&Q), g_free);
	return;
}

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief KSP computation using Dijkstra algorithm
 *
 *  @param pred
 *  @param g
 *	@param s
  *	@param SN
 *	@param RP
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint ksp_comp(struct pred_t* pred, struct graph_t* g, struct service_t* s,
	struct nodes_t* SN, struct compRouteOutputItem_t* RP, 
	struct map_nodes_t* mapNodes, guint arg) {
	g_assert(pred); g_assert(g); g_assert(s);

	DEBUG_PC("SOURCE: %s --> DESTINATION: %s", s->service_endpoints_id[0].device_uuid, 
								s->service_endpoints_id[1].device_uuid);

	// Check the both ingress src and dst endpoints are in the graph
	gint srcMapIndex = get_map_index_by_nodeId(s->service_endpoints_id[0].device_uuid, mapNodes);
	if (srcMapIndex == -1) {
		DEBUG_PC("ingress DeviceId: %s NOT in G", s->service_endpoints_id[0].device_uuid);
		return -1;
	}
	
	gint dstMapIndex = get_map_index_by_nodeId(s->service_endpoints_id[1].device_uuid, mapNodes);
	if (dstMapIndex == -1) {
		DEBUG_PC("egress DeviceId: %s NOT in G", s->service_endpoints_id[1].device_uuid);
		return -1;
	}

	//DEBUG_PC("srcMapIndex: %d (node: %s)", srcMapIndex, mapNodes->map[srcMapIndex].verticeId.nodeId);
	//DEBUG_PC("dstMapIndex: %d (node: %s)", dstMapIndex, mapNodes->map[dstMapIndex].verticeId.nodeId);

	// Compute the shortest path route
	dijkstra(srcMapIndex, dstMapIndex, g, s, mapNodes, SN, RP, arg);

	// Check that a feasible solution in term of latency and bandwidth is found
	gint map_dstIndex = get_map_index_by_nodeId(s->service_endpoints_id[1].device_uuid, mapNodes);
	struct map_t* dest_map = &mapNodes->map[map_dstIndex];
	if (!(dest_map->distance < INFINITY_COST)) {
		DEBUG_PC("DESTINATION: %s NOT reachable", s->service_endpoints_id[1].device_uuid);
		return -1;
	}

	DEBUG_PC("AvailBw @ %s is %f", dest_map->verticeId.nodeId, dest_map->avaiBandwidth);
	// Check that the computed available bandwidth is larger than 0.0
	if (dest_map->avaiBandwidth <= (gfloat)0.0) {
		DEBUG_PC("DESTINATION %s NOT REACHABLE", s->service_endpoints_id[1].device_uuid);
		return -1;
	}
	DEBUG_PC("DESTINATION %s REACHABLE", s->service_endpoints_id[1].device_uuid);
	// Handle predecessors
	build_predecessors(pred, s, mapNodes);
	return 1;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief set the path parameters (e.g., latency, cost, power, ...) to an under-constructed
 * path from the computed map vertex
 *
 *  @param p
 *  @param mapV
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void set_path_attributes(struct compRouteOutputItem_t* p, struct map_t* mapV) {
	g_assert(p); g_assert(mapV);
	memcpy(&p->cost, &mapV->distance, sizeof(gdouble));
	memcpy(&p->availCap, &mapV->avaiBandwidth, sizeof(mapV->avaiBandwidth));
	memcpy(&p->delay, &mapV->latency, sizeof(mapV->latency));
	memcpy(&p->power, &mapV->power, sizeof(gdouble));
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_tools.c
 * 	@brief K-CSPF algorithm execution (YEN algorithm)
 *
 *  @param s
 *  @param path
 *  @param g
 *  @param optimization_flag
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void alg_comp(struct service_t* s, struct compRouteOutput_t* path, struct graph_t* g, guint arg) {
	g_assert(s); g_assert(path); g_assert(g);

	// Check if the service specifies a nuumber of K paths to be explored/computed for the 
	// service. If not, compute that number; otherwise set the max number of explored
	// computed paths to MAX_KSP_VALUE
	guint maxK = 0;
	if(s->kPaths_inspected == 0) {
		maxK = MAX_KSP_VALUE;
	}
	else {
		maxK = s->kPaths_inspected;
	}
	DEBUG_PC("The KSP considers K: %d", maxK);
	
	// create map of devices/nodes to handle the path computation using the context
	struct map_nodes_t* mapNodes = create_map_node();
	build_map_node(mapNodes, g);

	// predecessors to store the computed path    
	struct pred_t* predecessors = create_predecessors();
	struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[0]);
	struct service_endpoints_id_t* eEp = &(s->service_endpoints_id[1]);

	DEBUG_PC("=======================================================================================");
	DEBUG_PC("STARTING PATH COMP FOR %s[%s] --> %s[%s]", iEp->device_uuid, iEp->endpoint_uuid, eEp->device_uuid, eEp->endpoint_uuid);

	// Compute the 1st KSP path
	gint done = ksp_comp(predecessors, g, s, NULL, NULL, mapNodes, arg);
	if (done == -1) {
		DEBUG_PC("NO PATH for %s[%s] --> %s[%s]", iEp->device_uuid, iEp->endpoint_uuid, eEp->device_uuid, eEp->endpoint_uuid);
		comp_route_connection_issue_handler(path, s);
		g_free(mapNodes); g_free(predecessors);
		return;
	}

	// Construct the path from the computed predecessors
	struct compRouteOutputItem_t* p = create_path_item();
	//print_predecessors(predecessors);
	build_path(p, predecessors, s);
	gint indexDest = get_map_index_by_nodeId(eEp->device_uuid, mapNodes);
	struct map_t* dst_map = &mapNodes->map[indexDest];
	// Get the delay and cost
	set_path_attributes(p, dst_map);		

	// Add the computed path, it may be a not feasible path, but at the end it is
	// checked all the feasible paths, and select the first one
	print_path(p);
	
	// Copy the serviceId
	copy_service_id(&path->serviceId, &s->serviceId);
	// copy the service endpoints, in general, there will be 2 (point-to-point network connectivity services)
	for (gint i = 0; i < s->num_service_endpoints_id; i++) {
		struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[i]);
		struct service_endpoints_id_t* oEp = &(path->service_endpoints_id[i]);
		copy_service_endpoint_id(oEp, iEp);
	}
	path->num_service_endpoints_id = s->num_service_endpoints_id;

	DEBUG_PC("COMPUTE UP TO K Feasible Paths A[%d]", maxK);	
	// Create A and B sets of paths to handle the YEN algorithm
	struct path_set_t *A = create_path_set(), *B = create_path_set();
	// Add 1st Computed path into A->paths[0]	
	duplicate_path(p, &A->paths[0]);
	A->numPaths++;
	g_free(predecessors); g_free(p);
	for (gint k = 1; k < maxK; k++) {
		DEBUG_PC("*************************** kth (%d) ***********************************", k);
		struct compRouteOutputItem_t* p = create_path_item();
		duplicate_path(&A->paths[k - 1], p);
		// The spurNode ranges from near-end node of the first link to the near-end of the last link forming the kth path
		gint i = 0;
		struct compRouteOutputItem_t* rootPath = create_path_item();
		for (i = 0; i < p->numRouteElements; i++) {
			struct nodes_t *spurNode = create_node(), *nextSpurNode = create_node();
			struct routeElement_t* re = &(p->routeElement[i]);
			// Create predecessors to store the computed path
			struct pred_t* predecessors = create_predecessors();
			// Clear previous mapNodes, i.e. create it again
			g_free(mapNodes);
			mapNodes = create_map_node();
			build_map_node(mapNodes, g);
			struct nodes_t* n = &re->aNodeId;
			duplicate_node_id(n, spurNode);
			n = &re->zNodeId;
			duplicate_node_id(n, nextSpurNode);
			DEBUG_PC("spurNode: %s --> nextSpurNode: %s", spurNode->nodeId, nextSpurNode->nodeId);

			// rootPath contains a set of links of A[k-1] from the source Node till the SpurNode -> NextSpurNode
			// Example: A[k-1] = {L1, L2, L3, L4}, i.e. " Node_a -- L1 --> Node_b -- L2 --> Node_c -- L3 --> Node_d -- L4 --> Node_e "
			// E.g., for the ith iteration if the spurNode = Node_c and NextSpurNode = Node_d; then rootPath = {L1, L2, L3}			
			add_routeElement_path_back(re, rootPath);
			DEBUG_PC("\n");
			DEBUG_PC("^^^^^^^rootPath^^^^^^^");
			print_path(rootPath);

			// For all existing and computed paths p in A check if from the source to the NextSpurNode
			// the set of links matches with those contained in the rootPath
			// If YES, remove from the auxiliary graph the next link in p from NextSpurNode
			// Otherwise do nothing 
			struct graph_t* gAux = create_graph();
			duplicate_graph(g, gAux);
			// Modified graph
			modify_targeted_graph(gAux, A, rootPath, spurNode);

			// Trigger the computation of the path from src to dst constrained to traverse all the links from src 
			// to spurNode contained into rootPath over the resulting graph			
			if (ksp_comp(predecessors, gAux, s, spurNode, rootPath, mapNodes, arg) == -1) {
				DEBUG_PC("FAILED SP from %s via spurNode: %s to %s", iEp->device_uuid, spurNode->nodeId, eEp->device_uuid);
				g_free(nextSpurNode); g_free(spurNode);
				g_free(gAux); g_free(predecessors);
				continue;
			}
			DEBUG_PC("SUCCESFUL SP from %s via spurNode: %s to %s", iEp->device_uuid, spurNode->nodeId, eEp->device_uuid);
			// Create the node list from the predecessors
			struct compRouteOutputItem_t* newKpath = create_path_item();
			build_path(newKpath, predecessors, s);
			DEBUG_PC("new K (for k: %d) Path is built", k);
			gint indexDest = get_map_index_by_nodeId(eEp->device_uuid, mapNodes);
			struct map_t* dst_map = &mapNodes->map[indexDest];
			set_path_attributes(newKpath, dst_map);
			DEBUG_PC("New PATH (@ kth: %d) ADDED to B[%d] - {Path Cost: %f, e2e latency: %f, bw: %f, Power: %f ", k, B->numPaths, newKpath->cost, 
													newKpath->delay, newKpath->availCap, newKpath->power);
			// Add the computed kth SP to the heap B
			duplicate_path(newKpath, &B->paths[B->numPaths]);
			B->numPaths++;
			DEBUG_PC("Number of B paths: %d", B->numPaths);

			g_free(newKpath); g_free(nextSpurNode); g_free(spurNode);
			g_free(gAux); g_free(predecessors);
		}
		// If B is empty then stops
		if (B->numPaths == 0) {
			DEBUG_PC("B does not have any path ... the stops kth computation");
			break;
		}

		// Sort the potential B paths according to different optimization parameters
		sort_path_set(B, arg);
		// Add the lowest path into A[k]		
		DEBUG_PC("-------------------------------------------------------------");
		DEBUG_PC("Append SP for B[0] to A[%d] --- Cost: %f, Latency: %f, Power: %f", A->numPaths, B->paths[0].cost, 
																				B->paths[0].delay, B->paths[0].power);
		duplicate_path(&B->paths[0], &A->paths[A->numPaths]);
		A->numPaths++;
		DEBUG_PC("A Set size: %d", A->numPaths);
		DEBUG_PC("-------------------------------------------------------------");

		// Remove/Pop front element from the path set B (i.e. remove B[0])
		pop_front_path_set(B);
		DEBUG_PC("B Set Size: %d", B->numPaths);
	}

	// Copy the serviceId
	copy_service_id(&path->serviceId, &s->serviceId);
	// copy the service endpoints, in general, there will be 2 (point-to-point network connectivity services)
	for (gint m = 0; m < s->num_service_endpoints_id; m++) {
		struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[m]);
		struct service_endpoints_id_t* oEp = &(path->service_endpoints_id[m]);
		copy_service_endpoint_id(oEp, iEp);
	}
	path->num_service_endpoints_id = s->num_service_endpoints_id;

	// Print all the paths i A
	for (gint h = 0; h < A->numPaths; h++) {
		DEBUG_PC("================== A[%d] =======================", h);
		print_path(&A->paths[h]);
	}
	DEBUG_PC("Number of paths: %d", path->numPaths);
	// For all the computed paths in A, pick the one being feasible wrt the service constraints
	for (gint ksp = 0; ksp < A->numPaths; ksp++) {
		if (ksp >= s->kPaths_returned) {
			DEBUG_PC("Number Requested/returned paths (%d) REACHED - STOP", ksp);
			break;
		}
		gdouble feasibleRoute = check_computed_path_feasibility(s, &A->paths[ksp]);
		if (feasibleRoute == TRUE) {
			DEBUG_PC("A[%d] available: %f, pathCost: %f; latency: %f, Power: %f", ksp, A->paths[ksp].availCap, 
											A->paths[ksp].cost, A->paths[ksp].delay, A->paths[ksp].power);
			struct compRouteOutputItem_t* pathaux = &A->paths[ksp];
			path->numPaths++;
			struct path_t* targetedPath = &path->paths[path->numPaths - 1];
			duplicate_path_t(pathaux, targetedPath);
			print_path_t(targetedPath);
			//remove_path_set(A);
			//remove_path_set(B);
			//return;
		}
	}
	remove_path_set(A);
	remove_path_set(B);
	// At least 1 out (K) paths was found, then K-SP succeded
	if (path->numPaths > 0) {
		DEBUG_PC("K-SP succeeded");
		return;
	}
	// No paths found --> Issue	
	DEBUG_PC("K-SP failed!!!");
	comp_route_connection_issue_handler(path, s);
	return;
}

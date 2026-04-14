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

#include "pathComp_log.h"
#include "pathComp_tools.h"
#include "pathComp_sp.h"

// Global Variables
GList* contextSet;

///////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_sp.c
 * 	@brief handling the Dijkstra algorithm
 *
 *  @param pred
 *  @param g
 *	@param s
 *  @param mapNodes
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint computation(struct pred_t* pred, struct graph_t* g, struct service_t* s, struct map_nodes_t* mapNodes) {
	g_assert(pred);
	g_assert(g);
	g_assert(s);

	// Check the both ingress src and dst endpoints are in the graph
	gint srcMapIndex = get_map_index_by_nodeId(s->service_endpoints_id[0].device_uuid, mapNodes);
	if (srcMapIndex == -1) {
		DEBUG_PC("ingress DeviceId: %s NOT in the graph", s->service_endpoints_id[0].device_uuid);
		return -1;
	}

	gint dstMapIndex = get_map_index_by_nodeId(s->service_endpoints_id[1].device_uuid, mapNodes);
	if (dstMapIndex == -1) {
		DEBUG_PC("egress DeviceId: %s NOT in the graph", s->service_endpoints_id[1].device_uuid);
		return -1;
	}

	// Compute the shortest path
	dijkstra(srcMapIndex, dstMapIndex, g, s, mapNodes, NULL, NULL, 0x00000000);

	// Check that a feasible solution in term of latency and bandwidth is found
	gint map_dstIndex = get_map_index_by_nodeId(s->service_endpoints_id[1].device_uuid, mapNodes);
	struct map_t* dest_map = &mapNodes->map[map_dstIndex];
	if (!(dest_map->distance < INFINITY_COST)) {
		DEBUG_PC("destination: %s NOT reachable", s->service_endpoints_id[1].device_uuid);
		return -1;
	}

	DEBUG_PC("AvailBw @ %s is %f", dest_map->verticeId.nodeId, dest_map->avaiBandwidth);
	// Check that the computed available bandwidth is larger than 0.0
	if (dest_map->avaiBandwidth <= (gfloat)0.0) {
		DEBUG_PC("dst: %s NOT REACHABLE", s->service_endpoints_id[1].device_uuid);
		return -1;
	}
	DEBUG_PC("dst: %s REACHABLE", s->service_endpoints_id[1].device_uuid);
	// Handle predecessors
	build_predecessors(pred, s, mapNodes);

	return 1;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_sp.c
 * 	@brief CSPF algorithm execution
 *
 *  @param s
 *  @param path
 *  @param g
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void computation_shortest_path(struct service_t* s, struct compRouteOutput_t* path, struct graph_t* g) {
	g_assert(s);
	g_assert(path);
	g_assert(g);

	// create map of devices / nodes to handle the path computation using the context
	struct map_nodes_t *mapNodes = create_map_node();
	build_map_node(mapNodes, g);

	// predecessors to store the computed path    
	struct pred_t* predecessors = create_predecessors();

	struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[0]);
	struct service_endpoints_id_t* eEp = &(s->service_endpoints_id[1]);

	// SP computation
	gint done = computation(predecessors, g, s, mapNodes);
	if (done == -1) {
		DEBUG_PC("NO PATH FOUND %s[%s] ---> %s[%s]", iEp->device_uuid, iEp->endpoint_uuid, eEp->device_uuid, eEp->endpoint_uuid);
		comp_route_connection_issue_handler(path, s);
		g_free(mapNodes); g_free(predecessors);
		return;
	}

	// Construct the path from the computed predecessors
	struct compRouteOutputItem_t* p = create_path_item();
	//print_predecessors(predecessors);
	build_path(p, predecessors, s);
	//DEBUG_PC ("Path is constructed");

	gint indexDest = get_map_index_by_nodeId(eEp->device_uuid, mapNodes);
	struct map_t* dst_map = &mapNodes->map[indexDest]; 	
	set_path_attributes(p, dst_map);
	DEBUG_PC("Computed Path Avail Bw: %f, Path Cost: %f, latency: %f", p->availCap, p->cost, p->delay);
	print_path(p);

	gboolean feasibleRoute = check_computed_path_feasibility(s, p);
	if (feasibleRoute == TRUE) {
		DEBUG_PC("SP Feasible");
		print_path(p);
		path->numPaths++;

		// Copy the serviceId
		DEBUG_PC("contextId: %s", s->serviceId.contextId);
		copy_service_id(&path->serviceId, &s->serviceId);

		// copy the service endpoints, in general, there will be 2 (point-to-point network connectivity services)
		for (gint i = 0; i < s->num_service_endpoints_id; i++) {
			struct service_endpoints_id_t* iEp = &(s->service_endpoints_id[i]);
			struct service_endpoints_id_t* oEp = &(path->service_endpoints_id[i]);
			copy_service_endpoint_id(oEp, iEp);
		}
		path->num_service_endpoints_id = s->num_service_endpoints_id;

		// Copy the computed path
		struct path_t* targetedPath = &(path->paths[path->numPaths - 1]);
		duplicate_path_t(p, targetedPath);
		print_path_t(targetedPath);
		g_free(predecessors);
		g_free(p);
		g_free(mapNodes);
		return;
	}
	DEBUG_PC("SP FAILED!!!");
	comp_route_connection_issue_handler(path, s);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_sp.c
 * 	@brief Iterates over the list of network connectivity service requests
 * to compute their own paths fulfilling the constraints
 *
 *  @param outputList
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
void sp_execution_services(struct compRouteOutputList_t* oPathList) {
	g_assert(oPathList);	
	// Check at least there is a service to be processed 
	if (g_list_length(serviceList) == 0) {
		DEBUG_PC("Lengtg requested serviceList is Empty...");
		return;
	}

	DEBUG_PC("----- Starting the SP Computation ------");
	gint i = 0;
	for (GList* listnode = g_list_first(serviceList);
		listnode;
		listnode = g_list_next(listnode), i++) {
		//struct service_t* service = &(serviceList->services[i]);
		struct service_t* service = (struct service_t*)(listnode->data);

		DEBUG_PC("Starting the Computation for ServiceId: %s [ContextId: %s]", service->serviceId.service_uuid, service->serviceId.contextId);
		struct compRouteOutput_t* pathService = &(oPathList->compRouteConnection[i]);
		// check endpoints of the service are different (PE devices/nodes are different)
		if (same_src_dst_pe_nodeid(service) == 0) {
			DEBUG_PC("PEs are the same... no path computation");
			comp_route_connection_issue_handler(pathService, service);
			oPathList->numCompRouteConnList++;
			continue;
		}

		// get the graph associated to the contextId in the contextSet, if no then error
		struct graph_t* g = get_graph_by_contextId(contextSet, service->serviceId.contextId);
		if (g == NULL) {
			DEBUG_PC("The targeted contextId is NOT in the ContextSet ... then NO graph");
			comp_route_connection_issue_handler(pathService, service);
			oPathList->numCompRouteConnList++;
			continue;
		}

		computation_shortest_path(service, pathService, g);
		oPathList->numCompRouteConnList++;

		// for each network connectivity service, a single computed path (out of the KCSP) is retuned
		// If path is found, then the selected resources must be pre-assigned into the context information
		if (pathService->noPathIssue == NO_PATH_CONS_ISSUE) {
			continue;
		}
		struct path_t* path = &(pathService->paths[pathService->numPaths - 1]);
		//allocate_graph_resources(path, service, g);			// LGR: crashes in some cases with assymetric topos
		//allocate_graph_reverse_resources(path, service, g);	// LGR: crashes in some cases with assymetric topos
		print_graph(g);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_sp.c
 * 	@brief handles the path computation for the constrained shortest path
 *
 *  @param compRouteOutput
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint pathComp_sp_alg(struct compRouteOutputList_t* routeConnList) {
	g_assert(routeConnList);
	gint numSuccesPathComp = 0, numPathCompIntents = 0;

	DEBUG_PC("================================================================");
	DEBUG_PC("===========================   SP   =========================");
	DEBUG_PC("================================================================");
	// increase the number of Path Comp. Intents
	numPathCompIntents++;
	gint http_code = HTTP_CODE_OK;

	// timestamp t0
	struct timeval t0;
	gettimeofday(&t0, NULL);

	// Allocate memory for the context
	contextSet = NULL;
	// Build up the contextSet (>= 1)
	build_contextSet(&contextSet);
	print_contextSet(contextSet);
#if 1	
	//Triggering the path computation for each specific network connectivity service
	sp_execution_services(routeConnList);

	// -- timestamp t1
	struct timeval t1, delta;
	gettimeofday(&t1, NULL);
	delta.tv_sec = t1.tv_sec - t0.tv_sec;
	delta.tv_usec = t1.tv_usec - t0.tv_usec;
	delta = tv_adjust(delta);

	numSuccesPathComp++;
	update_stats_path_comp(routeConnList, delta, numSuccesPathComp, numPathCompIntents);
	print_path_connection_list(routeConnList);
#endif

	g_list_free_full(g_steal_pointer(&contextSet), (GDestroyNotify)destroy_context);
	return http_code;
}



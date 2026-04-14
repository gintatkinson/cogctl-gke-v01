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
#include "pathComp_ksp.h"

// Global Variables
GList* contextSet;

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_ksp.c
 * 	@brief Iterates over the list of network connectivity service requests 
 * to compute their own paths fulfilling the constraints
 *
 *  @param outputList
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void ksp_alg_execution_services(struct compRouteOutputList_t* outputList) {
	g_assert(outputList);
	// Check at least there is a service to be processed 
	if (g_list_length(serviceList) == 0) {
		DEBUG_PC("serviceList is Empty...");
		return;
	}
	DEBUG_PC("----- Starting the KSP Computation ------");

	// Iterate over the list of requested network connectivity services
	gint i = 0;
	for (GList* listnode = g_list_first(serviceList);
		listnode;
		listnode = g_list_next(listnode), i++){		
		struct service_t* service = (struct service_t*)(listnode->data);

		DEBUG_PC("Starting the Computation for ServiceId: %s [ContextId: %s]", service->serviceId.service_uuid, service->serviceId.contextId);
		struct compRouteOutput_t* pathService = &(outputList->compRouteConnection[i]);
		// check endpoints of the service are different (PE devices/nodes are different)
		if (same_src_dst_pe_nodeid(service) == 0) {
			DEBUG_PC("PEs are the same... NO PATH COMPUTATION");
			comp_route_connection_issue_handler(pathService, service);
			outputList->numCompRouteConnList++;
			continue;
		}
		// get the graph associated to the contextId in the contextSet, if no then error
		struct graph_t* g = get_graph_by_contextId(contextSet, service->serviceId.contextId);
		if (g == NULL) {
			DEBUG_PC("The targeted contextId is NOT in the ContextSet ... then NO graph");
			comp_route_connection_issue_handler(pathService, service);
			outputList->numCompRouteConnList++;
			continue;
		}
		
		alg_comp(service, pathService, g, NO_OPTIMIZATION_ARGUMENT); // last parameter 0 is related to an optimization computation argument
		outputList->numCompRouteConnList++;

		// for each network connectivity service, a single computed path (out of the KSP) is retuned
		// If path is found, then the selected resources must be pre-assigned into the context information
		if (pathService->noPathIssue == NO_PATH_CONS_ISSUE) {
			continue;
		}
		// Out of the comnputed paths for the pathservice, the first one is chosen to be locally allocated		
		struct path_t* path = &(pathService->paths[0]);
		allocate_graph_resources(path, service, g);
		allocate_graph_reverse_resources(path, service, g);
		print_graph(g);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_ksp.c
 * 	@brief handles the path computation triggering k-cspf algorithm
 *
 *  @param compRouteOutput
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint pathComp_ksp_alg(struct compRouteOutputList_t * routeConnList) {   	
	g_assert(routeConnList);
	gint numSuccesPathComp = 0, numPathCompIntents = 0;
	
	DEBUG_PC ("================================================================");
	DEBUG_PC ("===========================   KSP   =========================");
	DEBUG_PC ("================================================================");
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
	ksp_alg_execution_services (routeConnList);

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
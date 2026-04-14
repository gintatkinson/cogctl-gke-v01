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
#include "pathComp_ear.h"

// Global Variables
GList* contextSet;

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_ear.c
 * 	@brief Iterates over the list of network connectivity service requests
 * to compute their own paths fulfilling the constraints and minimizing the 
 * total consume energy (power)
 *
 *  @param outputList
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
void ear_comp_services(struct compRouteOutputList_t* oPathList, gint activeFlag) {
	g_assert(oPathList);
	// Check at least there is a service to be processed 
	if (g_list_length(serviceList) == 0) {
		DEBUG_PC("serviceList is Empty...");
		return;
	}	
	gint i = 0;
	DEBUG_PC("[EAR]----- Starting the Energy Aware Routing Computation ------");
	DEBUG_PC("[EAR]----- Over Context %s Devices and Links", activeFlag ? "Active" : "All");
	for (GList* listnode = g_list_first(serviceList);
		listnode;
		listnode = g_list_next(listnode), i++) {
		struct service_t* service = (struct service_t*)(listnode->data);

		DEBUG_PC("[EAR] Triggering Computation ServiceId: %s [ContextId: %s]", service->serviceId.service_uuid, service->serviceId.contextId);
		struct compRouteOutput_t* pathService = &(oPathList->compRouteConnection[i]);
		DEBUG_PC("Number of pathService[%d]->paths: %d", i, pathService->numPaths);
		// check endpoints of the service are different (PE devices/nodes are different)
		if (same_src_dst_pe_nodeid(service) == 0) {
			DEBUG_PC("[EAR] PEs are the same... no path computation");
			comp_route_connection_issue_handler(pathService, service);
			oPathList->numCompRouteConnList++;
			continue;
		}
		struct graph_t* g = get_graph_by_contextId(contextSet, service->serviceId.contextId);
		if (g == NULL) {
			DEBUG_PC("[EAR] contextId: %s NOT in the ContextSet ... then NO graph", service->serviceId.contextId);
			comp_route_connection_issue_handler(pathService, service);
			oPathList->numCompRouteConnList++;
			continue;
		}
		alg_comp(service, pathService, g, ENERGY_EFFICIENT_ARGUMENT);
		oPathList->numCompRouteConnList++;

		// for each network connectivity service, a single computed path (out of the KCSP) is retuned
		// If path is found, then the selected resources must be pre-assigned into the context information
		if (pathService->noPathIssue == NO_PATH_CONS_ISSUE) {
			continue;
		}
		struct path_t* path = &(pathService->paths[pathService->numPaths - 1]);
		allocate_graph_resources(path, service, g);
		allocate_graph_reverse_resources(path, service, g);
		print_graph(g);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_ear.c
 * 	@brief Tries to route all the services over the active devices and links. If not all 
 * these services can be routed, then it is tried to route them through the whole context 
 * including both active and slept/power off devices and links
 *
 *  @param oList
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 ////////////////////////////////////////////////////////////////////////////////////////
void ear_comp(struct compRouteOutputList_t* oList) {
	g_assert(oList);

	DEBUG_PC("Number of services to be processed: %d", g_list_length(serviceList));
	// Make a copy of oList	to be derived from the active devices and links
	struct compRouteOutputList_t* oListTmp = create_route_list();
	duplicate_route_list(oListTmp, oList);
	print_path_connection_list(oListTmp);
	
	// 1st - try to accommodate all the requested service over the active device and links
	gint activeContext = 1;
	// Create the context for the active devicesand links
	DEBUG_PC("=========================== Building the Active ContextSet =================================");
	contextSet = NULL;
	build_contextSet_active(&contextSet);
	//print_contextSet(contextSet);
	ear_comp_services(oListTmp, activeContext);
	
	gint numSuccessPaths = 0;
	// Check the number of succesfully computed paths, i.e., without path issues
	for (gint i = 0; i < oListTmp->numCompRouteConnList; i++) {
		struct compRouteOutput_t* ro = &(oListTmp->compRouteConnection[i]);
		DEBUG_PC("Number of paths: %d for oListTmp[%d]", ro->numPaths, i);
		if (ro->noPathIssue == 0) {
			numSuccessPaths++;
		}
	}
	if (numSuccessPaths == oListTmp->numCompRouteConnList) {
		duplicate_route_list(oList, oListTmp);
		g_free(oListTmp);
		return;
	}	
	// 2nd - If not all the services have been accommodated, use the whole device and links
	// Create the context for all the devices and links

	// Remove the previous Context subject to active devices and links
	g_list_free_full(g_steal_pointer(&contextSet), (GDestroyNotify)destroy_context);
	contextSet = NULL;
	DEBUG_PC("====================== Building the whole ContextSet =====================================");
	build_contextSet(&contextSet);
	//print_contextSet(contextSet);

	activeContext = 0; // Active flag is not SET
	ear_comp_services(oList, activeContext);	
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_ear.c
 * 	@brief handles the path computation for energy aware routing
 *
 *  @param compRouteOutput
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint pathComp_ear_alg(struct compRouteOutputList_t* routeConnList) {
	g_assert(routeConnList);
	print_path_connection_list(routeConnList);

	gint numSuccesPathComp = 0, numPathCompIntents = 0;

	DEBUG_PC("================================================================");
	DEBUG_PC("===========================   EAR   =========================");
	DEBUG_PC("================================================================");
	// increase the number of Path Comp. Intents
	numPathCompIntents++;
	gint http_code = HTTP_CODE_OK;

	// timestamp t0
	struct timeval t0;
	gettimeofday(&t0, NULL);

	// Initialize and create the contextSet
	//contextSet = NULL;	
	//build_contextSet(contextSet);
	//print_contextSet(contextSet);
#if 1	
	//Triggering the path computation for each specific network connectivity service
	ear_comp(routeConnList);

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
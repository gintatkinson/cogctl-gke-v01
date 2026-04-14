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
#include <unistd.h>
#include <netdb.h>
#include <glib.h>
#include <sys/time.h>
#include <ctype.h>
#include <strings.h>
#include <time.h>
#include <fcntl.h>
#include <uuid/uuid.h>
#include <string.h>

#include "pathComp_log.h"
#include "pathComp_tools.h"
#include "pathComp_cjson.h"
#include "pathComp_ksp.h"
#include "pathComp_sp.h"
#include "pathComp_ear.h"
#include "pathComp_RESTapi.h"

#define ISspace(x) isspace((int)(x))

#define SERVER_STRING "Server: PATHCOMP/0.1.0\r\n"

// List of Clients connected to the PATH COMP
GList *RESTapi_tcp_client_list = NULL;

// Id for CLient HTTP (REST API) Connection
guint CLIENT_ID = 0;
guint32 paId_req = 0;

// Global variables
GList* linkList;
GList* deviceList;
GList* serviceList;
GList* activeServList;

gchar algId[MAX_ALG_ID_LENGTH];
gboolean syncPath = FALSE;

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Seek a connected tcp client by its fd in the RESTapi_tcp_client_list
 * 	
 * 	@param data
 *  @param userdata
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint find_rl_client_by_fd (gconstpointer data, gconstpointer userdata)
{
	 /** check values */
     g_assert(data != NULL);
     g_assert(userdata != NULL);
	 
	 struct pathComp_client *client = (struct pathComp_client*)data;
     gint fd = *(gint *)userdata; 
     
	 if (client->fd == fd) {
		 return 0;
	 }
    return -1;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to send a message to the corresponding channel
 * 	
 * 	@param source
 *  @param buf
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint rapi_send_message (GIOChannel *channel, char *buf)	{
	gsize nbytes, buffersize;

	//DEBUG_PC ("Msg prepared to be sent REST API RESPONSE ");
    gint len = strlen ((const char*) buf);
    //DEBUG_PC ("Targeted Length of the buffer: %d", len);       

    buffersize = g_io_channel_get_buffer_size (channel);
    //DEBUG_PC ("GIOChannel with Buffer Size: %d", (gint)buffersize);
    
    gsize newBufferSize = MAX_GIO_CHANNEL_BUFFER_SIZE;
    g_io_channel_set_buffer_size (channel, newBufferSize);
    
    buffersize = g_io_channel_get_buffer_size (channel);
    //DEBUG_PC ("GIOChannel with Buffer Size: %d", (gint)buffersize);
    
	/** Send message.  */
    GError *error = NULL;
    
    char *ptr = buf;
    gint nleft = strlen ((const char *)buf);
    
    while (nleft > 0) {
        g_io_channel_write_chars (channel, (void *)ptr, nleft, &nbytes, &error);
        if (error) {
            DEBUG_PC ("Error sending the message to TCP Client");
            return (-1);
        }
        
        //DEBUG_PC ("Sent %d bytes", (gint)nbytes);        
        nleft = nleft - nbytes;
        //DEBUG_PC ("Remaining to be sent %d", nleft);
        ptr += nbytes;        
    } 
	DEBUG_PC("RESPONSE MSG SENT");
	return 0;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to return when something goes wrong when processing the REST API Command
 * 	
 * 	@param source
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_unimplemented (GIOChannel *source)
{
	gint ret = 0;
	guchar buftmp[1024];
	char *buf = g_malloc0 (sizeof (char) * 2048000); 
	sprintf((char *)buf, "HTTP/1.1 400 Bad request\r\n");

	sprintf((char *)buftmp, SERVER_STRING);
	strcat ((char *)buf, (const char *)buftmp);

	sprintf((char *)buftmp, "Content-Type: text/plain\r\n");
	strcat ((char *)buf, (const char *)buftmp);

	sprintf((char *)buftmp, "\r\n");
	strcat ((char *)buf, (const char *)buftmp);
	      
	sprintf((char *)buftmp, "<HTML><HEAD><TITLE>Method Not Implemented\r\n");
	strcat ((char *)buf, (const char *)buftmp);

	sprintf((char *)buftmp, "</TITLE></HEAD>\r\n");
	strcat ((char *)buf, (const char *)buftmp);

	sprintf((char *)buftmp, "<BODY><P>HTTP request method not supported.\r\n");
	strcat ((char *)buf, (const char *)buftmp);	

	sprintf((char *)buftmp, "</BODY></HTML>\r\n");
	strcat ((char *)buf, (const char *)buftmp);

	ret = rapi_send_message (source, buf);
	g_free (buf);
	(void)ret;

	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to put in the buffer the date according to RFC 1123
 * 	
 * 	@param date
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void rapi_add_date_header (char *date)
{
    static const char *DAYS[] = { "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" };
    static const char *MONTHS[] = { "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" };

    time_t t = time(NULL);
    struct tm *tm = NULL;
    struct tm sys;
    gmtime_r(&t, &sys);
    tm = &sys;

    sprintf((char *)date, "DATE: %s, %02d %s %4d %02d:%02d:%02d GMT\r\n", DAYS[tm->tm_wday], tm->tm_mday, 
								      MONTHS[tm->tm_mon], 1900 + tm->tm_year, 
								      tm->tm_hour, tm->tm_min, tm->tm_sec);
    
    return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to add DeviceId and EndpointId forming the computed path
 *
 * 	@param pathObj
 *  @param p
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void add_comp_path_deviceId_endpointId_json(cJSON* pathObj, struct path_t* p, struct compRouteOutput_t* oElem) {
	g_assert(p);
	g_assert(pathObj);

	// add array for the devideId and endpointIds
	cJSON* devicesArray = cJSON_CreateArray();
	cJSON_AddItemToObject(pathObj, "devices", devicesArray);

	// Add the source endpoint
	cJSON* sEndPointIdObj;
	cJSON_AddItemToArray(devicesArray, sEndPointIdObj = cJSON_CreateObject());
	// Add the topology Id Object containing the topology uuid and context uuid
	cJSON* stopIdObj;
	cJSON_AddItemToObject(sEndPointIdObj, "topology_id", stopIdObj = cJSON_CreateObject());
	cJSON_AddItemToObject(stopIdObj, "contextId", cJSON_CreateString(oElem->service_endpoints_id[0].topology_id.contextId));
	cJSON_AddItemToObject(stopIdObj, "topology_uuid", cJSON_CreateString(oElem->service_endpoints_id[0].topology_id.topology_uuid));

	// Add the device Id (uuid) 
	cJSON_AddItemToObject(sEndPointIdObj, "device_id", cJSON_CreateString(oElem->service_endpoints_id[0].device_uuid));
	// Add the endpoint Id (uuid)
	cJSON_AddItemToObject(sEndPointIdObj, "endpoint_uuid", cJSON_CreateString(oElem->service_endpoints_id[0].endpoint_uuid));


	for (gint i = 0; i < p->numPathLinks; i++) {
		struct pathLink_t* pL = &(p->pathLinks[i]);
		cJSON* dElemObj; // Device Element Object of the array
		cJSON_AddItemToArray(devicesArray, dElemObj = cJSON_CreateObject());

		// Add the topologyId with the topologyuuid and contextId
		cJSON* tIdObj;
		cJSON_AddItemToObject(dElemObj, "topology_id", tIdObj = cJSON_CreateObject());
		cJSON_AddItemToObject(tIdObj, "contextId", cJSON_CreateString(pL->topologyId.contextId));
		cJSON_AddItemToObject(tIdObj, "topology_uuid", cJSON_CreateString(pL->topologyId.topology_uuid));

		// Add Device Id
		cJSON_AddItemToObject(dElemObj, "device_id", cJSON_CreateString(pL->aDeviceId));

		// Add endpoint Id
		cJSON_AddItemToObject(dElemObj, "endpoint_uuid", cJSON_CreateString(pL->aEndPointId));  
	}
	
	// Add the sink	endpoint
	cJSON* sinkEndPointIdObj;
	cJSON_AddItemToArray(devicesArray, sinkEndPointIdObj = cJSON_CreateObject());
	// Add the topology Id Object containing the topology uuid and context uuid
	cJSON* sinkTopIdObj;
	cJSON_AddItemToObject(sinkEndPointIdObj, "topology_id", sinkTopIdObj = cJSON_CreateObject());
	cJSON_AddItemToObject(sinkTopIdObj, "contextId", cJSON_CreateString(oElem->service_endpoints_id[1].topology_id.contextId));
	cJSON_AddItemToObject(sinkTopIdObj, "topology_uuid", cJSON_CreateString(oElem->service_endpoints_id[1].topology_id.topology_uuid));

	// Add the device Id (uuid) 
	cJSON_AddItemToObject(sinkEndPointIdObj, "device_id", cJSON_CreateString(oElem->service_endpoints_id[1].device_uuid));
	// Add the endpoint Id (uuid)
	cJSON_AddItemToObject(sinkEndPointIdObj, "endpoint_uuid", cJSON_CreateString(oElem->service_endpoints_id[1].endpoint_uuid));
	
	return;				 
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to add the links forming the computed path
 *
 * 	@param pathObj
 *  @param p
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void add_comp_path_link_json(cJSON* pathObj, struct path_t* p) {
	g_assert(p);
	g_assert(pathObj);

	// Add array for the links
	cJSON* linkArray = cJSON_CreateArray();
	cJSON_AddItemToObject(pathObj, "link", linkArray);

	for (gint i = 0; i < p->numPathLinks; i++) {
		struct pathLink_t* pL = &(p->pathLinks[i]);
		cJSON* lElemObj; // Link Element Object of the array
		cJSON_AddItemToArray(linkArray, lElemObj = cJSON_CreateObject());

		// Add link Id
		cJSON_AddItemToObject(lElemObj, "link_Id", cJSON_CreateString(pL->linkId));

		// Add link topologies
		cJSON* linkTopoArray = cJSON_CreateArray();
		cJSON_AddItemToObject(lElemObj, "topology", linkTopoArray);

		for (gint j = 0; j < pL->numLinkTopologies; j++) {
			struct linkTopology_t* linkTopo = &(pL->linkTopologies[j]);
			cJSON* lTopoElemObj;
			cJSON_AddItemToArray(linkTopoArray, lTopoElemObj = cJSON_CreateObject());
			cJSON_AddItemToObject(lTopoElemObj, "topology_uuid", cJSON_CreateString(linkTopo->topologyId));
		}
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Compose the JSON Body of the succesfully network connectivity service
 * 	
 * 	@param body
 *  @param length
 *  @param compRouteOutputList
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void rapi_response_json_contents (char *body, gint *length, struct compRouteOutputList_t *compRouteOutputList)
{
    char *buftmp;    
    cJSON *root = cJSON_CreateObject();     
	DEBUG_PC ("Creating the JSON body of the response"); 

	// Create response-list array
	cJSON *responseListArray = cJSON_CreateArray();
	cJSON_AddItemToObject(root, "response-list", responseListArray);
	
	// Add computed routes to the response-list
	for (gint i = 0; i < compRouteOutputList->numCompRouteConnList; i++) {
		struct compRouteOutput_t *oElem = &(compRouteOutputList->compRouteConnection[i]); // reference to output element from the list of computed routes
		cJSON *oElemObj;
		cJSON_AddItemToArray (responseListArray, oElemObj = cJSON_CreateObject());
		
		// Add the service Id Object
		cJSON* servIdObj;
		cJSON_AddItemToObject(oElemObj, "serviceId", servIdObj = cJSON_CreateObject());
		cJSON_AddItemToObject(servIdObj, "contextId", cJSON_CreateString(oElem->serviceId.contextId));
		cJSON_AddItemToObject(servIdObj, "service_uuid", cJSON_CreateString(oElem->serviceId.service_uuid));

		// Add the service endpoints ids array
		cJSON* sEndpointIdsArray = cJSON_CreateArray();
		cJSON_AddItemToObject(oElemObj, "service_endpoints_ids", sEndpointIdsArray);

		for (gint j = 0; j < oElem->num_service_endpoints_id; j++) {
			//DEBUG_PC("parsing service endpoints ids");
			//DEBUG_PC("endpoint: %s [%s]", oElem->service_endpoints_id[j].device_uuid, oElem->service_endpoints_id[j].endpoint_uuid);
			//struct service_endpoints_id_t* sEndPointId = &(oElem->service_endpoints_id[j]);
			cJSON* sEndPointIdObj;
			cJSON_AddItemToArray(sEndpointIdsArray, sEndPointIdObj = cJSON_CreateObject());
			// Add the topology Id Object containing the topology uuid and context uuid
			cJSON* topIdObj;
			cJSON_AddItemToObject(sEndPointIdObj, "topology_id", topIdObj = cJSON_CreateObject());
			cJSON_AddItemToObject(topIdObj, "contextId", cJSON_CreateString(oElem->service_endpoints_id[j].topology_id.contextId));
			cJSON_AddItemToObject(topIdObj, "topology_uuid", cJSON_CreateString(oElem->service_endpoints_id[j].topology_id.topology_uuid));

			// Add the device Id (uuid) 
			cJSON_AddItemToObject(sEndPointIdObj, "device_id", cJSON_CreateString(oElem->service_endpoints_id[j].device_uuid));
			// Add the endpoint Id (uuid)
			cJSON_AddItemToObject(sEndPointIdObj, "endpoint_uuid", cJSON_CreateString(oElem->service_endpoints_id[j].endpoint_uuid));
		}
		// Add no path issue
		if (oElem->noPathIssue == NO_PATH_CONS_ISSUE) { // Error on finding the route, e.g., no feasible path
			DEBUG_PC("NO PATH FOUND, AN ISSUE OCCURRED: %d", oElem->noPathIssue);
			cJSON* noPathObj;
			cJSON_AddItemToObject(oElemObj, "noPath", noPathObj = cJSON_CreateObject());
			char str[5];
			sprintf(str, "%d", oElem->noPathIssue);
			cJSON_AddItemToObject(noPathObj, "issue", cJSON_CreateString(str));
			continue;
		}
		
		// Create the array to parse the computed path from the oElemObj
		cJSON* pathArray = cJSON_CreateArray();
		cJSON_AddItemToObject(oElemObj, "path", pathArray);
		for (gint k = 0; k < oElem->numPaths; k++) {
			struct path_t* p = &(oElem->paths[k]);
			cJSON* pathObj;
			cJSON_AddItemToArray(pathArray, pathObj = cJSON_CreateObject());

			// Add path capacity
			cJSON* pathCapObj;
			cJSON_AddItemToObject(pathObj, "path-capacity", pathCapObj = cJSON_CreateObject());
			cJSON* totalSizeObj;
			cJSON_AddItemToObject(pathCapObj, "total-size", totalSizeObj = cJSON_CreateObject());
			cJSON_AddItemToObject(totalSizeObj, "value", cJSON_CreateNumber(p->path_capacity.value));
			cJSON_AddItemToObject(totalSizeObj, "unit", cJSON_CreateNumber(p->path_capacity.unit));

			// Add path latency
			cJSON* pathLatObj;
			char lat[16];
			sprintf(lat, "%lf", p->path_latency.fixed_latency);
			cJSON_AddItemToObject(pathObj, "path-latency", pathLatObj= cJSON_CreateObject());
			cJSON_AddItemToObject(pathLatObj, "fixed-latency-characteristic", cJSON_CreateString(lat));

			// Add path cost
			cJSON* pathCostObj;
			cJSON_AddItemToObject(pathObj, "path-cost", pathCostObj = cJSON_CreateObject());
			cJSON_AddItemToObject(pathCostObj, "cost-name", cJSON_CreateString(p->path_cost.cost_name));
			char value[16];
			sprintf(value, "%lf", p->path_cost.cost_value);
			cJSON_AddItemToObject(pathCostObj, "cost-value", cJSON_CreateString(value));
			char algorithm[16];
			sprintf(algorithm, "%lf", p->path_cost.cost_algorithm);
			cJSON_AddItemToObject(pathCostObj, "cost-algorithm", cJSON_CreateString(algorithm));

			// Add the links
			//add_comp_path_link_json(pathObj, p);
			// Add deviceId, endpointId
			add_comp_path_deviceId_endpointId_json(pathObj, p, oElem);
		}	
	}
	
    //DEBUG_PC ("JSON Body Response DONE");	
    buftmp = (char *)cJSON_Print(root);
    strcat (body, (const char*) buftmp);
    *length = strlen ((const char*)body);    
    //DEBUG_PC ("JSON Body (length: %d)", *length);
    //DEBUG_PC ("%s", body);    
	cJSON_Delete (root);
	g_free(buftmp);
    return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to return response OK via REST API with the computed serviceId
 * 	
 * 	@param source
 *  @param httpCode
 *  @param compRouteOutputList
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void rapi_response_ok (GIOChannel *source, gint httpCode, struct compRouteOutputList_t *compRouteOutputList) {
	gint ret = 0;
    
    //DEBUG_PC ("Creating the JSON Body and sending the response of the computed Route List");
    
    char buftmp[1024];
    char *buf = g_malloc0 (sizeof (char) * 2048000); 
    // Create the Body of the Response 
    char * msgBody = g_malloc0 (sizeof (char) * 2048000);    
    gint length = 0;
	
	//  If path computation was requested, the resulting computation is returned in the msg body
	if (compRouteOutputList != NULL) {
		rapi_response_json_contents(msgBody, &length, compRouteOutputList);
	}
	// no path computation was requested, then a basic msg is just added
	else {
		cJSON* root = cJSON_CreateObject();
		char status[3];
		sprintf(status, "OK");
		cJSON_AddItemToObject(root, "Status", cJSON_CreateString(status));
		msgBody = (char*)cJSON_Print(root);
		length = strlen((const char*)msgBody);
		cJSON_Delete(root);
	}
		
	sprintf((char *)buf, "HTTP/1.1 200 OK\r\n");    
	
    sprintf((char *)buftmp, SERVER_STRING);
    strcat ((char *)buf, (const char *)buftmp);    
  
    sprintf ((char *)buftmp, "Content-Type: application/json\r\n");
    strcat ((char *)buf, (const char *)buftmp);    
    
    // Add the length of the JSON enconding to the Content_Length
    char buff_length[16];    
    sprintf(buff_length, "%d", length);
    
    sprintf ((char *)buftmp, "Content-Length: ");
    strcat ((char *)buftmp, (const char *)buff_length);
    strcat ((char *)buftmp, "\r\n");
    strcat ((char *)buf, (const char *)buftmp);    
    
    // Add DATE header
    rapi_add_date_header ((char *)buftmp);
    strcat ((char *)buf, (const char *)buftmp);     
    sprintf((char *)buftmp, "\r\n");
    strcat ((char *)buf, (const char *)buftmp);

	strcat((char*)buf, (const char*)msgBody);
			
	//DEBUG_PC ("%s", buf);	    
    ret = rapi_send_message (source, buf);    
    g_free (buf);
    memset (buftmp, '\0', sizeof ( buftmp));    
    g_free (msgBody);
    (void)ret;    
    return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to return response OK via REST API
 * 	
 * 	@param source
 *  @param error
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void rapi_response (GIOChannel *source, gint error) {
	 int ret = 0;	
	 guchar buftmp[1024];
	 char * buf = g_malloc0 (sizeof (char) * 2048000);
	 if (error == HTTP_RETURN_CODE_BAD_REQUEST)
		sprintf((char *)buf, "HTTP/1.1 400 BAD REQUEST\r\n");
	 else if (error == HTTP_RETURN_CODE_UNAUTHORIZED)
		sprintf((char *)buf, "HTTP/1.1 401 UNAUTHORIZED\r\n");
	 else if (error == HTTP_RETURN_CODE_FORBIDDEN)
		sprintf((char *)buf, "HTTP/1.1 403 FORBIDDEN\r\n");    
	 else if (error == HTTP_RETURN_CODE_NOT_FOUND)
		sprintf((char *)buf, "HTTP/1.1 404 NOT FOUND\r\n");
	 
	 sprintf((char *)buftmp, SERVER_STRING);
	 strcat ((char *)buf, (const char *)buftmp);    
	
	 sprintf((char *)buftmp, "Content-Type: text/plain\r\n");
	 strcat ((char *)buf, (const char *)buftmp);    
	 
	 sprintf((char *)buftmp, "Content-Length: 0/plain\r\n");
	 strcat ((char *)buf, (const char *)buftmp);    
	 
	 // Add DATE header
	 rapi_add_date_header ((char *)buftmp);
	 strcat ((char *)buf, (const char *)buftmp);     
	     
	 sprintf((char *)buftmp, "\r\n");
	 strcat ((char *)buf, (const char *)buftmp);
	 // Print the prepared message
	 DEBUG_PC ("%s", buf);
	 
	 // Send the message
	 ret = rapi_send_message (source, buf);	 
	 g_free (buf);	 
	 (void)ret;
	
	 return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief parsing topology Identifier Object (contains Context Id and Toplogy UUID) JSON object
 *
 * 	@param obj
 *  @param topology_id
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_topology_Id(cJSON* obj, struct topology_id_t* topology_id) {
	g_assert(topology_id);
	// Get the context Id (UUID) from the topologyIdObj
	cJSON* contextIdObj = cJSON_GetObjectItem(obj, "contextId");
	if (cJSON_IsString(contextIdObj)) {
		duplicate_string(topology_id->contextId, contextIdObj->valuestring);
	}
	// Get the topologyId (UUID) from the topologyIdObj
	cJSON* topologyUuidObj = cJSON_GetObjectItem(obj, "topology_uuid");
	if (cJSON_IsString(topologyUuidObj)) {
		duplicate_string(topology_id->topology_uuid, topologyUuidObj->valuestring);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief parsing EndpointIds JSON object
 *
 * 	@param item
 *  @param serviceEndPointId
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_endPointsIds(cJSON* item, struct service_endpoints_id_t* serviceEndPointId) {
	// Get the topology Id Object
	cJSON* topologyIdObj = cJSON_GetObjectItem(item, "topology_id");
	if (cJSON_IsObject(topologyIdObj)) {
		parse_topology_Id(topologyIdObj, &serviceEndPointId->topology_id);
	}
	// Get the deviceId (UUID)
	cJSON* deviceIdObj = cJSON_GetObjectItem(item, "device_id");
	if (cJSON_IsString(deviceIdObj)) {
		duplicate_string(serviceEndPointId->device_uuid, deviceIdObj->valuestring);
		DEBUG_PC("DeviceId: %s", serviceEndPointId->device_uuid);
	}
	// Get the endpointId (UUID)
	cJSON* endPointIdObj = cJSON_GetObjectItem(item, "endpoint_uuid");
	if (cJSON_IsString(endPointIdObj)) {
		duplicate_string(serviceEndPointId->endpoint_uuid, endPointIdObj->valuestring);
		DEBUG_PC("EndPointId: %s", serviceEndPointId->endpoint_uuid);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the array of Endpoint Ids	of the active services
 *
 * 	@param endPointArray
 *  @param actServ
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_act_service_endPointsIds_array(cJSON* endPointIdArray, struct activeService_t* actServ) {
	g_assert(actServ);

	for (gint i = 0; i < cJSON_GetArraySize(endPointIdArray); i++) {
		actServ->num_service_endpoints_id++;
		struct service_endpoints_id_t* serviceEndPointId = &(actServ->service_endpoints_id[i]);
		cJSON* item = cJSON_GetArrayItem(endPointIdArray, i);
		parse_endPointsIds(item, serviceEndPointId);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the array of Endpoint Ids	of the requested services
 *
 * 	@param endPointArray
 *  @param s
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_service_endPointsIds_array(cJSON* endPointIdArray, struct service_t* s) {

	for (gint i = 0; i < cJSON_GetArraySize(endPointIdArray); i++) {
		s->num_service_endpoints_id++;
		struct service_endpoints_id_t* serviceEndPointId = &(s->service_endpoints_id[i]);

		cJSON* item = cJSON_GetArrayItem(endPointIdArray, i);
		parse_endPointsIds(item, serviceEndPointId);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the array with the required service constraints
 *
 * 	@param constraintArray
 *  @param s
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_service_constraints(cJSON* constraintArray, struct service_t* s) {
	for (gint i = 0; i < cJSON_GetArraySize(constraintArray); i++) {
		s->num_service_constraints++;
		struct constraint_t* constraint = &(s->constraints[i]);

		cJSON* item = cJSON_GetArrayItem(constraintArray, i);

		// Get the constraint type
		cJSON* typeObj = cJSON_GetObjectItem(item, "constraint_type");
		if (cJSON_IsString(typeObj)) {
			duplicate_string(constraint->constraint_type, typeObj->valuestring);
		}
		// Get the constraint value
		cJSON* valueObj = cJSON_GetObjectItem(item, "constraint_value");
		if (cJSON_IsString(valueObj)) {
			 duplicate_string(constraint->constraint_value, valueObj->valuestring);
		} 
		DEBUG_PC("Service Reqs [%d] -- Type: %s | Value: %s", i+1, constraint->constraint_type, constraint->constraint_value);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the serviceId information from a JSON obj
 *
 * 	@param obj
 *  @param serviceId
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_json_serviceId(cJSON* obj, struct serviceId_t* serviceId) {
	g_assert(obj);
	g_assert(serviceId);

	// Get context Id uuid
	cJSON* contextIdObj = cJSON_GetObjectItem(obj, "contextId");
	if (cJSON_IsString(contextIdObj)) {
		// convert the string in contextId->valuestring in uuid binary format
		duplicate_string(serviceId->contextId, contextIdObj->valuestring);
		DEBUG_PC("ContextId: %s (uuid string format)", serviceId->contextId);
	}
	// Get service Id uuid
	cJSON* serviceUuidObj = cJSON_GetObjectItem(obj, "service_uuid");
	if (cJSON_IsString(serviceUuidObj)) {
		duplicate_string(serviceId->service_uuid, serviceUuidObj->valuestring);
		DEBUG_PC("Service UUID: %s (uuid string format)", serviceId->service_uuid);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the array with the different
 * network services
 *
 * 	@param serviceArray
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parsing_json_serviceList_array(cJSON* serviceArray) {

	for (gint i = 0; i < cJSON_GetArraySize(serviceArray); i++)
	{
		struct service_t* service = g_malloc0(sizeof(struct service_t));
		if (service == NULL) {
			DEBUG_PC("Memory allocation error ...");
			exit(-1);
		}
		cJSON* item = cJSON_GetArrayItem(serviceArray, i);
		// Get the algorithm Id
		cJSON* algIdItem = cJSON_GetObjectItem(item, "algId");
		if (cJSON_IsString(algIdItem)) {
			duplicate_string(service->algId, algIdItem->valuestring);
			DEBUG_PC ("algId: %s", service->algId);
			// assumed that all the services request the same algId
			duplicate_string(algId, service->algId);
		}

		// Get the syncPaths
		cJSON* synchPathObj = cJSON_GetObjectItemCaseSensitive(item, "syncPaths");
		if (cJSON_IsBool(synchPathObj)) {
			// Check Synchronization of multiple Paths to attain e.g. global concurrent optimization
			if (cJSON_IsTrue(synchPathObj)) {
				syncPath = TRUE;
				DEBUG_PC("Path Synchronization is required");
			}
			if (cJSON_IsFalse(synchPathObj)) {
				syncPath = FALSE;
				DEBUG_PC("No Path Synchronization");
			}
		}

		// Get service Id in terms of contextId and service uuids
		cJSON* serviceIdObj = cJSON_GetObjectItem(item, "serviceId");
		if (cJSON_IsObject(serviceIdObj)) {
			parse_json_serviceId(serviceIdObj, &service->serviceId);
		}		

		// Get de service type
		cJSON* serviceTypeObj = cJSON_GetObjectItem(item, "serviceType");
		if (cJSON_IsNumber(serviceTypeObj))
		{
			service->service_type = (guint)(serviceTypeObj->valuedouble);
			print_service_type(service->service_type);
		}

		// Get the endPoints array of the service
		cJSON* endPointIdsArray = cJSON_GetObjectItem(item, "service_endpoints_ids");
		if (cJSON_IsArray(endPointIdsArray)) {
			parse_service_endPointsIds_array(endPointIdsArray, service);
		}	

		// Get the service constraints
		cJSON* constraintArray = cJSON_GetObjectItem(item, "service_constraints");
		if (cJSON_IsArray(constraintArray)) {
			parse_service_constraints(constraintArray, service);
		}		

		// Get the maximum number of paths to be computed (kPaths) inspected/explored
		cJSON* kPathsInspObj = cJSON_GetObjectItemCaseSensitive(item, "kPaths_inspection");
		if (cJSON_IsNumber(kPathsInspObj)){
			service->kPaths_inspected = (guint)(kPathsInspObj->valuedouble);
		}

		// Get the maximum number of paths to be computed (kPaths) returned
		cJSON* kPathsRetpObj = cJSON_GetObjectItemCaseSensitive(item, "kPaths_return");
		if (cJSON_IsNumber(kPathsRetpObj)){
			service->kPaths_returned = (guint)(kPathsRetpObj->valuedouble);
		}	
		
		// Append the requested service to the serviceList
		serviceList = g_list_append(serviceList, service);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function parsing the capacity attributes in the endpoint
 *
 * 	@param capacity
 *  @param c
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_capacity_object(cJSON* capacity, struct capacity_t* c) {
	cJSON* totalSizeObj = cJSON_GetObjectItem(capacity, "total-size");
	if (cJSON_IsObject(totalSizeObj)) {
		//Get the capacity value
		cJSON* valueObj = cJSON_GetObjectItem(totalSizeObj, "value");
		if (cJSON_IsNumber(valueObj)) {
			memcpy(&c->value, &valueObj->valuedouble, sizeof (gdouble));
		}
		// Get the Units
		cJSON* unitObj = cJSON_GetObjectItem(totalSizeObj, "unit");
		if (cJSON_IsNumber(unitObj)) {
			c->unit = (guint)(unitObj->valuedouble);
		}	
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function parsing the device endpoints
 *
 * 	@param endPointsArray
 *  @param d
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_json_device_endpoints_array(cJSON* endPointsArray, struct device_t* d) {
	for (gint i = 0; i < cJSON_GetArraySize(endPointsArray); i++) {
		d->numEndPoints++;
		if (d->numEndPoints >= MAX_DEV_ENDPOINT_LENGTH) {
			DEBUG_PC("d->numEndPoints(%d) exceeded MAX_DEV_ENDPOINT_LENGTH(%d)", d->numEndPoints, MAX_DEV_ENDPOINT_LENGTH);
		}
		struct endPoint_t* endpoint = &(d->endPoints[i]);

		cJSON* item = cJSON_GetArrayItem(endPointsArray, i);

		// Get the Endpoint Identifier: topology, context, device and endpointId
		cJSON* endPointIdObj = cJSON_GetObjectItem(item, "endpoint_id");
		if (cJSON_IsObject(endPointIdObj)) {
			// Get the topology Id Object
			cJSON* topologyIdObj = cJSON_GetObjectItem(endPointIdObj, "topology_id");
			if (cJSON_IsObject(topologyIdObj)) {
				parse_topology_Id(topologyIdObj, &endpoint->endPointId.topology_id);
			}
			// Get the deviceId
			cJSON* deviceIdObj = cJSON_GetObjectItem(endPointIdObj, "device_id");
			if (cJSON_IsString(deviceIdObj)) {				
				duplicate_string(endpoint->endPointId.device_id, deviceIdObj->valuestring);
			}
			// Get the endpoint_uuid
			cJSON* endPointUuidObj = cJSON_GetObjectItem(endPointIdObj, "endpoint_uuid");
			if (cJSON_IsString(endPointUuidObj)) {				
				duplicate_string(endpoint->endPointId.endpoint_uuid, endPointUuidObj->valuestring);
			}
		}
		// Get the EndPoint Type
		cJSON* endPointTypeObj = cJSON_GetObjectItem(item, "endpoint_type");
		if (cJSON_IsString(endPointTypeObj)) {
			duplicate_string(endpoint->endpointType, endPointTypeObj->valuestring);
			//DEBUG_PC("Device Endpoint (%d) -- EndPoint Type: %s", i + 1, endpoint->endpointType);
		}
		// Link Port Direction
		cJSON* linkPortDirectionObj = cJSON_GetObjectItem(item, "link_port_direction");
		if (cJSON_IsNumber(linkPortDirectionObj)) {
			endpoint->link_port_direction = (guint)(linkPortDirectionObj->valuedouble);
			print_link_port_direction(endpoint->link_port_direction);
		}
		// EndPoint Termination Direction
		cJSON* terminationDirectionObj = cJSON_GetObjectItem(item, "termination-direction");
		if (cJSON_IsNumber(terminationDirectionObj)) {
			endpoint->termination_direction = (guint)(terminationDirectionObj->valuedouble);
			print_termination_direction(endpoint->termination_direction);
		}
		// Endpoint Termination State
		cJSON* terminationStateObj = cJSON_GetObjectItem(item, "termination-state");
		if (cJSON_IsNumber(terminationStateObj)) {
			endpoint->termination_state = (guint)(terminationStateObj->valuedouble);
			print_termination_state(endpoint->termination_state);
		}
		// total potential capacity
		cJSON* totalPotentialCapacityObj = cJSON_GetObjectItem(item, "total-potential-capacity");
		if (cJSON_IsObject(totalPotentialCapacityObj))
		{
			parse_capacity_object(totalPotentialCapacityObj, &endpoint->potential_capacity);
			//DEBUG_PC("Device Endpoint (%d) -- Potential Capacity: %f", i + 1, endpoint->potential_capacity.value);
			print_capacity_unit(endpoint->potential_capacity.unit);
		}
		// total available capacity
		cJSON* availableCapacityObj = cJSON_GetObjectItem(item, "available-capacity");
		if (cJSON_IsObject(availableCapacityObj))
		{
			parse_capacity_object(availableCapacityObj, &endpoint->available_capacity);
			//DEBUG_PC("Device Endpoint (%d) -- Available Capacity: %f", i + 1, endpoint->available_capacity.value);
			print_capacity_unit(endpoint->available_capacity.unit);
		}
		// inter-domain plug-in
		cJSON* interDomainPlugInObj = cJSON_GetObjectItem(item, "inter-domain-plug-in");
		if (cJSON_IsObject(interDomainPlugInObj)) {
			// Get the local
			cJSON* idInterDomainLocal = cJSON_GetObjectItem(interDomainPlugInObj, "plug-id-inter-domain-local-id");
			if (cJSON_IsString(idInterDomainLocal)) {
				duplicate_string(endpoint->inter_domain_plug_in.inter_domain_plug_in_local_id, idInterDomainLocal->valuestring);
				//DEBUG_PC("Inter-Domain Local Id: %s", endpoint->inter_domain_plug_in.inter_domain_plug_in_local_id);				
			}
			// Get the remote
			cJSON* idInterDomainRemote = cJSON_GetObjectItem(interDomainPlugInObj, "plug-id-inter-domain-remote-id");
			if (cJSON_IsString(idInterDomainRemote)) {
				duplicate_string(endpoint->inter_domain_plug_in.inter_domain_plug_in_remote_id, idInterDomainRemote->valuestring);
				//DEBUG_PC("Inter-Domain Remote Id: %s", endpoint->inter_domain_plug_in.inter_domain_plug_in_remote_id);
			}
		}

		// Energy consumption per endPoint port
		cJSON* energyPortObj = cJSON_GetObjectItem(item, "energy_consumption");
		if (cJSON_IsNumber(energyPortObj)) {
			memcpy(&endpoint->energyConsumption, &energyPortObj->valuedouble, sizeof(gdouble));
			DEBUG_PC("Endpoint Energy Consumption: %f", endpoint->energyConsumption);
		}

		// Endpoint Operational Status
		cJSON* operationalStatusObj = cJSON_GetObjectItem(item, "operational_status");
		if (cJSON_IsNumber(operationalStatusObj)) {
			endpoint->operational_status = (gint)(operationalStatusObj->valuedouble);
			DEBUG_PC("Endpoint Operational Status: %d", endpoint->operational_status);
		}
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the set/list of devices forming the context/topology
 *
 * 	@param deviceArray
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parsing_json_deviceList_array(cJSON* deviceArray) {
	DEBUG_PC("");
	DEBUG_PC("========= PARSING DEVICE LIST ============");
	for (gint i = 0; i < cJSON_GetArraySize(deviceArray); i++) {		
		struct device_t* d = g_malloc0(sizeof(struct device_t));
		if (d == NULL) {
			DEBUG_PC("Memory Allocation Failure");
			exit(-1);
		}
		cJSON* item = cJSON_GetArrayItem(deviceArray, i);

		// Get the power idle of the switch
		cJSON* powerIdleObj = cJSON_GetObjectItem(item, "power_idle");
		if (cJSON_IsNumber(powerIdleObj)) {
			memcpy(&d->power_idle, &powerIdleObj->valuedouble, sizeof(gdouble));
			DEBUG_PC("Power Idle: %f", d->power_idle);
		}

		// Get the operational state
		cJSON* opeStatusObj = cJSON_GetObjectItem(item, "operational_status");
		if (cJSON_IsNumber(opeStatusObj)) {
			d->operational_status = (gint)(opeStatusObj->valuedouble);
			DEBUG_PC("Operational Status: %d (0 Undefined, 1 Disabled, 2 Enabled", d->operational_status);
		}

		// Get the device UUID
		cJSON* deviceUuidObj = cJSON_GetObjectItem(item, "device_Id");
		if (cJSON_IsString(deviceUuidObj)) {
			duplicate_string(d->deviceId, deviceUuidObj->valuestring);
			DEBUG_PC("Device (%d) -- Id: %s (uuid string format)", i + 1, d->deviceId);
		}

		// Get the device Type
		cJSON* deviceTypeObj = cJSON_GetObjectItem(item, "device_type");
		if (cJSON_IsString(deviceTypeObj)) {
			duplicate_string(d->deviceType, deviceTypeObj->valuestring);
			//DEBUG_PC("  Device Type: %s ---", d->deviceType);
		}
		DEBUG_PC("DeviceId: %s, Device Type: %s", d->deviceId, d->deviceType);

		// get the device endPoints
		cJSON* deviceEndpointsArray = cJSON_GetObjectItem(item, "device_endpoints");
		if (cJSON_IsArray(deviceEndpointsArray)) {
			parse_json_device_endpoints_array(deviceEndpointsArray, d);
		}
		// append the device into the deviceList
		deviceList = g_list_append(deviceList, d);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the JSON objects the endPoint of a link
 *
 * 	@param endPointsLinkObj
 *  @param l
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parse_json_link_endpoints_array(cJSON *endPointsLinkObj, struct link_t* l) {
	for (gint i = 0; i < cJSON_GetArraySize(endPointsLinkObj); i++) {
		//DEBUG_PC("link: %s has %d endPointIds", l->linkId, l->numLinkEndPointIds);
		l->numLinkEndPointIds++;
		struct link_endpointId_t* endPointLink = &(l->linkEndPointId[i]);

		cJSON* item = cJSON_GetArrayItem(endPointsLinkObj, i);

		// Get endPoint attributes (topologyId, deviceId, endpoint_uuid)
		cJSON* endPointIdObj = cJSON_GetObjectItem(item, "endpoint_id");
		if (cJSON_IsObject(endPointIdObj)) {
			// Get the topology Id Object
			cJSON* topologyIdObj = cJSON_GetObjectItem(endPointIdObj, "topology_id");
			if (cJSON_IsObject(topologyIdObj)) {
				parse_topology_Id(topologyIdObj, &endPointLink->topology_id);				
			}
			// Get the deviceId
			cJSON* deviceIdObj = cJSON_GetObjectItem(endPointIdObj, "device_id");
			if (cJSON_IsString(deviceIdObj)) {
				duplicate_string(endPointLink->deviceId, deviceIdObj->valuestring);
				DEBUG_PC("   Link Endpoint[%d] -- DeviceId: %s", i + 1, endPointLink->deviceId);
			}
			// Get the endpoint_uuid
			cJSON* endPointUuidObj = cJSON_GetObjectItem(endPointIdObj, "endpoint_uuid");
			if (cJSON_IsString(endPointUuidObj)) {
				duplicate_string(endPointLink->endPointId, endPointUuidObj->valuestring);
				//DEBUG_PC("Link Endpoint (%d) -- EndPoint Uuid: %s (uuid)", i + 1, endPointLink->endPointId);
			}
		}
	}
	//DEBUG_PC("link id: %s has %d endpoints", l->linkId, l->numLinkEndPointIds);
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the JSON objects describing the set of links
 *
 * 	@param linkListArray
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parsing_json_linkList_array(cJSON* linkListArray) {
	DEBUG_PC("");
	DEBUG_PC("======= PARSING OF THE LINK LIST ARRAY ==========");
	for (gint i = 0; i < cJSON_GetArraySize(linkListArray); i++) {		
		struct link_t* l = g_malloc0(sizeof(struct link_t));
		if (l == NULL) {
			DEBUG_PC("Memory Allocation Failure");
			exit(-1);
		}
		cJSON* item = cJSON_GetArrayItem(linkListArray, i);

		// Get the link Id (uuid)
		cJSON* linkIdObj = cJSON_GetObjectItem(item, "link_Id");
		if (cJSON_IsString(linkIdObj)) {
			duplicate_string(l->linkId, linkIdObj->valuestring);
			DEBUG_PC(" * Link (%d) -- Id: %s (uuid)", i + 1, l->linkId);
		}

		// Get the link endpoints (assumed to be p2p)
		cJSON* endPointsLinkObj = cJSON_GetObjectItem(item, "link_endpoint_ids");
		if (cJSON_IsArray(endPointsLinkObj)) {
			//DEBUG_PC("number linkEndPointIds: %d", l->numLinkEndPointIds);
			parse_json_link_endpoints_array(endPointsLinkObj, l);
		}
		// get the fowarding direction
		cJSON* fwdDirObj = cJSON_GetObjectItem(item, "forwarding_direction");
		if (cJSON_IsNumber(fwdDirObj)) {
			l->forwarding_direction = (guint)(fwdDirObj->valuedouble);
			print_link_forwarding_direction(l->forwarding_direction);
		}
		// total potential capacity
		cJSON* totalPotentialCapacityObj = cJSON_GetObjectItem(item, "total-potential-capacity");
		if (cJSON_IsObject(totalPotentialCapacityObj))
		{
			parse_capacity_object(totalPotentialCapacityObj, &l->potential_capacity);
			//DEBUG_PC("Link (%d) -- Potential Capacity: %f", i + 1, l->potential_capacity.value);
			print_capacity_unit(l->potential_capacity.unit);
		}
		// total available capacity
		cJSON* availableCapacityObj = cJSON_GetObjectItem(item, "available-capacity");
		if (cJSON_IsObject(availableCapacityObj))
		{
			parse_capacity_object(availableCapacityObj, &l->available_capacity);
			//DEBUG_PC("Link (%d) -- Available Capacity: %f", i + 1, l->available_capacity.value);
			print_capacity_unit(l->available_capacity.unit);
		}
		// Cost Characteristics
		cJSON* costCharacObj = cJSON_GetObjectItem(item, "cost-characteristics");
		if (cJSON_IsObject(costCharacObj)) {
			// Cost Name
			cJSON* costNameObj = cJSON_GetObjectItem(costCharacObj, "cost-name");
			if (cJSON_IsString(costNameObj)) {
				duplicate_string(l->cost_characteristics.cost_name, costNameObj->valuestring);
				//DEBUG_PC("Link (%d) -- Cost Name: %s", i + 1, l->cost_characteristics.cost_name);
			}
			// Cost value
			cJSON* costValueObj = cJSON_GetObjectItem(costCharacObj, "cost-value");
			if (cJSON_IsString(costValueObj)) {
				char* endpr;
				l->cost_characteristics.cost_value = (gdouble)(strtod(costValueObj->valuestring, &endpr));
				//DEBUG_PC("Link (%d) -- Cost Value: %f", i + 1, l->cost_characteristics.cost_value);
			}
			// Cost Algorithm
			cJSON* costAlgObj = cJSON_GetObjectItem(costCharacObj, "cost-algorithm");
			if (cJSON_IsString(costAlgObj)) {
				char* endpr;
				l->cost_characteristics.cost_algorithm = (gdouble)(strtod(costAlgObj->valuestring, &endpr));
				//DEBUG_PC("Link (%d) -- Cost Algorithm: %f", i + 1, l->cost_characteristics.cost_algorithm);
			}
		}
		// Latency Characteristics
		cJSON* latencyCharacObj = cJSON_GetObjectItem(item, "latency-characteristics");
		if (cJSON_IsObject(latencyCharacObj)) {
			cJSON* fixedLatencyCharacObj = cJSON_GetObjectItem(latencyCharacObj, "fixed-latency-characteristic");
			if (cJSON_IsString(fixedLatencyCharacObj)) {
				char* endpr;
				l->latency_characteristics.fixed_latency = (gdouble)(strtod(fixedLatencyCharacObj->valuestring, &endpr));
				//DEBUG_PC("Link (%d) -- Latency: %f", i + 1, l->latency_characteristics.fixed_latency);
			}	
		}
		linkList = g_list_append(linkList, l);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to generate the reverse (unidirecitonal) link from those being learnt
 *  from the received context
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 ////////////////////////////////////////////////////////////////////////////////////////
void generate_reverse_linkList() {
	DEBUG_PC("");
	DEBUG_PC("CREATION OF REVERSE LINKS");
	gint numLinks = g_list_length (linkList);
	DEBUG_PC("Initial Number of links in the main List: %d", numLinks);
	gint i = 0;
	for (GList* ln = g_list_first(linkList);
		(ln) && (i < numLinks);
		ln = g_list_next(ln), i++)
	{
		struct link_t* refLink = (struct link_t*)(ln->data);
		struct link_t* newLink = g_malloc0(sizeof(struct link_t));
		if (newLink == NULL) {
			DEBUG_PC("Memory Allocation Failure");
			exit(-1);
		}
		// Copy the linkId + appending "_rev"
		duplicate_string(newLink->linkId, refLink->linkId);
		strcat(newLink->linkId, "_rev"); 		

		//DEBUG_PC("refLink: %s // newLink: %s", refLink->linkId, newLink->linkId);

		// Assumption: p2p links. The newLink endpoints are the reversed ones form the reference Link (refLink)
		// i.e., refLink A->B, then newLink B->A
		//DEBUG_PC("ref: %s has %d endpoints", refLink->linkId, refLink->numLinkEndPointIds);
#if 1
		if (refLink->numLinkEndPointIds != 2) {
			DEBUG_PC("To construct the new Link from ref: %s, 2 EndPoints are a MUST", refLink->linkId);
			exit(-1);
		}
#endif
		//DEBUG_PC(" * Link[%d] -- Id: %s", numLinks + i, newLink->linkId);

		//DEBUG_PC("Number of Endpoints in Link: %d", refLink->numLinkEndPointIds);
		for (gint j = refLink->numLinkEndPointIds - 1, m = 0; j >= 0; j--, m++) {			
			struct link_endpointId_t* refEndPId = &(refLink->linkEndPointId[j]);
			struct link_endpointId_t* newEndPId = &(newLink->linkEndPointId[m]);
			// Duplicate the topologyId information, i.e., contextId and topology_uuid
			duplicate_string(newEndPId->topology_id.contextId, refEndPId->topology_id.contextId);
			duplicate_string(newEndPId->topology_id.topology_uuid, refEndPId->topology_id.topology_uuid);
			//duplicate the deviceId and endPoint_uuid
			duplicate_string(newEndPId->deviceId, refEndPId->endPointId);
			duplicate_string(newEndPId->endPointId, refEndPId->deviceId);
			//DEBUG_PC("refLink Endpoint[%d]: %s(%s)", j, refEndPId->deviceId, refEndPId->endPointId);
			//DEBUG_PC("newLink Endpoint[%d]: %s(%s)", m, newEndPId->deviceId, newEndPId->endPointId);
			newLink->numLinkEndPointIds++;
		}

		// duplicate forwarding direction
		newLink->forwarding_direction = refLink->forwarding_direction;

		// duplicate capacity attributes
		memcpy(&newLink->potential_capacity.value, &refLink->potential_capacity.value, sizeof(gdouble));
		newLink->potential_capacity.unit = refLink->potential_capacity.unit;

		memcpy(&newLink->available_capacity.value, &refLink->available_capacity.value, sizeof(gdouble));
		newLink->available_capacity.unit = refLink->available_capacity.unit;

		// duplicate cost characteristics
		memcpy(&newLink->cost_characteristics.cost_value, &refLink->cost_characteristics.cost_value, sizeof(gdouble));
		memcpy(&newLink->cost_characteristics.cost_algorithm, &refLink->cost_characteristics.cost_algorithm, sizeof(gdouble));
		duplicate_string(newLink->cost_characteristics.cost_name, refLink->cost_characteristics.cost_name);

		// duplicate latency characteristics
		memcpy(&newLink->latency_characteristics.fixed_latency, &refLink->latency_characteristics.fixed_latency, sizeof(gdouble));
		// Append in the linkList the new creted Link
		linkList = g_list_append(linkList, newLink);
	}
	DEBUG_PC("Terminating Reverse Links [total links: %d]", g_list_length(linkList));
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the JSON object/s for active services
 *
 * 	@param actServiceArray
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void parsing_json_activeService_array(cJSON* actServiceArray) {
	DEBUG_PC("");
	DEBUG_PC("====== PARSING THE JSON CONTENTS OF THE ACTIVE SERVICES =======");
	
	for (gint i = 0; i < cJSON_GetArraySize(actServiceArray); i++) {
		struct activeService_t* actServ = g_malloc0(sizeof(struct activeService_t));
		if (actServ == NULL) {
			DEBUG_PC("Memory Allocation Failure");
			exit(-1);
		}
		cJSON* item = cJSON_GetArrayItem(actServiceArray, i);
		// ServiceId
		cJSON* serviceIdObj = cJSON_GetObjectItem(item, "serviceId");
		if (cJSON_IsObject(serviceIdObj)) {
			parse_json_serviceId(serviceIdObj, &actServ->serviceId);
		}
		// Service Type
		cJSON* serviceTypeObj = cJSON_GetObjectItem(item, "serviceType");
		if (cJSON_IsNumber(serviceTypeObj))
		{
			actServ->service_type = (guint)(serviceTypeObj->valuedouble);
			print_service_type(actServ->service_type);
		}
		// Service Endpoints
		cJSON* endPointIdsArray = cJSON_GetObjectItem(item, "service_endpoints_ids");
		if (cJSON_IsArray(endPointIdsArray)) {
			parse_act_service_endPointsIds_array(endPointIdsArray, actServ);
		}
		// Parsing the active service path
		actServ->activeServPath = NULL;
		cJSON* actServPathArray = cJSON_GetObjectItem(item, "devices");
		if (cJSON_IsArray(endPointIdsArray)) {
			for (gint j = 0; j < cJSON_GetArraySize(actServPathArray); j++) {
				struct activeServPath_t* actServPath = g_malloc0(sizeof(struct activeServPath_t));
				if (actServPath == NULL) {
					DEBUG_PC("Memory Allocation Failure");
					exit(-1);
				}
				cJSON* item2 = cJSON_GetArrayItem(item, j);
				// Topology Id
				cJSON* topologyIdObj = cJSON_GetObjectItem(item2, "topology_id");
				if (cJSON_IsObject(topologyIdObj)) {
					parse_topology_Id(topologyIdObj, &actServPath->topology_id);
				}
				// Device Id
				cJSON* deviceIdObj = cJSON_GetObjectItem(item2, "device_id");
				if (cJSON_IsString(deviceIdObj)) {
					duplicate_string(actServPath->deviceId, deviceIdObj->valuestring);
				}
				// EndPointId
				cJSON* endPointUUIDObj = cJSON_GetObjectItem(item2, "endpoint_uuid");
				if (cJSON_IsString(endPointUUIDObj)) {
					duplicate_string(actServPath->endPointId, endPointUUIDObj->valuestring);
				}
				// Append element from the Active Service Path (i.e.,topologyId, deviceId and endpointId)
				actServ->activeServPath = g_list_append(actServ->activeServPath, actServPath);
			}
		}
		// append into the Actice Service List
		activeServList = g_list_append(activeServList, actServ);
	}
	return;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to parse the JSON object/s for the PATH COMP request (i.e. service
 *  requests, device and links)
 * 	
 * 	@param root
 * 	@param source
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void parsing_json_obj_pathComp_request(cJSON * root, GIOChannel * source)
{
	// Set of services to seek their path and resource selection
	cJSON* serviceListArray = cJSON_GetObjectItem(root, "serviceList");
	if (cJSON_IsArray(serviceListArray)) {
		parsing_json_serviceList_array(serviceListArray);
	}   
    
	// Get the deviceList
	cJSON* deviceListArray = cJSON_GetObjectItem(root, "deviceList");
	if (cJSON_IsArray(deviceListArray)) {
		parsing_json_deviceList_array(deviceListArray);
	}

	// Get the linkList
	cJSON* linkListArray = cJSON_GetObjectItem(root, "linkList");
	if (cJSON_IsArray(linkListArray)) {
		parsing_json_linkList_array(linkListArray);

		// In the context information, if solely the list of links are passed for a single direction, 
		// the reverse direction MUST be created sythetically 
		// LGR: deactivated; link duplication needs to be done smartly with TAPI. done manually in topology by now
		//generate_reverse_linkList();
	}

	// Get the list of active services
	cJSON* actServiceArray = cJSON_GetObjectItem(root, "activeServList");
	if (cJSON_IsArray(actServiceArray)) {
		parsing_json_activeService_array(actServiceArray);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used parse the JSON object/s 
 * 	
 * 	@param data
 *  @param source
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint parsing_json_obj (guchar *data, GIOChannel *source) {
    cJSON * root = cJSON_Parse((const char *)data);
    char * print = cJSON_Print(root);  

	DEBUG_PC("STARTING PARSING JSON CONTENTS");
	parsing_json_obj_pathComp_request (root, source);
	DEBUG_PC("ENDING PARSING JSON CONTENTS");
	// Release the root JSON object variable
	cJSON_free (root);
	g_free(print);
    return 0;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Create new tcp client connected to PATH COMP
 * 
 * 	@param channel_client, GIOChannel
 *  @param fd
 * 	
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
struct pathComp_client * RESTapi_client_create (GIOChannel * channel_client, gint fd) {
	/** check values */
	g_assert(channel_client != NULL); 

	struct pathComp_client* client = g_malloc0 (sizeof (struct pathComp_client));
	if (client == NULL )
	{
		DEBUG_PC ("Malloc for the client failed");
		exit(-1);
	}  

	/** Make client input/output buffer. */
	client->channel = channel_client;	
	client->obuf = stream_new(MAXLENGTH);
	client->ibuf = stream_new(MAXLENGTH);
	client->fd = fd;

	// Clients connected to the PATH COMP SERVER
	CLIENT_ID++;
	client->type = CLIENT_ID;

	//DEBUG_PC ("Client Id: %u is created (%p)", client->type, client);
	//DEBUG_PC ("Client ibuf: %p || obuf: %p", client->ibuf, client->obuf);

	// Add the tcp client to the list
	RESTapi_tcp_client_list = g_list_append (RESTapi_tcp_client_list, client);
	//DEBUG_PC ("Num of TCP Clients: %d", g_list_length (RESTapi_tcp_client_list));
	return client;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Close the tcp client, removing from the rapi_tcp_client_list
 * 
 * 	@param client
 * 	
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_client_close (struct pathComp_client* client) {
	//DEBUG_PC("Closing the client (Id: %d) %p", client->type, client);
	//DEBUG_PC("Client ibuf: %p || obuf: %p", client->ibuf, client->obuf);
	
	if (client->ibuf != NULL) {
		//DEBUG_PC("Client ibuf: %p", client->ibuf);
		stream_free(client->ibuf);
		client->ibuf = NULL;
	}
	if (client->obuf != NULL) {
		//DEBUG_PC("Client obuf: %p", client->obuf);
		stream_free(client->obuf);
		client->obuf = NULL;
	}
	// Remove from the list
	RESTapi_tcp_client_list = g_list_remove (RESTapi_tcp_client_list, client);
	//DEBUG_PC ("TCP Client List: %d", g_list_length(RESTapi_tcp_client_list));
	 
	g_free (client);
	client = NULL;	 
	DEBUG_PC ("client has been removed ...");	 
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Close operations over the passed tcp channel
 * 
 * 	@param source
 * 	
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_close_operations (GIOChannel * source)	{
	gint fd = g_io_channel_unix_get_fd (source);
	
	//DEBUG_PC ("Stop all the operations over the fd: %d", fd);	
	g_io_channel_flush(source, NULL);
	GError *error = NULL;    
	g_io_channel_shutdown (source, TRUE, &error);
	if(error) {
		DEBUG_PC ("An error occurred ...");
	}
	g_io_channel_unref (source);
	return;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Remove the client and close operations over the TCP connection
 * 
 * 	@param client
 *  @param source
 *  @param fd
 * 	
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_stop (struct pathComp_client* client, GIOChannel * source, gint fd) {
	
	DEBUG_PC("Client Socket: %d is Stopped", fd);
	// remove client
	RESTapi_client_close(client);
	// Stop operations over that channel
	RESTapi_close_operations(source);
	close (fd);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used read the different lines ending up in \r\n
 * 	
 * 	@param s
 * 	@param buf
 * 	@param size
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint RESTapi_get_line (GIOChannel *channel, gchar *buf, gint size) {
    gint i = 0;
    //DEBUG_PC ("\n");
    //DEBUG_PC ("----- Read REST API Line(\r\n) ------");
    gint n = 0;
    guchar c = '\0'; // END OF FILE    
    gboolean cr = FALSE;
    while (i < size - 1) {
		n = read_channel (channel, &c, 1);		
		if (n == -1) {
			//DEBUG_PC ("Close the channel and eliminate the client");
			return -1;			
		}	
		if (n > 0) {
			//DEBUG_PC ("%c", c);
			buf[i] = c;
			i++;	
			if (c == '\r') 			{
				cr = TRUE;	      
			}	  
			if ((c == '\n') && (cr == TRUE)) 			{	   
				break;
			}	        
		} 
		else {
			c = '\n';
			buf[i] = c;
			i++;
			break;
		}
    }
    buf[i] = '\0';    
    //DEBUG_PC ("Line (size: %d) buf: %s", i, buf);
    return i;
}  

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used read the HTTP method
 * 	
 * 	@param buf
 * 	@param j
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
guint RESTapi_get_method (gchar *buf, gint *j)
{
	guint RestApiMethod = 0;
	gchar method[255];
	gint i = 0;	
	while (!ISspace(buf[*j]) && (i < sizeof(method) - 1)) {
		method[i] = buf[*j];
		i++; 
		*j = *j + 1;
	}
	method[i] = '\0';
	DEBUG_PC ("REST API METHOD: %s", method);	
	
	// Check that the methods are GET, POST or PUT
	if (strcasecmp((const char *)method, "GET") && strcasecmp((const char *)method, "POST") && 
		strcasecmp ((const char *)method, "HTTP/1.1") && strcasecmp ((const char *)method, "PUT")) {
		DEBUG_PC ("%s is not a method ...", method);
		return RestApiMethod;	
	}
	// Method selector
	if (strncmp ((const char*)method, "GET", 3) == 0) {
		RestApiMethod = REST_API_METHOD_GET;		
	}
	else if (strncmp ((const char*)method, "POST", 4) == 0) {
		RestApiMethod = REST_API_METHOD_POST;
	}	
	else if (strncmp ((const char *)method, "HTTP/1.1", 8) == 0) {
		RestApiMethod = REST_API_METHOD_HTTP;
	}
	else if (strncmp ((const char *)method, "PUT", 3) == 0) {
		RestApiMethod = REST_API_METHOD_PUT;
	}	
	return RestApiMethod;	
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to check whether it is a supported method, and return the associated numerical id
 *
 * 	@param method
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
guint is_rest_api_method(char *method) {
	guint RestApiMethod = 0;
	if (strcasecmp((const char*)method, "GET") && strcasecmp((const char*)method, "POST") &&
		strcasecmp((const char*)method, "HTTP/1.1") && strcasecmp((const char*)method, "PUT")) {
		DEBUG_PC("The method: %s is not currently supported ...", method);
		return RestApiMethod;
	}
	// Method selector
	if (strncmp((const char*)method, "GET", 3) == 0) {
		RestApiMethod = REST_API_METHOD_GET;
	}
	else if (strncmp((const char*)method, "POST", 4) == 0) {
		RestApiMethod = REST_API_METHOD_POST;
	}
	else if (strncmp((const char*)method, "HTTP/1.1", 8) == 0) {
		RestApiMethod = REST_API_METHOD_HTTP;
	}
	else if (strncmp((const char*)method, "PUT", 3) == 0) {
		RestApiMethod = REST_API_METHOD_PUT;
	}
	return RestApiMethod;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used read the url
 * 	
 * 	@param buf
 * 	@param j
 *  @param url
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint get_url (gchar *buf, gint *j, gchar *url)
{
	// Skip space char
	while (ISspace(buf[*j]) && (*j < strlen(buf))) {
		*j = *j + 1;
	}
	
	//DEBUG_PC ("buf[%d]: %c", *j, buf[*j]);
	int result = isspace (buf[*j]);	
	*buf = *buf + *j;
	gint numChar = 0;
	gint initChar = *j;
	result = 0;
	while (result == 0)	{
		*j = *j + 1;
		result = isspace (buf[*j]);
		numChar++;
	}
	//DEBUG_PC ("numChar: %d", numChar);
	memcpy (url, buf + initChar, numChar);
	url[numChar] = '\0';
	//DEBUG_PC ("url: %s", url);
	return numChar;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used read the version
 * 	
 * 	@param buf
 * 	@param j
 *  @param version
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint get_version (gchar *buf, gint *j, gchar *version) {
	// Skip space char
	while (ISspace(buf[*j]) && (*j < strlen(buf))) {
		*j = *j + 1;
	}	
	//DEBUG_PC ("buf[%d]: %c", *j, buf[*j]);
	int result = isspace (buf[*j]);	
	*buf = *buf + *j;
	gint numChar = 0;
	gint initChar = *j;
	result = 0;
	while (result == 0)	{
		*j = *j + 1;
		result = isspace (buf[*j]);
		numChar++;
	}
	//DEBUG_PC ("numChar: %d", numChar);
	memcpy (version, buf + initChar, numChar);
	version[numChar] = '\0';
	//DEBUG_PC ("version: %s", version);
	return numChar;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to trigger the route computation for the network connectivity service
 *  List and retrieve the result
 * 	
 * 	@param compRouteList
 * 	@param raId
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gint triggering_routeComp (struct compRouteOutputList_t *compRouteList, gchar *algId) {
	g_assert (compRouteList);	
	gint httpCode = HTTP_RETURN_CODE_OK;
	DEBUG_PC("Requested Algorithm: %s", algId);
	//////////////////// Algorithm Selector (RAId)//////////////////////////////////////	
	// KSP algorithm
	if (strncmp ((const char*)algId, "KSP", 3) == 0) {
		DEBUG_PC ("Alg Id: KSP");
		httpCode = pathComp_ksp_alg(compRouteList);
	}
	// simple SP algorithm
	else if (strncmp((const char*)algId, "SP", 2) == 0) {
		DEBUG_PC("Alg Id: SP");
		httpCode = pathComp_sp_alg(compRouteList);
	}
	// energy-aware routing
	else if (strncmp((const char*)algId, "EAR", 3) == 0) {
		DEBUG_PC("Alg Id: Energy Aware Routing, EAR");
		httpCode = pathComp_ear_alg(compRouteList);
	}
	return httpCode;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to process the REST API commands
 * 	
 * 	@param source
 * 	@param cond
 * 	@param data
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gboolean RESTapi_activity(GIOChannel *source, GIOCondition cond, gpointer data) {  
	/** some checks */
	g_assert(source != NULL);
	g_assert(data != NULL);	
	
	gchar buf[1024];
	gchar version[255];
	gchar http_result[255];
	gint body_length = 0;	

	struct pathComp_client *client = (struct pathComp_client*)(data);
	DEBUG_PC (" ************************************************************************** ");    
	DEBUG_PC ("                      REST API ACTIVITY Triggered ");
	DEBUG_PC (" ************************************************************************** ");   

	gint fd = g_io_channel_unix_get_fd (source);
	DEBUG_PC ("fd: %d, cond: %d", fd, cond);

	if (cond != G_IO_IN) {
		DEBUG_PC ("Something happening with the channel and fd ... (cond: %d)", cond);
		RESTapi_stop(client, source, fd);
		return FALSE;
	}	
	// Clear input buffer
	stream_reset (client->ibuf);

	// get line
	gint nbytes = RESTapi_get_line (source, buf, sizeof (buf));
	if (nbytes == -1) {
		DEBUG_PC ("nbytes -1 ... CLOSE CLIENT FD and eliminate CLIENT");						
		RESTapi_stop(client, source, fd);
		return FALSE;						
	}	
	if ((buf[0] == '\n') && (nbytes  == 1))
	{
		//DEBUG_PC (" -- buf[0] = newline --");
		RESTapi_stop(client, source, fd);
		return FALSE;
	}
	
	gint i = 0, j = 0;

	while (1) {
		DEBUG_PC("%s", buf);
		char word[255];		
		while (!ISspace(buf[j]) && (i < sizeof(word) - 1)) {
			word[i] = buf[j]; i++; j++;
		}
		word[i] = '\0';
		// Check if word is bound to a Method, i.e., POST, GET, HTTP/1.1.
		guint method = is_rest_api_method(word);
		if (method == 0) {
			 // ignore other REST fields i.e., Host:, User-Agent:, Accept: ....			
			break;
		}
		// word is bound to a known / supported REST Method
		else {
			gchar url[255];
			i = get_url(buf, &j, url);
			url[i] = '\0';
			// GET - used for checking status of pathComp ... used url /pathComp/api/v1/health
			if (method == REST_API_METHOD_GET) {
				if (strncmp((const char*)url, "/health", 7) != 0) {
					DEBUG_PC("unknown url [%s] for GET method -- Heatlh function", url);
					RESTapi_stop(client, source, fd);
					exit(-1);
				}
				else {
					DEBUG_PC("Sending API Response OK to health requests");
					rapi_response_ok(source, HTTP_RETURN_CODE_OK, NULL);
					return TRUE;
				}
			}
			// for method POST, PUT check that the url is "/pathComp"
			if (method == REST_API_METHOD_POST) {
				if (strncmp((const char*)url, "/pathComp/api/v1/compRoute", 26) != 0) {
					DEBUG_PC("Unknown url: %s", url);
					RESTapi_stop(client, source, fd);
					exit(-1);
				}
			}
			// get the version	
			i = get_version(buf, &j, version);
			version[i] = '\0';
			break;
		}
	}
	// Assume HTTP/1.1, then there is Host Header
	memset(buf, '\0', sizeof(buf));        
	nbytes = RESTapi_get_line(source, buf, sizeof (buf));
	if (nbytes == -1) {
		DEBUG_PC ("nbytes -1 ... then close the fd and eliminate associated client");			
		RESTapi_stop(client, source, fd);
		return FALSE;					
	}	
	
	// Headers --- The Header Fields ends up with a void line (i.e., \r\n)
	while ((nbytes > 0) && (strcmp ("\r\n", (const char *)buf) != 0)) {	
		/* read & discard headers */
		memset(buf, '\0', sizeof(buf));  
		nbytes = RESTapi_get_line (source, buf, sizeof (buf));
		if (nbytes == -1) {
			DEBUG_PC ("nbytes -1 ... then close the fd and eliminate associated client");	
			RESTapi_stop(client, source, fd);
			return FALSE;
		}
		//DEBUG_PC ("Header: %s", buf);	  
		if (strncmp ((const char *)buf, "Content-Length:", 15) == 0) {
			//DEBUG_PC ("Header Content-Length Found");
			gchar str[20];
	  
			gint i = 15, k = 0;  // "Content-Length:" We skip the first 16 characters to directly retrieve the length in bytes of the Body of Request
			gchar contentLength[255];
			memset (contentLength, '\0', sizeof (contentLength));			
			while (buf[i] != '\r') {
				//DEBUG_PC ("%c", buf[i]);
				str[k] = buf[i];
				k++, i++;
			}
			str[k] = '\0';			
			j = 0, i = 0;
			while (ISspace(str[j]) && (j < strlen(str))) {
				j++;
			}
			while (j < strlen(str)) {
				contentLength[i] = str[j];
				i++; j++;
			}
			contentLength[i] = '\0';			
			body_length = atoi (contentLength);
			DEBUG_PC ("Body length: %d (%s) in Bytes", body_length, contentLength);
		}	  
	}
	DEBUG_PC("Read Entire HTTP Header");
	if (body_length == 0) {
		DEBUG_PC ("--- NO REST API Body length (length = %d) ---", body_length);
		return TRUE;
	}       
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Processing Body of the Request
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	DEBUG_PC ("REST API Request - Body -");
	nbytes = read_channel (source, (guchar *)(client->ibuf->data + client->ibuf->putp), body_length);
	if ((nbytes < 0) && (body_length > 0)) 	{
		DEBUG_PC ("nbytes: %d; body_length: %d", nbytes, body_length);
		exit (-1);
	}	
	client->ibuf->putp += nbytes;
	client->ibuf->endp += nbytes;		
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Parsing the contents of the Request
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// build the device list	
	deviceList = NULL;
	// build the link list
	linkList = NULL;
	// Create the network connectivity service list
	serviceList = NULL;
	// Create the active service List
	activeServList = NULL;
	
	DEBUG_PC("Parsing JSON...");
	// Process the json contents and store relevant information at Device, Link,
	// and network connectivity service
	gint ret = parsing_json_obj (client->ibuf->data, source);	
	if (ret == -1) 	{
		DEBUG_PC ("Something wrong with the JSON Objects ... ");		
		RESTapi_stop(client, source, fd);
		return FALSE;
	}
	DEBUG_PC("Parsing done");
	
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////		
	// Trigger the path computation	
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////
	DEBUG_PC ("Triggering the computation");
	struct compRouteOutputList_t *compRouteOutputList = create_route_list ();
	gint httpCode = triggering_routeComp (compRouteOutputList, algId);	

	// Send the response to the REST  API Client
	if (httpCode != HTTP_RETURN_CODE_OK) {
		DEBUG_PC ("HTTP CODE: %d -- NO OK", httpCode);
		rapi_response (source, httpCode);
	}
	else {
		DEBUG_PC ("HTTP CODE: %d -- OK", httpCode);
		rapi_response_ok (source, httpCode, compRouteOutputList);            
	}
	
	// Release the variables		
	g_free (compRouteOutputList);	
	g_list_free_full(g_steal_pointer(&linkList), (GDestroyNotify)destroy_link);
	g_list_free_full(g_steal_pointer(&deviceList), (GDestroyNotify)destroy_device);
	g_list_free_full(g_steal_pointer(&serviceList), (GDestroyNotify)destroy_requested_service);
	g_list_free_full(g_steal_pointer(&activeServList), (GDestroyNotify)destroy_active_service);
	return TRUE;  
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Function used to accept a new connection and add the client to list of clients
 * 
 * 	@param source, GIOChannel
 * 	@param cond, GIOCondition
 * 	@param data, gpointer
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
gboolean RESTapi_tcp_new_connection(GIOChannel *source, GIOCondition cond, gpointer data) {
	DEBUG_PC (" ****** New TCP Connection (REST API) ******");
	/** get size of client_addre structure */
	struct sockaddr_in client_addr;
	socklen_t client = sizeof(client_addr);
	
	if ((cond == G_IO_HUP) || (cond == G_IO_ERR) || (G_IO_NVAL)) {
		//DEBUG_PC ("Something happening with the channel and fd ... cond: %d", cond);		
		// Find the associated client (by the fd) and remove from PATH COMP client list. 
		// Stop all the operations over that PATH COMP client bound channel
		struct pathComp_client *pathComp_client = NULL;
		gint fd = g_io_channel_unix_get_fd (source);
		GList *found = g_list_find_custom (RESTapi_tcp_client_list, &fd, find_rl_client_by_fd);
		if (found != NULL) 	{
			pathComp_client = (struct pathComp_client*)(found->data);
			// remove client
			RESTapi_client_close(pathComp_client);
			// Stop operations over that channel
			RESTapi_close_operations(source);
			close (fd);
			return FALSE;
		}
	}
	if (cond == G_IO_IN) 	{
		gint new = accept(g_io_channel_unix_get_fd(source), (struct sockaddr*)&client_addr, &client);
		if (new < 0) {
			//DEBUG_PC ("Unable to accept new connection");
			return FALSE;
		}

		// new channel
		GIOChannel * new_channel = g_io_channel_unix_new (new);		
		//DEBUG_PC ("TCP Connection (REST API) is UP; (socket: %d)", new);
		// create pathComp client		
		struct pathComp_client *new_client = RESTapi_client_create (new_channel, new);
		
		// force binary encoding with NULL
		GError *error = NULL;
		if ( g_io_channel_set_encoding (new_channel, NULL, &error) != G_IO_STATUS_NORMAL) {		
			DEBUG_PC ("Error: %s", error->message);
			exit (-1);
		}
		g_io_channel_set_close_on_unref (new_channel, TRUE);
		// On unbuffered channels, it is safe to mix read
		// & write calls from the new and old APIs.
		g_io_channel_set_buffered (new_channel, FALSE);
		if (g_io_channel_set_flags (new_channel, G_IO_FLAG_NONBLOCK, &error) != G_IO_STATUS_NORMAL ) {
			DEBUG_PC ("Error: %s", error->message);
			exit (-1);
		}
		//Adds the new channel into the main event loop.
		g_io_add_watch (new_channel, G_IO_IN, RESTapi_activity, new_client);
    }	
	return TRUE;
}

///////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief enabling the reuse of the addr for the Server TCP
 * 	
 * 	@param sock
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_tcp_enable_reuseaddr (gint sock)
{
	gint tmp = 1;
	if (sock < 0)
	{
		DEBUG_PC (" socket: %d !!!",sock);
		exit (-1);
	}
	if (setsockopt (sock, SOL_SOCKET, SO_REUSEADDR, (gchar *)&tmp, sizeof (tmp)) == -1)
	{
		DEBUG_PC ("bad setsockopt ...");
		exit (-1);
	}
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_RESTapi.c
 * 	@brief Main function for the creating / maintaining TCP session for the REST API
 *
 *  @ port 
 * 
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void RESTapi_init(gint port)
{     
    DEBUG_PC ("REST API PORT (listening): %d", port);     
	
	// File Descriptor - FD - for the socket
	gint s = socket (AF_INET, SOCK_STREAM, 0);
	if (s == -1)
	{
		DEBUG_PC ("Socket creation: FAILED!!");
		exit (-1);
	}
	DEBUG_PC (" CREATED TCP Connection [@fd: %d]", s);

	// Re-bind
	RESTapi_tcp_enable_reuseaddr(s);	
	struct sockaddr_in addr;
	memset (&addr, 0, sizeof (addr));
	addr.sin_family       = AF_INET;
	addr.sin_port         = htons ((u_short)port);
	addr.sin_addr.s_addr  = INADDR_ANY;      

	// Associate IP address and Port to the created socket
	if (bind (s, (struct sockaddr *)&addr, sizeof(addr)) == -1)
	{
		close (s);
		DEBUG_PC ("Socket bind: FAILED!!");
		exit (-1);
	}
	DEBUG_PC ("Bind to Fd: %d DONE!!", s);

	/** Set up queue for incoming connections */
	if (listen (s, 10) == -1)
	{
		close (s);
		DEBUG_PC ("Socket listen: FAILED!!");
		exit (-1);
	}
	
	//DEBUG_PC ("Listen (up to 10) to Fd: %d Done", s);

	/** Create NEW channel to handle the socket operations*/
	GIOChannel *channel = g_io_channel_unix_new (s);
	gsize buffersize = g_io_channel_get_buffer_size (channel);
	//DEBUG_PC ("GIOChannel with Buffer Size: %d", (gint)buffersize);

	gsize newBufferSize = MAX_GIO_CHANNEL_BUFFER_SIZE;
	g_io_channel_set_buffer_size (channel, newBufferSize);
	buffersize = g_io_channel_get_buffer_size (channel);

	//DEBUG_PC ("GIOChannel with Buffer Size: %d", (gint)buffersize);
	//DEBUG_PC ("Channel associated to fd: %d is created", s);
	
	// Adds the new channel into the main event loop.
	g_io_add_watch (channel, G_IO_IN | G_IO_ERR | G_IO_HUP | G_IO_NVAL, RESTapi_tcp_new_connection, NULL);
	return;     
}
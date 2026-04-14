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

#ifndef _PATH_COMP_REST_API_H
#define _PATH_COMP_REST_API_H


#include <glib.h>
#include <glib/gstdio.h>
#include <glib-2.0/glib/gtypes.h>


#define MAX_GIO_CHANNEL_BUFFER_SIZE     131072

// HTTP RETURN CODES
#define HTTP_RETURN_CODE_OK				200
#define HTTP_RETURN_CODE_CREATED 		201
#define HTTP_RETURN_CODE_BAD_REQUEST    400
#define HTTP_RETURN_CODE_UNAUTHORIZED   401
#define HTTP_RETURN_CODE_FORBIDDEN      403
#define HTTP_RETURN_CODE_NOT_FOUND		404
#define HTTP_RETURN_CODE_NOT_ACCEPTABLE	406

// REST API METHODS (SIMPLY INT ENCODING)
#define REST_API_METHOD_GET		1
#define REST_API_METHOD_POST	2
#define REST_API_METHOD_HTTP	3
#define REST_API_METHOD_PUT		4

#define MAXLENGTH				1024*1024 // 131072 // LGR: increased stream size; otherwise fails for big networks

////////////////////////////////////////////////////
// Client Struct for connecting to PATH COMP SERVER
////////////////////////////////////////////////////
// List of tcp clients connected to PATH COMP

#define PATH_COMP_CLIENT_TYPE	1000
struct pathComp_client {
	/** IO Channel from client. */
	GIOChannel *channel;

	/** Input/output buffer to the client. */    
	struct stream *obuf;
	struct stream *ibuf;

	gint fd; // file descriptor     
    guint type;     
};

void RESTapi_init (gint);
#endif

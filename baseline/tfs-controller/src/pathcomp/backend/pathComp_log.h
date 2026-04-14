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

#ifndef _PATHCOMP_LOG_H
#define _PATHCOMP_LOG_H

#include <glib.h>
#include <glib/gstdio.h>
#include <glib-2.0/glib/gtypes.h>

#define MAXLENGTH 		131072

 /** Stream buffer. */
struct stream
{
	struct stream *next;

	guchar* data;

	/** Put pointer. */
	gulong putp;

	/** Get pointer. */
	gulong getp;

	/** End of pointer. */
	gulong endp;

	/** Data size. */
	gulong size;
};

extern FILE* logfile;

//////////////////////////////////////////////////////
// For debugging
//////////////////////////////////////////////////////
//////////////////////////////////////////////////////
// For debugging
//////////////////////////////////////////////////////
#define __SHORT_FILENAME__ \
        (strrchr(__FILE__,'/') \
         ? strrchr(__FILE__,'/')+1 \
         : __FILE__ \
        )

#define DEBUG_PC(format,...) \
{			       \
	if (logfile != NULL)   \
	{		       \
		g_fprintf(logfile,"%s:%1.5d  %30s "format"\n",\
                                __SHORT_FILENAME__,     		\
                                __LINE__, __FUNCTION__, ##__VA_ARGS__);	        \
		fflush(logfile);					        \
	}								        \
	else 								        \
	{	                                                                \
		g_fprintf(stdout,"%s:%1.5d  %30s "format"\n", \
                                __SHORT_FILENAME__,     		\
                                __LINE__, __FUNCTION__, ##__VA_ARGS__);	        \
		fflush(stdout);					                \
	}                                                                       \
} 

//// Prototypes ////////
struct stream* stream_new(size_t);
void stream_free(struct stream*);
void stream_reset(struct stream*);

gint read_channel(GIOChannel*, guchar*, gint);

#endif
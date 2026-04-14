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
#include <fcntl.h>

#include "pathComp_log.h"


////////////////////////////////////////////////////////////////////////////////////////
 /**
  * 	@file pathComp_log.c
  * 	@brief Create a new variable
  *
  * 	@param size
  *
  *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
  *	@date 2022
  */
/////////////////////////////////////////////////////////////////////////////////////////
struct stream* stream_new(size_t size)
{
	/** check values */
	g_assert(size > 0);

	struct stream* stream = g_malloc0(sizeof(struct stream));
	if (stream == NULL)
	{
		DEBUG_PC("%s memory failed\n", __FUNCTION__);
		exit(-1);
	}

	stream->data = g_malloc0(size);
	if (stream->data == NULL)
	{
		DEBUG_PC("%s memory failed\n", __FUNCTION__);
		exit(-1);
	}
	stream->size = size;

	/** check values */
	g_assert(stream != NULL);

	return stream;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_log.c
 * 	@brief removal of a stream variable
 *
 * 	@param stream
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
  /////////////////////////////////////////////////////////////////////////////////////////
void stream_free(struct stream* s)
{
	/** check values */
	g_assert(s != NULL);

	//DEBUG_PC("s: %p, s->data: %p", s, s->data);
	/** free data */
	g_free(s->data);
	g_free(s);
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_log.c
 * 	@brief reset the contents of the stream
 *
 * 	@param stream
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
void stream_reset(struct stream* s)
{
	/** check values */
	g_assert(s != NULL);
	g_assert(s->putp >= 0);
	g_assert(s->endp >= 0);
	g_assert(s->endp >= 0);

	/** reset */
	s->putp = 0;
	s->endp = 0;
	s->getp = 0;
	return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp_log.c
 * 	@brief Read over a TCP channel the contents
 *
 * 	@param channel
 *  @param ptr
 *  @nbytes
 *
 *	@author Ricardo Mart�nez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
 /////////////////////////////////////////////////////////////////////////////////////////
gint read_channel(GIOChannel* channel, guchar* ptr, gint nbytes)
{
	/** check values */
	g_assert(channel != NULL);
	g_assert(ptr != NULL);
	g_assert(nbytes >= 0);

	/** get the file descriptor */
	gint fd;
	fd = g_io_channel_unix_get_fd(channel);

	gsize nread;
	gint nleft;
	GError* error = NULL;
	GIOStatus status;

	nleft = nbytes;

	// Set blocking
	int flags = fcntl(fd, F_GETFL, 0);
	fcntl(fd, F_SETFL, flags &= ~O_NONBLOCK);

	while (nleft > 0)
	{
		status = g_io_channel_read_chars(channel, (void*)ptr, nleft, &nread, &error);
		if (status != G_IO_STATUS_NORMAL)
		{
			//DEBUG_PC ("gio-test: ...from %d: G_IO_STATUS_%s\n", fd,
			//		  (status == G_IO_STATUS_AGAIN ? "AGAIN" :
			//		  (status == G_IO_STATUS_EOF ? "EOF" :
			//		  (status == G_IO_STATUS_ERROR ? "ERROR" : "???"))));
			return -1;
		}
		if (nread < 0)
		{
			return (nread);
		}
		else
		{
			if (nread == 0)
				break;
		}

		nleft -= nread;
		ptr += nread;
	}

	/** check values */
	g_assert(channel != NULL);
	g_assert(ptr != NULL);
	g_assert(nleft >= 0);
	g_assert(nbytes >= 0);

	return nbytes - nleft;
}
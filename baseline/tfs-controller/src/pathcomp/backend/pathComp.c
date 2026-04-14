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
#include <ctype.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include <glib.h>
#include <sys/time.h>

#ifdef GCOV
// Instrumentation to report code coverage live
// Ref: https://www.osadl.org/fileadmin/dam/interface/docbook/howtos/coverage.pdf
#include <signal.h>

// Code coverage flush method; used to update code coverage reports while the server is running
void __gcov_flush(void); /* check in gcc sources gcc/gcov-io.h for the prototype */

void my_gcov_handler(int signum)
{
  printf("signal received: running __gcov_flush()\n");
  __gcov_flush(); /* dump coverage data on receiving SIGUSR1 */
}
#endif

#include "pathComp_log.h"
#include "pathComp_RESTapi.h"
#include "pathComp.h"

// External Variables
FILE *logfile = NULL;
// PATH COMP IP address API Client
struct in_addr pathComp_IpAddr;
// REST API ENABLED
int RESTAPI_ENABLED = 0;

GMainLoop * loop = NULL;

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp.c
 * 	@brief Read the pathComp.conf file @ /etc/pathComp/
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
void read_pathComp_config_file(FILE *fp)
{
    DEBUG_PC ("Processing pathComp.conf");
    
    char buff[128], ip[128];   
    
    // READ PATH COMP SERVER IP
    memset (&pathComp_IpAddr, (int)0, sizeof (struct in_addr));
    fscanf(fp, "%s %s ", buff, ip);
	pathComp_IpAddr.s_addr = inet_addr(ip);
    DEBUG_PC("pathComp_IpAddr: %s", inet_ntoa (pathComp_IpAddr));
    memset (buff, 0, sizeof (buff));
        
    // Read REST API 
    fscanf (fp, "%s %d ", buff, &RESTAPI_ENABLED);
    if (RESTAPI_ENABLED) DEBUG_PC ("REST API: ON");
    if (RESTAPI_ENABLED == 0) DEBUG_PC ("REST API: OFF");	

    memset (buff, 0, sizeof (buff));
    DEBUG_PC ("CommandLine: %s", buff);
  
    return;
}

////////////////////////////////////////////////////////////////////////////////////////
/**
 * 	@file pathComp.c
 * 	@brief Main function for pathComp server
 *
 *	@author Ricardo Martínez <ricardo.martinez@cttc.es>
 *	@date 2022
 */
/////////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char *argv[])
{
	#ifdef GCOV
	struct sigaction new_action, old_action;
	/* setup signal hander */
 	new_action.sa_handler = my_gcov_handler;
 	sigemptyset(&new_action.sa_mask);
 	new_action.sa_flags = 0;
 	sigaction(SIGUSR1, NULL, &old_action);
 	if (old_action.sa_handler != SIG_IGN)
 		sigaction (SIGUSR1, &new_action, NULL);
	#endif

	DEBUG_PC ("********************************************************************"); 
	DEBUG_PC ("********************************************************************");
	DEBUG_PC (" ---------------------- Path Computation Server---------------------");
	DEBUG_PC ("********************************************************************");
	DEBUG_PC ("********************************************************************"); 

	// processing input parameters
	if (argc == 1)
	{
		DEBUG_PC ("Arguments are missing ...");
		exit (-1);		
	}
	
	// argv[1] specifies the folder and the configuration file
	gchar configFile[50];
	strcpy (configFile, argv[1]);
	DEBUG_PC ("Path Computation Server Config File is: %s", configFile);  
	
	// argv[2] specifies the folder and the log file
	gchar log[50];
	strcpy (log, argv[2]);
	gint screen = strcmp(log, "screen_only");
	if (screen == 0) {
		DEBUG_PC("All logs shown through stdout, i.e.,screen");
		logfile = NULL;
	}
	else {
		DEBUG_PC("PATH COMP log File: %s", log);
		// open the log file	
		logfile = fopen(log, "w");
		DEBUG_PC("log file is opened");
	}
	
	// Read the pathComp.conf file
	FILE *pathComp_config = NULL;	
	pathComp_config = fopen (configFile, "r");
	if (pathComp_config == NULL)
	{	
		DEBUG_PC ("File error\n");
		exit (-1);
	}	
	DEBUG_PC ("pathComp_config.conf is opened");
	
	// Check if flag -d for daemonize 
	if (argc > 3)
	{
		gchar options[10];
		strcpy (options, argv[3]);
		gint ret = strcmp (options, "-d");
		if (ret == 0) daemon(0,0);
	}	
	
	// Process the config file
	read_pathComp_config_file (pathComp_config);

	DEBUG_PC ("\n ---- PATH COMP MAIN LOOP ------");
	/** Creates a new GMainLoop structure */
	loop = g_main_loop_new (NULL, FALSE);
      
	// Iff RESTAPI_ENABLED is ON
	if (RESTAPI_ENABLED)
	{
		RESTapi_init(PATH_COMP_PORT);
	}     
      
	/** execute loop */
	g_main_loop_run (loop);

	/** decrease the one reference of loop when it is finished */
	g_main_loop_unref(loop);
	loop = NULL;
    return 0;
}

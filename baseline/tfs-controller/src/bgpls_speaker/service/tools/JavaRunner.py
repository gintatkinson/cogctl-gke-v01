# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, logging,threading, queue,time,signal
from datetime import datetime, timedelta
from typing import Any, Iterator, List, Optional, Tuple, Union
import logging
import grpc

from concurrent import futures
from lxml import etree
import os
import subprocess
from multiprocessing import Pool

SERVER_ADDRESS = 'localhost:2021'
SERVER_ID = 1
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

XML_FILE="/var/teraflow/bgpls_speaker/service/java/BGP4Parameters_3.xml"
XML_CONFIG_FILE="BGP4Parameters_3.xml"

LOGGER = logging.getLogger(__name__)

class JavaRunner:

    def __init__(self,localPort : int, address : str ="", mngPort : int = 1112):
        self.__peerPort=179
        self.__localPort=localPort 
        self.__managementPort=mngPort
        self.__configFile=XML_CONFIG_FILE
        self.__process=0
        self.__lock = threading.Lock()
        self.__address = address
        self.__portConf=5007
        self.__asNumber=65000

    def getCurrentLocalPort(self):
        with self.__lock:
            return self.__localPort

    def getCurrentMngPort(self):
        with self.__lock:
            return self.__managementPort
    def getPid(self):
        return self.__process.pid

    def execBGPLSpeaker(self) -> bool:
            """
            Executes java BGPLS speaker in non-blocking process
            """
            LOGGER.debug("Before exec")
            os.chdir("/var/teraflow/bgpls_speaker/service/java/")
            self.__process=subprocess.Popen(['java' , '-jar' , 'bgp_ls.jar' , XML_CONFIG_FILE],
                shell=False,start_new_session=True)
            return self.__process

    def setPort(self,port):
         self.__peerPort=port
         return True
    def setAsNumber(self,asNumber):
         self.__asNumber=asNumber
         return True

    def setPeer(self) -> bool:
            """
            Sets XML existing config file with peer address and port. TODO: as_number
            """

            XMLParser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(XML_FILE, parser=XMLParser)
            root = tree.getroot()
            peerAddress = root.find(".//peer")
            peerAddress.text=self.__address
            peerPort = root.find(".//peerPort")
            peerPort.text=str(self.__peerPort)
            localPort = root.find(".//BGP4Port")
            localPort.text=str(self.__localPort)
            myAutonomousSystem = root.find(".//myAutonomousSystem")
            myAutonomousSystem.text=str(self.__asNumber)
            managePort = root.find(".//BGP4ManagementPort")
            managePort.text=str(self.__managementPort)
            tree.write(XML_FILE) #with ... as ..
            return True

    def endBGPSpeaker(self) -> bool:
            """
            Kills java program connected to BGPLS Speaker with SIGKILL signal
            """
            LOGGER.debug("sending kill signal to process %s",self.__process.pid)
            LOGGER.debug("PID: %d",self.__process.pid)
            self.__process.kill()
            return True
    
    def getRunnerInfo(self):
         return self.__address,self.__asNumber,self.__peerPort

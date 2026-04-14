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

import logging,threading
import grpc

from bgpls_speaker.service.tools.DiscoveredDBManager import DiscoveredDBManager
from .protos import grpcService_pb2_grpc
from .protos import grpcService_pb2
from .Tools import UpdateRequest

from concurrent import futures
import os
import subprocess
from multiprocessing import Pool
import logging

from .JavaRunner import JavaRunner

LOGGER = logging.getLogger(__name__)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
SERVER_ADDRESS = 'localhost:2021'

class GrpcServer():

    """
    This class gets the current topology from a bgps speaker module in java 
    and updates the posible new devices to add in the context topology.
    Needs the address, port and as_number from the device that will provide the information via bgpls
    to the java module.
    """
    def __init__(self,DiscoveredDB : DiscoveredDBManager) -> None: # pylint: disable=super-init-not-called
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__out_samples = queue.Queue()
        self.__server=grpc.aio.server()
        self.__javaLocalPort=0 
        self.__mngPort=0 
        self.__runnerList=[]
        self.__discoveredDB=DiscoveredDB
    
    def ConnectThread(self) -> bool:
        if self.__started.is_set(): return True
        self.__started.set() 
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        grpcService_pb2_grpc.add_updateServiceServicer_to_server(self, self.__server)
        self.__server.add_insecure_port(SERVER_ADDRESS)
        LOGGER.info("Starting server on %s", SERVER_ADDRESS)
        self.__server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            LOGGER.info("DISCONNECT")
            self.Disconnect()
        return True

    def Connect(self):
        grpcThread = threading.Thread(target=self.ConnectThread)
        grpcThread.start()
        return True

    def Disconnect(self) -> bool:
        self.__terminate.set()
        if not self.__started.is_set(): return True
        LOGGER.info("Keyboard interrupt, stop server")
        self.__server.stop(0)
        return True

    def update(self,request, context) -> bool:
        """
        Processes the messages recived by de grpc server
        """
        with self.__lock:
            LOGGER.info("(server) Update message from bgpls speaker: \n %s" % (request))
            response = grpcService_pb2.updateResponse(ack="OK")
            update_request = UpdateRequest.from_proto(request)
            self.__discoveredDB.AddToDB(update_request)
            return response
    
    def connectToJavaBgpls(self, address : str = "10.95.86.214", port : str = "179", asNumber : str = "65006"):
        self.setLocalPort()
        runner = JavaRunner(self.__javaLocalPort,address,self.__mngPort)
        runner.setAsNumber(asNumber)
        runner.setPort(port)
        runner.setPeer()
        process=runner.execBGPLSpeaker()
        self.__runnerList.append(runner)

        return process.pid

    def terminateRunners(self):
        for runner in self.__runnerList:
            runner.endBGPSpeaker()
        return True
    
    def terminateGrpcServer(self):
        LOGGER.debug("Terminating java programs...")
        self.terminateRunners()
        LOGGER.debug("Disconnecting grpc server...")
        self.Disconnect() 
        return True

    def terminateRunnerById(self,speaker_id):
        """
        Disconnect from BGP-LS speaker given an speaker Id. Its the same
        as the java running proccess PID.
        """
        for runner in self.__runnerList:
            if(runner.getPid()==speaker_id):
                runner.endBGPSpeaker()
                self.__runnerList.remove(runner)
        return True
        
    def setLocalPort(self,initPort=12179):
        """
        If java already running add 1 to current used port,
        else initialize port .
        initPort --> BGP4Port, usually 179 corresponding to BGP
        """
        with self.__lock:
            if(self.__runnerList):
                LOGGER.debug("Port exists %s",self.__javaLocalPort)
                lastRunner=self.__runnerList[-1]
                self.__javaLocalPort=lastRunner.getCurrentLocalPort()+1
                self.__mngPort=lastRunner.getCurrentMngPort()+1
            else:
                LOGGER.debug("Port DONT exists %s",self.__javaLocalPort)
                self.__javaLocalPort=initPort
                self.__mngPort=1112
            return self.__javaLocalPort
        
    def getSpeakerListIds(self):
        return [runner.getPid() for runner in self.__runnerList]

    def getSpeakerFromId(self,speaker_id):
        """
        Returns address,as_number,peer_port
        """
        for runner in self.__runnerList:
            if(runner.getPid()==speaker_id):
                return runner.getRunnerInfo()
        return None
    
    def getSpeakerIdFromIpAddr(self,addr):
        """
        Returns Id from the speaker IP Address
        """
        for runner in self.__runnerList:
            ip_addr,asN,port=runner.getRunnerInfo()
            if(ip_addr==addr):
                return runner.getPid()
        return

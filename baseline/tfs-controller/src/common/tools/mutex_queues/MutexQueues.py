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

# MutexQueues:
# ------------
# This class enables to schedule and serialize operations concurrently issued
# over a number of resources. For instance, when multiple components want to
# configure devices through the Device component, configuration operations
# have to be serialized to prevent data corruptions, and race conditions, etc.
# Usage Example:
#   class Servicer():
#       def __init__(self):
#           # init other stuff
#           self.drivers = dict()
#           self.mutex_queues = MutexQueues()
#       
#       def configure_device(self, device_uuid, settings):
#           self.mutex_queues.wait_my_turn(device_uuid)
#           driver = self.drivers.get(device_uuid)
#           if driver is None:
#               driver = Driver(device_uuid)
#               self.drivers[device_uuid] = driver
#           driver.configure(settings)
#           self.mutex_queues.signal_done(device_uuid)

import threading
from queue import Queue, Empty
from typing import Dict

class MutexQueues:
    def __init__(self) -> None:
        # lock to protect dictionary updates
        self.lock = threading.Lock()

        # dictionaty of queues of mutexes: queue_name => queue[mutex]
        # first mutex is the running one
        self.mutex_queues : Dict[str, Queue[threading.Event]] = dict()

    def add_alias(self, queue_name_a : str, queue_name_b : str) -> None:
        with self.lock:
            if queue_name_a in self.mutex_queues and queue_name_b not in self.mutex_queues:
                self.mutex_queues[queue_name_b] = self.mutex_queues[queue_name_a]
            elif queue_name_b in self.mutex_queues and queue_name_a not in self.mutex_queues:
                self.mutex_queues[queue_name_a] = self.mutex_queues[queue_name_b]
            elif queue_name_b not in self.mutex_queues and queue_name_a not in self.mutex_queues:
                self.mutex_queues[queue_name_b] = self.mutex_queues.setdefault(queue_name_a, Queue())

    def wait_my_turn(self, queue_name : str) -> None:
        # create my mutex and enqueue it
        mutex = threading.Event()
        with self.lock:
            queue : Queue = self.mutex_queues.setdefault(queue_name, Queue())
            first_in_queue = (queue.qsize() == 0)
            queue.put_nowait(mutex)

        # if I'm the first in the queue upon addition, means there are no running tasks
        # directly return without waiting
        if first_in_queue: return

        # otherwise, wait for my turn in the queue
        mutex.wait()

    def signal_done(self, queue_name : str) -> None:
        # I'm done with my work
        with self.lock:
            queue : Queue = self.mutex_queues.setdefault(queue_name, Queue())
            
            # remove myself from the queue
            try:
                queue.get(block=True, timeout=0.1)
            except Empty:
                pass

            # if there are no other tasks queued, return
            if queue.qsize() == 0: return

            # otherwise, signal the next task in the queue to start
            next_mutex : threading.Event = queue.queue[0]
            next_mutex.set()

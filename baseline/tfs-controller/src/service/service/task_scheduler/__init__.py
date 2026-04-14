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

# TaskScheduler is initialized with a PathComputation Reply or a Service, and it collects/identifies the sub-services,
# sub-connections, and operations associated to them. It discovers and takes care of the inter-dependencies among them,
# and produces an ordered list of tasks to be executed to implement the desired create/delete operation on the service.
# E.g., a service cannot be deleted if connections supporting that service still exist. If these connections are
# supported by sub-services, the connection needs to be torn down before destroying the services.
#
# Internally, it composes a Directed Acyclic Graph (DAG) of dependencies between tasks. Each task performs a specific
# operation on a connection or service. The DAG composition is based on information extracted from a PathComp reply
# and/or interrogating the Context component.
#
# Example:
#   A        B        C
#   *---L3---*---L3---*
#    *--L0--* *--L0--*
# - L3 service between A and C, depends on L3 connections A-B and B-C.
# - Each L3 connection is supported by an L0 service and its corresponding L0 connection.
#
# Dependency structure:
#   service L3:A-C
#       connection L3:A-B
#           service L0:A-B
#               connection L0:A-B
#       connection L3:B-C
#           service L0:B-C
#               connection L0:B-C
#
# Resolution:
#    - service.set(L3:A-C, state=PLANNING)
#    - service.set(L0:A-B, state=PLANNING)
#    - connection.configure(L0:A-B)
#    - service.set(L0:A-B, state=ACTIVE)
#    - connection.configure(L3:A-B)
#    - service.set(L0:B-C, state=PLANNING)
#    - connection.configure(L0:B-C)
#    - service.set(L0:B-C, state=ACTIVE)
#    - connection.configure(L3:B-C)
#    - service.set(L3:A-C, state=ACTIVE)

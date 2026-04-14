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

"""
P4Runtime manager.
"""

import enum
import os
import queue
import time
import logging
from collections import Counter, OrderedDict
from threading import Thread
from tabulate import tabulate
from p4.v1 import p4runtime_pb2
from p4.config.v1 import p4info_pb2

try:
    from .p4_client import P4RuntimeClient, P4RuntimeException,\
        P4RuntimeWriteException, WriteOperation, parse_p4runtime_error
    from .p4_context import P4RuntimeEntity, P4Type, Context
    from .p4_global_options import make_canonical_if_option_set
    from .p4_common import encode,\
        parse_resource_string_from_json, parse_resource_integer_from_json,\
        parse_resource_bytes_from_json, parse_match_operations_from_json,\
        parse_action_parameters_from_json, parse_integer_list_from_json,\
        parse_replicas_from_json
    from .p4_exception import UserError, InvalidP4InfoError
except ImportError:
    from p4_client import P4RuntimeClient, P4RuntimeException,\
        P4RuntimeWriteException, WriteOperation, parse_p4runtime_error
    from p4_context import P4RuntimeEntity, P4Type, Context
    from p4_global_options import make_canonical_if_option_set
    from p4_common import encode,\
        parse_resource_string_from_json, parse_resource_integer_from_json,\
        parse_resource_bytes_from_json, parse_match_operations_from_json,\
        parse_action_parameters_from_json, parse_integer_list_from_json
    from p4_exception import UserError, InvalidP4InfoError

# Logger instance
LOGGER = logging.getLogger(__name__)

# Global P4Runtime context
CONTEXT = Context()

# Global P4Runtime client
CLIENTS = {}

# Constant P4 entities
KEYS_P4 = []
KEY_TABLE = "table"
KEY_ACTION = "action"
KEY_ACTION_PROFILE = "action_profile"
KEY_COUNTER = "counter"
KEY_DIR_COUNTER = "direct_counter"
KEY_METER = "meter"
KEY_DIR_METER = "direct_meter"
KEY_CTL_PKT_METADATA = "controller_packet_metadata"
KEY_DIGEST = "digest"

# Extra resource keys
KEY_CLONE_SESSION = "clone_session"
KEY_ENDPOINT = "endpoint"


def get_context():
    """
    Return P4 context.

    :return: context object
    """
    return CONTEXT

def get_table_type(table):
    """
    Assess the type of P4 table based upon the matching scheme.

    :param table: P4 table
    :return: P4 table type
    """
    is_ternary = False

    for m_f in table.match_fields:
        # LPM and range are special forms of ternary
        if m_f.match_type in [
            p4info_pb2.MatchField.TERNARY,
            p4info_pb2.MatchField.LPM,
            p4info_pb2.MatchField.RANGE
        ]:
            is_ternary = True

    if is_ternary:
        return p4info_pb2.MatchField.TERNARY
    return p4info_pb2.MatchField.EXACT

def match_type_to_str(match_type):
    """
    Convert table match type to string.

    :param match_type: table match type object
    :return: table match type string
    """
    if match_type == p4info_pb2.MatchField.EXACT:
        return "Exact"
    if match_type == p4info_pb2.MatchField.LPM:
        return "LPM"
    if match_type == p4info_pb2.MatchField.TERNARY:
        return "Ternary"
    if match_type == p4info_pb2.MatchField.RANGE:
        return "Range"
    if match_type == p4info_pb2.MatchField.OPTIONAL:
        return "Optional"
    return None



class P4Manager:
    """
    Class to manage the runtime entries of a P4 pipeline.
    """
    local_client = None
    key_id = None

    def __init__(self, device_id: int, ip_address: str, port: int,
                 election_id: tuple, role_name=None, ssl_options=None):
        global CLIENTS

        self.__id = device_id
        self.__ip_address = ip_address
        self.__port = int(port)
        self.__grpc_endpoint = f"{self.__ip_address}:{self.__port}"
        self.key_id = ip_address+str(port)
        CLIENTS[self.key_id] = P4RuntimeClient(
            self.__id, self.__grpc_endpoint, election_id, role_name, ssl_options)
        self.__p4info = None

        self.local_client = CLIENTS[self.key_id]

        # Internal memory for whitebox management
        # | -> P4 entities
        self.p4_objects = {}

        # | -> P4 entities
        self.table_entries = {}
        self.action_profile_members = {}
        self.action_profile_groups = {}
        self.counter_entries = {}
        self.direct_counter_entries = {}
        self.meter_entries = {}
        self.direct_meter_entries = {}
        self.clone_session_entries = {}
        self.multicast_groups = {}

    def start(self, p4bin_path, p4info_path):
        """
        Start the P4 manager. This involves:
        (i) setting the forwarding pipeline of the target switch,
        (ii) creating a P4 context object,
        (iii) Discovering all the entities of the pipeline, and
        (iv) initializing necessary data structures of the manager

        :param p4bin_path: Path to the P4 binary file
        :param p4info_path: Path to the P4 info file
        :return: void
        """

        if not p4bin_path or not os.path.exists(p4bin_path):
            LOGGER.warning("P4 binary file not found")

        if not p4info_path or not os.path.exists(p4info_path):
            LOGGER.warning("P4 info file not found")

        # Forwarding pipeline is only set iff both files are present
        if p4bin_path and p4info_path:
            try:
                self.local_client.set_fwd_pipe_config(p4info_path, p4bin_path)
            except FileNotFoundError as ex:
                LOGGER.critical(ex)
                self.local_client.tear_down()
                raise FileNotFoundError(ex) from ex
            except P4RuntimeException as ex:
                LOGGER.critical("Error when setting config")
                LOGGER.critical(ex)
                self.local_client.tear_down()
                raise P4RuntimeException(ex) from ex
            except Exception as ex:  # pylint: disable=broad-except
                LOGGER.critical("Error when setting config")
                self.local_client.tear_down()
                raise Exception(ex) from ex

        try:
            self.__p4info = self.local_client.get_p4info()
        except P4RuntimeException as ex:
            LOGGER.critical("Error when retrieving P4Info")
            LOGGER.critical(ex)
            self.local_client.tear_down()
            raise P4RuntimeException(ex) from ex

        CONTEXT.set_p4info(self.__p4info)
        self.__discover_objects()
        self.__init_objects()
        LOGGER.info("P4Runtime manager started")

    def stop(self):
        """
        Stop the P4 manager. This involves:
        (i) tearing the P4Runtime client down and
        (ii) cleaning up the manager's internal memory

        :return: void
        """
        global CLIENTS

        # gRPC client must already be instantiated
        assert self.local_client

        # Trigger connection tear down with the P4Runtime server
        self.local_client.tear_down()
        # Remove client entry from global dictionary
        CLIENTS.pop(self.key_id)
        self.__clear()
        LOGGER.info("P4Runtime manager stopped")

    def __clear(self):
        """
        Reset basic members of the P4 manager.

        :return: void
        """
        self.__id = None
        self.__ip_address = None
        self.__port = None
        self.__grpc_endpoint = None
        self.__clear_state()

    def __clear_state(self):
        """
        Reset the manager's internal memory.

        :return: void
        """
        self.table_entries.clear()
        self.action_profile_members.clear()
        self.action_profile_groups.clear()
        self.counter_entries.clear()
        self.direct_counter_entries.clear()
        self.meter_entries.clear()
        self.direct_meter_entries.clear()
        self.clone_session_entries.clear()
        self.multicast_groups.clear()
        self.p4_objects.clear()

    def __init_objects(self):
        """
        Parse the discovered P4 objects and initialize internal memory for all
        the underlying P4 entities.

        :return: void
        """
        global KEY_TABLE, KEY_ACTION, KEY_ACTION_PROFILE, \
            KEY_COUNTER, KEY_DIR_COUNTER, \
            KEY_METER, KEY_DIR_METER, \
            KEY_CTL_PKT_METADATA, KEY_DIGEST, KEYS_P4

        KEY_TABLE = P4Type.table.name
        KEY_ACTION = P4Type.action.name
        KEY_ACTION_PROFILE = P4Type.action_profile.name
        KEY_COUNTER = P4Type.counter.name
        KEY_DIR_COUNTER = P4Type.direct_counter.name
        KEY_METER = P4Type.meter.name
        KEY_DIR_METER = P4Type.direct_meter.name
        KEY_CTL_PKT_METADATA = P4Type.controller_packet_metadata.name
        KEY_DIGEST = P4Type.digest.name

        KEYS_P4 = [
            KEY_TABLE, KEY_ACTION, KEY_ACTION_PROFILE,
            KEY_COUNTER, KEY_DIR_COUNTER,
            KEY_METER, KEY_DIR_METER,
            KEY_CTL_PKT_METADATA, KEY_DIGEST
        ]
        assert (k for k in KEYS_P4)

        if not self.p4_objects:
            LOGGER.warning(
                "Cannot initialize internal memory without discovering "
                "the pipeline\'s P4 objects")
            return

        # Initialize all sorts of entries
        if KEY_TABLE in self.p4_objects:
            for table in self.p4_objects[KEY_TABLE]:
                self.table_entries[table.name] = []

        if KEY_ACTION_PROFILE in self.p4_objects:
            for act_prof in self.p4_objects[KEY_ACTION_PROFILE]:
                self.action_profile_members[act_prof.name] = []
                self.action_profile_groups[act_prof.name] = []

        if KEY_COUNTER in self.p4_objects:
            for cnt in self.p4_objects[KEY_COUNTER]:
                self.counter_entries[cnt.name] = []

        if KEY_DIR_COUNTER in self.p4_objects:
            for d_cnt in self.p4_objects[KEY_DIR_COUNTER]:
                self.direct_counter_entries[d_cnt.name] = []

        if KEY_METER in self.p4_objects:
            for meter in self.p4_objects[KEY_METER]:
                self.meter_entries[meter.name] = []

        if KEY_DIR_METER in self.p4_objects:
            for d_meter in self.p4_objects[KEY_DIR_METER]:
                self.direct_meter_entries[d_meter.name] = []

    def __discover_objects(self):
        """
        Discover and store all P4 objects.

        :return: void
        """
        self.__clear_state()

        for obj_type in P4Type:
            for obj in P4Objects(obj_type):
                if obj_type.name not in self.p4_objects:
                    self.p4_objects[obj_type.name] = []
                self.p4_objects[obj_type.name].append(obj)

    def get_table(self, table_name):
        """
        Get a P4 table by name.

        :param table_name: P4 table name
        :return: P4 table object
        """
        if KEY_TABLE not in self.p4_objects:
            return None
        for table in self.p4_objects[KEY_TABLE]:
            if table.name == table_name:
                return table
        return None

    def get_tables(self):
        """
        Get a list of all P4 tables.

        :return: list of P4 tables or empty list
        """
        if KEY_TABLE not in self.p4_objects:
            return []
        return self.p4_objects[KEY_TABLE]

    def get_action(self, action_name):
        """
        Get action by name.

        :param action_name: name of a P4 action
        :return: action object or None
        """
        if KEY_ACTION not in self.p4_objects:
            return None
        for action in self.p4_objects[KEY_ACTION]:
            if action.name == action_name:
                return action
        return None

    def get_actions(self):
        """
        Get a list of all P4 actions.

        :return: list of P4 actions or empty list
        """
        if KEY_ACTION not in self.p4_objects:
            return []
        return self.p4_objects[KEY_ACTION]

    def get_action_profile(self, action_prof_name):
        """
        Get action profile by name.

        :param action_prof_name: name of the action profile
        :return: action profile object or None
        """
        if KEY_ACTION_PROFILE not in self.p4_objects:
            return None
        for action_prof in self.p4_objects[KEY_ACTION_PROFILE]:
            if action_prof.name == action_prof_name:
                return action_prof
        return None

    def get_action_profiles(self):
        """
        Get a list of all P4 action profiles.

        :return: list of P4 action profiles or empty list
        """
        if KEY_ACTION_PROFILE not in self.p4_objects:
            return []
        return self.p4_objects[KEY_ACTION_PROFILE]

    def get_counter(self, cnt_name):
        """
        Get counter by name.

        :param cnt_name: name of a P4 counter
        :return: counter object or None
        """
        if KEY_COUNTER not in self.p4_objects:
            return None
        for cnt in self.p4_objects[KEY_COUNTER]:
            if cnt.name == cnt_name:
                return cnt
        return None

    def get_counters(self):
        """
        Get a list of all P4 counters.

        :return: list of P4 counters or empty list
        """
        if KEY_COUNTER not in self.p4_objects:
            return []
        return self.p4_objects[KEY_COUNTER]

    def get_direct_counter(self, dir_cnt_name):
        """
        Get direct counter by name.

        :param dir_cnt_name: name of a direct P4 counter
        :return: direct counter object or None
        """
        if KEY_DIR_COUNTER not in self.p4_objects:
            return None
        for d_cnt in self.p4_objects[KEY_DIR_COUNTER]:
            if d_cnt.name == dir_cnt_name:
                return d_cnt
        return None

    def get_direct_counters(self):
        """
        Get a list of all direct P4 counters.

        :return: list of direct P4 counters or empty list
        """
        if KEY_DIR_COUNTER not in self.p4_objects:
            return []
        return self.p4_objects[KEY_DIR_COUNTER]

    def get_meter(self, meter_name):
        """
        Get meter by name.

        :param meter_name: name of a P4 meter
        :return: meter object or None
        """
        if KEY_METER not in self.p4_objects:
            return None
        for meter in self.p4_objects[KEY_METER]:
            if meter.name == meter_name:
                return meter
        return None

    def get_meters(self):
        """
        Get a list of all P4 meters.

        :return: list of P4 meters or empty list
        """
        if KEY_METER not in self.p4_objects:
            return []
        return self.p4_objects[KEY_METER]

    def get_direct_meter(self, dir_meter_name):
        """
        Get direct meter by name.

        :param dir_meter_name: name of a direct P4 meter
        :return: direct meter object or None
        """
        if KEY_DIR_METER not in self.p4_objects:
            return None
        for d_meter in self.p4_objects[KEY_DIR_METER]:
            if d_meter.name == dir_meter_name:
                return d_meter
        return None

    def get_direct_meters(self):
        """
        Get a list of all direct P4 meters.

        :return: list of direct P4 meters or empty list
        """
        if KEY_DIR_METER not in self.p4_objects:
            return []
        return self.p4_objects[KEY_DIR_METER]

    def get_ctl_pkt_metadata(self, ctl_pkt_meta_name):
        """
        Get a packet replication object by name.

        :param ctl_pkt_meta_name: name of a P4 packet replication object
        :return: P4 packet replication object or None
        """
        if KEY_CTL_PKT_METADATA not in self.p4_objects:
            return None
        for pkt_meta in self.p4_objects[KEY_CTL_PKT_METADATA]:
            if ctl_pkt_meta_name == pkt_meta.name:
                return pkt_meta
        return None

    def get_digest(self, digest_name):
        """
        Get a digest object by name.

        :param digest_name: name of a digest object
        :return: digest object or None
        """
        if KEY_DIGEST not in self.p4_objects:
            return None
        for dg in self.p4_objects[KEY_DIGEST]:
            if dg == digest_name.name:
                return digest_name
        return None

    def get_resource_keys(self):
        """
        Retrieve the available P4 resource keys.

        :return: list of P4 resource keys
        """
        return list(self.p4_objects.keys())

    def count_active_entries(self):
        """
        Count the number of active entries across all supported P4 entities.

        :return: active number of entries
        """
        tot_cnt = \
            self.count_table_entries_all() + \
            self.count_counter_entries_all() + \
            self.count_direct_counter_entries_all() + \
            self.count_meter_entries_all() + \
            self.count_direct_meter_entries_all() + \
            self.count_action_prof_member_entries_all() + \
            self.count_action_prof_group_entries_all()

        return tot_cnt

    ############################################################################
    # Table methods
    ############################################################################
    def get_table_names(self):
        """
        Retrieve a list of P4 table names.

        :return: list of P4 table names
        """
        if KEY_TABLE not in self.p4_objects:
            return []
        return list(table.name for table in self.p4_objects[KEY_TABLE])

    def get_table_entries(self, table_name, action_name=None):
        """
        Get a list of P4 table entries by table name and optionally by action.

        :param table_name: name of a P4 table
        :param action_name: action name
        :return: list of P4 table entries or None
        """
        if table_name not in self.table_entries:
            return None
        self.table_entries[table_name].clear()
        self.table_entries[table_name] = []

        try:
            entries = TableEntry(self.local_client, table_name).read()
            assert self.local_client
            for table_entry in entries:
                self.table_entries[table_name].append(table_entry)
            return self.table_entries[table_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get table %s entries: %s",
                         table_name, str(ex))
        return []

    def table_entries_to_json(self, table_name):
        """
        Encode all entries of a P4 table into a JSON object.

        :param table_name: name of a P4 table
        :return: JSON object with table entries
        """
        if (KEY_TABLE not in self.p4_objects) or \
                not self.p4_objects[KEY_TABLE]:
            LOGGER.warning("No table entries to retrieve\n")
            return {}

        table_res = {}

        for table in self.p4_objects[KEY_TABLE]:
            if not table.name == table_name:
                continue

            entries = self.get_table_entries(table.name)
            if len(entries) == 0:
                continue

            table_res["table-name"] = table_name

            for ent in entries:
                entry_match_field = "\n".join(ent.match.fields())
                entry_match_type = match_type_to_str(
                    ent.match.match_type(entry_match_field))

                table_res["id"] = ent.id
                table_res["match-fields"] = []
                for match_field in ent.match.fields():
                    table_res["match-fields"].append(
                        {
                            "match-field": match_field,
                            "match-value": ent.match.value(match_field),
                            "match-type": entry_match_type
                        }
                    )
                table_res["actions"] = []
                table_res["actions"].append(
                    {
                        "action-id": ent.action.id(),
                        "action": ent.action.alias()
                    }
                )
                table_res["priority"] = ent.priority
                table_res["is-default"] = ent.is_default
                table_res["idle-timeout"] = ent.idle_timeout_ns
                if ent.metadata:
                    table_res["metadata"] = ent.metadata

        return table_res

    def count_table_entries(self, table_name, action_name=None):
        """
        Count the number of entries in a P4 table.

        :param table_name: name of a P4 table
        :param action_name: action name
        :return: number of P4 table entries or negative integer
        upon missing table
        """
        count = 0
        try:
            entries = TableEntry(self.local_client, table_name).read()
            count = sum(1 for _ in entries)
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.error("Failed to read entries of table: %s", table_name)

        return count

    def count_table_entries_all(self):
        """
        Count all entries in a P4 table.

        :return: number of P4 table entries
        """
        total_cnt = 0
        for table_name in self.get_table_names():
            cnt = self.count_table_entries(table_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def table_entry_operation_from_json(
            self, json_resource, operation: WriteOperation):
        """
        Parse a JSON-based table entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based table entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """

        table_name = parse_resource_string_from_json(
            json_resource, "table-name")
        match_map = parse_match_operations_from_json(json_resource)
        action_name = parse_resource_string_from_json(
            json_resource, "action-name")
        action_params = parse_action_parameters_from_json(json_resource)
        priority = parse_resource_integer_from_json(json_resource, "priority")
        metadata = parse_resource_bytes_from_json(json_resource, "metadata")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            LOGGER.info("Table entry to insert/update: %s", json_resource)
            return self.insert_table_entry(
                table_name=table_name,
                match_map=match_map,
                action_name=action_name,
                action_params=action_params,
                priority=priority,
                metadata=metadata if metadata else None
            )
        if operation == WriteOperation.delete:
            LOGGER.info("Table entry to delete: %s", json_resource)
            return self.delete_table_entry(
                table_name=table_name,
                match_map=match_map,
                action_name=action_name,
                action_params=action_params,
                priority=priority
            )
        return None

    def insert_table_entry_exact(self,
            table_name, match_map, action_name, action_params, metadata,
            cnt_pkt=-1, cnt_byte=-1):
        """
        Insert an entry into an exact match table.

        :param table_name: P4 table name
        :param match_map: Map of match operations
        :param action_name: Action name
        :param action_params: Map of action parameters
        :param metadata: table metadata
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        assert match_map, "Table entry without match operations is not accepted"
        assert action_name, "Table entry without action is not accepted"

        table_entry = TableEntry(self.local_client, table_name)(action=action_name)

        for match_k, match_v in match_map.items():
            table_entry.match[match_k] = match_v

        for action_k, action_v in action_params.items():
            table_entry.action[action_k] = action_v

        if metadata:
            table_entry.metadata = metadata

        if cnt_pkt > 0:
            table_entry.counter_data.packet_count = cnt_pkt

        if cnt_byte > 0:
            table_entry.counter_data.byte_count = cnt_byte

        ex_msg = ""
        try:
            table_entry.insert()
            LOGGER.info("Inserted exact table entry: %s", table_entry)
        except (P4RuntimeException, P4RuntimeWriteException) as ex:
            ex_msg = str(ex)
            LOGGER.warning(ex)

        # Table entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            table_entry.modify()
            LOGGER.info("Updated exact table entry: %s", table_entry)

        return table_entry

    def insert_table_entry_ternary(self,
            table_name, match_map, action_name, action_params, metadata,
            priority, cnt_pkt=-1, cnt_byte=-1):
        """
        Insert an entry into a ternary match table.

        :param table_name: P4 table name
        :param match_map: Map of match operations
        :param action_name: Action name
        :param action_params: Map of action parameters
        :param metadata: table metadata
        :param priority: entry priority
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        assert match_map, "Table entry without match operations is not accepted"
        assert action_name, "Table entry without action is not accepted"

        table_entry = TableEntry(self.local_client, table_name)(action=action_name)

        for match_k, match_v in match_map.items():
            table_entry.match[match_k] = match_v

        for action_k, action_v in action_params.items():
            table_entry.action[action_k] = action_v

        table_entry.priority = priority

        if metadata:
            table_entry.metadata = metadata

        if cnt_pkt > 0:
            table_entry.counter_data.packet_count = cnt_pkt

        if cnt_byte > 0:
            table_entry.counter_data.byte_count = cnt_byte

        ex_msg = ""
        try:
            table_entry.insert()
            LOGGER.info("Inserted ternary table entry: %s", table_entry)
        except (P4RuntimeException, P4RuntimeWriteException) as ex:
            ex_msg = str(ex)
            LOGGER.error(ex)

        # Table entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            table_entry.modify()
            LOGGER.info("Updated ternary table entry: %s", table_entry)

        return table_entry

    def insert_table_entry_range(self,
            table_name, match_map, action_name, action_params, metadata,
            priority, cnt_pkt=-1, cnt_byte=-1):  # pylint: disable=unused-argument
        """
        Insert an entry into a range match table.

        :param table_name: P4 table name
        :param match_map: Map of match operations
        :param action_name: Action name
        :param action_params: Map of action parameters
        :param metadata: table metadata
        :param priority: entry priority
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        assert match_map, "Table entry without match operations is not accepted"
        assert action_name, "Table entry without action is not accepted"

        raise NotImplementedError(
            "Range-based table insertion not implemented yet")

    def insert_table_entry_optional(self,
            table_name, match_map, action_name, action_params, metadata,
            priority, cnt_pkt=-1, cnt_byte=-1):  # pylint: disable=unused-argument
        """
        Insert an entry into an optional match table.

        :param table_name: P4 table name
        :param match_map: Map of match operations
        :param action_name: Action name
        :param action_params: Map of action parameters
        :param metadata: table metadata
        :param priority: entry priority
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        assert match_map, "Table entry without match operations is not accepted"
        assert action_name, "Table entry without action is not accepted"

        raise NotImplementedError(
            "Optional-based table insertion not implemented yet")

    def insert_table_entry(self, table_name,
                           match_map, action_name, action_params,
                           priority, metadata=None, cnt_pkt=-1, cnt_byte=-1):
        """
        Insert an entry into a P4 table.
        This method has internal logic to discriminate among:
        (i) Exact matches,
        (ii) Ternary matches,
        (iii) LPM matches,
        (iv) Range matches, and
        (v) Optional matches

        :param table_name: name of a P4 table
        :param match_map: map of match operations
        :param action_name: action name
        :param action_params: map of action parameters
        :param priority: entry priority
        :param metadata: entry metadata
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        table = self.get_table(table_name)
        assert table, \
            "P4 pipeline does not implement table " + table_name

        table_type = get_table_type(table)

        if not table_type:
            msg = f"Table {table_name} is undefined, cannot insert entry"
            LOGGER.error(msg)
            raise UserError(msg)

        LOGGER.debug("Table {}: {}".format(table_name, match_type_to_str(table_type)))

        # Exact match is supported
        if table_type == p4info_pb2.MatchField.EXACT:
            return self.insert_table_entry_exact(
                table_name, match_map, action_name, action_params, metadata,
                cnt_pkt, cnt_byte)

        # Ternary and LPM matches are supported
        if table_type in \
                [p4info_pb2.MatchField.TERNARY, p4info_pb2.MatchField.LPM]:
            return self.insert_table_entry_ternary(
                table_name, match_map, action_name, action_params, metadata,
                priority, cnt_pkt, cnt_byte)

        # TODO: Cover RANGE match  # pylint: disable=W0511
        if table_type == p4info_pb2.MatchField.RANGE:
            return self.insert_table_entry_range(
                table_name, match_map, action_name, action_params, metadata,
                priority, cnt_pkt, cnt_byte)

        # TODO: Cover OPTIONAL match  # pylint: disable=W0511
        if table_type == p4info_pb2.MatchField.OPTIONAL:
            return self.insert_table_entry_optional(
                table_name, match_map, action_name, action_params, metadata,
                priority, cnt_pkt, cnt_byte)

        return None

    def delete_table_entry(self, table_name,
                           match_map, action_name, action_params, priority=0):
        """
        Delete an entry from a P4 table.

        :param table_name: name of a P4 table
        :param match_map: map of match operations
        :param action_name: action name
        :param action_params: map of action parameters
        :param priority: entry priority
        :return: deleted entry
        """
        table = self.get_table(table_name)
        assert table, \
            "P4 pipeline does not implement table " + table_name

        table_type = get_table_type(table)

        if not table_type:
            msg = f"Table {table_name} is undefined, cannot delete entry"
            LOGGER.error(msg)
            raise UserError(msg)

        table_entry = TableEntry(self.local_client, table_name)(action=action_name)

        for match_k, match_v in match_map.items():
            table_entry.match[match_k] = match_v

        for action_k, action_v in action_params.items():
            table_entry.action[action_k] = action_v

        if table_type in \
                [p4info_pb2.MatchField.TERNARY, p4info_pb2.MatchField.LPM]:
            if priority == 0:
                msg = f"Table {table_name} is ternary, priority must be != 0"
                LOGGER.error(msg)
                raise UserError(msg)

        # TODO: Ensure correctness of RANGE & OPTIONAL  # pylint: disable=W0511
        if table_type in \
                [p4info_pb2.MatchField.RANGE, p4info_pb2.MatchField.OPTIONAL]:
            raise NotImplementedError(
                "Range and optional-based table deletion not implemented yet")

        table_entry.priority = priority

        ex_msg = ""
        try:
            table_entry.delete()
            LOGGER.info("Deleted entry %s from table: %s", table_entry, table_name)
        except (P4RuntimeException, P4RuntimeWriteException) as ex:
            ex_msg = str(ex)
            LOGGER.warning(ex)

        # Table entry exists, needs to be modified
        if "NOT_FOUND" in ex_msg:
            # TODO: No way to discriminate between a modified entry and an actual table miss
            LOGGER.warning("Table entry was initially modified, thus cannot be removed: %s", table_entry)

        return table_entry

    def delete_table_entries(self, table_name):
        """
        Delete all entries of a P4 table.

        :param table_name: name of a P4 table
        :return: void
        """
        table = self.get_table(table_name)
        assert table, \
            "P4 pipeline does not implement table " + table_name

        if not get_table_type(table):
            msg = f"Table {table_name} is undefined, cannot delete entry"
            LOGGER.error(msg)
            raise UserError(msg)

        TableEntry(self.local_client, table_name).read(function=lambda x: x.delete())
        LOGGER.info("Deleted all entries from table: %s", table_name)

    def print_table_entries_spec(self, table_name):
        """
        Print the specification of a P4 table.
        Specification covers:
        (i) match id,
        (ii) match field name (e.g., ip_proto),
        (iii) match type (e.g., exact, ternary, etc.),
        (iv) match bitwidth
        (v) action id, and
        (vi) action name

        :param table_name: name of a P4 table
        :return: void
        """
        if (KEY_TABLE not in self.p4_objects) or \
                not self.p4_objects[KEY_TABLE]:
            LOGGER.warning("No table specification to print\n")
            return

        for table in self.p4_objects[KEY_TABLE]:
            if not table.name == table_name:
                continue

            entry = []

            for i, match_field in enumerate(table.match_fields):
                table_name = table.name if i == 0 else ""
                match_field_id = match_field.id
                match_field_name = match_field.name
                match_type_str = match_type_to_str(match_field.match_type)
                match_field_bitwidth = match_field.bitwidth

                entry.append(
                    [
                        table_name, str(match_field_id), match_field_name,
                        match_type_str, str(match_field_bitwidth)
                    ]
                )

            print(
                tabulate(
                    entry,
                    headers=[
                        KEY_TABLE, "match id", "match field",
                        "match type", "match width"
                    ],
                    stralign="right",
                    tablefmt="pretty"
                )
            )

            entry.clear()

            for i, action in enumerate(table.action_refs):
                table_name = table.name if i == 0 else ""
                action_id = action.id
                action_name = CONTEXT.get_name_from_id(action.id)
                entry.append([table_name, str(action_id), action_name])

            print(
                tabulate(
                    entry,
                    headers=[KEY_TABLE, "action id", "action name"],
                    stralign="right",
                    tablefmt="pretty"
                )
            )
            print("\n")
            entry.clear()

    def print_table_entries_summary(self):
        """
        Print a summary of a P4 table state.
        Summary covers:
        (i) table name,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_TABLE not in self.p4_objects) or \
                not self.p4_objects[KEY_TABLE]:
            LOGGER.warning("No tables to print\n")
            return

        entry = []

        for table in self.p4_objects[KEY_TABLE]:
            table_name = table.name
            entries = self.get_table_entries(table_name)
            entries_nb = len(entries)
            entry_ids_str = "\n".join(str(e.id) for e in entries) \
                if entries_nb > 0 else "-"

            entry.append([table_name, entries_nb, entry_ids_str])

        print(
            tabulate(
                entry,
                headers=[KEY_TABLE, "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    def print_table_entries(self, table_name):
        """
        Print all entries of a P4 table.

        :param table_name: name of a P4 table
        :return: void
        """
        if (KEY_TABLE not in self.p4_objects) or \
                not self.p4_objects[KEY_TABLE]:
            LOGGER.warning("No table entries to print\n")
            return

        for table in self.p4_objects[KEY_TABLE]:
            if not table.name == table_name:
                continue

            entry = []

            entries = self.get_table_entries(table.name)
            for ent in entries:
                entry_id = ent.id
                mfs = ent.match.fields()
                entry_match_field = "\n".join(mfs)
                entry_match_value = "\n".join(
                    ent.match.value(match_field) for match_field in mfs
                )
                entry_match_type = match_type_to_str(
                    ent.match.match_type(entry_match_field))
                entry_action_id = ent.action.id()
                entry_action = ent.action.alias()
                entry_priority = ent.priority
                entry_is_default = ent.is_default
                entry_idle_timeout_ns = ent.idle_timeout_ns
                entry_metadata = ent.metadata

                entry.append(
                    [
                        table_name, str(entry_id),
                        entry_match_field, entry_match_value, entry_match_type,
                        str(entry_action_id), entry_action,
                        str(entry_priority), str(entry_is_default),
                        str(entry_idle_timeout_ns), str(entry_metadata)
                    ]
                )

            if not entry:
                entry.append([table_name] + ["-"] * 10)

            print(
                tabulate(
                    entry,
                    headers=[
                        KEY_TABLE, "table id",
                        "match field", "match value", "match type",
                        "action id", "action", "priority", "is default",
                        "idle timeout (ns)", "metadata"
                    ],
                    stralign="right",
                    tablefmt="pretty",
                )
            )
            print("\n")

    ############################################################################

    ############################################################################
    # Counter methods
    ############################################################################
    def get_counter_names(self):
        """
        Retrieve a list of P4 counter names.

        :return: list of P4 counter names
        """
        if KEY_COUNTER not in self.p4_objects:
            return []
        return list(cnt.name for cnt in self.p4_objects[KEY_COUNTER])

    def get_counter_entries(self, cnt_name):
        """
        Get a list of P4 counters by name.

        :param cnt_name: name of a P4 counter
        :return: list of P4 counters or None
        """
        if cnt_name not in self.counter_entries:
            return None
        self.counter_entries[cnt_name].clear()
        self.counter_entries[cnt_name] = []

        try:
            for count, cnt_entry in enumerate(CounterEntry(self.local_client, cnt_name).read()):
                LOGGER.debug(
                    "Counter %s - Entry %d\n%s", cnt_name, count, cnt_entry)
                self.counter_entries[cnt_name].append(cnt_entry)
            return self.counter_entries[cnt_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get counter %s entries: %s",
                         cnt_name, str(ex))
            return []

    def counter_entries_to_json(self, cnt_name):
        """
        Encode all counter entries into a JSON object.

        :param cnt_name: counter name
        :return: JSON object with counter entries
        """
        if (KEY_COUNTER not in self.p4_objects) or \
                not self.p4_objects[KEY_COUNTER]:
            LOGGER.warning("No counter entries to retrieve\n")
            return {}

        cnt_res = {}

        for cnt in self.p4_objects[KEY_COUNTER]:
            if not cnt.name == cnt_name:
                continue

            entries = self.get_counter_entries(cnt.name)
            if len(entries) == 0:
                continue

            cnt_res["counter-name"] = cnt_name

            for ent in entries:
                cnt_res["index"] = ent.index
                cnt_res["packet-count"] = ent.packet_count
                cnt_res["byte-count"] = ent.byte_count

        return cnt_res

    def count_counter_entries(self, cnt_name):
        """
        Count the number of P4 counter entries by counter name.

        :param cnt_name: name of a P4 counter
        :return: number of P4 counters or negative integer
        upon missing counter
        """
        entries = self.get_counter_entries(cnt_name)
        if entries is None:
            return -1
        return len(entries)

    def count_counter_entries_all(self):
        """
        Count all entries of a P4 counter.

        :return: number of P4 counter entries
        """
        total_cnt = 0
        for cnt_name in self.get_counter_names():
            cnt = self.count_counter_entries(cnt_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def counter_entry_operation_from_json(self,
                                          json_resource,
                                          operation: WriteOperation):
        """
        Parse a JSON-based counter entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based counter entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        cnt_name = parse_resource_string_from_json(
            json_resource, "counter-name")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            index = parse_resource_integer_from_json(
                json_resource, "index")
            cnt_pkt = parse_resource_integer_from_json(
                json_resource, "packet-count")
            cnt_byte = parse_resource_integer_from_json(
                json_resource, "byte-count")

            LOGGER.debug("Counter entry to insert/update: %s", json_resource)
            return self.insert_counter_entry(
                cnt_name=cnt_name,
                index=index,
                cnt_pkt=cnt_pkt,
                cnt_byte=cnt_byte
            )
        if operation == WriteOperation.delete:
            LOGGER.debug("Counter entry to delete: %s", json_resource)
            return self.clear_counter_entry(
                cnt_name=cnt_name
            )
        return None

    def insert_counter_entry(self, cnt_name, index=None,
                             cnt_pkt=-1, cnt_byte=-1):
        """
        Insert a P4 counter entry.

        :param cnt_name: name of a P4 counter
        :param index: counter index
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        cnt = self.get_counter(cnt_name)
        assert cnt, \
            "P4 pipeline does not implement counter " + cnt_name

        cnt_entry = CounterEntry(self.local_client, cnt_name)

        if index:
            cnt_entry.index = index

        if cnt_pkt > 0:
            cnt_entry.packet_count = cnt_pkt

        if cnt_byte > 0:
            cnt_entry.byte_count = cnt_byte

        cnt_entry.modify()
        LOGGER.info("Updated counter entry: %s", cnt_entry)

        return cnt_entry

    def clear_counter_entry(self, cnt_name):
        """
        Clear the counters of a counter entry by name.

        :param cnt_name: name of a P4 counter
        :return: cleared entry
        """
        cnt = self.get_counter(cnt_name)
        assert cnt, \
            "P4 pipeline does not implement counter " + cnt_name

        cnt_entry = CounterEntry(self.local_client, cnt_name)
        cnt_entry.clear_data()
        LOGGER.info("Cleared data of counter entry: %s", cnt_entry)

        return cnt_entry

    def print_counter_entries_summary(self):
        """
        Print a summary of a P4 counter state.
        Summary covers:
        (i) counter name,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_COUNTER not in self.p4_objects) or \
                not self.p4_objects[KEY_COUNTER]:
            LOGGER.warning("No counters to print\n")
            return

        entry = []

        for cnt in self.p4_objects[KEY_COUNTER]:
            entries = self.get_counter_entries(cnt.name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([cnt.name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=[KEY_COUNTER, "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################

    ############################################################################
    # Direct counter methods
    ############################################################################
    def get_direct_counter_names(self):
        """
        Retrieve a list of direct P4 counter names.

        :return: list of direct P4 counter names
        """
        if KEY_DIR_COUNTER not in self.p4_objects:
            return []
        return list(d_cnt.name for d_cnt in self.p4_objects[KEY_DIR_COUNTER])

    def get_direct_counter_entries(self, d_cnt_name):
        """
        Get a list of direct P4 counters by name.

        :param d_cnt_name: name of a direct P4 counter
        :return: list of direct P4 counters or None
        """
        if d_cnt_name not in self.direct_counter_entries:
            return None
        self.direct_counter_entries[d_cnt_name].clear()
        self.direct_counter_entries[d_cnt_name] = []

        try:
            for count, d_cnt_entry in enumerate(
                    DirectCounterEntry(self.local_client, d_cnt_name).read()):
                LOGGER.debug(
                    "Direct counter %s - Entry %d\n%s",
                    d_cnt_name, count, d_cnt_entry)
                self.direct_counter_entries[d_cnt_name].append(d_cnt_entry)
            return self.direct_counter_entries[d_cnt_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get direct counter %s entries: %s",
                         d_cnt_name, str(ex))
            return []

    def direct_counter_entries_to_json(self, d_cnt_name):
        """
        Encode all direct counter entries into a JSON object.

        :param d_cnt_name: direct counter name
        :return: JSON object with direct counter entries
        """
        if (KEY_DIR_COUNTER not in self.p4_objects) or \
                not self.p4_objects[KEY_DIR_COUNTER]:
            LOGGER.warning("No direct counter entries to retrieve\n")
            return {}

        d_cnt_res = {}

        for d_cnt in self.p4_objects[KEY_DIR_COUNTER]:
            if not d_cnt.name == d_cnt_name:
                continue

            entries = self.get_direct_counter_entries(d_cnt.name)
            if len(entries) == 0:
                continue

            d_cnt_res["direct-counter-name"] = d_cnt_name

            for ent in entries:
                d_cnt_res["match-fields"] = []
                for k, v in ent.table_entry.match.items():
                    d_cnt_res["match-fields"].append(
                        {
                            "match-field": k,
                            "match-value": v
                        }
                    )
                d_cnt_res["priority"] = ent.priority
                d_cnt_res["packet-count"] = ent.packet_count
                d_cnt_res["byte-count"] = ent.byte_count

        return d_cnt_res

    def count_direct_counter_entries(self, d_cnt_name):
        """
        Count the number of direct P4 counter entries by counter name.

        :param d_cnt_name: name of a direct P4 counter
        :return: number of direct P4 counters or negative integer
        upon missing direct counter
        """
        entries = self.get_direct_counter_entries(d_cnt_name)
        if entries is None:
            return -1
        return len(entries)

    def count_direct_counter_entries_all(self):
        """
        Count all entries of a direct P4 counter.

        :return: number of direct P4 counter entries
        """
        total_cnt = 0
        for d_cnt_name in self.get_direct_counter_names():
            cnt = self.count_direct_counter_entries(d_cnt_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def direct_counter_entry_operation_from_json(self,
                                                 json_resource,
                                                 operation: WriteOperation):
        """
        Parse a JSON-based direct counter entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based direct counter entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        d_cnt_name = parse_resource_string_from_json(
            json_resource, "direct-counter-name")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            match_map = parse_match_operations_from_json(json_resource)
            priority = parse_resource_integer_from_json(
                json_resource, "priority")
            cnt_pkt = parse_resource_integer_from_json(
                json_resource, "packet-count")
            cnt_byte = parse_resource_integer_from_json(
                json_resource, "byte-count")

            LOGGER.debug(
                "Direct counter entry to insert/update: %s", json_resource)
            return self.insert_direct_counter_entry(
                d_cnt_name=d_cnt_name,
                match_map=match_map,
                priority=priority,
                cnt_pkt=cnt_pkt,
                cnt_byte=cnt_byte
            )
        if operation == WriteOperation.delete:
            LOGGER.debug("Direct counter entry to delete: %s", json_resource)
            return self.clear_direct_counter_entry(
                d_cnt_name=d_cnt_name
            )
        return None

    def insert_direct_counter_entry(self, d_cnt_name, match_map,
                                    priority, cnt_pkt=-1, cnt_byte=-1):
        """
        Insert a direct P4 counter entry.

        :param d_cnt_name: name of a direct P4 counter
        :param match_map: map of match operations
        :param priority: entry priority
        :param cnt_pkt: packet count
        :param cnt_byte: byte count
        :return: inserted entry
        """
        d_cnt = self.get_direct_counter(d_cnt_name)
        assert d_cnt, \
            "P4 pipeline does not implement direct counter " + d_cnt_name

        assert match_map,\
            "Direct counter entry without match operations is not accepted"

        d_cnt_entry = DirectCounterEntry(self.local_client, d_cnt_name)

        for match_k, match_v in match_map.items():
            d_cnt_entry.table_entry.match[match_k] = match_v

        d_cnt_entry.table_entry.priority = priority

        if cnt_pkt > 0:
            d_cnt_entry.packet_count = cnt_pkt

        if cnt_byte > 0:
            d_cnt_entry.byte_count = cnt_byte

        d_cnt_entry.modify()
        LOGGER.info("Updated direct counter entry: %s", d_cnt_entry)

        return d_cnt_entry

    def clear_direct_counter_entry(self, d_cnt_name):
        """
        Clear the counters of a direct counter entry by name.

        :param d_cnt_name: name of a direct P4 counter
        :return: cleared entry
        """
        d_cnt = self.get_direct_counter(d_cnt_name)
        assert d_cnt, \
            "P4 pipeline does not implement direct counter " + d_cnt_name

        d_cnt_entry = DirectCounterEntry(self.local_client, d_cnt_name)
        d_cnt_entry.clear_data()
        LOGGER.info("Cleared direct counter entry: %s", d_cnt_entry)

        return d_cnt_entry

    def print_direct_counter_entries_summary(self):
        """
        Print a summary of a direct P4 counter state.
        Summary covers:
        (i) direct counter name,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_DIR_COUNTER not in self.p4_objects) or \
                not self.p4_objects[KEY_DIR_COUNTER]:
            LOGGER.warning("No direct counters to print\n")
            return

        entry = []

        for d_cnt in self.p4_objects[KEY_DIR_COUNTER]:
            entries = self.get_direct_counter_entries(d_cnt.name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([d_cnt.name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=[KEY_DIR_COUNTER, "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################

    ############################################################################
    # Meter methods
    ############################################################################
    def get_meter_names(self):
        """
        Retrieve a list of P4 meter names.

        :return: list of P4 meter names
        """
        if KEY_METER not in self.p4_objects:
            return []
        return list(meter.name for meter in self.p4_objects[KEY_METER])

    def get_meter_entries(self, meter_name):
        """
        Get a list of P4 meters by name.

        :param meter_name: name of a P4 meter
        :return: list of P4 meters or None
        """
        if meter_name not in self.meter_entries:
            return None
        self.meter_entries[meter_name].clear()
        self.meter_entries[meter_name] = []

        try:
            for count, meter_entry in enumerate(MeterEntry(self.local_client, meter_name).read()):
                LOGGER.debug(
                    "Meter %s - Entry %d\n%s", meter_name, count, meter_entry)
                self.meter_entries[meter_name].append(meter_entry)
            return self.meter_entries[meter_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get meter %s entries: %s",
                         meter_name, str(ex))
            return []

    def meter_entries_to_json(self, meter_name):
        """
        Encode all meter entries into a JSON object.

        :param meter_name: meter name
        :return: JSON object with meter entries
        """
        if (KEY_METER not in self.p4_objects) or \
                not self.p4_objects[KEY_METER]:
            LOGGER.warning("No meter entries to retrieve\n")
            return {}

        meter_res = {}

        for meter in self.p4_objects[KEY_METER]:
            if not meter.name == meter_name:
                continue

            entries = self.get_meter_entries(meter.name)
            if len(entries) == 0:
                continue

            meter_res["meter-name"] = meter_name

            for ent in entries:
                meter_res["index"] = ent.index
                meter_res["cir"] = ent.cir
                meter_res["cburst"] = ent.cburst
                meter_res["pir"] = ent.pir
                meter_res["pburst"] = ent.pburst

        return meter_res

    def count_meter_entries(self, meter_name):
        """
        Count the number of P4 meter entries by meter name.

        :param meter_name: name of a P4 meter
        :return: number of P4 meters or negative integer
        upon missing meter
        """
        entries = self.get_meter_entries(meter_name)
        if entries is None:
            return -1
        return len(entries)

    def count_meter_entries_all(self):
        """
        Count all entries of a P4 meter.

        :return: number of direct P4 meter entries
        """
        total_cnt = 0
        for meter_name in self.get_meter_names():
            cnt = self.count_meter_entries(meter_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def meter_entry_operation_from_json(self,
                                        json_resource,
                                        operation: WriteOperation):
        """
        Parse a JSON-based meter entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based meter entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        meter_name = parse_resource_string_from_json(
            json_resource, "meter-name")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            index = parse_resource_integer_from_json(
                json_resource, "index")
            cir = parse_resource_integer_from_json(
                json_resource, "committed-information-rate")
            cburst = parse_resource_integer_from_json(
                json_resource, "committed-burst-size")
            pir = parse_resource_integer_from_json(
                json_resource, "peak-information-rate")
            pburst = parse_resource_integer_from_json(
                json_resource, "peak-burst-size")

            LOGGER.debug("Meter entry to insert/update: %s", json_resource)
            return self.insert_meter_entry(
                meter_name=meter_name,
                index=index,
                cir=cir,
                cburst=cburst,
                pir=pir,
                pburst=pburst
            )
        if operation == WriteOperation.delete:
            LOGGER.debug("Meter entry to delete: %s", json_resource)
            return self.clear_meter_entry(
                meter_name=meter_name
            )
        return None

    def insert_meter_entry(self, meter_name, index=None,
                           cir=-1, cburst=-1, pir=-1, pburst=-1):
        """
        Insert a P4 meter entry.

        :param meter_name: name of a P4 meter
        :param index: P4 meter index
        :param cir: meter's committed information rate
        :param cburst: meter's committed burst size
        :param pir: meter's peak information rate
        :param pburst: meter's peak burst size
        :return: inserted entry
        """
        meter = self.get_meter(meter_name)
        assert meter, \
            "P4 pipeline does not implement meter " + meter_name

        meter_entry = MeterEntry(self.local_client, meter_name)

        if index:
            meter_entry.index = index

        if cir > 0:
            meter_entry.cir = cir

        if cburst > 0:
            meter_entry.cburst = cburst

        if pir > 0:
            meter_entry.pir = pir

        if pburst > 0:
            meter_entry.pburst = pburst

        meter_entry.modify()
        LOGGER.info("Updated meter entry: %s", meter_entry)

        return meter_entry

    def clear_meter_entry(self, meter_name):
        """
        Clear the rates and sizes of a meter entry by name.

        :param meter_name: name of a P4 meter
        :return: cleared entry
        """
        meter = self.get_meter(meter_name)
        assert meter, \
            "P4 pipeline does not implement meter " + meter_name

        meter_entry = MeterEntry(self.local_client, meter_name)
        meter_entry.clear_config()
        LOGGER.info("Cleared meter entry: %s", meter_entry)

        return meter_entry

    def print_meter_entries_summary(self):
        """
        Print a summary of a P4 meter state.
        Summary covers:
        (i) meter name,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_METER not in self.p4_objects) or \
                not self.p4_objects[KEY_METER]:
            LOGGER.warning("No meters to print\n")
            return

        entry = []

        for meter in self.p4_objects[KEY_METER]:
            entries = self.get_meter_entries(meter.name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([meter.name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=[KEY_METER, "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################

    ############################################################################
    # Direct meter methods
    ############################################################################
    def get_direct_meter_names(self):
        """
        Retrieve a list of direct P4 meter names.

        :return: list of direct P4 meter names
        """
        if KEY_DIR_METER not in self.p4_objects:
            return []
        return list(d_meter.name for d_meter in self.p4_objects[KEY_DIR_METER])

    def get_direct_meter_entries(self, d_meter_name):
        """
        Get a list of direct P4 meters by name.

        :param d_meter_name: name of a direct P4 meter
        :return: list of direct P4 meters or None
        """
        if d_meter_name not in self.direct_meter_entries:
            return None
        self.direct_meter_entries[d_meter_name].clear()
        self.direct_meter_entries[d_meter_name] = []

        try:
            for count, d_meter_entry in enumerate(
                    MeterEntry(self.local_client, d_meter_name).read()):
                LOGGER.debug(
                    "Direct meter %s - Entry %d\n%s",
                    d_meter_name, count, d_meter_entry)
                self.direct_meter_entries[d_meter_name].append(d_meter_entry)
            return self.direct_meter_entries[d_meter_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get direct meter %s entries: %s",
                         d_meter_name, str(ex))
            return []

    def direct_meter_entries_to_json(self, d_meter_name):
        """
        Encode all direct meter entries into a JSON object.

        :param d_meter_name: direct meter name
        :return: JSON object with direct meter entries
        """
        if (KEY_DIR_METER not in self.p4_objects) or \
                not self.p4_objects[KEY_DIR_METER]:
            LOGGER.warning("No direct meter entries to retrieve\n")
            return {}

        d_meter_res = {}

        for d_meter in self.p4_objects[KEY_DIR_METER]:
            if not d_meter.name == d_meter_name:
                continue

            entries = self.get_direct_meter_entries(d_meter.name)
            if len(entries) == 0:
                continue

            d_meter_res["direct-meter-name"] = d_meter_name

            for ent in entries:
                d_meter_res["match-fields"] = []
                for k, v in ent.table_entry.match.items():
                    d_meter_res["match-fields"].append(
                        {
                            "match-field": k,
                            "match-value": v
                        }
                    )
                d_meter_res["cir"] = ent.cir
                d_meter_res["cburst"] = ent.cburst
                d_meter_res["pir"] = ent.pir
                d_meter_res["pburst"] = ent.pburst

        return d_meter_res

    def count_direct_meter_entries(self, d_meter_name):
        """
        Count the number of direct P4 meter entries by meter name.

        :param d_meter_name: name of a direct P4 meter
        :return: number of direct P4 meters or negative integer
        upon missing direct meter
        """
        entries = self.get_direct_meter_entries(d_meter_name)
        if entries is None:
            return -1
        return len(entries)

    def count_direct_meter_entries_all(self):
        """
        Count all entries of a direct P4 meter.

        :return: number of direct P4 meter entries
        """
        total_cnt = 0
        for d_meter_name in self.get_direct_meter_names():
            cnt = self.count_direct_meter_entries(d_meter_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def direct_meter_entry_operation_from_json(self,
                                               json_resource,
                                               operation: WriteOperation):
        """
        Parse a JSON-based direct meter entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based direct meter entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        d_meter_name = parse_resource_string_from_json(
            json_resource, "direct-meter-name")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            match_map = parse_match_operations_from_json(json_resource)
            cir = parse_resource_integer_from_json(
                json_resource, "committed-information-rate")
            cburst = parse_resource_integer_from_json(
                json_resource, "committed-burst-size")
            pir = parse_resource_integer_from_json(
                json_resource, "peak-information-rate")
            pburst = parse_resource_integer_from_json(
                json_resource, "peak-burst-size")

            LOGGER.debug(
                "Direct meter entry to insert/update: %s", json_resource)
            return self.insert_direct_meter_entry(
                d_meter_name=d_meter_name,
                match_map=match_map,
                cir=cir,
                cburst=cburst,
                pir=pir,
                pburst=pburst
            )
        if operation == WriteOperation.delete:
            LOGGER.debug("Direct meter entry to delete: %s", json_resource)
            return self.clear_direct_meter_entry(
                d_meter_name=d_meter_name
            )
        return None

    def insert_direct_meter_entry(self, d_meter_name, match_map,
                                  cir=-1, cburst=-1, pir=-1, pburst=-1):
        """
        Insert a direct P4 meter entry.

        :param d_meter_name: name of a direct P4 meter
        :param match_map: map of P4 table match operations
        :param cir: meter's committed information rate
        :param cburst: meter's committed burst size
        :param pir: meter's peak information rate
        :param pburst: meter's peak burst size
        :return: inserted entry
        """
        d_meter = self.get_direct_meter(d_meter_name)
        assert d_meter, \
            "P4 pipeline does not implement direct meter " + d_meter_name

        assert match_map,\
            "Direct meter entry without match operations is not accepted"

        d_meter_entry = DirectMeterEntry(self.local_client, d_meter_name)

        for match_k, match_v in match_map.items():
            d_meter_entry.table_entry.match[match_k] = match_v

        if cir > 0:
            d_meter_entry.cir = cir

        if cburst > 0:
            d_meter_entry.cburst = cburst

        if pir > 0:
            d_meter_entry.pir = pir

        if pburst > 0:
            d_meter_entry.pburst = pburst

        d_meter_entry.modify()
        LOGGER.info("Updated direct meter entry: %s", d_meter_entry)

        return d_meter_entry

    def clear_direct_meter_entry(self, d_meter_name):
        """
        Clear the rates and sizes of a direct meter entry by name.

        :param d_meter_name: name of a direct P4 meter
        :return: cleared entry
        """
        d_meter = self.get_direct_meter(d_meter_name)
        assert d_meter, \
            "P4 pipeline does not implement direct meter " + d_meter_name

        d_meter_entry = DirectMeterEntry(self.local_client, d_meter_name)
        d_meter_entry.clear_config()
        LOGGER.info("Cleared direct meter entry: %s", d_meter_entry)

        return d_meter_entry

    def print_direct_meter_entries_summary(self):
        """
        Print a summary of a direct P4 meter state.
        Summary covers:
        (i) direct meter name,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_DIR_METER not in self.p4_objects) or \
                not self.p4_objects[KEY_DIR_METER]:
            LOGGER.warning("No direct meters to print\n")
            return

        entry = []

        for d_meter in self.p4_objects[KEY_DIR_METER]:
            entries = self.get_direct_meter_entries(d_meter.name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([d_meter.name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=[KEY_DIR_METER, "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################

    ############################################################################
    # Action profile member
    ############################################################################
    def get_action_profile_names(self):
        """
        Retrieve a list of action profile names.

        :return: list of action profile names
        """
        if KEY_ACTION_PROFILE not in self.p4_objects:
            return []
        return list(ap_name for ap_name in self.p4_objects[KEY_ACTION_PROFILE])

    def get_action_prof_member_entries(self, ap_name):
        """
        Get a list of action profile members by name.

        :param ap_name: name of a P4 action profile
        :return: list of P4 action profile members
        """
        if ap_name not in self.action_profile_members:
            return None
        self.action_profile_members[ap_name].clear()
        self.action_profile_members[ap_name] = []

        try:
            for count, ap_entry in enumerate(
                    ActionProfileMember(self.local_client, ap_name).read()):
                LOGGER.debug(
                    "Action profile member %s - Entry %d\n%s",
                    ap_name, count, ap_entry)
                self.action_profile_members[ap_name].append(ap_entry)
            return self.action_profile_members[ap_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get action profile member %s entries: %s",
                         ap_name, str(ex))
            return []

    def action_prof_member_entries_to_json(self, ap_name):
        """
        Encode all action profile members into a JSON object.

        :param ap_name: name of a P4 action profile
        :return: JSON object with action profile member entries
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile member entries to retrieve\n")
            return {}

        ap_res = {}

        for act_p in self.p4_objects[KEY_ACTION_PROFILE]:
            if not act_p.name == ap_name:
                continue

            ap_res["action-profile-name"] = ap_name

            entries = self.get_action_prof_member_entries(ap_name)
            for ent in entries:
                action = ent.action
                action_name = CONTEXT.get_name_from_id(action.id)
                ap_res["action"] = action_name
                ap_res["action-params"] = []
                for k, v in action.items():
                    ap_res["action-params"].append(
                        {
                            "param": k,
                            "value": v
                        }
                    )

                ap_res["member-id"] = ent.member_id

        return ap_res

    def count_action_prof_member_entries(self, ap_name):
        """
        Count the number of action profile members by name.

        :param ap_name: name of a P4 action profile
        :return: number of action profile members or negative integer
        upon missing member
        """
        entries = self.get_action_prof_member_entries(ap_name)
        if entries is None:
            return -1
        return len(entries)

    def count_action_prof_member_entries_all(self):
        """
        Count all action profile member entries.

        :return: number of action profile member entries
        """
        total_cnt = 0
        for ap_name in self.get_action_profile_names():
            cnt = self.count_action_prof_member_entries(ap_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def action_prof_member_entry_operation_from_json(self,
                                                     json_resource,
                                                     operation: WriteOperation):
        """
        Parse a JSON-based action profile member entry and insert/update/delete
        it into/from the switch.

        :param json_resource: JSON-based action profile member entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        ap_name = parse_resource_string_from_json(
            json_resource, "action-profile-name")
        member_id = parse_resource_integer_from_json(json_resource, "member-id")
        action_name = parse_resource_string_from_json(
            json_resource, "action-name")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            action_params = parse_action_parameters_from_json(json_resource)

            LOGGER.debug(
                "Action profile member entry to insert/update: %s",
                json_resource)
            return self.insert_action_prof_member_entry(
                ap_name=ap_name,
                member_id=member_id,
                action_name=action_name,
                action_params=action_params
            )
        if operation == WriteOperation.delete:
            LOGGER.debug(
                "Action profile member entry to delete: %s", json_resource)
            return self.delete_action_prof_member_entry(
                ap_name=ap_name,
                member_id=member_id,
                action_name=action_name
            )
        return None

    def insert_action_prof_member_entry(self, ap_name, member_id,
                                        action_name, action_params):
        """
        Insert a P4 action profile member entry.

        :param ap_name: name of a P4 action profile
        :param member_id: action profile member id
        :param action_name: P4 action name
        :param action_params: map of P4 action parameters
        :return: inserted entry
        """
        act_p = self.get_action_profile(ap_name)
        assert act_p, \
            "P4 pipeline does not implement action profile " + ap_name

        ap_member_entry = ActionProfileMember(self.local_client, ap_name)(
            member_id=member_id, action=action_name)

        for action_k, action_v in action_params.items():
            ap_member_entry.action[action_k] = action_v

        ex_msg = ""
        try:
            ap_member_entry.insert()
            LOGGER.info(
                "Inserted action profile member entry: %s", ap_member_entry)
        except P4RuntimeWriteException as ex:
            ex_msg = str(ex)
        except P4RuntimeException as ex:
            raise P4RuntimeException from ex

        # Entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            ap_member_entry.modify()
            LOGGER.info(
                "Updated action profile member entry: %s", ap_member_entry)

        return ap_member_entry

    def delete_action_prof_member_entry(self, ap_name, member_id, action_name):
        """
        Delete a P4 action profile member entry.

        :param ap_name: name of a P4 action profile
        :param member_id: action profile member id
        :param action_name: P4 action name
        :return: deleted entry
        """
        act_p = self.get_action_profile(ap_name)
        assert act_p, \
            "P4 pipeline does not implement action profile " + ap_name

        ap_member_entry = ActionProfileMember(self.local_client, ap_name)(
            member_id=member_id, action=action_name)
        ap_member_entry.delete()
        LOGGER.info("Deleted action profile member entry: %s", ap_member_entry)

        return ap_member_entry

    def print_action_prof_members_summary(self):
        """
        Print a summary of a P4 action profile member state.
        Summary covers:
        (i) action profile member id,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile members to print\n")
            return

        entry = []

        for ap_name in self.p4_objects[KEY_ACTION_PROFILE]:
            entries = self.get_action_prof_member_entries(ap_name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.member_id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([ap_name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=["action profile member", "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    def print_action_prof_member_entries(self, ap_name):
        """
        Print all entries of a P4 action profile member.

        :param ap_name: name of a P4 action profile
        :return: void
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile member entries to print\n")
            return

        for act_p in self.p4_objects[KEY_ACTION_PROFILE]:
            if not act_p.name == ap_name:
                continue

            entry = []

            entries = self.get_action_prof_member_entries(ap_name)
            for ent in entries:
                member_id = ent.member_id
                action = ent.action
                action_name = CONTEXT.get_name_from_id(action.id)

                entry.append([ap_name, str(member_id), action_name])

            if not entry:
                entry.append([ap_name] + ["-"] * 2)

            print(
                tabulate(
                    entry,
                    headers=["action profile member", "member id", "action"],
                    stralign="right",
                    tablefmt="pretty"
                )
            )
            print("\n")

    ############################################################################
    # Action profile group
    ############################################################################
    def get_action_prof_group_entries(self, ap_name):
        """
        Get a list of action profile groups by name.

        :param ap_name: name of a P4 action profile
        :return: list of P4 action profile groups
        """
        if ap_name not in self.action_profile_groups:
            return None
        self.action_profile_groups[ap_name].clear()
        self.action_profile_groups[ap_name] = []

        try:
            for count, ap_entry in enumerate(
                    ActionProfileGroup(self.local_client, ap_name).read()):
                LOGGER.debug("Action profile group %s - Entry %d\n%s",
                             ap_name, count, ap_entry)
                self.action_profile_groups[ap_name].append(ap_entry)
            return self.action_profile_groups[ap_name]
        except P4RuntimeException as ex:
            LOGGER.error("Failed to get action profile group %s entries: %s",
                         ap_name, str(ex))
            return []

    def count_action_prof_group_entries(self, ap_name):
        """
        Count the number of action profile groups by name.

        :param ap_name: name of a P4 action profile
        :return: number of action profile groups or negative integer
        upon missing group
        """
        entries = self.get_action_prof_group_entries(ap_name)
        if entries is None:
            return -1
        return len(entries)

    def count_action_prof_group_entries_all(self):
        """
        Count all action profile group entries.

        :return: number of action profile group entries
        """
        total_cnt = 0
        for ap_name in self.get_action_profile_names():
            cnt = self.count_action_prof_group_entries(ap_name)
            if cnt < 0:
                continue
            total_cnt += cnt
        return total_cnt

    def action_prof_group_entries_to_json(self, ap_name):
        """
        Encode all action profile groups into a JSON object.

        :param ap_name: name of a P4 action profile
        :return: JSON object with action profile group entries
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile group entries to retrieve\n")
            return {}

        ap_res = {}

        for act_p in self.p4_objects[KEY_ACTION_PROFILE]:
            if not act_p.name == ap_name:
                continue

            ap_res["action-profile-name"] = ap_name

            entries = self.get_action_prof_group_entries(ap_name)
            for ent in entries:
                ap_res["group-id"] = ent.group_id
                ap_res["members"] = []
                for mem in ent.members:
                    ap_res["members"].append(
                        {
                            "member": mem
                        }
                    )

        return ap_res

    def action_prof_group_entry_operation_from_json(self,
                                                    json_resource,
                                                    operation: WriteOperation):
        """
        Parse a JSON-based action profile group entry and insert/update/delete
        it into/from the switch.

        :param json_resource: JSON-based action profile group entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        ap_name = parse_resource_string_from_json(
            json_resource, "action-profile-name")
        group_id = parse_resource_integer_from_json(json_resource, "group-id")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            members = parse_integer_list_from_json(
                json_resource, "members", "member")

            LOGGER.debug(
                "Action profile group entry to insert/update: %s",
                json_resource)
            return self.insert_action_prof_group_entry(
                ap_name=ap_name,
                group_id=group_id,
                members=members
            )
        if operation == WriteOperation.delete:
            LOGGER.debug(
                "Action profile group entry to delete: %s", json_resource)
            return self.delete_action_prof_group_entry(
                ap_name=ap_name,
                group_id=group_id
            )
        return None

    def insert_action_prof_group_entry(self, ap_name, group_id, members=None):
        """
        Insert a P4 action profile group entry.

        :param ap_name: name of a P4 action profile
        :param group_id: action profile group id
        :param members: list of associated action profile members
        :return: inserted entry
        """
        ap = self.get_action_profile(ap_name)
        assert ap, \
            "P4 pipeline does not implement action profile " + ap_name

        ap_group_entry = ActionProfileGroup(self.local_client, ap_name)(group_id=group_id)

        if members:
            for m in members:
                ap_group_entry.add(member_id=m)

        ex_msg = ""
        try:
            ap_group_entry.insert()
            LOGGER.info(
                "Inserted action profile group entry: %s", ap_group_entry)
        except P4RuntimeWriteException as ex:
            ex_msg = str(ex)
        except P4RuntimeException as ex:
            raise P4RuntimeException from ex

        # Entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            ap_group_entry.modify()
            LOGGER.info(
                "Updated action profile group entry: %s", ap_group_entry)

        return ap_group_entry

    def delete_action_prof_group_entry(self, ap_name, group_id):
        """
        Delete a P4 action profile group entry.

        :param ap_name: name of a P4 action profile
        :param group_id: action profile group id
        :return: deleted entry
        """
        ap = self.get_action_profile(ap_name)
        assert ap, \
            "P4 pipeline does not implement action profile " + ap_name

        ap_group_entry = ActionProfileGroup(self.local_client, ap_name)(group_id=group_id)
        ap_group_entry.delete()
        LOGGER.info("Deleted action profile group entry: %s", ap_group_entry)

        return ap_group_entry

    def clear_action_prof_group_entry(self, ap_name, group_id):
        """
        Clean a P4 action profile group entry.

        :param ap_name: name of a P4 action profile
        :param group_id: action profile group id
        :return: cleaned entry
        """
        ap = self.get_action_profile(ap_name)
        assert ap, \
            "P4 pipeline does not implement action profile " + ap_name

        ap_group_entry = ActionProfileGroup(self.local_client, ap_name)(group_id=group_id)
        ap_group_entry.clear()
        LOGGER.info("Cleared action profile group entry: %s", ap_group_entry)

        return ap_group_entry

    def print_action_prof_groups_summary(self):
        """
        Print a summary of a P4 action profile group state.
        Summary covers:
        (i) action profile group id,
        (ii) number of entries in the table, and
        (iii) a string of \n-separated entry IDs.

        :return: void
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile groups to print\n")
            return

        entry = []

        for ap_name in self.p4_objects[KEY_ACTION_PROFILE]:
            entries = self.get_action_prof_group_entries(ap_name)
            entries_nb = len(entries)
            entry_ids_str = ",".join(str(e.group_id) for e in entries) \
                if entries_nb > 0 else "-"
            entry.append([ap_name, str(entries_nb), entry_ids_str])

        print(
            tabulate(
                entry,
                headers=["action profile group", "# of entries", "entry ids"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    def print_action_prof_group_entries(self, ap_name):
        """
        Print all entries of a P4 action profile group.

        :param ap_name: name of a P4 action profile
        :return: void
        """
        if (KEY_ACTION_PROFILE not in self.p4_objects) or \
                not self.p4_objects[KEY_ACTION_PROFILE]:
            LOGGER.warning("No action profile group entries to print\n")
            return

        for ap in self.p4_objects[KEY_ACTION_PROFILE]:
            if not ap.name == ap_name:
                continue

            entry = []

            entries = self.get_action_prof_group_entries(ap_name)
            for e in entries:
                group_id = e.group_id
                members_str = "\n".join(m for m in e.members)
                entry.append([ap_name, str(group_id), members_str])

            if not entry:
                entry.append([ap_name] + ["-"] * 2)

            print(
                tabulate(
                    entry,
                    headers=[
                        "action profile group", "group id", "members"
                    ],
                    stralign="right",
                    tablefmt="pretty"
                )
            )
            print("\n")

    ############################################################################
    # Packet replication method 1: Multicast group
    ############################################################################
    def get_multicast_group_entry(self, group_id):
        """
        Get a multicast group entry by group id.

        :param group_id: id of a multicast group
        :return: multicast group entry or none
        """
        if group_id not in self.multicast_groups:
            return None
        self.multicast_groups[group_id] = None

        try:
            mcast_group = MulticastGroupEntry(self.local_client, group_id).read()
            LOGGER.debug("Multicast group %d\n%s", group_id, mcast_group)
            self.multicast_groups[group_id] = mcast_group
            return self.multicast_groups[group_id]
        except P4RuntimeException as ex:
            LOGGER.error(ex)
            return None

    def count_multicast_groups(self):
        """
        Count the number of multicast groups.

        :return: number of multicast groups
        """
        return len(self.multicast_groups.keys())

    def multicast_group_entries_to_json(self):
        """
        Encode all multicast groups into a JSON object.

        :return: JSON object with multicast group entries
        """
        if not self.multicast_groups:
            LOGGER.warning("No multicast group entries to retrieve\n")
            return {}

        mcast_list_res = []

        for mcast_group in self.multicast_groups.values():
            mcast_res = {}
            mcast_res["group-id"] = mcast_group.group_id

            mcast_res["egress-ports"] = []
            mcast_res["instances"] = []
            for r in mcast_group.replicas:
                mcast_res["egress-ports"].append(
                    {
                        "egress-port": r.egress_port
                    }
                )
                mcast_res["instances"].append(
                    {
                        "instance": r.instance
                    }
                )
            mcast_list_res.append(mcast_res)

        return mcast_list_res

    def multicast_group_entry_operation_from_json(self,
                                                  json_resource,
                                                  operation: WriteOperation):
        """
        Parse a JSON-based multicast group entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based multicast group entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        group_id = parse_resource_integer_from_json(json_resource, "group-id")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            ports = parse_integer_list_from_json(
                json_resource, "ports", "port")

            LOGGER.debug(
                "Multicast group entry to insert/update: %s", json_resource)
            return self.insert_multicast_group_entry(
                group_id=group_id,
                ports=ports
            )
        if operation == WriteOperation.delete:
            LOGGER.debug("Multicast group entry to delete: %s", json_resource)
            return self.delete_multicast_group_entry(
                group_id=group_id
            )
        return None

    def insert_multicast_group_entry(self, group_id, ports):
        """
        Insert a new multicast group.

        :param group_id: id of a multicast group
        :param ports: list of egress ports to multicast
        :return: inserted multicast group
        """
        assert group_id > 0, \
            "Multicast group " + group_id + " must be > 0"
        assert ports, \
            "No multicast group ports are provided"

        mcast_group = MulticastGroupEntry(self.local_client, group_id)
        for p in ports:
            mcast_group.add(p, 1)

        ex_msg = ""
        try:
            mcast_group.insert()
            LOGGER.info("Inserted multicast group entry: %s", mcast_group)
        except P4RuntimeWriteException as ex:
            ex_msg = str(ex)
        except P4RuntimeException as ex:
            raise P4RuntimeException from ex

        # Entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            mcast_group.modify()
            LOGGER.info("Updated multicast group entry: %s", mcast_group)

        self.multicast_groups[group_id] = mcast_group

        return mcast_group

    def delete_multicast_group_entry(self, group_id):
        """
        Delete a multicast group by id.

        :param group_id: id of a multicast group
        :return: deleted multicast group
        """
        assert group_id > 0, \
            "Multicast group " + group_id + " must be > 0"

        mcast_group = MulticastGroupEntry(self.local_client, group_id)
        mcast_group.delete()

        if group_id in self.multicast_groups:
            del self.multicast_groups[group_id]
        LOGGER.info(
            "Deleted multicast group %d", group_id)

        return mcast_group

    def delete_multicast_group_entries(self):
        """
        Delete all multicast groups.

        :return: void
        """
        for mcast_group in MulticastGroupEntry(self.local_client).read():
            gid = mcast_group.group_id
            mcast_group.delete()
            del self.multicast_groups[gid]

        assert self.count_multicast_groups() == 0, \
            "Failed to purge all multicast groups"
        LOGGER.info("Deleted all multicast groups")

    def print_multicast_groups_summary(self):
        """
        Print a summary of a P4 multicast group state.
        Summary covers:
        (i) multicast group id,
        (ii) a string of \n-separated egress ports, and
        (iii) a string of \n-separated replica instances.

        :return: void
        """
        entry = []

        for mcast_group in self.multicast_groups.values():
            ports_str = "\n".join(
                str(r.egress_port) for r in mcast_group.replicas)
            inst_str = "\n".join(
                str(r.instance) for r in mcast_group.replicas)
            entry.append([str(mcast_group.group_id), ports_str, inst_str])

        if not entry:
            entry.append(3 * ["-"])

        print(
            tabulate(
                entry,
                headers=["multicast group id", "egress ports", "instances"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################
    # Packet replication method 2: Clone session
    ############################################################################
    def get_clone_session_entry(self, session_id):
        """
        Get a clone session entry by session id.

        :param session_id: id of a clone session
        :return: clone session entry or none
        """
        if session_id not in self.clone_session_entries:
            return None
        self.clone_session_entries[session_id] = None

        try:
            session = CloneSessionEntry(self.local_client, session_id).read()
            LOGGER.debug("Clone session %d\n%s", session_id, session)
            self.clone_session_entries[session_id] = session
            return self.clone_session_entries[session_id]
        except P4RuntimeException as ex:
            LOGGER.error(ex)
            return None

    def count_clone_session_entries(self):
        """
        Count the number of clone sessions.

        :return: number of clone sessions
        """
        return len(self.clone_session_entries.keys())

    def clone_session_entries_to_json(self):
        """
        Encode all clone sessions into a JSON object.

        :return: JSON object with clone session entries
        """
        if not self.clone_session_entries:
            LOGGER.warning("No clone session entries to retrieve\n")
            return {}

        session_list_res = []

        for session in self.clone_session_entries.values():
            session_res = {}
            session_res["session-id"] = session.session_id

            session_res["egress-ports"] = []
            session_res["instances"] = []
            for r in session.replicas:
                session_res["egress-ports"].append(
                    {
                        "egress-port": r.egress_port
                    }
                )
                session_res["instances"].append(
                    {
                        "instance": r.instance
                    }
                )
            session_list_res.append(session_res)

        return session_list_res

    def clone_session_entry_operation_from_json(self,
                                                json_resource,
                                                operation: WriteOperation):
        """
        Parse a JSON-based clone session entry and insert/update/delete it
        into/from the switch.

        :param json_resource: JSON-based clone session entry
        :param operation: Write operation (i.e., insert, modify, delete)
        to perform.
        :return: inserted entry or None in case of parsing error
        """
        session_id = parse_resource_integer_from_json(
            json_resource, "session-id")

        if operation in [WriteOperation.insert, WriteOperation.update]:
            replicas = parse_replicas_from_json(json_resource)

            LOGGER.debug(
                "Clone session entry to insert/update: %s", json_resource)
            return self.insert_clone_session_entry(
                session_id=session_id,
                replicas=replicas
            )
        if operation == WriteOperation.delete:
            LOGGER.debug(
                "Clone session entry to delete: %s", json_resource)
            return self.delete_clone_session_entry(
                session_id=session_id
            )
        return None

    def insert_clone_session_entry(self, session_id, replicas):
        """
        Insert a new clone session.

        :param session_id: id of a clone session
        :param replicas: list of egress ports to clone session
        :return: inserted clone session
        """
        assert session_id > 0, \
            "Clone session " + session_id + " must be > 0"
        assert replicas, \
            "No clone session replicas are provided"
        assert isinstance(replicas, dict), \
            "Clone session replicas must be a dictionary"

        session = CloneSessionEntry(self.local_client, session_id)
        for eg_port,instance in replicas.items():
            session.add(eg_port, instance)

        ex_msg = ""
        try:
            session.insert()
            LOGGER.info("Inserted clone session entry: %s", session)
        except P4RuntimeWriteException as ex:
            ex_msg = str(ex)
        except P4RuntimeException as ex:
            raise P4RuntimeException from ex

        # Entry exists, needs to be modified
        if "ALREADY_EXISTS" in ex_msg:
            session.modify()
            LOGGER.info("Updated clone session entry: %s", session)

        self.clone_session_entries[session_id] = session

        return session

    def delete_clone_session_entry(self, session_id):
        """
        Delete a clone session by id.

        :param session_id: id of a clone session
        :return: deleted clone session
        """
        assert session_id > 0, \
            "Clone session " + session_id + " must be > 0"

        session = CloneSessionEntry(self.local_client, session_id)

        try:
            session.delete()
            LOGGER.info("Deleted clone session %d", session_id)
        except (P4RuntimeException, P4RuntimeWriteException) as ex:
            LOGGER.error(ex)

        if session_id in self.clone_session_entries:
            del self.clone_session_entries[session_id]

        return session

    def delete_clone_session_entries(self):
        """
        Delete all clone sessions.

        :return: void
        """
        for e in CloneSessionEntry(self.local_client).read():
            sid = e.session_id
            e.delete()
            del self.clone_session_entries[sid]

        assert self.count_multicast_groups() == 0, \
            "Failed to purge all clone sessions"
        LOGGER.info("Deleted all clone sessions")

    def print_clone_sessions_summary(self):
        """
        Print a summary of a P4 clone session state.
        Summary covers:
        (i) clone session id,
        (ii) a string of \n-separated egress ports, and
        (iii) a string of \n-separated replica instances.

        :return: void
        """
        entry = []

        for session in self.clone_session_entries.values():
            ports_str = "\n".join(
                str(r.egress_port) for r in session.replicas)
            inst_str = "\n".join(
                str(r.instance) for r in session.replicas)
            entry.append([str(session.session_id), ports_str, inst_str])

        if not entry:
            entry.append(3 * ["-"])

        print(
            tabulate(
                entry,
                headers=["clone session id", "egress ports", "instances"],
                stralign="right",
                tablefmt="pretty"
            )
        )
        print("\n")

    ############################################################################
    # Packet replication method 3: Packet in
    ############################################################################
    def get_packet_metadata(self, meta_type, attr_name=None, attr_id=None):
        """
        Retrieve the pipeline's metadata by metadata type field.

        :param meta_type: metadata type field
        :param attr_name: metadata name field (optional)
        :param attr_id: metadata id field (optional)
        :return: packet metadata
        """
        for table in self.__p4info.controller_packet_metadata:
            pre = table.preamble
            if pre.name == meta_type:
                for meta in table.metadata:
                    if attr_name is not None:
                        if meta.name == attr_name:
                            return meta
                    elif attr_id is not None:
                        if meta.id == attr_id:
                            return meta
        raise AttributeError(
            f"ControllerPacketMetadata {meta_type} has no metadata "
            f"{attr_name if attr_name is not None else attr_id} (check P4Info)")

    # TODO: test packet in  # pylint: disable=W0511
    def create_packet_in(self, payload, metadata=None):
        """
        Create a packet-in object.

        :param payload: packet-in payload
        :param metadata: packet-in metadata (optional)
        :return: packet-in object
        """
        if not self.p4_objects[KEY_CTL_PKT_METADATA]:
            LOGGER.warning("Cannot create packet in. "
                           "No controller packet metadata in the pipeline\n")
            return None

        packet_in = PacketIn(self.local_client)
        packet_in.payload = payload
        if metadata:
            for name, value in metadata.items():
                p4info_meta = self.get_packet_metadata("packet_in", name)
                meta = packet_in.metadata.add()
                meta.metadata_id = p4info_meta.id
                meta.value = encode(value, p4info_meta.bitwidth)
        return packet_in

    def send_packet_in(self, payload, metadata=None, timeout=1):
        """
        Send a packet-in message.
        Note that the sniff method is blocking, thus it should be invoked by
        another thread.

        :param payload: packet-in payload
        :param metadata: packet-in metadata (optional)
        :param timeout: packet-in timeout (defaults to 1s)
        :return: void
        """
        packet_in = self.create_packet_in(payload, metadata)

        # TODO: experimental piece of code  # pylint: disable=W0511
        captured_packet = []

        def _sniff_packet(captured_pkt):
            """
            Invoke packet-in sniff method.

            :param captured_pkt: buffer for the packet to be captured
            :return: void
            """
            captured_pkt += packet_in.sniff(timeout=timeout)

        _t = Thread(target=_sniff_packet, args=(captured_packet,))
        _t.start()
        # P4Runtime client sends the packet to the switch
        self.local_client.stream_in_q["packet"].put(packet_in)
        _t.join()
        LOGGER.info("Packet-in sent: %s", packet_in)

    ############################################################################
    # Packet replication method 4: Packet out
    ############################################################################
    # TODO: test packet out  # pylint: disable=W0511
    def create_packet_out(self, payload, metadata=None):
        """
        Create a packet-out object.

        :param payload: packet-out payload
        :param metadata: packet-out metadata (optional)
        :return: packet-out object
        """
        if not self.p4_objects[KEY_CTL_PKT_METADATA]:
            LOGGER.warning("Cannot create packet out. "
                           "No controller packet metadata in the pipeline\n")
            return None

        packet_out = PacketOut(self.local_client)
        packet_out.payload = payload
        if metadata:
            for name, value in metadata.items():
                p4info_meta = self.get_packet_metadata("packet_out", name)
                meta = packet_out.metadata.add()
                meta.metadata_id = p4info_meta.id
                meta.value = encode(value, p4info_meta.bitwidth)
        return packet_out

    def send_packet_out(self, payload, metadata=None):
        """
        Send a packet-out message.

        :param payload: packet-out payload
        :param metadata: packet-out metadata (optional)
        :return: void
        """
        packet_out = self.create_packet_out(payload, metadata)
        packet_out.send()
        LOGGER.info("Packet-out sent: %s", packet_out)

    ############################################################################
    # Packet replication method 5: Idle timeout notification
    ############################################################################
    # TODO: Support IdleTimeoutNotification  # pylint: disable=W0511
    ############################################################################

    def print_objects(self):
        """
        Print all P4 objects of the installed pipeline.

        :return: void
        """
        if not self.p4_objects:
            self.__discover_objects()

        for obj_name, objects in self.p4_objects.items():
            entry = []

            for obj in objects:
                entry.append([obj.name])

            if not entry:
                entry.append("-")
            print(
                tabulate(
                    entry,
                    headers=[obj_name],
                    stralign="right",
                    tablefmt="pretty"
                )
            )
        print("\n")


class P4Object:
    """
    P4 object.
    """

    def __init__(self, obj_type, obj):
        self.name = obj.preamble.name
        self.id = obj.preamble.id
        self._obj_type = obj_type
        self._obj = obj
        self.__doc__ = f"""
A wrapper around the P4Info Protobuf message for
{obj_type.pretty_name} '{self.name}'.
You can access any field from the message with <self>.<field name>.
You can access the name directly with <self>.name.
You can access the id directly with <self>.id.
If you need the underlying Protobuf message, you can access it with msg().
"""

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __settattr__(self, name, value):
        return UserError(
            f"Operation {name}:{value} not supported")

    def msg(self):
        """Get Protobuf message object"""
        return self._obj

    def actions(self):
        """Print list of actions, only for tables and action profiles."""
        if self._obj_type == P4Type.table:
            for action in self._obj.action_refs:
                print(CONTEXT.get_name_from_id(action.id))
        elif self._obj_type == P4Type.action_profile:
            t_id = self._obj.table_ids[0]
            t_name = CONTEXT.get_name_from_id(t_id)
            t = CONTEXT.get_table(t_name)
            for action in t.action_refs:
                print(CONTEXT.get_name_from_id(action.id))
        else:
            raise UserError(
                "'actions' is only available for tables and action profiles")


class P4Objects:
    """
    P4 objects.
    """

    def __init__(self, obj_type):
        self._obj_type = obj_type
        self._names = sorted([name for name, _ in CONTEXT.get_objs(obj_type)])
        self._iter = None
        self.__doc__ = """
All the {pnames} in the P4 program.
To access a specific {pname}, use {p4info}['<name>'].
You can use this class to iterate over all {pname} instances:
\tfor x in {p4info}:
\t\tprint(x.id)
""".format(pname=obj_type.pretty_name, pnames=obj_type.pretty_names,
           p4info=obj_type.p4info_name)

    def __getitem__(self, name):
        obj = CONTEXT.get_obj(self._obj_type, name)
        if obj is None:
            raise UserError(
                f"{self._obj_type.pretty_name} '{name}' does not exist")
        return P4Object(self._obj_type, obj)

    def __setitem__(self, name, value):
        raise UserError("Operation not allowed")

    def __iter__(self):
        self._iter = iter(self._names)
        return self

    def __next__(self):
        name = next(self._iter)
        return self[name]


class MatchKey:
    """
    P4 match key.
    """

    def __init__(self, table_name, match_fields):
        self._table_name = table_name
        self._fields = OrderedDict()
        self._fields_suffixes = {}
        for mf in match_fields:
            self._add_field(mf)
        self._mk = OrderedDict()
        self._set_docstring()

    def _set_docstring(self):
        self.__doc__ = f"Match key fields for table '{self._table_name}':\n\n"
        for _, info in self._fields.items():
            self.__doc__ += str(info)
        self.__doc__ += """
Set a field value with <self>['<field_name>'] = '...'
  * For exact match: <self>['<f>'] = '<value>'
  * For ternary match: <self>['<f>'] = '<value>&&&<mask>'
  * For LPM match: <self>['<f>'] = '<value>/<mask>'
  * For range match: <self>['<f>'] = '<value>..<mask>'
  * For optional match: <self>['<f>'] = '<value>'

If it's inconvenient to use the whole field name, you can use a unique suffix.

You may also use <self>.set(<f>='<value>')
\t(<f> must not include a '.' in this case,
but remember that you can use a unique suffix)
"""

    def _get_mf(self, name):
        if name in self._fields:
            return self._fields[name]
        if name in self._fields_suffixes:
            return self._fields[self._fields_suffixes[name]]
        raise UserError(
            f"'{name}' is not a valid match field name, nor a valid unique "
            f"suffix, for table '{self._table_name}'")

    def __setitem__(self, name, value):
        field_info = self._get_mf(name)
        self._mk[name] = self._parse_mf(value, field_info)
        print(self._mk[name])

    def __getitem__(self, name):
        _ = self._get_mf(name)
        print(self._mk.get(name, "Unset"))

    def _parse_mf(self, s, field_info):
        if not isinstance(s, str):
            raise UserError("Match field value must be a string")
        if field_info.match_type == p4info_pb2.MatchField.EXACT:
            return self._parse_mf_exact(s, field_info)
        if field_info.match_type == p4info_pb2.MatchField.LPM:
            return self._parse_mf_lpm(s, field_info)
        if field_info.match_type == p4info_pb2.MatchField.TERNARY:
            return self._parse_mf_ternary(s, field_info)
        if field_info.match_type == p4info_pb2.MatchField.RANGE:
            return self._parse_mf_range(s, field_info)
        if field_info.match_type == p4info_pb2.MatchField.OPTIONAL:
            return self._parse_mf_optional(s, field_info)
        raise UserError(
            f"Unsupported match type for field:\n{field_info}")

    def _parse_mf_exact(self, s, field_info):
        v = encode(s.strip(), field_info.bitwidth)
        return self._sanitize_and_convert_mf_exact(v, field_info)

    def _sanitize_and_convert_mf_exact(self, value, field_info):
        mf = p4runtime_pb2.FieldMatch()
        mf.field_id = field_info.id
        mf.exact.value = make_canonical_if_option_set(value)
        return mf

    def _parse_mf_optional(self, s, field_info):
        v = encode(s.strip(), field_info.bitwidth)
        return self._sanitize_and_convert_mf_optional(v, field_info)

    def _sanitize_and_convert_mf_optional(self, value, field_info):
        mf = p4runtime_pb2.FieldMatch()
        mf.field_id = field_info.id
        mf.optional.value = make_canonical_if_option_set(value)
        return mf

    def _parse_mf_lpm(self, s, field_info):
        try:
            prefix, length = s.split('/')
            prefix, length = prefix.strip(), length.strip()
        except ValueError:
            prefix = s
            length = str(field_info.bitwidth)

        prefix = encode(prefix, field_info.bitwidth)
        try:
            length = int(length)
        except ValueError as ex:
            raise UserError(f"'{length}' is not a valid prefix length") from ex

        return self._sanitize_and_convert_mf_lpm(prefix, length, field_info)

    def _sanitize_and_convert_mf_lpm(self, prefix, length, field_info):
        if length == 0:
            raise UserError(
                "Ignoring LPM don't care match (prefix length of 0) "
                "as per P4Runtime spec")

        mf = p4runtime_pb2.FieldMatch()
        mf.field_id = field_info.id
        mf.lpm.prefix_len = length

        first_byte_masked = length // 8
        if first_byte_masked == len(prefix):
            mf.lpm.value = prefix
            return mf

        barray = bytearray(prefix)
        transformed = False
        r = length % 8
        byte_mask = 0xff & ((0xff << (8 - r)))
        if barray[first_byte_masked] & byte_mask != barray[first_byte_masked]:
            transformed = True
            barray[first_byte_masked] = barray[first_byte_masked] & byte_mask

        for i in range(first_byte_masked + 1, len(prefix)):
            if barray[i] != 0:
                transformed = True
                barray[i] = 0
        if transformed:
            print("LPM value was transformed to conform to the P4Runtime spec "
                  "(trailing bits must be unset)")
        mf.lpm.value = bytes(make_canonical_if_option_set(barray))
        return mf

    def _parse_mf_ternary(self, s, field_info):
        try:
            value, mask = s.split('&&&')
            value, mask = value.strip(), mask.strip()
        except ValueError:
            value = s.strip()
            mask = "0b" + ("1" * field_info.bitwidth)

        value = encode(value, field_info.bitwidth)
        mask = encode(mask, field_info.bitwidth)

        return self._sanitize_and_convert_mf_ternary(value, mask, field_info)

    def _sanitize_and_convert_mf_ternary(self, value, mask, field_info):
        if int.from_bytes(mask, byteorder='big') == 0:
            raise UserError(
                "Ignoring ternary don't care match (mask of 0s) "
                "as per P4Runtime spec")

        mf = p4runtime_pb2.FieldMatch()
        mf.field_id = field_info.id

        barray = bytearray(value)
        transformed = False
        for i in range(len(value)):
            if barray[i] & mask[i] != barray[i]:
                transformed = True
                barray[i] = barray[i] & mask[i]
        if transformed:
            print("Ternary value was transformed to conform to "
                  "the P4Runtime spec (masked off bits must be unset)")
        mf.ternary.value = bytes(
            make_canonical_if_option_set(barray))
        mf.ternary.mask = make_canonical_if_option_set(mask)
        return mf

    def _parse_mf_range(self, s, field_info):
        try:
            start, end = s.split('..')
            start, end = start.strip(), end.strip()
        except ValueError as ex:
            raise UserError(f"'{s}' does not specify a valid range, "
                            f"use '<start>..<end>'") from ex

        start = encode(start, field_info.bitwidth)
        end = encode(end, field_info.bitwidth)

        return self._sanitize_and_convert_mf_range(start, end, field_info)

    def _sanitize_and_convert_mf_range(self, start, end, field_info):
        start_ = int.from_bytes(start, byteorder='big')
        end_ = int.from_bytes(end, byteorder='big')
        if start_ > end_:
            raise UserError("Invalid range match: start is greater than end")
        if start_ == 0 and end_ == ((1 << field_info.bitwidth) - 1):
            raise UserError(
                "Ignoring range don't care match (all possible values) "
                "as per P4Runtime spec")
        mf = p4runtime_pb2.FieldMatch()
        mf.field_id = field_info.id
        mf.range.low = make_canonical_if_option_set(start)
        mf.range.high = make_canonical_if_option_set(end)
        return mf

    def _add_field(self, field_info):
        self._fields[field_info.name] = field_info
        self._recompute_suffixes()

    def _recompute_suffixes(self):
        suffixes = {}
        suffix_count = Counter()
        for fname in self._fields:
            suffix = None
            for s in reversed(fname.split(".")):
                suffix = s if suffix is None else s + "." + suffix
                suffixes[suffix] = fname
                suffix_count[suffix] += 1
        for suffix, c in suffix_count.items():
            if c > 1:
                del suffixes[suffix]
        self._fields_suffixes = suffixes

    def __str__(self):
        return '\n'.join([str(mf) for name, mf in self._mk.items()])

    def fields(self):
        """
        Return a list of match fields.

        :return: list of match fields or None
        """
        fields = []
        for name, _ in self._mk.items():
            fields.append(name)
        return fields

    def value(self, field_name):
        """
        Get the value of a match field.

        :param field_name: match field name
        :return: match field value
        """
        for name, info in self._fields.items():
            if name != field_name:
                continue
            if info.match_type == p4info_pb2.MatchField.EXACT:
                return self._mk[name].exact.value.hex()
            if info.match_type == p4info_pb2.MatchField.LPM:
                return self._mk[name].lpm.value.hex()
            if info.match_type == p4info_pb2.MatchField.TERNARY:
                return self._mk[name].ternary.value.hex()
            if info.match_type == p4info_pb2.MatchField.RANGE:
                return self._mk[name].range.value.hex()
            if info.match_type == p4info_pb2.MatchField.OPTIONAL:
                return self._mk[name].optional.value.hex()
        return None

    def match_type(self, field_name):
        """
        Get the type of a match field.

        :param field_name: match field name
        :return: match field type
        """
        for name, info in self._fields.items():
            if name not in field_name:
                continue
            return info.match_type
        return None

    def set(self, **kwargs):
        """
        Set match field parameter.

        :param kwargs: parameters
        :return: void
        """
        for name, value in kwargs.items():
            self[name] = value

    def clear(self):
        """
        Clear all match fields.

        :return: void
        """
        self._mk.clear()

    def _count(self):
        return len(self._mk)


class Action:
    """
    P4 action.
    """

    def __init__(self, action_name=None):
        self._init = False
        if action_name is None:
            raise UserError("Please provide name for action")
        self.action_name = action_name
        action_info = CONTEXT.get_action(action_name)
        if action_info is None:
            raise UserError(f"Unknown action '{action_name}'")
        self._action_id = action_info.preamble.id
        self._params = OrderedDict()
        for param in action_info.params:
            self._params[param.name] = param
        self._action_info = action_info
        self._param_values = OrderedDict()
        self._set_docstring()
        self._init = True

    def _set_docstring(self):
        self.__doc__ = f"Action parameters for action '{self.action_name}':\n\n"
        for _, info in self._params.items():
            self.__doc__ += str(info)
        self.__doc__ += "\n\n"
        self.__doc__ += "Set a param value with " \
                        "<self>['<param_name>'] = '<value>'\n"
        self.__doc__ += "You may also use <self>.set(<param_name>='<value>')\n"

    def _get_param(self, name):
        if name not in self._params:
            raise UserError("'{name}' is not a valid action parameter name "
                            "for action '{self._action_name}'")
        return self._params[name]

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "action_name":
            raise UserError("Cannot change action name")
        super().__setattr__(name, value)

    def __setitem__(self, name, value):
        param_info = self._get_param(name)
        self._param_values[name] = self._parse_param(value, param_info)
        print(self._param_values[name])

    def __getitem__(self, name):
        _ = self._get_param(name)
        print(self._param_values.get(name, "Unset"))

    def _parse_param(self, s, param_info):
        if not isinstance(s, str):
            raise UserError("Action parameter value must be a string")
        v = encode(s, param_info.bitwidth)
        p = p4runtime_pb2.Action.Param()
        p.param_id = param_info.id
        p.value = make_canonical_if_option_set(v)
        return p

    def msg(self):
        """
        Create an action message.

        :return: action message
        """
        msg = p4runtime_pb2.Action()
        msg.action_id = self._action_id
        msg.params.extend(self._param_values.values())
        return msg

    def _from_msg(self, msg):
        assert self._action_id == msg.action_id
        self._params.clear()
        for p in msg.params:
            p_name = CONTEXT.get_param_name(self.action_name, p.param_id)
            self._param_values[p_name] = p

    def __str__(self):
        return str(self.msg())

    def id(self):
        """
        Get action ID.

        :return: action ID
        """
        return self._action_info.preamble.id

    def alias(self):
        """
        Get action alias.

        :return: action alias
        """
        return str(self._action_info.preamble.alias)

    def set(self, **kwargs):
        """
        Set action parameters.

        :param kwargs: parameters
        :return: void
        """
        for name, value in kwargs.items():
            self[name] = value


class _EntityBase:
    """
    Basic entity.
    """
    local_client = None

    def __init__(self, p4_client, entity_type, p4runtime_cls, modify_only=False):
        self._init = False
        self._entity_type = entity_type
        self._entry = p4runtime_cls()
        self._modify_only = modify_only
        self.local_client = p4_client

    def __dir__(self):
        d = ["msg", "read"]
        if self._modify_only:
            d.append("modify")
        else:
            d.extend(["insert", "modify", "delete"])
        return d

    # to be called before issuing a P4Runtime request
    # enforces checks that cannot be performed when setting individual fields
    def _validate_msg(self):
        return True

    def _update_msg(self):
        pass

    def __getattr__(self, name):
        raise AttributeError(f"'{self.__class__.__name__}' object "
                             f"has no attribute '{name}'")

    def msg(self):
        """
        Get a basic entity message.

        :return: entity message
        """
        self._update_msg()
        return self._entry

    def _write(self, type_):
        self._update_msg()
        self._validate_msg()
        update = p4runtime_pb2.Update()
        update.type = type_
        getattr(update.entity, self._entity_type.name).CopyFrom(self._entry)
        self.local_client.write_update(update)

    def insert(self):
        """
        Insert an entity.

        :return: void
        """
        if self._modify_only:
            raise NotImplementedError(
                f"Insert not supported for {self._entity_type.name}")
        logging.debug("Inserting entry")
        self._write(p4runtime_pb2.Update.INSERT)

    def delete(self):
        """
        Delete an entity.

        :return: void
        """
        if self._modify_only:
            raise NotImplementedError(
                f"Delete not supported for {self._entity_type.name}")
        logging.debug("Deleting entry")
        self._write(p4runtime_pb2.Update.DELETE)

    def modify(self):
        """
        Modify an entity.

        :return: void
        """
        logging.debug("Modifying entry")
        self._write(p4runtime_pb2.Update.MODIFY)

    def _from_msg(self, msg):
        raise NotImplementedError

    def read(self, function=None):
        """
        Read an entity.

        :param function: function to read (optional)
        :return: retrieved entity
        """
        # Entities should override this method and provide a helpful docstring
        self._update_msg()
        self._validate_msg()
        entity = p4runtime_pb2.Entity()
        getattr(entity, self._entity_type.name).CopyFrom(self._entry)

        iterator = self.local_client.read_one(entity)

        # Cannot use a (simpler) generator here as we need to
        # decorate __next__ with @parse_p4runtime_error.
        class _EntryIterator:
            def __init__(self, entity, it):
                self._entity = entity
                self._it = it
                self._entities_it = None

            def __iter__(self):
                return self

            @parse_p4runtime_error
            def __next__(self):
                if self._entities_it is None:
                    rep = next(self._it)
                    self._entities_it = iter(rep.entities)
                try:
                    entity = next(self._entities_it)
                except StopIteration:
                    self._entities_it = None
                    return next(self)

                if isinstance(self._entity, _P4EntityBase):
                    ent = type(self._entity)(
                        self._entity.name)  # create new instance of same entity
                else:
                    ent = type(self._entity)()
                msg = getattr(entity, self._entity._entity_type.name)
                ent._from_msg(msg)
                # neither of these should be needed
                # ent._update_msg()
                # ent._entry.CopyFrom(msg)
                return ent

        if function is None:
            return _EntryIterator(self, iterator)
        for x in _EntryIterator(self, iterator):
            function(x)


class _P4EntityBase(_EntityBase):
    """
    Basic P4 entity.
    """

    def __init__(self, p4_client, p4_type, entity_type, p4runtime_cls, name=None,
                 modify_only=False):
        super().__init__(p4_client, entity_type, p4runtime_cls, modify_only)
        assert self.local_client, "No local P4 client instance"
        self._p4_type = p4_type
        if name is None:
            raise UserError(
                f"Please provide name for {p4_type.pretty_name}")
        self.name = name
        self._info = P4Objects(p4_type)[name]
        self.id = self._info.id

    def __dir__(self):
        return super().__dir__() + ["name", "id", "info"]

    def _from_msg(self, msg):
        raise NotImplementedError

    def info(self):
        """
        Display P4Info entry for the object.

        :return: P4 info entry
        """
        return self._info


class ActionProfileMember(_P4EntityBase):
    """
    P4 action profile member.
    """

    def __init__(self, p4_client, action_profile_name=None):
        super().__init__(p4_client,
            P4Type.action_profile, P4RuntimeEntity.action_profile_member,
            p4runtime_pb2.ActionProfileMember, action_profile_name)
        self.member_id = 0
        self.action = None
        self._valid_action_ids = self._get_action_set()
        self.__doc__ = f"""
An action profile member for '{action_profile_name}'

Use <self>.info to display the P4Info entry for the action profile.

Set the member id with <self>.member_id = <expr>.

To set the action specification <self>.action = <instance of type Action>.
To set the value of action parameters,
use <self>.action['<param name>'] = <expr>.
Type <self>.action? for more details.


Typical usage to insert an action profile member:
m = action_profile_member['<action_profile_name>'](action='<action_name>',
member_id=1)
m.action['<p1>'] = ...
...
m.action['<pM>'] = ...
# OR m.action.set(p1=..., ..., pM=...)
m.insert

For information about how to read members, use <self>.read?
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["member_id", "action"]

    def _get_action_set(self):
        t_id = self._info.table_ids[0]
        t_name = CONTEXT.get_name_from_id(t_id)
        t = CONTEXT.get_table(t_name)
        return {action.id for action in t.action_refs}

    def __call__(self, **kwargs):
        for name, value in kwargs.items():
            if name == "action" and isinstance(value, str):
                value = Action(value)
            setattr(self, name, value)
        return self

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "name":
            raise UserError("Cannot change action profile name")
        if name == "member_id":
            if not isinstance(value, int):
                raise UserError("member_id must be an integer")
        if name == "action" and value is not None:
            if not isinstance(value, Action):
                raise UserError("action must be an instance of Action")
            if not self._is_valid_action_id(value._action_id):
                raise UserError(f"action '{value.action_name}' is not a valid "
                                f"action for this action profile")
        super().__setattr__(name, value)

    def _is_valid_action_id(self, action_id):
        return action_id in self._valid_action_ids

    def _update_msg(self):
        self._entry.action_profile_id = self.id
        self._entry.member_id = self.member_id
        if self.action is not None:
            self._entry.action.CopyFrom(self.action.msg())

    def _from_msg(self, msg):
        self.member_id = msg.member_id
        if msg.HasField('action'):
            action = msg.action
            action_name = CONTEXT.get_name_from_id(action.action_id)
            self.action = Action(action_name)
            self.action._from_msg(action)

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the appropriate fields unset).

        If function is None, returns an iterator. Iterate over it to get all the
        members (as ActionProfileMember instances) returned by the
        server. Otherwise, function is applied to all the members returned
        by the server.
        """
        return super().read(function)


class GroupMember:
    """
    P4 group member.

    A member in an ActionProfileGroup.
    Construct with GroupMember(<member_id>, weight=<weight>, watch=<watch>,
    watch_port=<watch_port>).
    You can set / get attributes member_id (required), weight (default 1),
    watch (default 0), watch_port (default "").
    """

    def __init__(self, member_id=None, weight=1, watch=0, watch_port=b""):
        if member_id is None:
            raise UserError("member_id is required")
        self._msg = p4runtime_pb2.ActionProfileGroup.Member()
        self._msg.member_id = member_id
        self._msg.weight = weight
        if watch:
            self._msg.watch = watch
        if watch_port:
            self._msg.watch_port = watch_port

    def __dir__(self):
        return ["member_id", "weight", "watch", "watch_port"]

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name == "member_id":
            if not isinstance(value, int):
                raise UserError("member_id must be an integer")
            self._msg.member_id = value
            return
        if name == "weight":
            if not isinstance(value, int):
                raise UserError("weight must be an integer")
            self._msg.weight = value
            return
        if name == "watch":
            if not isinstance(value, int):
                raise UserError("watch must be an integer")
            self._msg.watch = value
            return
        if name == "watch_port":
            if not isinstance(value, bytes):
                raise UserError("watch_port must be a byte string")
            self._msg.watch_port = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "member_id":
            return self._msg.member_id
        if name == "weight":
            return self._msg.weight
        if name == "watch":
            return self._msg.watch
        if name == "watch_port":
            return self._msg.watch_port
        return super().__getattr__(name)

    def __str__(self):
        return str(self._msg)


class ActionProfileGroup(_P4EntityBase):
    """
    P4 action profile group.
    """

    def __init__(self, p4_client, action_profile_name=None):
        super().__init__(p4_client,
            P4Type.action_profile, P4RuntimeEntity.action_profile_group,
            p4runtime_pb2.ActionProfileGroup, action_profile_name)
        self.group_id = 0
        self.max_size = 0
        self.members = []
        self.__doc__ = f"""
An action profile group for '{action_profile_name}'

Use <self>.info to display the P4Info entry for the action profile.

Set the group id with <self>.group_id = <expr>. Default is 0.
Set the max size with <self>.max_size = <expr>. Default is 0.

Add members to the group with <self>.add(<member_id>, weight=<weight>, watch=<watch>,
watch_port=<watch_port>).
weight, watch and watch port are optional (default to 1, 0 and "" respectively).

Typical usage to insert an action profile group:
g = action_profile_group['<action_profile_name>'](group_id=1)
g.add(<member id 1>)
g.add(<member id 2>)
# OR g.add(<member id 1>).add(<member id 2>)

For information about how to read groups, use <self>.read?
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["group_id", "max_size", "members", "add",
                                    "clear"]

    def __call__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "name":
            raise UserError("Cannot change action profile name")
        if name == "group_id":
            if not isinstance(value, int):
                raise UserError("group_id must be an integer")
        if name == "members":
            if not isinstance(value, list):
                raise UserError("members must be a list of GroupMember objects")
            for member in value:
                if not isinstance(member, GroupMember):
                    raise UserError(
                        "members must be a list of GroupMember objects")
        super().__setattr__(name, value)

    def add(self, member_id=None, weight=1, watch=0, watch_port=b""):
        """Add a member to the members list."""
        self.members.append(GroupMember(member_id, weight, watch, watch_port))
        return self

    def clear(self):
        """Empty members list."""
        self.members = []

    def _update_msg(self):
        self._entry.action_profile_id = self.id
        self._entry.group_id = self.group_id
        self._entry.max_size = self.max_size
        del self._entry.members[:]
        for member in self.members:
            if not isinstance(member, GroupMember):
                raise UserError("members must be a list of GroupMember objects")
            m = self._entry.members.add()
            m.CopyFrom(member._msg)

    def _from_msg(self, msg):
        self.group_id = msg.group_id
        self.max_size = msg.max_size
        self.members = []
        for member in msg.members:
            self.add(member.member_id, member.weight, member.watch,
                     member.watch_port)

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the appropriate fields unset).

        If function is None, returns an iterator. Iterate over it to get all the
        members (as ActionProfileGroup instances) returned by the
        server. Otherwise, function is applied to all the groups returned by the
        server.
        """
        return super().read(function)


def _get_action_profile(table_name):
    table = CONTEXT.get_table(table_name)
    implementation_id = table.implementation_id
    if implementation_id == 0:
        return None
    try:
        implementation_name = CONTEXT.get_name_from_id(implementation_id)
    except KeyError as ex:
        raise InvalidP4InfoError(
            f"Invalid implementation_id {implementation_id} for "
            f"table '{table_name}'") from ex
    ap = CONTEXT.get_obj(P4Type.action_profile, implementation_name)
    if ap is None:
        raise InvalidP4InfoError(
            f"Unknown implementation for table '{table_name}'")
    return ap


class OneshotAction:
    """
    A P4 action in a oneshot action set.
    Construct with OneshotAction(<action (Action instance)>,
    weight=<weight>, watch=<watch>, watch_port=<watch_port>).
    You can set / get attributes action (required), weight (default 1),
    watch (default 0), watch_port (default "").
    """

    def __init__(self, action=None, weight=1, watch=0, watch_port=b""):
        if action is None:
            raise UserError("action is required")
        self.action = action
        self.weight = weight
        self.watch = watch
        self.watch_port = watch_port

    def __dir__(self):
        return ["action", "weight", "watch", "watch_port", "msg"]

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name == "action":
            if not isinstance(value, Action):
                raise UserError("action must be an instance of Action")
        elif name == "weight":
            if not isinstance(value, int):
                raise UserError("weight must be an integer")
        elif name == "watch":
            if not isinstance(value, int):
                raise UserError("watch must be an integer")
        elif name == "watch_port":
            print(type(value), value)
            if not isinstance(value, bytes):
                raise UserError("watch_port must be a byte string")
        super().__setattr__(name, value)

    def msg(self):
        """
        Create an one shot action message.

        :return: one shot action message
        """
        msg = p4runtime_pb2.ActionProfileAction()
        msg.action.CopyFrom(self.action.msg())
        msg.weight = self.weight
        if self.watch:
            msg.watch = self.watch
        if self.watch_port:
            msg.watch_port = self.watch_port
        return msg

    def __str__(self):
        return str(self.msg())


class Oneshot:
    """
    One shot action set.
    """

    def __init__(self, table_name=None):
        self._init = False
        if table_name is None:
            raise UserError("Please provide table name")
        self.table_name = table_name
        self.actions = []
        self._table_info = P4Objects(P4Type.table)[table_name]
        ap = _get_action_profile(table_name)
        if not ap:
            raise UserError("Cannot create Oneshot instance for a direct table")
        if not ap.with_selector:
            raise UserError(
                "Cannot create Oneshot instance for a table "
                "with an action profile without selector")
        self.__doc__ = f"""
A "oneshot" action set for table '{self.table_name}'.

To add an action to the set, use <self>.add(<Action instance>).
You can also access the set of actions with <self>.actions (which is a Python list).
"""
        self._init = True

    def __dir__(self):
        return ["table_name", "actions", "add", "msg"]

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "table_name":
            raise UserError("Cannot change table name")
        if name == "actions":
            if not isinstance(value, list):
                raise UserError(
                    "actions must be a list of OneshotAction objects")
            for member in value:
                if not isinstance(member, OneshotAction):
                    raise UserError(
                        "actions must be a list of OneshotAction objects")
                if not self._is_valid_action_id(value.action._action_id):
                    raise UserError(
                        f"action '{value.action.action_name}' is not a valid "
                        f"action for table {self.table_name}")
        super().__setattr__(name, value)

    def _is_valid_action_id(self, action_id):
        for action_ref in self._table_info.action_refs:
            if action_id == action_ref.id:
                return True
        return False

    def add(self, action=None, weight=1, watch=0, watch_port=b""):
        """
        Add an action to the oneshot action set.

        :param action: action object
        :param weight: weight (integer)
        :param watch: watch (integer)
        :param watch_port: watch port
        :return:
        """
        self.actions.append(OneshotAction(action, weight, watch, watch_port))
        return self

    def msg(self):
        """
        Create an action profile message.

        :return: action profile message
        """
        msg = p4runtime_pb2.ActionProfileActionSet()
        msg.action_profile_actions.extend(
            [action.msg() for action in self.actions])
        return msg

    def _from_msg(self, msg):
        for action in msg.action_profile_actions:
            action_name = CONTEXT.get_name_from_id(action.action.action_id)
            a = Action(action_name)
            a._from_msg(action.action)
            self.actions.append(OneshotAction(a, action.weight, action.watch,
                                              action.watch_port))

    def __str__(self):
        return str(self.msg())


class _CounterData:
    """
    P4 counter data.
    """

    @staticmethod
    def attrs_for_counter_type(counter_type):
        """
        Return counter attributes.

        :param counter_type: P4 counter type
        :return: list of counter attributes
        """
        attrs = []
        if counter_type in {p4info_pb2.CounterSpec.BYTES,
                            p4info_pb2.CounterSpec.BOTH}:
            attrs.append("byte_count")
        if counter_type in {p4info_pb2.CounterSpec.PACKETS,
                            p4info_pb2.CounterSpec.BOTH}:
            attrs.append("packet_count")
        return attrs

    def __init__(self, counter_name, counter_type):
        self._counter_name = counter_name
        self._counter_type = counter_type
        self._msg = p4runtime_pb2.CounterData()
        self._attrs = _CounterData.attrs_for_counter_type(counter_type)

    def __dir__(self):
        return self._attrs

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name not in self._attrs:
            type_name = p4info_pb2._COUNTERSPEC_UNIT.values_by_number[
                self._counter_type].name
            raise UserError(
                f"Counter '{self._counter_name}' is of type '{type_name}', "
                f"you cannot set '{name}'")
        if not isinstance(value, int):
            raise UserError(f"{name} must be an integer")
        setattr(self._msg, name, value)

    def __getattr__(self, name):
        if name in ("byte_count", "packet_count"):
            return getattr(self._msg, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no "
                             f"attribute '{name}'")

    def msg(self):
        """
        Create a counter data message.

        :return: counter data message
        """
        return self._msg

    def _from_msg(self, msg):
        self._msg.CopyFrom(msg)

    def __str__(self):
        return str(self.msg())

    @classmethod
    def set_count(cls, instance, counter_name, counter_type, name, value):
        """
        Set the value of a certain counter.

        :param instance: counter instance
        :param counter_name: counter name
        :param counter_type: counter type
        :param name: counter attribute name
        :param value: counter attribute value
        :return: updated counter instance
        """
        if instance is None:
            d = cls(counter_name, counter_type)
        else:
            d = instance
        setattr(d, name, value)
        return d

    @classmethod
    def get_count(cls, instance, counter_name, counter_type, name):
        """
        Get the value of a certain counter.

        :param instance:
        :param counter_name: counter name
        :param counter_type: counter type
        :param name: counter attribute name
        :return: counter name and value
        """
        if instance is None:
            d = cls(counter_name, counter_type)
        else:
            d = instance
        r = getattr(d, name)
        return d, r


class _MeterConfig:
    """
    P4 meter configuration.
    """

    @staticmethod
    def attrs():
        """
        Get the attributes in this scope.

        :return: list of scope attributes
        """
        return ["cir", "cburst", "pir", "pburst"]

    def __init__(self, meter_name, meter_type):
        self._meter_name = meter_name
        self._meter_type = meter_type
        self._msg = p4runtime_pb2.MeterConfig()
        self._attrs = _MeterConfig.attrs()

    def __dir__(self):
        return self._attrs

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name in self._attrs:
            if not isinstance(value, int):
                raise UserError(f"{name} must be an integer")
        setattr(self._msg, name, value)

    def __getattr__(self, name):
        if name in self._attrs:
            return getattr(self._msg, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def msg(self):
        """
        Create a meter config message.

        :return: meter config message
        """
        return self._msg

    def _from_msg(self, msg):
        self._msg.CopyFrom(msg)

    def __str__(self):
        return str(self.msg())

    @classmethod
    def set_param(cls, instance, meter_name, meter_type, name, value):
        """
        Set the value of a certain meter parameter.

        :param instance: meter instance
        :param meter_name: meter name
        :param meter_type: meter type
        :param name: meter parameter name
        :param value: meter parameter value
        :return: updated meter
        """
        if instance is None:
            d = cls(meter_name, meter_type)
        else:
            d = instance
        setattr(d, name, value)
        return d

    @classmethod
    def get_param(cls, instance, meter_name, meter_type, name):
        """
        Get the value of a certain meter parameter.

        :param instance: meter instance
        :param meter_name: meter name
        :param meter_type: meter type
        :param name: meter parameter name
        :return: meter with parameter
        """
        if instance is None:
            d = cls(meter_name, meter_type)
        else:
            d = instance
        r = getattr(d, name)
        return d, r


class _IdleTimeout:
    """
    P4 idle timeout.
    """

    @staticmethod
    def attrs():
        """
        Get the attributes in this scope.

        :return: list of scope attributes
        """
        return ["elapsed_ns"]

    def __init__(self):
        self._msg = p4runtime_pb2.TableEntry.IdleTimeout()
        self._attrs = _IdleTimeout.attrs()

    def __dir__(self):
        return self._attrs

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name in self._attrs:
            if not isinstance(value, int):
                raise UserError(f"{name} must be an integer")
        setattr(self._msg, name, value)

    def __getattr__(self, name):
        if name in self._attrs:
            return getattr(self._msg, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def msg(self):
        """
        Create an idle timeout message.

        :return: idle timeout message
        """
        return self._msg

    def _from_msg(self, msg):
        self._msg.CopyFrom(msg)

    def __str__(self):
        return str(self.msg())

    @classmethod
    def set_param(cls, instance, name, value):
        """
        Set the value of a certain idle timeout parameter.

        :param instance: idle timeout instance
        :param name: idle timeout parameter name
        :param value: idle timeout parameter value
        :return: updated idle timeout instance
        """
        if instance is None:
            d = cls()
        else:
            d = instance
        setattr(d, name, value)
        return d

    @classmethod
    def get_param(cls, instance, name):
        """
        Set the value of a certain idle timeout parameter.

        :param instance: idle timeout instance
        :param name: idle timeout parameter name
        :return: idle timeout instance with parameter
        """
        if instance is None:
            d = cls()
        else:
            d = instance
        r = getattr(d, name)
        return d, r


class TableEntry(_P4EntityBase):
    """
    P4 table entry.
    """

    @enum.unique
    class _ActionSpecType(enum.Enum):
        NONE = 0
        DIRECT_ACTION = 1
        MEMBER_ID = 2
        GROUP_ID = 3
        ONESHOT = 4

    @classmethod
    def _action_spec_name_to_type(cls, name):
        return {
            "action": cls._ActionSpecType.DIRECT_ACTION,
            "member_id": cls._ActionSpecType.MEMBER_ID,
            "group_id": cls._ActionSpecType.GROUP_ID,
            "oneshot": cls._ActionSpecType.ONESHOT,
        }.get(name, None)

    def __init__(self, p4_client, table_name=None):
        super().__init__(p4_client,
            P4Type.table, P4RuntimeEntity.table_entry,
            p4runtime_pb2.TableEntry, table_name)
        self.match = MatchKey(table_name, self._info.match_fields)
        self._action_spec_type = self._ActionSpecType.NONE
        self._action_spec = None
        self.action: Action
        self.member_id = -1
        self.group_id = -1
        self.oneshot = None
        self.priority = 0
        self.is_default = False
        ap = _get_action_profile(table_name)
        if ap is None:
            self._support_members = False
            self._support_groups = False
        else:
            self._support_members = True
            self._support_groups = ap.with_selector
        self._direct_counter = None
        self._direct_meter = None
        for res_id in self._info.direct_resource_ids:
            prefix = (res_id & 0xff000000) >> 24
            if prefix == p4info_pb2.P4Ids.DIRECT_COUNTER:
                self._direct_counter = CONTEXT.get_obj_by_id(res_id)
            elif prefix == p4info_pb2.P4Ids.DIRECT_METER:
                self._direct_meter = CONTEXT.get_obj_by_id(res_id)
        self._counter_data = None
        self._meter_config = None
        self.idle_timeout_ns = 0
        self._time_since_last_hit = None
        self._idle_timeout_behavior = None
        table = CONTEXT.get_table(table_name)
        if table.idle_timeout_behavior > 0:
            self._idle_timeout_behavior = table.idle_timeout_behavior
        self.metadata = b""
        self.__doc__ = f"""
An entry for table '{table_name}'

Use <self>.info to display the P4Info entry for this table.

To set the match key, use <self>.match['<field name>'] = <expr>.
Type <self>.match? for more details.
"""
        if self._direct_counter is not None:
            self.__doc__ += """
To set the counter spec, use <self>.counter_data.byte_count and/or <self>.counter_data.packet_count.
To unset it, use <self>.counter_data = None or <self>.clear_counter_data().
"""
        if self._direct_meter is not None:
            self.__doc__ += """
To access the meter config, use <self>.meter_config.<cir|cburst|pir|pburst>.
To unset it, use <self>.meter_config = None or <self>.clear_meter_config().
"""
        if ap is None:
            self.__doc__ += """
To set the action specification (this is a direct table):
<self>.action = <instance of type Action>.
To set the value of action parameters, use <self>.action['<param name>'] = <expr>.
Type <self>.action? for more details.
"""
        if self._support_members:
            self.__doc__ += """
Access the member_id with <self>.member_id.
"""
        if self._support_groups:
            self.__doc__ += """
Or access the group_id with <self>.group_id.
"""
        if self._idle_timeout_behavior is not None:
            self.__doc__ += """
To access the time this entry was last hit, use <self>.time_since_last_hit.elapsed_ns.
To unset it, use <self>.time_since_last_hit = None or <self>.clear_time_since_last_hit().
"""
        self.__doc__ += """
To set the priority, use <self>.priority = <expr>.

To mark the entry as default, use <self>.is_default = True.

To add an idle timeout to the entry, use <self>.idle_timeout_ns = <expr>.

To add metadata to the entry, use <self>.metadata = <expr>.
"""
        if ap is None:
            self.__doc__ += """
Typical usage to insert a table entry:
t = table_entry['<table_name>'](action='<action_name>')
t.match['<f1>'] = ...
...
t.match['<fN>'] = ...
# OR t.match.set(f1=..., ..., fN=...)
t.action['<p1>'] = ...
...
t.action['<pM>'] = ...
# OR t.action.set(p1=..., ..., pM=...)
t.insert

Typical usage to set the default entry:
t = table_entry['<table_name>'](is_default=True)
t.action['<p1>'] = ...
...
t.action['<pM>'] = ...
# OR t.action.set(p1=..., ..., pM=...)
t.modify
"""
        else:
            self.__doc__ += """
Typical usage to insert a table entry:
t = table_entry['<table_name>']
t.match['<f1>'] = ...
...
t.match['<fN>'] = ...
# OR t.match.set(f1=..., ..., fN=...)
t.member_id = <expr>
"""
        self.__doc__ += """
For information about how to read table entries, use <self>.read?
"""

        self._init = True

    def __dir__(self):
        d = super().__dir__() + [
            "match", "priority", "is_default", "idle_timeout_ns", "metadata",
            "clear_action", "clear_match", "clear_counter_data",
            "clear_meter_config",
            "clear_time_since_last_hit"]
        if self._support_groups:
            d.extend(["member_id", "group_id", "oneshot"])
        elif self._support_members:
            d.append("member_id")
        else:
            d.append("action")
        if self._direct_counter is not None:
            d.append("counter_data")
        if self._direct_meter is not None:
            d.append("meter_config")
        if self._idle_timeout_behavior is not None:
            d.append("time_since_last_hit")
        return d

    def __call__(self, **kwargs):
        for name, value in kwargs.items():
            if name == "action" and isinstance(value, str):
                value = Action(value)
            setattr(self, name, value)
        return self

    def _action_spec_set_member(self, member_id):
        if isinstance(member_id, type(None)):
            if self._action_spec_type == self._ActionSpecType.MEMBER_ID:
                super().__setattr__("_action_spec_type",
                                    self._ActionSpecType.NONE)
                super().__setattr__("_action_spec", None)
            return
        if not isinstance(member_id, int):
            raise UserError("member_id must be an integer")
        if not self._support_members:
            raise UserError("Table does not have an action profile and "
                            "therefore does not support members")
        super().__setattr__("_action_spec_type", self._ActionSpecType.MEMBER_ID)
        super().__setattr__("_action_spec", member_id)

    def _action_spec_set_group(self, group_id):
        if isinstance(group_id, type(None)):
            if self._action_spec_type == self._ActionSpecType.GROUP_ID:
                super().__setattr__("_action_spec_type",
                                    self._ActionSpecType.NONE)
                super().__setattr__("_action_spec", None)
            return
        if not isinstance(group_id, int):
            raise UserError("group_id must be an integer")
        if not self._support_groups:
            raise UserError(
                "Table does not have an action profile with selector "
                "and therefore does not support groups")
        super().__setattr__("_action_spec_type", self._ActionSpecType.GROUP_ID)
        super().__setattr__("_action_spec", group_id)

    def _action_spec_set_action(self, action):
        if isinstance(action, type(None)):
            if self._action_spec_type == self._ActionSpecType.DIRECT_ACTION:
                super().__setattr__("_action_spec_type",
                                    self._ActionSpecType.NONE)
                super().__setattr__("_action_spec", None)
            return
        if not isinstance(action, Action):
            raise UserError("action must be an instance of Action")
        if self._info.implementation_id != 0:
            raise UserError(
                "Table has an implementation and therefore "
                "does not support direct actions (P4Runtime 1.0 doesn't "
                "support writing the default action for indirect tables")
        if not self._is_valid_action_id(action._action_id):
            raise UserError(f"action '{action.action_name}' is not a valid "
                            f"action for this table")
        super().__setattr__("_action_spec_type",
                            self._ActionSpecType.DIRECT_ACTION)
        super().__setattr__("_action_spec", action)

    def _action_spec_set_oneshot(self, oneshot):
        if isinstance(oneshot, type(None)):
            if self._action_spec_type == self._ActionSpecType.ONESHOT:
                super().__setattr__("_action_spec_type",
                                    self._ActionSpecType.NONE)
                super().__setattr__("_action_spec", None)
            return
        if not isinstance(oneshot, Oneshot):
            raise UserError("oneshot must be an instance of Oneshot")
        if not self._support_groups:
            raise UserError(
                "Table does not have an action profile with selector "
                "and therefore does not support oneshot programming")
        if self.name != oneshot.table_name:
            raise UserError(
                "This Oneshot instance was not created for this table")
        super().__setattr__("_action_spec_type", self._ActionSpecType.ONESHOT)
        super().__setattr__("_action_spec", oneshot)

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "name":
            raise UserError("Cannot change table name")
        if name == "priority":
            if not isinstance(value, int):
                raise UserError("priority must be an integer")
        if name == "match" and not isinstance(value, MatchKey):
            raise UserError("match must be an instance of MatchKey")
        if name == "is_default":
            if not isinstance(value, bool):
                raise UserError("is_default must be a boolean")
            # TODO: handle other cases  # pylint: disable=W0511
            # is_default is set to True)?
            if value is True and self.match._count() > 0:
                print("Clearing match key because entry is now default")
                self.match.clear()
        if name == "member_id":
            self._action_spec_set_member(value)
            return
        if name == "group_id":
            self._action_spec_set_group(value)
            return
        if name == "oneshot":
            self._action_spec_set_oneshot(value)
        if name == "action" and value is not None:
            self._action_spec_set_action(value)
            return
        if name == "counter_data":
            if self._direct_counter is None:
                raise UserError("Table has no direct counter")
            if value is None:
                self._counter_data = None
                return
            raise UserError("Cannot set 'counter_data' directly")
        if name == "meter_config":
            if self._direct_meter is None:
                raise UserError("Table has no direct meter")
            if value is None:
                self._meter_config = None
                return
            raise UserError("Cannot set 'meter_config' directly")
        if name == "idle_timeout_ns":
            if not isinstance(value, int):
                raise UserError("idle_timeout_ns must be an integer")
        if name == "time_since_last_hit":
            if self._idle_timeout_behavior is None:
                raise UserError("Table has no idle timeouts")
            if value is None:
                self._time_since_last_hit = None
                return
            raise UserError("Cannot set 'time_since_last_hit' directly")
        if name == "metadata":
            if not isinstance(value, bytes):
                raise UserError("metadata must be a byte string")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "counter_data":
            if self._direct_counter is None:
                raise UserError("Table has no direct counter")
            if self._counter_data is None:
                self._counter_data = _CounterData(
                    self._direct_counter.preamble.name,
                    self._direct_counter.spec.unit)
            return self._counter_data
        if name == "meter_config":
            if self._direct_meter is None:
                raise UserError("Table has no direct meter")
            if self._meter_config is None:
                self._meter_config = _MeterConfig(
                    self._direct_meter.preamble.name,
                    self._direct_meter.spec.unit)
            return self._meter_config
        if name == "time_since_last_hit":
            if self._idle_timeout_behavior is None:
                raise UserError("Table has no idle timeouts")
            if self._time_since_last_hit is None:
                self._time_since_last_hit = _IdleTimeout()
            return self._time_since_last_hit

        t = self._action_spec_name_to_type(name)
        if t is None:
            return super().__getattr__(name)
        if self._action_spec_type == t:
            return self._action_spec
        if t == self._ActionSpecType.ONESHOT:
            self._action_spec_type = self._ActionSpecType.ONESHOT
            self._action_spec = Oneshot(self.name)
            return self._action_spec
        return None

    def _is_valid_action_id(self, action_id):
        for action_ref in self._info.action_refs:
            if action_id == action_ref.id:
                return True
        return False

    def _from_msg(self, msg):
        self.priority = msg.priority
        self.is_default = msg.is_default_action
        self.idle_timeout_ns = msg.idle_timeout_ns
        self.metadata = msg.metadata
        for mf in msg.match:
            mf_name = CONTEXT.get_mf_name(self.name, mf.field_id)
            self.match._mk[mf_name] = mf
        if msg.action.HasField('action'):
            action = msg.action.action
            action_name = CONTEXT.get_name_from_id(action.action_id)
            self.action = Action(action_name)
            self.action._from_msg(action)
        elif msg.action.HasField('action_profile_member_id'):
            self.member_id = msg.action.action_profile_member_id
        elif msg.action.HasField('action_profile_group_id'):
            self.group_id = msg.action.action_profile_group_id
        elif msg.action.HasField('action_profile_action_set'):
            self.oneshot = Oneshot(self.name)
            self.oneshot._from_msg(msg.action.action_profile_action_set)
        if msg.HasField('counter_data'):
            self._counter_data = _CounterData(
                self._direct_counter.preamble.name,
                self._direct_counter.spec.unit)
            self._counter_data._from_msg(msg.counter_data)
        else:
            self._counter_data = None
        if msg.HasField('meter_config'):
            self._meter_config = _MeterConfig(
                self._direct_meter.preamble.name, self._direct_meter.spec.unit)
            self._meter_config._from_msg(msg.meter_config)
        else:
            self._meter_config = None
        if msg.HasField("time_since_last_hit"):
            self._time_since_last_hit = _IdleTimeout()
            self._time_since_last_hit._from_msg(msg.time_since_last_hit)
        else:
            self._time_since_last_hit = None

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the appropriate fields unset).
        If function is None, returns an iterator. Iterate over it to get all the
        table entries (TableEntry instances) returned by the server. Otherwise,
        function is applied to all the table entries returned by the server.

        For example:
        for te in <self>.read():
            print(te)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda te: print(te))

        To delete all the entries from a table, simply use:
        table_entry['<table_name>'].read(function=lambda x: x.delete())
        """
        return super().read(function)

    def _update_msg(self):
        entry = p4runtime_pb2.TableEntry()
        entry.table_id = self.id
        entry.match.extend(self.match._mk.values())
        entry.priority = self.priority
        entry.is_default_action = self.is_default
        entry.idle_timeout_ns = self.idle_timeout_ns
        entry.metadata = self.metadata
        if self._action_spec_type == self._ActionSpecType.DIRECT_ACTION:
            entry.action.action.CopyFrom(self._action_spec.msg())
        elif self._action_spec_type == self._ActionSpecType.MEMBER_ID:
            entry.action.action_profile_member_id = self._action_spec
        elif self._action_spec_type == self._ActionSpecType.GROUP_ID:
            entry.action.action_profile_group_id = self._action_spec
        elif self._action_spec_type == self._ActionSpecType.ONESHOT:
            entry.action.action_profile_action_set.CopyFrom(
                self._action_spec.msg())
        if self._counter_data is None:
            entry.ClearField('counter_data')
        else:
            entry.counter_data.CopyFrom(self._counter_data.msg())
        if self._meter_config is None:
            entry.ClearField('meter_config')
        else:
            entry.meter_config.CopyFrom(self._meter_config.msg())
        if self._time_since_last_hit is None:
            entry.ClearField("time_since_last_hit")
        else:
            entry.time_since_last_hit.CopyFrom(self._time_since_last_hit.msg())
        self._entry = entry

    def _validate_msg(self):
        if self.is_default and self.match._count() > 0:
            raise UserError("Match key must be empty for default entry, "
                            "use <self>.is_default = False "
                            "or <self>.match.clear "
                            "(whichever one is appropriate)")

    def clear_action(self):
        """Clears the action spec for the TableEntry."""
        super().__setattr__("_action_spec_type", self._ActionSpecType.NONE)
        super().__setattr__("_action_spec", None)

    def clear_match(self):
        """Clears the match spec for the TableEntry."""
        self.match.clear()

    def clear_counter_data(self):
        """Clear all counter data, same as <self>.counter_data = None"""
        self._counter_data = None

    def clear_meter_config(self):
        """Clear the meter config, same as <self>.meter_config = None"""
        self._meter_config = None

    def clear_time_since_last_hit(self):
        """Clear the idle timeout, same as <self>.time_since_last_hit = None"""
        self._time_since_last_hit = None


class _CounterEntryBase(_P4EntityBase):
    """
    Basic P4 counter entry.
    """

    def __init__(self, p4_client, *args, **kwargs):
        super().__init__(p4_client, *args, **kwargs)
        self._counter_type = self._info.spec.unit
        self.packet_count = -1
        self.byte_count = -1
        self._data = None

    def __dir__(self):
        return super().__dir__() + _CounterData.attrs_for_counter_type(
            self._counter_type) + [
                   "clear_data"]

    def __call__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "name":
            raise UserError("Cannot change counter name")
        if name in ("byte_count", "packet_count"):
            self._data = _CounterData.set_count(
                self._data, self.name, self._counter_type, name, value)
            return
        if name == "data":
            if value is None:
                self._data = None
                return
            raise UserError("Cannot set 'data' directly")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in ("byte_count", "packet_count"):
            self._data, r = _CounterData.get_count(
                self._data, self.name, self._counter_type, name)
            return r
        if name == "data":
            if self._data is None:
                self._data = _CounterData(self.name, self._counter_type)
            return self._data
        return super().__getattr__(name)

    def _from_msg(self, msg):
        self._entry.CopyFrom(msg)
        if msg.HasField('data'):
            self._data = _CounterData(self.name, self._counter_type)
            self._data._from_msg(msg.data)
        else:
            self._data = None

    def _update_msg(self):
        if self._data is None:
            self._entry.ClearField('data')
        else:
            self._entry.data.CopyFrom(self._data.msg())

    def clear_data(self):
        """Clear all counter data, same as <self>.data = None"""
        self._data = None


class CounterEntry(_CounterEntryBase):
    """
    P4 counter entry.
    """

    def __init__(self, p4_client, counter_name=None):
        super().__init__(p4_client,
            P4Type.counter, P4RuntimeEntity.counter_entry,
            p4runtime_pb2.CounterEntry, counter_name,
            modify_only=True)
        self._entry.counter_id = self.id
        self.index = -1
        self.__doc__ = f"""
An entry for counter '{counter_name}'

Use <self>.info to display the P4Info entry for this counter.

Set the index with <self>.index = <expr>.
To reset it (e.g. for wildcard read), set it to None.

Access byte count and packet count with <self>.byte_count / <self>.packet_count.

To read from the counter, use <self>.read
To write to the counter, use <self>.modify
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["index", "data"]

    def __setattr__(self, name, value):
        if name == "index":
            if value is None:
                self._entry.ClearField('index')
                return
            if not isinstance(value, int):
                raise UserError("index must be an integer")
            self._entry.index.index = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "index":
            return self._entry.index.index
        return super().__getattr__(name)

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the index unset).
        If function is None, returns an iterator. Iterate over it to get all the
        counter entries (CounterEntry instances) returned by the
        server. Otherwise, function is applied to all the counter entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)


class DirectCounterEntry(_CounterEntryBase):
    """
    Direct P4 counter entry.
    """
    local_client = None

    def __init__(self, p4_client, direct_counter_name=None):
        super().__init__(p4_client,
            P4Type.direct_counter, P4RuntimeEntity.direct_counter_entry,
            p4runtime_pb2.DirectCounterEntry, direct_counter_name,
            modify_only=True)
        self._direct_table_id = self._info.direct_table_id
        try:
            self._direct_table_name = CONTEXT.get_name_from_id(
                self._direct_table_id)
        except KeyError as ex:
            raise InvalidP4InfoError(f"direct_table_id {self._direct_table_id} "
                                     f"is not a valid table id") from ex
        self._table_entry = TableEntry(p4_client, self._direct_table_name)
        self.local_client = p4_client
        self.__doc__ = f"""
An entry for direct counter '{direct_counter_name}'

Use <self>.info to display the P4Info entry for this direct counter.

Set the table_entry with <self>.table_entry = <TableEntry instance>.
The TableEntry instance must be for the table to which the direct counter is
attached.
To reset it (e.g. for wildcard read), set it to None. It is the same as:
<self>.table_entry = TableEntry({self._direct_table_name})

Access byte count and packet count with <self>.byte_count / <self>.packet_count.

To read from the counter, use <self>.read
To write to the counter, use <self>.modify
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["table_entry"]

    def __setattr__(self, name, value):
        if name == "index":
            raise UserError("Direct counters are not index-based")
        if name == "table_entry":
            if value is None:
                self._table_entry = TableEntry(self.local_client, self._direct_table_name)
                return
            if not isinstance(value, TableEntry):
                raise UserError("table_entry must be an instance of TableEntry")
            if value.name != self._direct_table_name:
                raise UserError(f"This DirectCounterEntry is for "
                                f"table '{self._direct_table_name}'")
            self._table_entry = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "index":
            raise UserError("Direct counters are not index-based")
        if name == "table_entry":
            return self._table_entry
        return super().__getattr__(name)

    def _update_msg(self):
        super()._update_msg()
        if self._table_entry is None:
            self._entry.ClearField('table_entry')
        else:
            self._entry.table_entry.CopyFrom(self._table_entry.msg())

    def _from_msg(self, msg):
        super()._from_msg(msg)
        if msg.HasField('table_entry'):
            self._table_entry._from_msg(msg.table_entry)
        else:
            self._table_entry = None

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the index unset).
        If function is None, returns an iterator. Iterate over it to get all the
        direct counter entries (DirectCounterEntry instances) returned by the
        server. Otherwise, function is applied to all the direct counter entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)


class _MeterEntryBase(_P4EntityBase):
    """
    Basic P4 meter entry.
    """

    def __init__(self, p4_client, *args, **kwargs):
        super().__init__(p4_client, *args, **kwargs)
        self._meter_type = self._info.spec.unit
        self.index = -1
        self.cir = -1
        self.cburst = -1
        self.pir = -1
        self.pburst = -1
        self._config = None

    def __dir__(self):
        return super().__dir__() + _MeterConfig.attrs() + ["clear_config"]

    def __call__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self

    def __setattr__(self, name, value):
        if name[0] == "_" or not self._init:
            super().__setattr__(name, value)
            return
        if name == "name":
            raise UserError("Cannot change meter name")
        if name in _MeterConfig.attrs():
            self._config = _MeterConfig.set_param(
                self._config, self.name, self._meter_type, name, value)
            return
        if name == "config":
            if value is None:
                self._config = None
                return
            raise UserError("Cannot set 'config' directly")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in _MeterConfig.attrs():
            self._config, r = _MeterConfig.get_param(
                self._config, self.name, self._meter_type, name)
            return r
        if name == "config":
            if self._config is None:
                self._config = _MeterConfig(self.name, self._meter_type)
            return self._config
        return super().__getattr__(name)

    def _from_msg(self, msg):
        self._entry.CopyFrom(msg)
        if msg.HasField('config'):
            self._config = _MeterConfig(self.name, self._meter_type)
            self._config._from_msg(msg.config)
        else:
            self._config = None

    def _update_msg(self):
        if self._config is None:
            self._entry.ClearField('config')
        else:
            self._entry.config.CopyFrom(self._config.msg())

    def clear_config(self):
        """Clear the meter config, same as <self>.config = None"""
        self._config = None


class MeterEntry(_MeterEntryBase):
    """
    P4 meter entry.
    """

    def __init__(self, p4_client, meter_name=None):
        super().__init__(p4_client,
            P4Type.meter, P4RuntimeEntity.meter_entry,
            p4runtime_pb2.MeterEntry, meter_name,
            modify_only=True)
        self._entry.meter_id = self.id
        self.__doc__ = f"""
An entry for meter '{meter_name}'

Use <self>.info to display the P4Info entry for this meter.

Set the index with <self>.index = <expr>.
To reset it (e.g. for wildcard read), set it to None.

Access meter rates and burst sizes with:
<self>.cir
<self>.cburst
<self>.pir
<self>.pburst

To read from the meter, use <self>.read
To write to the meter, use <self>.modify
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["index", "config"]

    def __setattr__(self, name, value):
        if name == "index":
            if value is None:
                self._entry.ClearField('index')
                return
            if not isinstance(value, int):
                raise UserError("index must be an integer")
            self._entry.index.index = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "index":
            return self._entry.index.index
        return super().__getattr__(name)

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the index unset).
        If function is None, returns an iterator. Iterate over it to get all the
        meter entries (MeterEntry instances) returned by the
        server. Otherwise, function is applied to all the meter entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)


class DirectMeterEntry(_MeterEntryBase):
    """
    Direct P4 meter entry.
    """
    local_client = None

    def __init__(self, p4_client, direct_meter_name=None):
        super().__init__(p4_client,
            P4Type.direct_meter, P4RuntimeEntity.direct_meter_entry,
            p4runtime_pb2.DirectMeterEntry, direct_meter_name,
            modify_only=True)
        self._direct_table_id = self._info.direct_table_id
        try:
            self._direct_table_name = CONTEXT.get_name_from_id(
                self._direct_table_id)
        except KeyError as ex:
            raise InvalidP4InfoError(f"direct_table_id {self._direct_table_id} "
                                     f"is not a valid table id") from ex
        self._table_entry = TableEntry(p4_client, self._direct_table_name)
        self.local_client = p4_client
        self.__doc__ = f"""
An entry for direct meter '{direct_meter_name}'

Use <self>.info to display the P4Info entry for this direct meter.

Set the table_entry with <self>.table_entry = <TableEntry instance>.
The TableEntry instance must be for the table to which the direct meter is attached.
To reset it (e.g. for wildcard read), set it to None. It is the same as:
<self>.table_entry = TableEntry({self._direct_table_name})

Access meter rates and burst sizes with:
<self>.cir
<self>.cburst
<self>.pir
<self>.pburst

To read from the meter, use <self>.read
To write to the meter, use <self>.modify
"""
        self._init = True

    def __dir__(self):
        return super().__dir__() + ["table_entry"]

    def __setattr__(self, name, value):
        if name == "index":
            raise UserError("Direct meters are not index-based")
        if name == "table_entry":
            if value is None:
                self._table_entry = TableEntry(self.local_client, self._direct_table_name)
                return
            if not isinstance(value, TableEntry):
                raise UserError("table_entry must be an instance of TableEntry")
            if value.name != self._direct_table_name:
                raise UserError(f"This DirectMeterEntry is for "
                                f"table '{self._direct_table_name}'")
            self._table_entry = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "index":
            raise UserError("Direct meters are not index-based")
        if name == "table_entry":
            return self._table_entry
        return super().__getattr__(name)

    def _update_msg(self):
        super()._update_msg()
        if self._table_entry is None:
            self._entry.ClearField('table_entry')
        else:
            self._entry.table_entry.CopyFrom(self._table_entry.msg())

    def _from_msg(self, msg):
        super()._from_msg(msg)
        if msg.HasField('table_entry'):
            self._table_entry._from_msg(msg.table_entry)
        else:
            self._table_entry = None

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the index unset).
        If function is None, returns an iterator. Iterate over it to get all the
        direct meter entries (DirectMeterEntry instances) returned by the
        server. Otherwise, function is applied to all the direct meter entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)


class P4RuntimeEntityBuilder:
    """
    P4 entity builder.
    """

    def __init__(self, obj_type, entity_type, entity_cls):
        self._obj_type = obj_type
        self._names = sorted([name for name, _ in CONTEXT.get_objs(obj_type)])
        self._entity_type = entity_type
        self._entity_cls = entity_cls
        self.__doc__ = f"""Construct a {entity_cls.__name__} entity
Usage: <var> = {entity_type.name}["<{obj_type.pretty_name} name>"]
This is equivalent to <var>={entity_cls.__name__}(<{obj_type.pretty_name} name>)
Use command '{obj_type.p4info_name}' to see list of {obj_type.pretty_names}
"""

    def _ipython_key_completions_(self):
        return self._names

    def __getitem__(self, name):
        obj = CONTEXT.get_obj(self._obj_type, name)
        if obj is None:
            raise UserError(
                f"{self._obj_type.pretty_name} '{name}' does not exist")
        return self._entity_cls(name)

    def __setitem__(self, name, value):
        raise UserError("Operation not allowed")

    def __str__(self):
        return f"Construct a {self.entity_cls.__name__} entity"


class Replica:
    """
    A port "replica" (port number + instance id) used for multicast
    and clone session programming.
    Construct with Replica(egress_port, instance=<instance>).
    You can set / get attributes egress_port (required), instance (default 0).
    """

    def __init__(self, egress_port=None, instance=0):
        if egress_port is None:
            raise UserError("egress_port is required")
        self._msg = p4runtime_pb2.Replica()
        self._msg.egress_port = egress_port
        self._msg.instance = instance

    def __dir__(self):
        return ["port", "egress_port", "instance"]

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name in ("egress_port", "port"):
            if not isinstance(value, int):
                raise UserError("egress_port must be an integer")
            self._msg.egress_port = value
            return
        if name == "instance":
            if not isinstance(value, int):
                raise UserError("instance must be an integer")
            self._msg.instance = value
            return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in ("egress_port", "port"):
            return self._msg.egress_port
        if name == "instance":
            return self._msg.instance
        return super().__getattr__(name)

    def __str__(self):
        return str(self._msg)


class MulticastGroupEntry(_EntityBase):
    """
    P4 multicast group entry.
    """

    def __init__(self, p4_client, group_id=0):
        super().__init__(p4_client,
            P4RuntimeEntity.packet_replication_engine_entry,
            p4runtime_pb2.PacketReplicationEngineEntry)
        self.group_id = group_id
        self.replicas = []
        self.__doc__ = """
Multicast group entry.
Create an instance with multicast_group_entry(<group_id>).
Add replicas with <self>.add(<eg_port_1>, <instance_1>).add(<eg_port_2>, <instance_2>)...
"""
        self._init = True

    def __dir__(self):
        return ["group_id", "replicas"]

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name == "group_id":
            if not isinstance(value, int):
                raise UserError("group_id must be an integer")
        if name == "replicas":
            if not isinstance(value, list):
                raise UserError("replicas must be a list of Replica objects")
            for r in value:
                if not isinstance(r, Replica):
                    raise UserError(
                        "replicas must be a list of Replica objects")
        super().__setattr__(name, value)

    def _from_msg(self, msg):
        self.group_id = msg.multicast_group_entry.multicast_group_id
        for r in msg.multicast_group_entry.replicas:
            self.add(r.egress_port, r.instance)

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the group_id as 0).
        If function is None, returns an iterator. Iterate over it to get all the
        multicast group entries (MulticastGroupEntry instances) returned by the
        server. Otherwise, function is applied to all the multicast group entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)

    def _update_msg(self):
        entry = p4runtime_pb2.PacketReplicationEngineEntry()
        mcg_entry = entry.multicast_group_entry
        mcg_entry.multicast_group_id = self.group_id
        for replica in self.replicas:
            r = mcg_entry.replicas.add()
            r.CopyFrom(replica._msg)
        self._entry = entry

    def add(self, egress_port=None, instance=0):
        """Add a replica to the multicast group."""
        self.replicas.append(Replica(egress_port, instance))
        return self

    def _write(self, type_):
        if self.group_id == 0:
            raise UserError("0 is not a valid group_id for MulticastGroupEntry")
        super()._write(type_)


class CloneSessionEntry(_EntityBase):
    """
    P4 clone session entry.
    """

    def __init__(self, p4_client, session_id=0):
        super().__init__(p4_client,
            P4RuntimeEntity.packet_replication_engine_entry,
            p4runtime_pb2.PacketReplicationEngineEntry)
        self.session_id = session_id
        self.replicas = []
        self.cos = 0
        self.packet_length_bytes = 0
        self.__doc__ = """
Clone session entry.
Create an instance with clone_session_entry(<session_id>).
Add replicas with <self>.add(<eg_port_1>, <instance_1>).add(<eg_port_2>,
<instance_2>)...
Access class of service with <self>.cos.
Access truncation length with <self>.packet_length_bytes.
"""
        self._init = True

    def __dir__(self):
        return ["session_id", "replicas", "cos", "packet_length_bytes"]

    def __setattr__(self, name, value):
        if name[0] == "_":
            super().__setattr__(name, value)
            return
        if name == "session_id":
            if not isinstance(value, int):
                raise UserError("session_id must be an integer")
        if name == "replicas":
            if not isinstance(value, list):
                raise UserError("replicas must be a list of Replica objects")
            for r in value:
                if not isinstance(r, Replica):
                    raise UserError(
                        "replicas must be a list of Replica objects")
        if name == "cos":
            if not isinstance(value, int):
                raise UserError("cos must be an integer")
        if name == "packet_length_bytes":
            if not isinstance(value, int):
                raise UserError("packet_length_bytes must be an integer")
        super().__setattr__(name, value)

    def _from_msg(self, msg):
        self.session_id = msg.clone_session_entry.session_id
        for r in msg.clone_session_entry.replicas:
            self.add(r.egress_port, r.instance)
        self.cos = msg.clone_session_entry.class_of_service
        self.packet_length_bytes = msg.clone_session_entry.packet_length_bytes

    def read(self, function=None):
        """Generate a P4Runtime Read RPC. Supports wildcard reads (just leave
        the session_id as 0).
        If function is None, returns an iterator. Iterate over it to get all the
        clone session entries (CloneSessionEntry instances) returned by the
        server. Otherwise, function is applied to all the clone session entries
        returned by the server.

        For example:
        for c in <self>.read():
            print(c)
        The above code is equivalent to the following one-liner:
        <self>.read(lambda c: print(c))
        """
        return super().read(function)

    def _update_msg(self):
        entry = p4runtime_pb2.PacketReplicationEngineEntry()
        cs_entry = entry.clone_session_entry
        cs_entry.session_id = self.session_id
        for replica in self.replicas:
            r = cs_entry.replicas.add()
            r.CopyFrom(replica._msg)
        cs_entry.class_of_service = self.cos
        cs_entry.packet_length_bytes = self.packet_length_bytes
        self._entry = entry

    def add(self, egress_port=None, instance=0):
        """Add a replica to the clone session."""
        self.replicas.append(Replica(egress_port, instance))
        return self

    def _write(self, type_):
        if self.session_id == 0:
            raise UserError("0 is not a valid group_id for CloneSessionEntry")
        super()._write(type_)


class PacketMetadata:
    """
    P4 packet metadata.
    """

    def __init__(self, metadata_info_list):
        self._md_info = OrderedDict()
        self._md = OrderedDict()
        # Initialize every metadata to zero value
        for md in metadata_info_list:
            self._md_info[md.name] = md
            self._md[md.name] = self._parse_md('0', md)
        self._set_docstring()

    def _set_docstring(self):
        self.__doc__ = "Available metadata:\n\n"
        for _, info in self._md_info.items():
            self.__doc__ += str(info)
        self.__doc__ += """
Set a metadata value with <self>.['<metadata_name>'] = '...'

You may also use <self>.set(<md_name>='<value>')
"""

    def __dir__(self):
        return ["clear"]

    def _get_md_info(self, name):
        if name in self._md_info:
            return self._md_info[name]
        raise UserError(f"'{name}' is not a valid metadata name")

    def __getitem__(self, name):
        _ = self._get_md_info(name)
        print(self._md.get(name, "Unset"))

    def _parse_md(self, value, md_info):
        if not isinstance(value, str):
            raise UserError("Metadata value must be a string")
        md = p4runtime_pb2.PacketMetadata()
        md.metadata_id = md_info.id
        md.value = encode(value.strip(), md_info.bitwidth)
        return md

    def __setitem__(self, name, value):
        md_info = self._get_md_info(name)
        self._md[name] = self._parse_md(value, md_info)

    def _ipython_key_completions_(self):
        return self._md_info.keys()

    def set(self, **kwargs):
        """
        Set packet metadata parameters.

        :param kwargs: packet metadata parameter map
        :return: void
        """
        for name, value in kwargs.items():
            self[name] = value

    def clear(self):
        """
        Clear packet metadata.

        :return: void
        """
        self._md.clear()

    def values(self):
        """
        Get packet metadata values.

        :return: list of packet metadata values
        """
        return self._md.values()


class PacketIn():
    """
    P4 packet in.
    """
    local_client = None

    def __init__(self, p4_client):
        ctrl_pkt_md = P4Objects(P4Type.controller_packet_metadata)
        self.md_info_list = {}
        if "packet_in" in ctrl_pkt_md:
            self.p4_info = ctrl_pkt_md["packet_in"]
            for md_info in self.p4_info.metadata:
                self.md_info_list[md_info.name] = md_info
        self.packet_in_queue = queue.Queue()
        self.local_client = p4_client

        def _packet_in_recv_func(packet_in_queue):
            while True:
                msg = self.local_client.get_stream_packet("packet", timeout=None)
                if not msg:
                    break
                packet_in_queue.put(msg)

        self.recv_t = Thread(target=_packet_in_recv_func,
                             args=(self.packet_in_queue,))
        self.recv_t.start()

    def sniff(self, function=None, timeout=None):
        """
        Return an iterator of packet-in messages.
        If the function is provided, we do not return an iterator;
        instead we apply the function to every packet-in message.

        :param function: packet-in function
        :param timeout: timeout in seconds
        :return: list of packet-in messages
        """
        msgs = []

        if timeout is not None and timeout < 0:
            raise ValueError("Timeout can't be a negative number.")

        if timeout is None:
            while True:
                try:
                    msgs.append(self.packet_in_queue.get(block=True))
                except KeyboardInterrupt:
                    # User sends a Ctrl+C -> breaking
                    break

        else:  # timeout parameter is provided
            deadline = time.time() + timeout
            remaining_time = timeout
            while remaining_time > 0:
                try:
                    msgs.append(self.packet_in_queue.get(block=True,
                                                         timeout=remaining_time))
                    remaining_time = deadline - time.time()
                except KeyboardInterrupt:
                    # User sends an interrupt(e.g., Ctrl+C).
                    break
                except queue.Empty:
                    # No item available on timeout. Exiting
                    break

        if function is None:
            return iter(msgs)
        for msg in msgs:
            function(msg)

    def str(self):
        """
        Packet-in metadata to string.

        :return: void
        """
        for name, info in self.md_info_list.itmes():
            print(f"Packet-in metadata attribute '{name}':'{info}'")


class PacketOut:
    """
    P4 packet out.
    """
    local_client = None

    def __init__(self, p4_client, payload=b'', **kwargs):

        self.p4_info = P4Objects(P4Type.controller_packet_metadata)[
            "packet_out"]
        self._entry = None
        self.payload = payload
        self.metadata = PacketMetadata(self.p4_info.metadata)
        if kwargs:
            for key, value in kwargs.items():
                self.metadata[key] = value
        self.local_client = p4_client

    def _update_msg(self):
        self._entry = p4runtime_pb2.PacketOut()
        self._entry.payload = self.payload
        self._entry.metadata.extend(self.metadata.values())

    def __setattr__(self, name, value):
        if name == "payload" and not isinstance(value, bytes):
            raise UserError("payload must be a bytes type")
        if name == "metadata" and not isinstance(value, PacketMetadata):
            raise UserError("metadata must be a PacketMetadata type")
        return super().__setattr__(name, value)

    def __dir__(self):
        return ["metadata", "send", "payload"]

    def __str__(self):
        self._update_msg()
        return str(self._entry)

    def send(self):
        """
        Send a packet-out message.

        :return: void
        """
        self._update_msg()
        msg = p4runtime_pb2.StreamMessageRequest()
        msg.packet.CopyFrom(self._entry)
        self.local_client.stream_out_q.put(msg)

    def str(self):
        """
        Packet-out metadata to string.

        :return: void
        """
        for key, value in self.metadata.itmes():
            print(f"Packet-out metadata attribute '{key}':'{value}'")


class IdleTimeoutNotification():
    """
    P4 idle timeout notification.
    """

    local_client = None

    def __init__(self, p4_client):
        self.notification_queue = queue.Queue()
        self.local_client = p4_client.local_client

        def _notification_recv_func(notification_queue):
            while True:
                msg = self.local_client.get_stream_packet("idle_timeout_notification",
                                               timeout=None)
                if not msg:
                    break
                notification_queue.put(msg)

        self.recv_t = Thread(target=_notification_recv_func,
                             args=(self.notification_queue,))
        self.recv_t.start()

    def sniff(self, function=None, timeout=None):
        """
        Return an iterator of notification messages.
        If the function is provided, we do not return an iterator and instead we apply
        the function to every notification message.
        """
        msgs = []

        if timeout is not None and timeout < 0:
            raise ValueError("Timeout can't be a negative number.")

        if timeout is None:
            while True:
                try:
                    msgs.append(self.notification_queue.get(block=True))
                except KeyboardInterrupt:
                    # User sends a Ctrl+C -> breaking
                    break

        else:  # timeout parameter is provided
            deadline = time.time() + timeout
            remaining_time = timeout
            while remaining_time > 0:
                try:
                    msgs.append(self.notification_queue.get(block=True,
                                                            timeout=remaining_time))
                    remaining_time = deadline - time.time()
                except KeyboardInterrupt:
                    # User sends an interrupt(e.g., Ctrl+C).
                    break
                except queue.Empty:
                    # No item available on timeout. Exiting
                    break

        if function is None:
            return iter(msgs)
        for msg in msgs:
            function(msg)

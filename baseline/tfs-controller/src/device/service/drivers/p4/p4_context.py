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
Build some context around a given P4 info file.
"""

from collections import Counter
import enum
from functools import partialmethod


@enum.unique
class P4Type(enum.Enum):
    """
    P4 types.
    """
    table = 1
    action = 2
    action_profile = 3
    counter = 4
    direct_counter = 5
    meter = 6
    direct_meter = 7
    controller_packet_metadata = 8
    digest = 9


P4Type.table.p4info_name = "tables"
P4Type.action.p4info_name = "actions"
P4Type.action_profile.p4info_name = "action_profiles"
P4Type.counter.p4info_name = "counters"
P4Type.direct_counter.p4info_name = "direct_counters"
P4Type.meter.p4info_name = "meters"
P4Type.direct_meter.p4info_name = "direct_meters"
P4Type.controller_packet_metadata.p4info_name = "controller_packet_metadata"
P4Type.digest.p4info_name = "digests"

for object_type in P4Type:
    object_type.pretty_name = object_type.name.replace('_', ' ')
    object_type.pretty_names = object_type.pretty_name + 's'


@enum.unique
class P4RuntimeEntity(enum.Enum):
    """
    P4 runtime entities.
    """
    table_entry = 1
    action_profile_member = 2
    action_profile_group = 3
    counter_entry = 4
    direct_counter_entry = 5
    meter_entry = 6
    direct_meter_entry = 7
    packet_replication_engine_entry = 8
    digest_entry = 9


class Context:
    """
    P4 context.
    """
    def __init__(self):
        self.p4info = None
        self.p4info_obj_map = {}
        self.p4info_obj_map_by_id = {}
        self.p4info_objs_by_type = {}

    def set_p4info(self, p4info):
        """
        Set a p4 info file.

        :param p4info: p4 info file
        :return: void
        """
        self.p4info = p4info
        self._import_p4info_names()

    def get_obj(self, obj_type, name):
        """
        Retrieve an object by type and name.

        :param obj_type: P4 object type
        :param name: P4 object name
        :return: P4 object
        """
        key = (obj_type, name)
        return self.p4info_obj_map.get(key, None)

    def get_obj_id(self, obj_type, name):
        """
        Retrieve a P4 object's ID by type and name.

        :param obj_type: P4 object type
        :param name: P4 object name
        :return: P4 object ID
        """
        obj = self.get_obj(obj_type, name)
        if obj is None:
            return None
        return obj.preamble.id

    def get_param(self, action_name, name):
        """
        Get an action parameter by action name.

        :param action_name: P4 action name
        :param name: action parameter name
        :return: action parameter
        """
        action = self.get_obj(P4Type.action, action_name)
        if action is None:
            return None
        for param in action.params:
            if param.name == name:
                return param
        return None

    def get_mf(self, table_name, name):
        """
        Get a table's match field by name.

        :param table_name: P4 table name
        :param name: match field name
        :return: match field
        """
        table = self.get_obj(P4Type.table, table_name)
        if table is None:
            return None
        for match_field in table.match_fields:
            if match_field.name == name:
                return match_field
        return None

    def get_param_id(self, action_name, name):
        """
        Get an action parameter ID by the action and parameter names.

        :param action_name: P4 action name
        :param name: action parameter name
        :return: action parameter ID
        """
        param = self.get_param(action_name, name)
        return None if param is None else param.id

    def get_mf_id(self, table_name, name):
        """
        Get a table's match field ID by name.

        :param table_name: P4 table name
        :param name: match field name
        :return: match field ID
        """
        match_field = self.get_mf(table_name, name)
        return None if match_field is None else match_field.id

    def get_param_name(self, action_name, id_):
        """
        Get an action parameter name by the action name and action ID.

        :param action_name: P4 action name
        :param id_: action parameter ID
        :return: action parameter name
        """
        action = self.get_obj(P4Type.action, action_name)
        if action is None:
            return None
        for param in action.params:
            if param.id == id_:
                return param.name
        return None

    def get_mf_name(self, table_name, id_):
        """
        Get a table's match field name by ID.

        :param table_name: P4 table name
        :param id_: match field ID
        :return: match field name
        """
        table = self.get_obj(P4Type.table, table_name)
        if table is None:
            return None
        for match_field in table.match_fields:
            if match_field.id == id_:
                return match_field.name
        return None

    def get_objs(self, obj_type):
        """
        Get P4 objects by type.

        :param obj_type: P4 object type
        :return: list of tuples (object name, object)
        """
        objects = self.p4info_objs_by_type[obj_type]
        for name, obj in objects.items():
            yield name, obj

    def get_name_from_id(self, id_):
        """
        Get P4 object name by its ID.

        :param id_: P4 object ID
        :return: P4 object name
        """
        return self.p4info_obj_map_by_id[id_].preamble.name

    def get_obj_by_id(self, id_):
        """
        Get P4 object by its ID.

        :param id_: P4 object ID
        :return: P4 object
        """
        return self.p4info_obj_map_by_id[id_]

    def get_packet_metadata_name_from_id(self, ctrl_pkt_md_name, id_):
        """
        Get packet metadata name by ID.

        :param ctrl_pkt_md_name: packet replication entity name
        :param id_: packet metadata ID
        :return: packet metadata name
        """
        ctrl_pkt_md = self.get_obj(
            P4Type.controller_packet_metadata, ctrl_pkt_md_name)
        if not ctrl_pkt_md:
            return None
        for meta in ctrl_pkt_md.metadata:
            if meta.id == id_:
                return meta.name
        return None

    # We accept any suffix that uniquely identifies the object
    # among p4info objects of the same type.
    def _import_p4info_names(self):
        """
        Import p4 info into memory.

        :return: void
        """
        suffix_count = Counter()
        for obj_type in P4Type:
            self.p4info_objs_by_type[obj_type] = {}
            for obj in getattr(self.p4info, obj_type.p4info_name):
                pre = obj.preamble
                self.p4info_obj_map_by_id[pre.id] = obj
                self.p4info_objs_by_type[obj_type][pre.name] = obj
                suffix = None
                for suf in reversed(pre.name.split(".")):
                    suffix = suf if suffix is None else suf + "." + suffix
                    key = (obj_type, suffix)
                    self.p4info_obj_map[key] = obj
                    suffix_count[key] += 1
        for key, cnt in suffix_count.items():
            if cnt > 1:
                del self.p4info_obj_map[key]


# Add p4info object and object id "getters" for each object type;
# these are just wrappers around Context.get_obj and Context.get_obj_id.
# For example: get_table(x) and get_table_id(x) respectively call
# get_obj(P4Type.table, x) and get_obj_id(P4Type.table, x)
for object_type in P4Type:
    object_name = "_".join(["get", object_type.name])
    setattr(Context, object_name, partialmethod(
        Context.get_obj, object_type))
    object_name = "_".join(["get", object_type.name, "id"])
    setattr(Context, object_name, partialmethod(
        Context.get_obj_id, object_type))

for object_type in P4Type:
    object_name = "_".join(["get", object_type.p4info_name])
    setattr(Context, object_name, partialmethod(Context.get_objs, object_type))

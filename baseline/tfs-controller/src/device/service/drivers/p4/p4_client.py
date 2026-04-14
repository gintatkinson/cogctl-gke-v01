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
P4Runtime client.
"""

import logging
import queue
import sys
import enum
import threading
from functools import wraps
from typing import NamedTuple
import grpc
import google.protobuf.text_format
from google.rpc import status_pb2, code_pb2

from p4.v1 import p4runtime_pb2
from p4.v1 import p4runtime_pb2_grpc

STREAM_ATTR_ARBITRATION = "arbitration"
STREAM_ATTR_PACKET = "packet"
STREAM_ATTR_DIGEST = "digest"
STREAM_ATTR_IDLE_NOT = "idle_timeout_notification"
STREAM_ATTR_UNKNOWN = "unknown"

LOGGER = logging.getLogger(__name__)


class P4RuntimeErrorFormatException(Exception):
    """
    P4Runtime error format exception.
    """


# Used to iterate over the p4.Error messages in a gRPC error Status object
class P4RuntimeErrorIterator:
    """
    P4Runtime error iterator.

    Attributes
    ----------
    grpc_error : object
        gRPC error
    """

    def __init__(self, grpc_error):
        assert grpc_error.code() == grpc.StatusCode.UNKNOWN
        self.grpc_error = grpc_error

        error = None
        # The gRPC Python package does not have a convenient way to access the
        # binary details for the error: they are treated as trailing metadata.
        for meta in self.grpc_error.trailing_metadata():
            if meta[0] == "grpc-status-details-bin":
                error = status_pb2.Status()
                error.ParseFromString(meta[1])
                break
        if error is None:
            raise P4RuntimeErrorFormatException("No binary details field")

        if len(error.details) == 0:
            raise P4RuntimeErrorFormatException(
                "Binary details field has empty Any details repeated field")
        self.errors = error.details
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.idx < len(self.errors):
            p4_error = p4runtime_pb2.Error()
            one_error_any = self.errors[self.idx]
            if not one_error_any.Unpack(p4_error):
                raise P4RuntimeErrorFormatException(
                    "Cannot convert Any message to p4.Error")
            if p4_error.canonical_code == code_pb2.OK:
                continue
            val = self.idx, p4_error
            self.idx += 1
            return val
        raise StopIteration


class P4RuntimeWriteException(Exception):
    """
    P4Runtime write exception handler.

    Attributes
    ----------
    grpc_error : object
        gRPC error
    """

    def __init__(self, grpc_error):
        assert grpc_error.code() == grpc.StatusCode.UNKNOWN
        super().__init__()
        self.errors = []
        try:
            error_iterator = P4RuntimeErrorIterator(grpc_error)
            for error_tuple in error_iterator:
                self.errors.append(error_tuple)
        except P4RuntimeErrorFormatException as ex:
            raise P4RuntimeException(grpc_error) from ex

    def __str__(self):
        message = "Error(s) during Write:\n"
        for idx, p4_error in self.errors:
            code_name = code_pb2._CODE.values_by_number[
                p4_error.canonical_code].name
            message += f"\t* At index {idx}: {code_name}, " \
                       f"'{p4_error.message}'\n"
        return message


class P4RuntimeException(Exception):
    """
    P4Runtime exception handler.

    Attributes
    ----------
    grpc_error : object
        gRPC error
    """

    def __init__(self, grpc_error):
        super().__init__()
        self.grpc_error = grpc_error

    def __str__(self):
        message = f"P4Runtime RPC error ({self.grpc_error.code().name}): " \
                  f"{self.grpc_error.details()}"
        return message


def parse_p4runtime_write_error(func):
    """
    Parse P4Runtime write error.

    :param func: function
    :return: parsed error
    """

    @wraps(func)
    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.UNKNOWN:
                raise ex
            raise P4RuntimeWriteException(ex) from None

    return handle


def parse_p4runtime_error(func):
    """
    Parse P4Runtime error.

    :param func: function
    :return: parsed error
    """

    @wraps(func)
    def handle(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except grpc.RpcError as ex:
            raise P4RuntimeException(ex) from None

    return handle


class SSLOptions(NamedTuple):
    """
    Tuple of SSL options.
    """
    insecure: bool
    cacert: str = None
    cert: str = None
    key: str = None


def read_pem_file(path):
    """
    Load and read PEM file.

    :param path: path to PEM file
    :return: file descriptor
    """
    try:
        with open(path, "rb") as f_d:
            return f_d.read()
    except (FileNotFoundError, IOError, OSError):
        logging.critical("Cannot read from PEM file '%s'", path)
        sys.exit(1)


@enum.unique
class WriteOperation(enum.Enum):
    """
    Write Operations.
    """
    insert = 1
    update = 2
    delete = 3


def select_operation(mode):
    """
    Select P4 operation based upon the operation mode.

    :param mode: operation mode
    :return: P4 operation protobuf object
    """
    if mode == WriteOperation.insert:
        return p4runtime_pb2.Update.INSERT
    if mode == WriteOperation.update:
        return p4runtime_pb2.Update.UPDATE
    if mode == WriteOperation.delete:
        return p4runtime_pb2.Update.DELETE
    return None


def select_entity_type(entity, update):
    """
    Select P4 entity type for an update.

    :param entity: P4 entity object
    :param update: update operation
    :return: the correct update entity or None
    """
    if isinstance(entity, p4runtime_pb2.TableEntry):
        return update.entity.table_entry
    if isinstance(entity, p4runtime_pb2.ActionProfileGroup):
        return update.entity.action_profile_group
    if isinstance(entity, p4runtime_pb2.ActionProfileMember):
        return update.entity.action_profile_member
    return None


class P4RuntimeClient:
    """
    P4Runtime client.

    Attributes
    ----------
    device_id : int
        P4 device ID
    grpc_address : str
        IP address and port
    election_id : tuple
        Mastership election ID
    role_name : str
        Role name (optional)
    ssl_options: tuple
        SSL options" named tuple (optional)
    """

    def __init__(self, device_id, grpc_address,
                 election_id, role_name=None, ssl_options=None):
        self.device_id = device_id
        self.election_id = election_id
        self.role_name = role_name
        if ssl_options is None:
            self.ssl_options = SSLOptions(True)
        else:
            self.ssl_options = ssl_options
        LOGGER.debug(
            "Connecting to device %d at %s", device_id, grpc_address)

        if self.ssl_options.insecure:
            logging.debug("Using insecure channel")
            self.channel = grpc.insecure_channel(grpc_address)
        else:
            # root certificates are retrieved from a default location
            # chosen by gRPC runtime unless the user provides
            # custom certificates.
            root_certificates = None
            if self.ssl_options.cacert is not None:
                root_certificates = read_pem_file(self.ssl_options.cacert)
            certificate_chain = None
            if self.ssl_options.cert is not None:
                certificate_chain = read_pem_file(self.ssl_options.cert)
            private_key = None
            if self.ssl_options.key is not None:
                private_key = read_pem_file(self.ssl_options.key)
            creds = grpc.ssl_channel_credentials(root_certificates, private_key,
                                                 certificate_chain)
            self.channel = grpc.secure_channel(grpc_address, creds)
        self.stream_in_q = None
        self.stream_out_q = None
        self.stream = None
        self.stream_recv_thread = None
        self.stub = p4runtime_pb2_grpc.P4RuntimeStub(self.channel)

        try:
            self.set_up_stream()
        except P4RuntimeException:
            LOGGER.critical("Failed to connect to P4Runtime server")
            sys.exit(1)
        LOGGER.info("P4Runtime client is successfully invoked")

    def set_up_stream(self):
        """
        Set up a gRPC stream.
        """
        self.stream_out_q = queue.Queue()
        # queues for different messages
        self.stream_in_q = {
            STREAM_ATTR_ARBITRATION: queue.Queue(),
            STREAM_ATTR_PACKET: queue.Queue(),
            STREAM_ATTR_DIGEST: queue.Queue(),
            STREAM_ATTR_IDLE_NOT: queue.Queue(),
            STREAM_ATTR_UNKNOWN: queue.Queue(),
        }

        def stream_req_iterator():
            while True:
                stream_p = self.stream_out_q.get()
                if stream_p is None:
                    break
                yield stream_p

        def stream_recv_wrapper(stream):
            @parse_p4runtime_error
            def stream_recv():
                for stream_p in stream:
                    if stream_p.HasField("arbitration"):
                        self.stream_in_q["arbitration"].put(stream_p)
                    elif stream_p.HasField("packet"):
                        self.stream_in_q["packet"].put(stream_p)
                    elif stream_p.HasField("digest"):
                        self.stream_in_q["digest"].put(stream_p)
                    else:
                        self.stream_in_q["unknown"].put(stream_p)

            try:
                stream_recv()
            except P4RuntimeException as ex:
                logging.critical("StreamChannel error, closing stream")
                logging.critical(ex)
                for k in self.stream_in_q:
                    self.stream_in_q[k].put(None)

        self.stream = self.stub.StreamChannel(stream_req_iterator())
        self.stream_recv_thread = threading.Thread(
            target=stream_recv_wrapper, args=(self.stream,))
        self.stream_recv_thread.start()
        self.handshake()

    def handshake(self):
        """
        Handshake with gRPC server.
        """

        req = p4runtime_pb2.StreamMessageRequest()
        arbitration = req.arbitration
        arbitration.device_id = self.device_id
        election_id = arbitration.election_id
        election_id.high = self.election_id[0]
        election_id.low = self.election_id[1]
        if self.role_name is not None:
            arbitration.role.name = self.role_name
        self.stream_out_q.put(req)

        rep = self.get_stream_packet(STREAM_ATTR_ARBITRATION, timeout=2)
        if rep is None:
            logging.critical("Failed to establish session with server")
            sys.exit(1)
        is_primary = (rep.arbitration.status.code == code_pb2.OK)
        logging.debug("Session established, client is '%s'",
                      "primary" if is_primary else "backup")
        if not is_primary:
            print("You are not the primary client,"
                  "you only have read access to the server")

    def get_stream_packet(self, type_, timeout=1):
        """
        Get a new message from the stream.

        :param type_: stream type.
        :param timeout: time to wait.
        :return: message or None
        """
        if type_ not in self.stream_in_q:
            print("Unknown stream type 's"'', type_)
            return None
        try:
            msg = self.stream_in_q[type_].get(timeout=timeout)
            return msg
        except queue.Empty:  # timeout expired
            return None

    @parse_p4runtime_error
    def get_p4info(self):
        """
        Retrieve P4Info content.

        :return: P4Info object.
        """
        logging.debug("Retrieving P4Info file")
        req = p4runtime_pb2.GetForwardingPipelineConfigRequest()
        req.device_id = self.device_id
        req.response_type = \
            p4runtime_pb2.GetForwardingPipelineConfigRequest.P4INFO_AND_COOKIE
        rep = self.stub.GetForwardingPipelineConfig(req)
        return rep.config.p4info

    @parse_p4runtime_error
    def set_fwd_pipe_config(self, p4info_path, bin_path):
        """
        Configure the pipeline.

        :param p4info_path: path to the P4Info file
        :param bin_path: path to the binary file
        :return:
        """
        logging.debug("Setting forwarding pipeline config")
        req = p4runtime_pb2.SetForwardingPipelineConfigRequest()
        req.device_id = self.device_id
        if self.role_name is not None:
            req.role = self.role_name
        election_id = req.election_id
        election_id.high = self.election_id[0]
        election_id.low = self.election_id[1]
        req.action = \
            p4runtime_pb2.SetForwardingPipelineConfigRequest.VERIFY_AND_COMMIT
        with open(p4info_path, "r", encoding="utf-8") as f_info:
            with open(bin_path, "rb") as f_bin:
                try:
                    google.protobuf.text_format.Merge(
                        f_info.read(), req.config.p4info)
                except google.protobuf.text_format.ParseError:
                    logging.error("Error when parsing P4Info")
                    raise
                req.config.p4_device_config = f_bin.read()
        return self.stub.SetForwardingPipelineConfig(req)

    def tear_down(self):
        """
        Tear connection with the gRPC server down.
        """
        if self.stream_out_q:
            logging.debug("Cleaning up stream")
            self.stream_out_q.put(None)
        if self.stream_in_q:
            for k in self.stream_in_q:
                self.stream_in_q[k].put(None)
        if self.stream_recv_thread:
            self.stream_recv_thread.join()
        self.channel.close()
        # avoid a race condition if channel deleted when process terminates
        del self.channel

    @parse_p4runtime_write_error
    def __write(self, entity, mode=WriteOperation.insert):
        """
        Perform a write operation.

        :param entity: P4 entity to write
        :param mode: operation mode (defaults to insert)
        :return: void
        """
        if isinstance(entity, (list, tuple)):
            for ent in entity:
                self.__write(ent)
            return
        req = self.__get_new_write_request()
        update = req.updates.add()
        update.type = select_operation(mode)
        msg_entity = select_entity_type(entity, update)
        if not msg_entity:
            msg = f"{mode.name} operation for entity {entity.__name__}" \
                  f"not supported"
            raise P4RuntimeWriteException(msg)
        msg_entity.CopyFrom(entity)
        self.__simple_write(req)

    def __get_new_write_request(self):
        """
        Create a new write request message.

        :return: write request message
        """
        req = p4runtime_pb2.WriteRequest()
        req.device_id = self.device_id
        if self.role_name is not None:
            req.role = self.role_name
        election_id = req.election_id
        election_id.high = self.election_id[0]
        election_id.low = self.election_id[1]
        return req

    @parse_p4runtime_write_error
    def __simple_write(self, req):
        """
        Send a write operation into the wire.

        :param req: write operation request
        :return: void
        """
        try:
            return self.stub.Write(req)
        except grpc.RpcError as ex:
            if ex.code() != grpc.StatusCode.UNKNOWN:
                raise ex
            raise P4RuntimeWriteException(ex) from ex

    @parse_p4runtime_write_error
    def insert(self, entity):
        """
        Perform an insert write operation.

        :param entity: P4 entity to insert
        :return: void
        """
        return self.__write(entity, WriteOperation.insert)

    @parse_p4runtime_write_error
    def update(self, entity):
        """
        Perform an update write operation.

        :param entity: P4 entity to update
        :return: void
        """
        return self.__write(entity, WriteOperation.update)

    @parse_p4runtime_write_error
    def delete(self, entity):
        """
        Perform a delete write operation.

        :param entity: P4 entity to delete
        :return: void
        """
        return self.__write(entity, WriteOperation.delete)

    @parse_p4runtime_write_error
    def write(self, req):
        """
        Write device operation.

        :param req: write request message
        :return: status
        """
        req.device_id = self.device_id
        if self.role_name is not None:
            req.role = self.role_name
        election_id = req.election_id
        election_id.high = self.election_id[0]
        election_id.low = self.election_id[1]
        return self.__simple_write(req)

    @parse_p4runtime_write_error
    def write_update(self, update):
        """
        Update device operation.

        :param update: update request message
        :return: status
        """
        req = self.__get_new_write_request()
        req.updates.extend([update])
        return self.__simple_write(req)

    # Decorator is useless here: in case of server error,
    # the exception is raised during the iteration (when next() is called).
    @parse_p4runtime_error
    def read_one(self, entity):
        """
        Read device operation.

        :param entity: P4 entity for which the read is issued
        :return: status
        """
        req = p4runtime_pb2.ReadRequest()
        if self.role_name is not None:
            req.role = self.role_name
        req.device_id = self.device_id
        req.entities.extend([entity])
        return self.stub.Read(req)

    @parse_p4runtime_error
    def api_version(self):
        """
        P4Runtime API version.

        :return: API version hex
        """
        req = p4runtime_pb2.CapabilitiesRequest()
        rep = self.stub.Capabilities(req)
        return rep.p4runtime_api_version

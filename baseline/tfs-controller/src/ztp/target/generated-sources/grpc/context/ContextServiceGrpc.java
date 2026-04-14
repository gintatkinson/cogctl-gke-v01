package context;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: context.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ContextServiceGrpc {

    private ContextServiceGrpc() {
    }

    public static final String SERVICE_NAME = "context.ContextService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList> getListContextIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListContextIds", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.ContextIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList> getListContextIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList> getListContextIdsMethod;
        if ((getListContextIdsMethod = ContextServiceGrpc.getListContextIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListContextIdsMethod = ContextServiceGrpc.getListContextIdsMethod) == null) {
                    ContextServiceGrpc.getListContextIdsMethod = getListContextIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListContextIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListContextIds")).build();
                }
            }
        }
        return getListContextIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList> getListContextsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListContexts", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.ContextList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList> getListContextsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList> getListContextsMethod;
        if ((getListContextsMethod = ContextServiceGrpc.getListContextsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListContextsMethod = ContextServiceGrpc.getListContextsMethod) == null) {
                    ContextServiceGrpc.getListContextsMethod = getListContextsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListContexts")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListContexts")).build();
                }
            }
        }
        return getListContextsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context> getGetContextMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetContext", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.Context.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context> getGetContextMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context> getGetContextMethod;
        if ((getGetContextMethod = ContextServiceGrpc.getGetContextMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetContextMethod = ContextServiceGrpc.getGetContextMethod) == null) {
                    ContextServiceGrpc.getGetContextMethod = getGetContextMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetContext")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Context.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetContext")).build();
                }
            }
        }
        return getGetContextMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId> getSetContextMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetContext", requestType = context.ContextOuterClass.Context.class, responseType = context.ContextOuterClass.ContextId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId> getSetContextMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId> getSetContextMethod;
        if ((getSetContextMethod = ContextServiceGrpc.getSetContextMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetContextMethod = ContextServiceGrpc.getSetContextMethod) == null) {
                    ContextServiceGrpc.getSetContextMethod = getSetContextMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetContext")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Context.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetContext")).build();
                }
            }
        }
        return getSetContextMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty> getRemoveContextMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveContext", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty> getRemoveContextMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty> getRemoveContextMethod;
        if ((getRemoveContextMethod = ContextServiceGrpc.getRemoveContextMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveContextMethod = ContextServiceGrpc.getRemoveContextMethod) == null) {
                    ContextServiceGrpc.getRemoveContextMethod = getRemoveContextMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveContext")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveContext")).build();
                }
            }
        }
        return getRemoveContextMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent> getGetContextEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetContextEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.ContextEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent> getGetContextEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent> getGetContextEventsMethod;
        if ((getGetContextEventsMethod = ContextServiceGrpc.getGetContextEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetContextEventsMethod = ContextServiceGrpc.getGetContextEventsMethod) == null) {
                    ContextServiceGrpc.getGetContextEventsMethod = getGetContextEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetContextEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetContextEvents")).build();
                }
            }
        }
        return getGetContextEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList> getListTopologyIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListTopologyIds", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.TopologyIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList> getListTopologyIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList> getListTopologyIdsMethod;
        if ((getListTopologyIdsMethod = ContextServiceGrpc.getListTopologyIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListTopologyIdsMethod = ContextServiceGrpc.getListTopologyIdsMethod) == null) {
                    ContextServiceGrpc.getListTopologyIdsMethod = getListTopologyIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListTopologyIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListTopologyIds")).build();
                }
            }
        }
        return getListTopologyIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList> getListTopologiesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListTopologies", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.TopologyList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList> getListTopologiesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList> getListTopologiesMethod;
        if ((getListTopologiesMethod = ContextServiceGrpc.getListTopologiesMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListTopologiesMethod = ContextServiceGrpc.getListTopologiesMethod) == null) {
                    ContextServiceGrpc.getListTopologiesMethod = getListTopologiesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListTopologies")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListTopologies")).build();
                }
            }
        }
        return getListTopologiesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology> getGetTopologyMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetTopology", requestType = context.ContextOuterClass.TopologyId.class, responseType = context.ContextOuterClass.Topology.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology> getGetTopologyMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology> getGetTopologyMethod;
        if ((getGetTopologyMethod = ContextServiceGrpc.getGetTopologyMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetTopologyMethod = ContextServiceGrpc.getGetTopologyMethod) == null) {
                    ContextServiceGrpc.getGetTopologyMethod = getGetTopologyMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetTopology")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Topology.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetTopology")).build();
                }
            }
        }
        return getGetTopologyMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails> getGetTopologyDetailsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetTopologyDetails", requestType = context.ContextOuterClass.TopologyId.class, responseType = context.ContextOuterClass.TopologyDetails.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails> getGetTopologyDetailsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails> getGetTopologyDetailsMethod;
        if ((getGetTopologyDetailsMethod = ContextServiceGrpc.getGetTopologyDetailsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetTopologyDetailsMethod = ContextServiceGrpc.getGetTopologyDetailsMethod) == null) {
                    ContextServiceGrpc.getGetTopologyDetailsMethod = getGetTopologyDetailsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetTopologyDetails")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyDetails.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetTopologyDetails")).build();
                }
            }
        }
        return getGetTopologyDetailsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId> getSetTopologyMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetTopology", requestType = context.ContextOuterClass.Topology.class, responseType = context.ContextOuterClass.TopologyId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId> getSetTopologyMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId> getSetTopologyMethod;
        if ((getSetTopologyMethod = ContextServiceGrpc.getSetTopologyMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetTopologyMethod = ContextServiceGrpc.getSetTopologyMethod) == null) {
                    ContextServiceGrpc.getSetTopologyMethod = getSetTopologyMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetTopology")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Topology.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetTopology")).build();
                }
            }
        }
        return getSetTopologyMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty> getRemoveTopologyMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveTopology", requestType = context.ContextOuterClass.TopologyId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty> getRemoveTopologyMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty> getRemoveTopologyMethod;
        if ((getRemoveTopologyMethod = ContextServiceGrpc.getRemoveTopologyMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveTopologyMethod = ContextServiceGrpc.getRemoveTopologyMethod) == null) {
                    ContextServiceGrpc.getRemoveTopologyMethod = getRemoveTopologyMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveTopology")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveTopology")).build();
                }
            }
        }
        return getRemoveTopologyMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent> getGetTopologyEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetTopologyEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.TopologyEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent> getGetTopologyEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent> getGetTopologyEventsMethod;
        if ((getGetTopologyEventsMethod = ContextServiceGrpc.getGetTopologyEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetTopologyEventsMethod = ContextServiceGrpc.getGetTopologyEventsMethod) == null) {
                    ContextServiceGrpc.getGetTopologyEventsMethod = getGetTopologyEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetTopologyEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.TopologyEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetTopologyEvents")).build();
                }
            }
        }
        return getGetTopologyEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList> getListDeviceIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListDeviceIds", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.DeviceIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList> getListDeviceIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList> getListDeviceIdsMethod;
        if ((getListDeviceIdsMethod = ContextServiceGrpc.getListDeviceIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListDeviceIdsMethod = ContextServiceGrpc.getListDeviceIdsMethod) == null) {
                    ContextServiceGrpc.getListDeviceIdsMethod = getListDeviceIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListDeviceIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListDeviceIds")).build();
                }
            }
        }
        return getListDeviceIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList> getListDevicesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListDevices", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.DeviceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList> getListDevicesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList> getListDevicesMethod;
        if ((getListDevicesMethod = ContextServiceGrpc.getListDevicesMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListDevicesMethod = ContextServiceGrpc.getListDevicesMethod) == null) {
                    ContextServiceGrpc.getListDevicesMethod = getListDevicesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListDevices")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListDevices")).build();
                }
            }
        }
        return getListDevicesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device> getGetDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetDevice", requestType = context.ContextOuterClass.DeviceId.class, responseType = context.ContextOuterClass.Device.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device> getGetDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device> getGetDeviceMethod;
        if ((getGetDeviceMethod = ContextServiceGrpc.getGetDeviceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetDeviceMethod = ContextServiceGrpc.getGetDeviceMethod) == null) {
                    ContextServiceGrpc.getGetDeviceMethod = getGetDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Device.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetDevice")).build();
                }
            }
        }
        return getGetDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getSetDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetDevice", requestType = context.ContextOuterClass.Device.class, responseType = context.ContextOuterClass.DeviceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getSetDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId> getSetDeviceMethod;
        if ((getSetDeviceMethod = ContextServiceGrpc.getSetDeviceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetDeviceMethod = ContextServiceGrpc.getSetDeviceMethod) == null) {
                    ContextServiceGrpc.getSetDeviceMethod = getSetDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Device.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetDevice")).build();
                }
            }
        }
        return getSetDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getRemoveDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveDevice", requestType = context.ContextOuterClass.DeviceId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getRemoveDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty> getRemoveDeviceMethod;
        if ((getRemoveDeviceMethod = ContextServiceGrpc.getRemoveDeviceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveDeviceMethod = ContextServiceGrpc.getRemoveDeviceMethod) == null) {
                    ContextServiceGrpc.getRemoveDeviceMethod = getRemoveDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveDevice")).build();
                }
            }
        }
        return getRemoveDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent> getGetDeviceEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetDeviceEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.DeviceEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent> getGetDeviceEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent> getGetDeviceEventsMethod;
        if ((getGetDeviceEventsMethod = ContextServiceGrpc.getGetDeviceEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetDeviceEventsMethod = ContextServiceGrpc.getGetDeviceEventsMethod) == null) {
                    ContextServiceGrpc.getGetDeviceEventsMethod = getGetDeviceEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetDeviceEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetDeviceEvents")).build();
                }
            }
        }
        return getGetDeviceEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList> getSelectDeviceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SelectDevice", requestType = context.ContextOuterClass.DeviceFilter.class, responseType = context.ContextOuterClass.DeviceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList> getSelectDeviceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList> getSelectDeviceMethod;
        if ((getSelectDeviceMethod = ContextServiceGrpc.getSelectDeviceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSelectDeviceMethod = ContextServiceGrpc.getSelectDeviceMethod) == null) {
                    ContextServiceGrpc.getSelectDeviceMethod = getSelectDeviceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SelectDevice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceFilter.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.DeviceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SelectDevice")).build();
                }
            }
        }
        return getSelectDeviceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList> getListEndPointNamesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListEndPointNames", requestType = context.ContextOuterClass.EndPointIdList.class, responseType = context.ContextOuterClass.EndPointNameList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList> getListEndPointNamesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList> getListEndPointNamesMethod;
        if ((getListEndPointNamesMethod = ContextServiceGrpc.getListEndPointNamesMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListEndPointNamesMethod = ContextServiceGrpc.getListEndPointNamesMethod) == null) {
                    ContextServiceGrpc.getListEndPointNamesMethod = getListEndPointNamesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListEndPointNames")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.EndPointIdList.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.EndPointNameList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListEndPointNames")).build();
                }
            }
        }
        return getListEndPointNamesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList> getListLinkIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListLinkIds", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.LinkIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList> getListLinkIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList> getListLinkIdsMethod;
        if ((getListLinkIdsMethod = ContextServiceGrpc.getListLinkIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListLinkIdsMethod = ContextServiceGrpc.getListLinkIdsMethod) == null) {
                    ContextServiceGrpc.getListLinkIdsMethod = getListLinkIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListLinkIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListLinkIds")).build();
                }
            }
        }
        return getListLinkIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList> getListLinksMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListLinks", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.LinkList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList> getListLinksMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList> getListLinksMethod;
        if ((getListLinksMethod = ContextServiceGrpc.getListLinksMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListLinksMethod = ContextServiceGrpc.getListLinksMethod) == null) {
                    ContextServiceGrpc.getListLinksMethod = getListLinksMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListLinks")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListLinks")).build();
                }
            }
        }
        return getListLinksMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link> getGetLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetLink", requestType = context.ContextOuterClass.LinkId.class, responseType = context.ContextOuterClass.Link.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link> getGetLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link> getGetLinkMethod;
        if ((getGetLinkMethod = ContextServiceGrpc.getGetLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetLinkMethod = ContextServiceGrpc.getGetLinkMethod) == null) {
                    ContextServiceGrpc.getGetLinkMethod = getGetLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Link.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetLink")).build();
                }
            }
        }
        return getGetLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId> getSetLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetLink", requestType = context.ContextOuterClass.Link.class, responseType = context.ContextOuterClass.LinkId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId> getSetLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId> getSetLinkMethod;
        if ((getSetLinkMethod = ContextServiceGrpc.getSetLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetLinkMethod = ContextServiceGrpc.getSetLinkMethod) == null) {
                    ContextServiceGrpc.getSetLinkMethod = getSetLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Link.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetLink")).build();
                }
            }
        }
        return getSetLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getRemoveLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveLink", requestType = context.ContextOuterClass.LinkId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getRemoveLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getRemoveLinkMethod;
        if ((getRemoveLinkMethod = ContextServiceGrpc.getRemoveLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveLinkMethod = ContextServiceGrpc.getRemoveLinkMethod) == null) {
                    ContextServiceGrpc.getRemoveLinkMethod = getRemoveLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveLink")).build();
                }
            }
        }
        return getRemoveLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent> getGetLinkEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetLinkEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.LinkEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent> getGetLinkEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent> getGetLinkEventsMethod;
        if ((getGetLinkEventsMethod = ContextServiceGrpc.getGetLinkEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetLinkEventsMethod = ContextServiceGrpc.getGetLinkEventsMethod) == null) {
                    ContextServiceGrpc.getGetLinkEventsMethod = getGetLinkEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetLinkEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetLinkEvents")).build();
                }
            }
        }
        return getGetLinkEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList> getListServiceIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListServiceIds", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.ServiceIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList> getListServiceIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList> getListServiceIdsMethod;
        if ((getListServiceIdsMethod = ContextServiceGrpc.getListServiceIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListServiceIdsMethod = ContextServiceGrpc.getListServiceIdsMethod) == null) {
                    ContextServiceGrpc.getListServiceIdsMethod = getListServiceIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListServiceIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListServiceIds")).build();
                }
            }
        }
        return getListServiceIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList> getListServicesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListServices", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.ServiceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList> getListServicesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList> getListServicesMethod;
        if ((getListServicesMethod = ContextServiceGrpc.getListServicesMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListServicesMethod = ContextServiceGrpc.getListServicesMethod) == null) {
                    ContextServiceGrpc.getListServicesMethod = getListServicesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListServices")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListServices")).build();
                }
            }
        }
        return getListServicesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service> getGetServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetService", requestType = context.ContextOuterClass.ServiceId.class, responseType = context.ContextOuterClass.Service.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service> getGetServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service> getGetServiceMethod;
        if ((getGetServiceMethod = ContextServiceGrpc.getGetServiceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetServiceMethod = ContextServiceGrpc.getGetServiceMethod) == null) {
                    ContextServiceGrpc.getGetServiceMethod = getGetServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetService")).build();
                }
            }
        }
        return getGetServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getSetServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetService", requestType = context.ContextOuterClass.Service.class, responseType = context.ContextOuterClass.ServiceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getSetServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getSetServiceMethod;
        if ((getSetServiceMethod = ContextServiceGrpc.getSetServiceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetServiceMethod = ContextServiceGrpc.getSetServiceMethod) == null) {
                    ContextServiceGrpc.getSetServiceMethod = getSetServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetService")).build();
                }
            }
        }
        return getSetServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUnsetServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "UnsetService", requestType = context.ContextOuterClass.Service.class, responseType = context.ContextOuterClass.ServiceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUnsetServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId> getUnsetServiceMethod;
        if ((getUnsetServiceMethod = ContextServiceGrpc.getUnsetServiceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getUnsetServiceMethod = ContextServiceGrpc.getUnsetServiceMethod) == null) {
                    ContextServiceGrpc.getUnsetServiceMethod = getUnsetServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "UnsetService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Service.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("UnsetService")).build();
                }
            }
        }
        return getUnsetServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getRemoveServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveService", requestType = context.ContextOuterClass.ServiceId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getRemoveServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty> getRemoveServiceMethod;
        if ((getRemoveServiceMethod = ContextServiceGrpc.getRemoveServiceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveServiceMethod = ContextServiceGrpc.getRemoveServiceMethod) == null) {
                    ContextServiceGrpc.getRemoveServiceMethod = getRemoveServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveService")).build();
                }
            }
        }
        return getRemoveServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent> getGetServiceEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetServiceEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.ServiceEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent> getGetServiceEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent> getGetServiceEventsMethod;
        if ((getGetServiceEventsMethod = ContextServiceGrpc.getGetServiceEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetServiceEventsMethod = ContextServiceGrpc.getGetServiceEventsMethod) == null) {
                    ContextServiceGrpc.getGetServiceEventsMethod = getGetServiceEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetServiceEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetServiceEvents")).build();
                }
            }
        }
        return getGetServiceEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList> getSelectServiceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SelectService", requestType = context.ContextOuterClass.ServiceFilter.class, responseType = context.ContextOuterClass.ServiceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList> getSelectServiceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList> getSelectServiceMethod;
        if ((getSelectServiceMethod = ContextServiceGrpc.getSelectServiceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSelectServiceMethod = ContextServiceGrpc.getSelectServiceMethod) == null) {
                    ContextServiceGrpc.getSelectServiceMethod = getSelectServiceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SelectService")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceFilter.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SelectService")).build();
                }
            }
        }
        return getSelectServiceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList> getListSliceIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListSliceIds", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.SliceIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList> getListSliceIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList> getListSliceIdsMethod;
        if ((getListSliceIdsMethod = ContextServiceGrpc.getListSliceIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListSliceIdsMethod = ContextServiceGrpc.getListSliceIdsMethod) == null) {
                    ContextServiceGrpc.getListSliceIdsMethod = getListSliceIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListSliceIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListSliceIds")).build();
                }
            }
        }
        return getListSliceIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList> getListSlicesMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListSlices", requestType = context.ContextOuterClass.ContextId.class, responseType = context.ContextOuterClass.SliceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList> getListSlicesMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList> getListSlicesMethod;
        if ((getListSlicesMethod = ContextServiceGrpc.getListSlicesMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListSlicesMethod = ContextServiceGrpc.getListSlicesMethod) == null) {
                    ContextServiceGrpc.getListSlicesMethod = getListSlicesMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListSlices")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ContextId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListSlices")).build();
                }
            }
        }
        return getListSlicesMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice> getGetSliceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetSlice", requestType = context.ContextOuterClass.SliceId.class, responseType = context.ContextOuterClass.Slice.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice> getGetSliceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice> getGetSliceMethod;
        if ((getGetSliceMethod = ContextServiceGrpc.getGetSliceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetSliceMethod = ContextServiceGrpc.getGetSliceMethod) == null) {
                    ContextServiceGrpc.getGetSliceMethod = getGetSliceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetSlice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Slice.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetSlice")).build();
                }
            }
        }
        return getGetSliceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getSetSliceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetSlice", requestType = context.ContextOuterClass.Slice.class, responseType = context.ContextOuterClass.SliceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getSetSliceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getSetSliceMethod;
        if ((getSetSliceMethod = ContextServiceGrpc.getSetSliceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetSliceMethod = ContextServiceGrpc.getSetSliceMethod) == null) {
                    ContextServiceGrpc.getSetSliceMethod = getSetSliceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetSlice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Slice.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetSlice")).build();
                }
            }
        }
        return getSetSliceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getUnsetSliceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "UnsetSlice", requestType = context.ContextOuterClass.Slice.class, responseType = context.ContextOuterClass.SliceId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getUnsetSliceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId> getUnsetSliceMethod;
        if ((getUnsetSliceMethod = ContextServiceGrpc.getUnsetSliceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getUnsetSliceMethod = ContextServiceGrpc.getUnsetSliceMethod) == null) {
                    ContextServiceGrpc.getUnsetSliceMethod = getUnsetSliceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "UnsetSlice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Slice.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("UnsetSlice")).build();
                }
            }
        }
        return getUnsetSliceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty> getRemoveSliceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveSlice", requestType = context.ContextOuterClass.SliceId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty> getRemoveSliceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty> getRemoveSliceMethod;
        if ((getRemoveSliceMethod = ContextServiceGrpc.getRemoveSliceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveSliceMethod = ContextServiceGrpc.getRemoveSliceMethod) == null) {
                    ContextServiceGrpc.getRemoveSliceMethod = getRemoveSliceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveSlice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveSlice")).build();
                }
            }
        }
        return getRemoveSliceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent> getGetSliceEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetSliceEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.SliceEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent> getGetSliceEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent> getGetSliceEventsMethod;
        if ((getGetSliceEventsMethod = ContextServiceGrpc.getGetSliceEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetSliceEventsMethod = ContextServiceGrpc.getGetSliceEventsMethod) == null) {
                    ContextServiceGrpc.getGetSliceEventsMethod = getGetSliceEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetSliceEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetSliceEvents")).build();
                }
            }
        }
        return getGetSliceEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList> getSelectSliceMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SelectSlice", requestType = context.ContextOuterClass.SliceFilter.class, responseType = context.ContextOuterClass.SliceList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList> getSelectSliceMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList> getSelectSliceMethod;
        if ((getSelectSliceMethod = ContextServiceGrpc.getSelectSliceMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSelectSliceMethod = ContextServiceGrpc.getSelectSliceMethod) == null) {
                    ContextServiceGrpc.getSelectSliceMethod = getSelectSliceMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SelectSlice")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceFilter.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.SliceList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SelectSlice")).build();
                }
            }
        }
        return getSelectSliceMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList> getListConnectionIdsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListConnectionIds", requestType = context.ContextOuterClass.ServiceId.class, responseType = context.ContextOuterClass.ConnectionIdList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList> getListConnectionIdsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList> getListConnectionIdsMethod;
        if ((getListConnectionIdsMethod = ContextServiceGrpc.getListConnectionIdsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListConnectionIdsMethod = ContextServiceGrpc.getListConnectionIdsMethod) == null) {
                    ContextServiceGrpc.getListConnectionIdsMethod = getListConnectionIdsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListConnectionIds")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionIdList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListConnectionIds")).build();
                }
            }
        }
        return getListConnectionIdsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList> getListConnectionsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "ListConnections", requestType = context.ContextOuterClass.ServiceId.class, responseType = context.ContextOuterClass.ConnectionList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList> getListConnectionsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList> getListConnectionsMethod;
        if ((getListConnectionsMethod = ContextServiceGrpc.getListConnectionsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getListConnectionsMethod = ContextServiceGrpc.getListConnectionsMethod) == null) {
                    ContextServiceGrpc.getListConnectionsMethod = getListConnectionsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "ListConnections")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("ListConnections")).build();
                }
            }
        }
        return getListConnectionsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection> getGetConnectionMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetConnection", requestType = context.ContextOuterClass.ConnectionId.class, responseType = context.ContextOuterClass.Connection.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection> getGetConnectionMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection> getGetConnectionMethod;
        if ((getGetConnectionMethod = ContextServiceGrpc.getGetConnectionMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetConnectionMethod = ContextServiceGrpc.getGetConnectionMethod) == null) {
                    ContextServiceGrpc.getGetConnectionMethod = getGetConnectionMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetConnection")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Connection.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetConnection")).build();
                }
            }
        }
        return getGetConnectionMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId> getSetConnectionMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetConnection", requestType = context.ContextOuterClass.Connection.class, responseType = context.ContextOuterClass.ConnectionId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId> getSetConnectionMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId> getSetConnectionMethod;
        if ((getSetConnectionMethod = ContextServiceGrpc.getSetConnectionMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetConnectionMethod = ContextServiceGrpc.getSetConnectionMethod) == null) {
                    ContextServiceGrpc.getSetConnectionMethod = getSetConnectionMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetConnection")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Connection.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetConnection")).build();
                }
            }
        }
        return getSetConnectionMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty> getRemoveConnectionMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "RemoveConnection", requestType = context.ContextOuterClass.ConnectionId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty> getRemoveConnectionMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty> getRemoveConnectionMethod;
        if ((getRemoveConnectionMethod = ContextServiceGrpc.getRemoveConnectionMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getRemoveConnectionMethod = ContextServiceGrpc.getRemoveConnectionMethod) == null) {
                    ContextServiceGrpc.getRemoveConnectionMethod = getRemoveConnectionMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "RemoveConnection")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("RemoveConnection")).build();
                }
            }
        }
        return getRemoveConnectionMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent> getGetConnectionEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetConnectionEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.ConnectionEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent> getGetConnectionEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent> getGetConnectionEventsMethod;
        if ((getGetConnectionEventsMethod = ContextServiceGrpc.getGetConnectionEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetConnectionEventsMethod = ContextServiceGrpc.getGetConnectionEventsMethod) == null) {
                    ContextServiceGrpc.getGetConnectionEventsMethod = getGetConnectionEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetConnectionEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ConnectionEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetConnectionEvents")).build();
                }
            }
        }
        return getGetConnectionEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent> getGetAllEventsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetAllEvents", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.AnyEvent.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent> getGetAllEventsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent> getGetAllEventsMethod;
        if ((getGetAllEventsMethod = ContextServiceGrpc.getGetAllEventsMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetAllEventsMethod = ContextServiceGrpc.getGetAllEventsMethod) == null) {
                    ContextServiceGrpc.getGetAllEventsMethod = getGetAllEventsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetAllEvents")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.AnyEvent.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetAllEvents")).build();
                }
            }
        }
        return getGetAllEventsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList> getGetOpticalConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetOpticalConfig", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.OpticalConfigList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList> getGetOpticalConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList> getGetOpticalConfigMethod;
        if ((getGetOpticalConfigMethod = ContextServiceGrpc.getGetOpticalConfigMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetOpticalConfigMethod = ContextServiceGrpc.getGetOpticalConfigMethod) == null) {
                    ContextServiceGrpc.getGetOpticalConfigMethod = getGetOpticalConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetOpticalConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfigList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetOpticalConfig")).build();
                }
            }
        }
        return getGetOpticalConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getSetOpticalConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetOpticalConfig", requestType = context.ContextOuterClass.OpticalConfig.class, responseType = context.ContextOuterClass.OpticalConfigId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getSetOpticalConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getSetOpticalConfigMethod;
        if ((getSetOpticalConfigMethod = ContextServiceGrpc.getSetOpticalConfigMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetOpticalConfigMethod = ContextServiceGrpc.getSetOpticalConfigMethod) == null) {
                    ContextServiceGrpc.getSetOpticalConfigMethod = getSetOpticalConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetOpticalConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfig.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfigId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetOpticalConfig")).build();
                }
            }
        }
        return getSetOpticalConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getUpdateOpticalConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "UpdateOpticalConfig", requestType = context.ContextOuterClass.OpticalConfig.class, responseType = context.ContextOuterClass.OpticalConfigId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getUpdateOpticalConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId> getUpdateOpticalConfigMethod;
        if ((getUpdateOpticalConfigMethod = ContextServiceGrpc.getUpdateOpticalConfigMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getUpdateOpticalConfigMethod = ContextServiceGrpc.getUpdateOpticalConfigMethod) == null) {
                    ContextServiceGrpc.getUpdateOpticalConfigMethod = getUpdateOpticalConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "UpdateOpticalConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfig.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfigId.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("UpdateOpticalConfig")).build();
                }
            }
        }
        return getUpdateOpticalConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig> getSelectOpticalConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SelectOpticalConfig", requestType = context.ContextOuterClass.OpticalConfigId.class, responseType = context.ContextOuterClass.OpticalConfig.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig> getSelectOpticalConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig> getSelectOpticalConfigMethod;
        if ((getSelectOpticalConfigMethod = ContextServiceGrpc.getSelectOpticalConfigMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSelectOpticalConfigMethod = ContextServiceGrpc.getSelectOpticalConfigMethod) == null) {
                    ContextServiceGrpc.getSelectOpticalConfigMethod = getSelectOpticalConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SelectOpticalConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfigId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfig.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SelectOpticalConfig")).build();
                }
            }
        }
        return getSelectOpticalConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty> getDeleteOpticalConfigMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteOpticalConfig", requestType = context.ContextOuterClass.OpticalConfigId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty> getDeleteOpticalConfigMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty> getDeleteOpticalConfigMethod;
        if ((getDeleteOpticalConfigMethod = ContextServiceGrpc.getDeleteOpticalConfigMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getDeleteOpticalConfigMethod = ContextServiceGrpc.getDeleteOpticalConfigMethod) == null) {
                    ContextServiceGrpc.getDeleteOpticalConfigMethod = getDeleteOpticalConfigMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteOpticalConfig")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfigId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("DeleteOpticalConfig")).build();
                }
            }
        }
        return getDeleteOpticalConfigMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty> getDeleteOpticalChannelMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteOpticalChannel", requestType = context.ContextOuterClass.OpticalConfig.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty> getDeleteOpticalChannelMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty> getDeleteOpticalChannelMethod;
        if ((getDeleteOpticalChannelMethod = ContextServiceGrpc.getDeleteOpticalChannelMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getDeleteOpticalChannelMethod = ContextServiceGrpc.getDeleteOpticalChannelMethod) == null) {
                    ContextServiceGrpc.getDeleteOpticalChannelMethod = getDeleteOpticalChannelMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteOpticalChannel")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalConfig.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("DeleteOpticalChannel")).build();
                }
            }
        }
        return getDeleteOpticalChannelMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty> getSetOpticalLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetOpticalLink", requestType = context.ContextOuterClass.OpticalLink.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty> getSetOpticalLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty> getSetOpticalLinkMethod;
        if ((getSetOpticalLinkMethod = ContextServiceGrpc.getSetOpticalLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSetOpticalLinkMethod = ContextServiceGrpc.getSetOpticalLinkMethod) == null) {
                    ContextServiceGrpc.getSetOpticalLinkMethod = getSetOpticalLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetOpticalLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalLink.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SetOpticalLink")).build();
                }
            }
        }
        return getSetOpticalLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink> getGetOpticalLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetOpticalLink", requestType = context.ContextOuterClass.LinkId.class, responseType = context.ContextOuterClass.OpticalLink.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink> getGetOpticalLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink> getGetOpticalLinkMethod;
        if ((getGetOpticalLinkMethod = ContextServiceGrpc.getGetOpticalLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetOpticalLinkMethod = ContextServiceGrpc.getGetOpticalLinkMethod) == null) {
                    ContextServiceGrpc.getGetOpticalLinkMethod = getGetOpticalLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetOpticalLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalLink.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetOpticalLink")).build();
                }
            }
        }
        return getGetOpticalLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getDeleteOpticalLinkMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteOpticalLink", requestType = context.ContextOuterClass.LinkId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getDeleteOpticalLinkMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty> getDeleteOpticalLinkMethod;
        if ((getDeleteOpticalLinkMethod = ContextServiceGrpc.getDeleteOpticalLinkMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getDeleteOpticalLinkMethod = ContextServiceGrpc.getDeleteOpticalLinkMethod) == null) {
                    ContextServiceGrpc.getDeleteOpticalLinkMethod = getDeleteOpticalLinkMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteOpticalLink")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.LinkId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("DeleteOpticalLink")).build();
                }
            }
        }
        return getDeleteOpticalLinkMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList> getGetOpticalLinkListMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetOpticalLinkList", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.OpticalLinkList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList> getGetOpticalLinkListMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList> getGetOpticalLinkListMethod;
        if ((getGetOpticalLinkListMethod = ContextServiceGrpc.getGetOpticalLinkListMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetOpticalLinkListMethod = ContextServiceGrpc.getGetOpticalLinkListMethod) == null) {
                    ContextServiceGrpc.getGetOpticalLinkListMethod = getGetOpticalLinkListMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetOpticalLinkList")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalLinkList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetOpticalLinkList")).build();
                }
            }
        }
        return getGetOpticalLinkListMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList> getGetOpticalBandMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetOpticalBand", requestType = context.ContextOuterClass.Empty.class, responseType = context.ContextOuterClass.OpticalBandList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList> getGetOpticalBandMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList> getGetOpticalBandMethod;
        if ((getGetOpticalBandMethod = ContextServiceGrpc.getGetOpticalBandMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getGetOpticalBandMethod = ContextServiceGrpc.getGetOpticalBandMethod) == null) {
                    ContextServiceGrpc.getGetOpticalBandMethod = getGetOpticalBandMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetOpticalBand")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalBandList.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("GetOpticalBand")).build();
                }
            }
        }
        return getGetOpticalBandMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand> getSelectOpticalBandMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SelectOpticalBand", requestType = context.ContextOuterClass.OpticalBandId.class, responseType = context.ContextOuterClass.OpticalBand.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand> getSelectOpticalBandMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand> getSelectOpticalBandMethod;
        if ((getSelectOpticalBandMethod = ContextServiceGrpc.getSelectOpticalBandMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getSelectOpticalBandMethod = ContextServiceGrpc.getSelectOpticalBandMethod) == null) {
                    ContextServiceGrpc.getSelectOpticalBandMethod = getSelectOpticalBandMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SelectOpticalBand")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalBandId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.OpticalBand.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("SelectOpticalBand")).build();
                }
            }
        }
        return getSelectOpticalBandMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty> getDeleteServiceConfigRuleMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteServiceConfigRule", requestType = context.ContextOuterClass.ServiceConfigRule.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty> getDeleteServiceConfigRuleMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty> getDeleteServiceConfigRuleMethod;
        if ((getDeleteServiceConfigRuleMethod = ContextServiceGrpc.getDeleteServiceConfigRuleMethod) == null) {
            synchronized (ContextServiceGrpc.class) {
                if ((getDeleteServiceConfigRuleMethod = ContextServiceGrpc.getDeleteServiceConfigRuleMethod) == null) {
                    ContextServiceGrpc.getDeleteServiceConfigRuleMethod = getDeleteServiceConfigRuleMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteServiceConfigRule")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.ServiceConfigRule.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new ContextServiceMethodDescriptorSupplier("DeleteServiceConfigRule")).build();
                }
            }
        }
        return getDeleteServiceConfigRuleMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static ContextServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextServiceStub>() {

            @java.lang.Override
            public ContextServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextServiceStub(channel, callOptions);
            }
        };
        return ContextServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static ContextServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextServiceBlockingStub>() {

            @java.lang.Override
            public ContextServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextServiceBlockingStub(channel, callOptions);
            }
        };
        return ContextServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static ContextServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<ContextServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<ContextServiceFutureStub>() {

            @java.lang.Override
            public ContextServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new ContextServiceFutureStub(channel, callOptions);
            }
        };
        return ContextServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void listContextIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListContextIdsMethod(), responseObserver);
        }

        /**
         */
        default void listContexts(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListContextsMethod(), responseObserver);
        }

        /**
         */
        default void getContext(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Context> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetContextMethod(), responseObserver);
        }

        /**
         */
        default void setContext(context.ContextOuterClass.Context request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetContextMethod(), responseObserver);
        }

        /**
         */
        default void removeContext(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveContextMethod(), responseObserver);
        }

        /**
         */
        default void getContextEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetContextEventsMethod(), responseObserver);
        }

        /**
         */
        default void listTopologyIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListTopologyIdsMethod(), responseObserver);
        }

        /**
         */
        default void listTopologies(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListTopologiesMethod(), responseObserver);
        }

        /**
         */
        default void getTopology(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Topology> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetTopologyMethod(), responseObserver);
        }

        /**
         */
        default void getTopologyDetails(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyDetails> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetTopologyDetailsMethod(), responseObserver);
        }

        /**
         */
        default void setTopology(context.ContextOuterClass.Topology request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetTopologyMethod(), responseObserver);
        }

        /**
         */
        default void removeTopology(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveTopologyMethod(), responseObserver);
        }

        /**
         */
        default void getTopologyEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetTopologyEventsMethod(), responseObserver);
        }

        /**
         */
        default void listDeviceIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListDeviceIdsMethod(), responseObserver);
        }

        /**
         */
        default void listDevices(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListDevicesMethod(), responseObserver);
        }

        /**
         */
        default void getDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Device> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetDeviceMethod(), responseObserver);
        }

        /**
         */
        default void setDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetDeviceMethod(), responseObserver);
        }

        /**
         */
        default void removeDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveDeviceMethod(), responseObserver);
        }

        /**
         */
        default void getDeviceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetDeviceEventsMethod(), responseObserver);
        }

        /**
         */
        default void selectDevice(context.ContextOuterClass.DeviceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSelectDeviceMethod(), responseObserver);
        }

        /**
         */
        default void listEndPointNames(context.ContextOuterClass.EndPointIdList request, io.grpc.stub.StreamObserver<context.ContextOuterClass.EndPointNameList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListEndPointNamesMethod(), responseObserver);
        }

        /**
         */
        default void listLinkIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListLinkIdsMethod(), responseObserver);
        }

        /**
         */
        default void listLinks(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListLinksMethod(), responseObserver);
        }

        /**
         */
        default void getLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Link> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetLinkMethod(), responseObserver);
        }

        /**
         */
        default void setLink(context.ContextOuterClass.Link request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetLinkMethod(), responseObserver);
        }

        /**
         */
        default void removeLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveLinkMethod(), responseObserver);
        }

        /**
         */
        default void getLinkEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetLinkEventsMethod(), responseObserver);
        }

        /**
         */
        default void listServiceIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListServiceIdsMethod(), responseObserver);
        }

        /**
         */
        default void listServices(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListServicesMethod(), responseObserver);
        }

        /**
         */
        default void getService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Service> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetServiceMethod(), responseObserver);
        }

        /**
         */
        default void setService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetServiceMethod(), responseObserver);
        }

        /**
         */
        default void unsetService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUnsetServiceMethod(), responseObserver);
        }

        /**
         */
        default void removeService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveServiceMethod(), responseObserver);
        }

        /**
         */
        default void getServiceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetServiceEventsMethod(), responseObserver);
        }

        /**
         */
        default void selectService(context.ContextOuterClass.ServiceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSelectServiceMethod(), responseObserver);
        }

        /**
         */
        default void listSliceIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListSliceIdsMethod(), responseObserver);
        }

        /**
         */
        default void listSlices(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListSlicesMethod(), responseObserver);
        }

        /**
         */
        default void getSlice(context.ContextOuterClass.SliceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Slice> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetSliceMethod(), responseObserver);
        }

        /**
         */
        default void setSlice(context.ContextOuterClass.Slice request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetSliceMethod(), responseObserver);
        }

        /**
         */
        default void unsetSlice(context.ContextOuterClass.Slice request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUnsetSliceMethod(), responseObserver);
        }

        /**
         */
        default void removeSlice(context.ContextOuterClass.SliceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveSliceMethod(), responseObserver);
        }

        /**
         */
        default void getSliceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetSliceEventsMethod(), responseObserver);
        }

        /**
         */
        default void selectSlice(context.ContextOuterClass.SliceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSelectSliceMethod(), responseObserver);
        }

        /**
         */
        default void listConnectionIds(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionIdList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListConnectionIdsMethod(), responseObserver);
        }

        /**
         */
        default void listConnections(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getListConnectionsMethod(), responseObserver);
        }

        /**
         */
        default void getConnection(context.ContextOuterClass.ConnectionId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Connection> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetConnectionMethod(), responseObserver);
        }

        /**
         */
        default void setConnection(context.ContextOuterClass.Connection request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetConnectionMethod(), responseObserver);
        }

        /**
         */
        default void removeConnection(context.ContextOuterClass.ConnectionId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRemoveConnectionMethod(), responseObserver);
        }

        /**
         */
        default void getConnectionEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetConnectionEventsMethod(), responseObserver);
        }

        /**
         */
        default void getAllEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.AnyEvent> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetAllEventsMethod(), responseObserver);
        }

        /**
         * <pre>
         * ------------------------------ Experimental -----------------------------
         * </pre>
         */
        default void getOpticalConfig(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetOpticalConfigMethod(), responseObserver);
        }

        /**
         */
        default void setOpticalConfig(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetOpticalConfigMethod(), responseObserver);
        }

        /**
         */
        default void updateOpticalConfig(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getUpdateOpticalConfigMethod(), responseObserver);
        }

        /**
         */
        default void selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfig> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSelectOpticalConfigMethod(), responseObserver);
        }

        /**
         */
        default void deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteOpticalConfigMethod(), responseObserver);
        }

        /**
         */
        default void deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteOpticalChannelMethod(), responseObserver);
        }

        /**
         */
        default void setOpticalLink(context.ContextOuterClass.OpticalLink request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetOpticalLinkMethod(), responseObserver);
        }

        /**
         */
        default void getOpticalLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLink> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetOpticalLinkMethod(), responseObserver);
        }

        /**
         */
        default void deleteOpticalLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteOpticalLinkMethod(), responseObserver);
        }

        /**
         */
        default void getOpticalLinkList(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLinkList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetOpticalLinkListMethod(), responseObserver);
        }

        /**
         */
        default void getOpticalBand(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBandList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetOpticalBandMethod(), responseObserver);
        }

        /**
         */
        default void selectOpticalBand(context.ContextOuterClass.OpticalBandId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBand> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSelectOpticalBandMethod(), responseObserver);
        }

        /**
         */
        default void deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteServiceConfigRuleMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service ContextService.
     */
    public static abstract class ContextServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return ContextServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service ContextService.
     */
    public static class ContextServiceStub extends io.grpc.stub.AbstractAsyncStub<ContextServiceStub> {

        private ContextServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextServiceStub(channel, callOptions);
        }

        /**
         */
        public void listContextIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListContextIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listContexts(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListContextsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getContext(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Context> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetContextMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setContext(context.ContextOuterClass.Context request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetContextMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeContext(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveContextMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getContextEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetContextEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listTopologyIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListTopologyIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listTopologies(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListTopologiesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getTopology(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Topology> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetTopologyMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getTopologyDetails(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyDetails> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetTopologyDetailsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setTopology(context.ContextOuterClass.Topology request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetTopologyMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeTopology(context.ContextOuterClass.TopologyId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveTopologyMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getTopologyEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetTopologyEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listDeviceIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListDeviceIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listDevices(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListDevicesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Device> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setDevice(context.ContextOuterClass.Device request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeDevice(context.ContextOuterClass.DeviceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getDeviceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetDeviceEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void selectDevice(context.ContextOuterClass.DeviceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSelectDeviceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listEndPointNames(context.ContextOuterClass.EndPointIdList request, io.grpc.stub.StreamObserver<context.ContextOuterClass.EndPointNameList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListEndPointNamesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listLinkIds(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListLinkIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listLinks(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListLinksMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Link> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setLink(context.ContextOuterClass.Link request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getLinkEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetLinkEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listServiceIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListServiceIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listServices(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListServicesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Service> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void unsetService(context.ContextOuterClass.Service request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getUnsetServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeService(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getServiceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetServiceEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void selectService(context.ContextOuterClass.ServiceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSelectServiceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listSliceIds(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListSliceIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listSlices(context.ContextOuterClass.ContextId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListSlicesMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getSlice(context.ContextOuterClass.SliceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Slice> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetSliceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setSlice(context.ContextOuterClass.Slice request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetSliceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void unsetSlice(context.ContextOuterClass.Slice request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getUnsetSliceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeSlice(context.ContextOuterClass.SliceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveSliceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getSliceEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetSliceEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void selectSlice(context.ContextOuterClass.SliceFilter request, io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSelectSliceMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listConnectionIds(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionIdList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListConnectionIdsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void listConnections(context.ContextOuterClass.ServiceId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getListConnectionsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getConnection(context.ContextOuterClass.ConnectionId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Connection> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetConnectionMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setConnection(context.ContextOuterClass.Connection request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetConnectionMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void removeConnection(context.ContextOuterClass.ConnectionId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getRemoveConnectionMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getConnectionEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetConnectionEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getAllEvents(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.AnyEvent> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetAllEventsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         * <pre>
         * ------------------------------ Experimental -----------------------------
         * </pre>
         */
        public void getOpticalConfig(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetOpticalConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setOpticalConfig(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetOpticalConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void updateOpticalConfig(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getUpdateOpticalConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfig> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSelectOpticalConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteOpticalConfigMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteOpticalChannelMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setOpticalLink(context.ContextOuterClass.OpticalLink request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetOpticalLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getOpticalLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLink> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetOpticalLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteOpticalLink(context.ContextOuterClass.LinkId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteOpticalLinkMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getOpticalLinkList(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLinkList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetOpticalLinkListMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getOpticalBand(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBandList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetOpticalBandMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void selectOpticalBand(context.ContextOuterClass.OpticalBandId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBand> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSelectOpticalBandMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteServiceConfigRuleMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service ContextService.
     */
    public static class ContextServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<ContextServiceBlockingStub> {

        private ContextServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public context.ContextOuterClass.ContextIdList listContextIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListContextIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ContextList listContexts(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListContextsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Context getContext(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetContextMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ContextId setContext(context.ContextOuterClass.Context request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetContextMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeContext(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveContextMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetContextEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.TopologyIdList listTopologyIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListTopologyIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.TopologyList listTopologies(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListTopologiesMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Topology getTopology(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetTopologyMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.TopologyDetails getTopologyDetails(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetTopologyDetailsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.TopologyId setTopology(context.ContextOuterClass.Topology request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetTopologyMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeTopology(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveTopologyMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetTopologyEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceIdList listDeviceIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListDeviceIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceList listDevices(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListDevicesMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Device getDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceId setDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetDeviceEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.DeviceList selectDevice(context.ContextOuterClass.DeviceFilter request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSelectDeviceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.EndPointNameList listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListEndPointNamesMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.LinkIdList listLinkIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListLinkIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.LinkList listLinks(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListLinksMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Link getLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.LinkId setLink(context.ContextOuterClass.Link request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetLinkEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceIdList listServiceIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListServiceIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceList listServices(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListServicesMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Service getService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceId setService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceId unsetService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getUnsetServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetServiceEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ServiceList selectService(context.ContextOuterClass.ServiceFilter request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSelectServiceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.SliceIdList listSliceIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListSliceIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.SliceList listSlices(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListSlicesMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Slice getSlice(context.ContextOuterClass.SliceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetSliceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.SliceId setSlice(context.ContextOuterClass.Slice request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetSliceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.SliceId unsetSlice(context.ContextOuterClass.Slice request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getUnsetSliceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeSlice(context.ContextOuterClass.SliceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveSliceMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetSliceEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.SliceList selectSlice(context.ContextOuterClass.SliceFilter request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSelectSliceMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ConnectionIdList listConnectionIds(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListConnectionIdsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ConnectionList listConnections(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getListConnectionsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Connection getConnection(context.ContextOuterClass.ConnectionId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetConnectionMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.ConnectionId setConnection(context.ContextOuterClass.Connection request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetConnectionMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty removeConnection(context.ContextOuterClass.ConnectionId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getRemoveConnectionMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetConnectionEventsMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetAllEventsMethod(), getCallOptions(), request);
        }

        /**
         * <pre>
         * ------------------------------ Experimental -----------------------------
         * </pre>
         */
        public context.ContextOuterClass.OpticalConfigList getOpticalConfig(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetOpticalConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalConfigId setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetOpticalConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalConfigId updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getUpdateOpticalConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalConfig selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSelectOpticalConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteOpticalConfigMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteOpticalChannelMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty setOpticalLink(context.ContextOuterClass.OpticalLink request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetOpticalLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalLink getOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetOpticalLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteOpticalLinkMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalLinkList getOpticalLinkList(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetOpticalLinkListMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalBandList getOpticalBand(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetOpticalBandMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.OpticalBand selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSelectOpticalBandMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteServiceConfigRuleMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service ContextService.
     */
    public static class ContextServiceFutureStub extends io.grpc.stub.AbstractFutureStub<ContextServiceFutureStub> {

        private ContextServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected ContextServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new ContextServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListContextIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListContextsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetContextMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetContextMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveContextMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListTopologyIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListTopologiesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetTopologyMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetTopologyDetailsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetTopologyMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveTopologyMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListDeviceIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListDevicesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSelectDeviceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListEndPointNamesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListLinkIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListLinksMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListServiceIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListServicesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getUnsetServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSelectServiceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListSliceIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListSlicesMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetSliceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetSliceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getUnsetSliceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveSliceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSelectSliceMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListConnectionIdsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getListConnectionsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetConnectionMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetConnectionMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getRemoveConnectionMethod(), getCallOptions()), request);
        }

        /**
         * <pre>
         * ------------------------------ Experimental -----------------------------
         * </pre>
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetOpticalConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetOpticalConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getUpdateOpticalConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSelectOpticalConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteOpticalConfigMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteOpticalChannelMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetOpticalLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetOpticalLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteOpticalLinkMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetOpticalLinkListMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetOpticalBandMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSelectOpticalBandMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteServiceConfigRuleMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_LIST_CONTEXT_IDS = 0;

    private static final int METHODID_LIST_CONTEXTS = 1;

    private static final int METHODID_GET_CONTEXT = 2;

    private static final int METHODID_SET_CONTEXT = 3;

    private static final int METHODID_REMOVE_CONTEXT = 4;

    private static final int METHODID_GET_CONTEXT_EVENTS = 5;

    private static final int METHODID_LIST_TOPOLOGY_IDS = 6;

    private static final int METHODID_LIST_TOPOLOGIES = 7;

    private static final int METHODID_GET_TOPOLOGY = 8;

    private static final int METHODID_GET_TOPOLOGY_DETAILS = 9;

    private static final int METHODID_SET_TOPOLOGY = 10;

    private static final int METHODID_REMOVE_TOPOLOGY = 11;

    private static final int METHODID_GET_TOPOLOGY_EVENTS = 12;

    private static final int METHODID_LIST_DEVICE_IDS = 13;

    private static final int METHODID_LIST_DEVICES = 14;

    private static final int METHODID_GET_DEVICE = 15;

    private static final int METHODID_SET_DEVICE = 16;

    private static final int METHODID_REMOVE_DEVICE = 17;

    private static final int METHODID_GET_DEVICE_EVENTS = 18;

    private static final int METHODID_SELECT_DEVICE = 19;

    private static final int METHODID_LIST_END_POINT_NAMES = 20;

    private static final int METHODID_LIST_LINK_IDS = 21;

    private static final int METHODID_LIST_LINKS = 22;

    private static final int METHODID_GET_LINK = 23;

    private static final int METHODID_SET_LINK = 24;

    private static final int METHODID_REMOVE_LINK = 25;

    private static final int METHODID_GET_LINK_EVENTS = 26;

    private static final int METHODID_LIST_SERVICE_IDS = 27;

    private static final int METHODID_LIST_SERVICES = 28;

    private static final int METHODID_GET_SERVICE = 29;

    private static final int METHODID_SET_SERVICE = 30;

    private static final int METHODID_UNSET_SERVICE = 31;

    private static final int METHODID_REMOVE_SERVICE = 32;

    private static final int METHODID_GET_SERVICE_EVENTS = 33;

    private static final int METHODID_SELECT_SERVICE = 34;

    private static final int METHODID_LIST_SLICE_IDS = 35;

    private static final int METHODID_LIST_SLICES = 36;

    private static final int METHODID_GET_SLICE = 37;

    private static final int METHODID_SET_SLICE = 38;

    private static final int METHODID_UNSET_SLICE = 39;

    private static final int METHODID_REMOVE_SLICE = 40;

    private static final int METHODID_GET_SLICE_EVENTS = 41;

    private static final int METHODID_SELECT_SLICE = 42;

    private static final int METHODID_LIST_CONNECTION_IDS = 43;

    private static final int METHODID_LIST_CONNECTIONS = 44;

    private static final int METHODID_GET_CONNECTION = 45;

    private static final int METHODID_SET_CONNECTION = 46;

    private static final int METHODID_REMOVE_CONNECTION = 47;

    private static final int METHODID_GET_CONNECTION_EVENTS = 48;

    private static final int METHODID_GET_ALL_EVENTS = 49;

    private static final int METHODID_GET_OPTICAL_CONFIG = 50;

    private static final int METHODID_SET_OPTICAL_CONFIG = 51;

    private static final int METHODID_UPDATE_OPTICAL_CONFIG = 52;

    private static final int METHODID_SELECT_OPTICAL_CONFIG = 53;

    private static final int METHODID_DELETE_OPTICAL_CONFIG = 54;

    private static final int METHODID_DELETE_OPTICAL_CHANNEL = 55;

    private static final int METHODID_SET_OPTICAL_LINK = 56;

    private static final int METHODID_GET_OPTICAL_LINK = 57;

    private static final int METHODID_DELETE_OPTICAL_LINK = 58;

    private static final int METHODID_GET_OPTICAL_LINK_LIST = 59;

    private static final int METHODID_GET_OPTICAL_BAND = 60;

    private static final int METHODID_SELECT_OPTICAL_BAND = 61;

    private static final int METHODID_DELETE_SERVICE_CONFIG_RULE = 62;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final AsyncService serviceImpl;

        private final int methodId;

        MethodHandlers(AsyncService serviceImpl, int methodId) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_LIST_CONTEXT_IDS:
                    serviceImpl.listContextIds((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextIdList>) responseObserver);
                    break;
                case METHODID_LIST_CONTEXTS:
                    serviceImpl.listContexts((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextList>) responseObserver);
                    break;
                case METHODID_GET_CONTEXT:
                    serviceImpl.getContext((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Context>) responseObserver);
                    break;
                case METHODID_SET_CONTEXT:
                    serviceImpl.setContext((context.ContextOuterClass.Context) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextId>) responseObserver);
                    break;
                case METHODID_REMOVE_CONTEXT:
                    serviceImpl.removeContext((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_CONTEXT_EVENTS:
                    serviceImpl.getContextEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextEvent>) responseObserver);
                    break;
                case METHODID_LIST_TOPOLOGY_IDS:
                    serviceImpl.listTopologyIds((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyIdList>) responseObserver);
                    break;
                case METHODID_LIST_TOPOLOGIES:
                    serviceImpl.listTopologies((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyList>) responseObserver);
                    break;
                case METHODID_GET_TOPOLOGY:
                    serviceImpl.getTopology((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Topology>) responseObserver);
                    break;
                case METHODID_GET_TOPOLOGY_DETAILS:
                    serviceImpl.getTopologyDetails((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyDetails>) responseObserver);
                    break;
                case METHODID_SET_TOPOLOGY:
                    serviceImpl.setTopology((context.ContextOuterClass.Topology) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyId>) responseObserver);
                    break;
                case METHODID_REMOVE_TOPOLOGY:
                    serviceImpl.removeTopology((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_TOPOLOGY_EVENTS:
                    serviceImpl.getTopologyEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyEvent>) responseObserver);
                    break;
                case METHODID_LIST_DEVICE_IDS:
                    serviceImpl.listDeviceIds((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceIdList>) responseObserver);
                    break;
                case METHODID_LIST_DEVICES:
                    serviceImpl.listDevices((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList>) responseObserver);
                    break;
                case METHODID_GET_DEVICE:
                    serviceImpl.getDevice((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Device>) responseObserver);
                    break;
                case METHODID_SET_DEVICE:
                    serviceImpl.setDevice((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver);
                    break;
                case METHODID_REMOVE_DEVICE:
                    serviceImpl.removeDevice((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_DEVICE_EVENTS:
                    serviceImpl.getDeviceEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceEvent>) responseObserver);
                    break;
                case METHODID_SELECT_DEVICE:
                    serviceImpl.selectDevice((context.ContextOuterClass.DeviceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList>) responseObserver);
                    break;
                case METHODID_LIST_END_POINT_NAMES:
                    serviceImpl.listEndPointNames((context.ContextOuterClass.EndPointIdList) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.EndPointNameList>) responseObserver);
                    break;
                case METHODID_LIST_LINK_IDS:
                    serviceImpl.listLinkIds((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkIdList>) responseObserver);
                    break;
                case METHODID_LIST_LINKS:
                    serviceImpl.listLinks((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkList>) responseObserver);
                    break;
                case METHODID_GET_LINK:
                    serviceImpl.getLink((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Link>) responseObserver);
                    break;
                case METHODID_SET_LINK:
                    serviceImpl.setLink((context.ContextOuterClass.Link) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkId>) responseObserver);
                    break;
                case METHODID_REMOVE_LINK:
                    serviceImpl.removeLink((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_LINK_EVENTS:
                    serviceImpl.getLinkEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkEvent>) responseObserver);
                    break;
                case METHODID_LIST_SERVICE_IDS:
                    serviceImpl.listServiceIds((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceIdList>) responseObserver);
                    break;
                case METHODID_LIST_SERVICES:
                    serviceImpl.listServices((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList>) responseObserver);
                    break;
                case METHODID_GET_SERVICE:
                    serviceImpl.getService((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Service>) responseObserver);
                    break;
                case METHODID_SET_SERVICE:
                    serviceImpl.setService((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver);
                    break;
                case METHODID_UNSET_SERVICE:
                    serviceImpl.unsetService((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver);
                    break;
                case METHODID_REMOVE_SERVICE:
                    serviceImpl.removeService((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_SERVICE_EVENTS:
                    serviceImpl.getServiceEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceEvent>) responseObserver);
                    break;
                case METHODID_SELECT_SERVICE:
                    serviceImpl.selectService((context.ContextOuterClass.ServiceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList>) responseObserver);
                    break;
                case METHODID_LIST_SLICE_IDS:
                    serviceImpl.listSliceIds((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceIdList>) responseObserver);
                    break;
                case METHODID_LIST_SLICES:
                    serviceImpl.listSlices((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList>) responseObserver);
                    break;
                case METHODID_GET_SLICE:
                    serviceImpl.getSlice((context.ContextOuterClass.SliceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Slice>) responseObserver);
                    break;
                case METHODID_SET_SLICE:
                    serviceImpl.setSlice((context.ContextOuterClass.Slice) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId>) responseObserver);
                    break;
                case METHODID_UNSET_SLICE:
                    serviceImpl.unsetSlice((context.ContextOuterClass.Slice) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId>) responseObserver);
                    break;
                case METHODID_REMOVE_SLICE:
                    serviceImpl.removeSlice((context.ContextOuterClass.SliceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_SLICE_EVENTS:
                    serviceImpl.getSliceEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceEvent>) responseObserver);
                    break;
                case METHODID_SELECT_SLICE:
                    serviceImpl.selectSlice((context.ContextOuterClass.SliceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList>) responseObserver);
                    break;
                case METHODID_LIST_CONNECTION_IDS:
                    serviceImpl.listConnectionIds((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionIdList>) responseObserver);
                    break;
                case METHODID_LIST_CONNECTIONS:
                    serviceImpl.listConnections((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionList>) responseObserver);
                    break;
                case METHODID_GET_CONNECTION:
                    serviceImpl.getConnection((context.ContextOuterClass.ConnectionId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Connection>) responseObserver);
                    break;
                case METHODID_SET_CONNECTION:
                    serviceImpl.setConnection((context.ContextOuterClass.Connection) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionId>) responseObserver);
                    break;
                case METHODID_REMOVE_CONNECTION:
                    serviceImpl.removeConnection((context.ContextOuterClass.ConnectionId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_CONNECTION_EVENTS:
                    serviceImpl.getConnectionEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionEvent>) responseObserver);
                    break;
                case METHODID_GET_ALL_EVENTS:
                    serviceImpl.getAllEvents((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.AnyEvent>) responseObserver);
                    break;
                case METHODID_GET_OPTICAL_CONFIG:
                    serviceImpl.getOpticalConfig((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigList>) responseObserver);
                    break;
                case METHODID_SET_OPTICAL_CONFIG:
                    serviceImpl.setOpticalConfig((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId>) responseObserver);
                    break;
                case METHODID_UPDATE_OPTICAL_CONFIG:
                    serviceImpl.updateOpticalConfig((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId>) responseObserver);
                    break;
                case METHODID_SELECT_OPTICAL_CONFIG:
                    serviceImpl.selectOpticalConfig((context.ContextOuterClass.OpticalConfigId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfig>) responseObserver);
                    break;
                case METHODID_DELETE_OPTICAL_CONFIG:
                    serviceImpl.deleteOpticalConfig((context.ContextOuterClass.OpticalConfigId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_DELETE_OPTICAL_CHANNEL:
                    serviceImpl.deleteOpticalChannel((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_SET_OPTICAL_LINK:
                    serviceImpl.setOpticalLink((context.ContextOuterClass.OpticalLink) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_OPTICAL_LINK:
                    serviceImpl.getOpticalLink((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLink>) responseObserver);
                    break;
                case METHODID_DELETE_OPTICAL_LINK:
                    serviceImpl.deleteOpticalLink((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_OPTICAL_LINK_LIST:
                    serviceImpl.getOpticalLinkList((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLinkList>) responseObserver);
                    break;
                case METHODID_GET_OPTICAL_BAND:
                    serviceImpl.getOpticalBand((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBandList>) responseObserver);
                    break;
                case METHODID_SELECT_OPTICAL_BAND:
                    serviceImpl.selectOpticalBand((context.ContextOuterClass.OpticalBandId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBand>) responseObserver);
                    break;
                case METHODID_DELETE_SERVICE_CONFIG_RULE:
                    serviceImpl.deleteServiceConfigRule((context.ContextOuterClass.ServiceConfigRule) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                default:
                    throw new AssertionError();
            }
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public io.grpc.stub.StreamObserver<Req> invoke(io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                default:
                    throw new AssertionError();
            }
        }
    }

    public static io.grpc.ServerServiceDefinition bindService(AsyncService service) {
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getListContextIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList>(service, METHODID_LIST_CONTEXT_IDS))).addMethod(getListContextsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList>(service, METHODID_LIST_CONTEXTS))).addMethod(getGetContextMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context>(service, METHODID_GET_CONTEXT))).addMethod(getSetContextMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId>(service, METHODID_SET_CONTEXT))).addMethod(getRemoveContextMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_CONTEXT))).addMethod(getGetContextEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent>(service, METHODID_GET_CONTEXT_EVENTS))).addMethod(getListTopologyIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList>(service, METHODID_LIST_TOPOLOGY_IDS))).addMethod(getListTopologiesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList>(service, METHODID_LIST_TOPOLOGIES))).addMethod(getGetTopologyMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology>(service, METHODID_GET_TOPOLOGY))).addMethod(getGetTopologyDetailsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails>(service, METHODID_GET_TOPOLOGY_DETAILS))).addMethod(getSetTopologyMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId>(service, METHODID_SET_TOPOLOGY))).addMethod(getRemoveTopologyMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_TOPOLOGY))).addMethod(getGetTopologyEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent>(service, METHODID_GET_TOPOLOGY_EVENTS))).addMethod(getListDeviceIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList>(service, METHODID_LIST_DEVICE_IDS))).addMethod(getListDevicesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList>(service, METHODID_LIST_DEVICES))).addMethod(getGetDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device>(service, METHODID_GET_DEVICE))).addMethod(getSetDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(service, METHODID_SET_DEVICE))).addMethod(getRemoveDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_DEVICE))).addMethod(getGetDeviceEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent>(service, METHODID_GET_DEVICE_EVENTS))).addMethod(getSelectDeviceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList>(service, METHODID_SELECT_DEVICE))).addMethod(getListEndPointNamesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList>(service, METHODID_LIST_END_POINT_NAMES))).addMethod(getListLinkIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList>(service, METHODID_LIST_LINK_IDS))).addMethod(getListLinksMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList>(service, METHODID_LIST_LINKS))).addMethod(getGetLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link>(service, METHODID_GET_LINK))).addMethod(getSetLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId>(service, METHODID_SET_LINK))).addMethod(getRemoveLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_LINK))).addMethod(getGetLinkEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent>(service, METHODID_GET_LINK_EVENTS))).addMethod(getListServiceIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList>(service, METHODID_LIST_SERVICE_IDS))).addMethod(getListServicesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList>(service, METHODID_LIST_SERVICES))).addMethod(getGetServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service>(service, METHODID_GET_SERVICE))).addMethod(getSetServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(service, METHODID_SET_SERVICE))).addMethod(getUnsetServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(service, METHODID_UNSET_SERVICE))).addMethod(getRemoveServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_SERVICE))).addMethod(getGetServiceEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent>(service, METHODID_GET_SERVICE_EVENTS))).addMethod(getSelectServiceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList>(service, METHODID_SELECT_SERVICE))).addMethod(getListSliceIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList>(service, METHODID_LIST_SLICE_IDS))).addMethod(getListSlicesMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList>(service, METHODID_LIST_SLICES))).addMethod(getGetSliceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice>(service, METHODID_GET_SLICE))).addMethod(getSetSliceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>(service, METHODID_SET_SLICE))).addMethod(getUnsetSliceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>(service, METHODID_UNSET_SLICE))).addMethod(getRemoveSliceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_SLICE))).addMethod(getGetSliceEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent>(service, METHODID_GET_SLICE_EVENTS))).addMethod(getSelectSliceMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList>(service, METHODID_SELECT_SLICE))).addMethod(getListConnectionIdsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList>(service, METHODID_LIST_CONNECTION_IDS))).addMethod(getListConnectionsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList>(service, METHODID_LIST_CONNECTIONS))).addMethod(getGetConnectionMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection>(service, METHODID_GET_CONNECTION))).addMethod(getSetConnectionMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId>(service, METHODID_SET_CONNECTION))).addMethod(getRemoveConnectionMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty>(service, METHODID_REMOVE_CONNECTION))).addMethod(getGetConnectionEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent>(service, METHODID_GET_CONNECTION_EVENTS))).addMethod(getGetAllEventsMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent>(service, METHODID_GET_ALL_EVENTS))).addMethod(getGetOpticalConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList>(service, METHODID_GET_OPTICAL_CONFIG))).addMethod(getSetOpticalConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>(service, METHODID_SET_OPTICAL_CONFIG))).addMethod(getUpdateOpticalConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>(service, METHODID_UPDATE_OPTICAL_CONFIG))).addMethod(getSelectOpticalConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig>(service, METHODID_SELECT_OPTICAL_CONFIG))).addMethod(getDeleteOpticalConfigMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty>(service, METHODID_DELETE_OPTICAL_CONFIG))).addMethod(getDeleteOpticalChannelMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty>(service, METHODID_DELETE_OPTICAL_CHANNEL))).addMethod(getSetOpticalLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty>(service, METHODID_SET_OPTICAL_LINK))).addMethod(getGetOpticalLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink>(service, METHODID_GET_OPTICAL_LINK))).addMethod(getDeleteOpticalLinkMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>(service, METHODID_DELETE_OPTICAL_LINK))).addMethod(getGetOpticalLinkListMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList>(service, METHODID_GET_OPTICAL_LINK_LIST))).addMethod(getGetOpticalBandMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList>(service, METHODID_GET_OPTICAL_BAND))).addMethod(getSelectOpticalBandMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand>(service, METHODID_SELECT_OPTICAL_BAND))).addMethod(getDeleteServiceConfigRuleMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty>(service, METHODID_DELETE_SERVICE_CONFIG_RULE))).build();
    }

    private static abstract class ContextServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        ContextServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return context.ContextOuterClass.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("ContextService");
        }
    }

    private static final class ContextServiceFileDescriptorSupplier extends ContextServiceBaseDescriptorSupplier {

        ContextServiceFileDescriptorSupplier() {
        }
    }

    private static final class ContextServiceMethodDescriptorSupplier extends ContextServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        ContextServiceMethodDescriptorSupplier(String methodName) {
            this.methodName = methodName;
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
            return getServiceDescriptor().findMethodByName(methodName);
        }
    }

    private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

    public static io.grpc.ServiceDescriptor getServiceDescriptor() {
        io.grpc.ServiceDescriptor result = serviceDescriptor;
        if (result == null) {
            synchronized (ContextServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new ContextServiceFileDescriptorSupplier()).addMethod(getListContextIdsMethod()).addMethod(getListContextsMethod()).addMethod(getGetContextMethod()).addMethod(getSetContextMethod()).addMethod(getRemoveContextMethod()).addMethod(getGetContextEventsMethod()).addMethod(getListTopologyIdsMethod()).addMethod(getListTopologiesMethod()).addMethod(getGetTopologyMethod()).addMethod(getGetTopologyDetailsMethod()).addMethod(getSetTopologyMethod()).addMethod(getRemoveTopologyMethod()).addMethod(getGetTopologyEventsMethod()).addMethod(getListDeviceIdsMethod()).addMethod(getListDevicesMethod()).addMethod(getGetDeviceMethod()).addMethod(getSetDeviceMethod()).addMethod(getRemoveDeviceMethod()).addMethod(getGetDeviceEventsMethod()).addMethod(getSelectDeviceMethod()).addMethod(getListEndPointNamesMethod()).addMethod(getListLinkIdsMethod()).addMethod(getListLinksMethod()).addMethod(getGetLinkMethod()).addMethod(getSetLinkMethod()).addMethod(getRemoveLinkMethod()).addMethod(getGetLinkEventsMethod()).addMethod(getListServiceIdsMethod()).addMethod(getListServicesMethod()).addMethod(getGetServiceMethod()).addMethod(getSetServiceMethod()).addMethod(getUnsetServiceMethod()).addMethod(getRemoveServiceMethod()).addMethod(getGetServiceEventsMethod()).addMethod(getSelectServiceMethod()).addMethod(getListSliceIdsMethod()).addMethod(getListSlicesMethod()).addMethod(getGetSliceMethod()).addMethod(getSetSliceMethod()).addMethod(getUnsetSliceMethod()).addMethod(getRemoveSliceMethod()).addMethod(getGetSliceEventsMethod()).addMethod(getSelectSliceMethod()).addMethod(getListConnectionIdsMethod()).addMethod(getListConnectionsMethod()).addMethod(getGetConnectionMethod()).addMethod(getSetConnectionMethod()).addMethod(getRemoveConnectionMethod()).addMethod(getGetConnectionEventsMethod()).addMethod(getGetAllEventsMethod()).addMethod(getGetOpticalConfigMethod()).addMethod(getSetOpticalConfigMethod()).addMethod(getUpdateOpticalConfigMethod()).addMethod(getSelectOpticalConfigMethod()).addMethod(getDeleteOpticalConfigMethod()).addMethod(getDeleteOpticalChannelMethod()).addMethod(getSetOpticalLinkMethod()).addMethod(getGetOpticalLinkMethod()).addMethod(getDeleteOpticalLinkMethod()).addMethod(getGetOpticalLinkListMethod()).addMethod(getGetOpticalBandMethod()).addMethod(getSelectOpticalBandMethod()).addMethod(getDeleteServiceConfigRuleMethod()).build();
                }
            }
        }
        return result;
    }
}

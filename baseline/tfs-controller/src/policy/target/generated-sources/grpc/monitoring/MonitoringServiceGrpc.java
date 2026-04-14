package monitoring;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@io.quarkus.grpc.common.Generated(value = "by gRPC proto compiler (version 1.55.1)", comments = "Source: monitoring.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class MonitoringServiceGrpc {

    private MonitoringServiceGrpc() {
    }

    public static final String SERVICE_NAME = "monitoring.MonitoringService";

    // Static method descriptors that strictly reflect the proto.
    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId> getSetKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetKpi", requestType = monitoring.Monitoring.KpiDescriptor.class, responseType = monitoring.Monitoring.KpiId.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId> getSetKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId> getSetKpiMethod;
        if ((getSetKpiMethod = MonitoringServiceGrpc.getSetKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getSetKpiMethod = MonitoringServiceGrpc.getSetKpiMethod) == null) {
                    MonitoringServiceGrpc.getSetKpiMethod = getSetKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiDescriptor.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiId.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("SetKpi")).build();
                }
            }
        }
        return getSetKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty> getDeleteKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteKpi", requestType = monitoring.Monitoring.KpiId.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty> getDeleteKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty> getDeleteKpiMethod;
        if ((getDeleteKpiMethod = MonitoringServiceGrpc.getDeleteKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getDeleteKpiMethod = MonitoringServiceGrpc.getDeleteKpiMethod) == null) {
                    MonitoringServiceGrpc.getDeleteKpiMethod = getDeleteKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("DeleteKpi")).build();
                }
            }
        }
        return getDeleteKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor> getGetKpiDescriptorMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetKpiDescriptor", requestType = monitoring.Monitoring.KpiId.class, responseType = monitoring.Monitoring.KpiDescriptor.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor> getGetKpiDescriptorMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor> getGetKpiDescriptorMethod;
        if ((getGetKpiDescriptorMethod = MonitoringServiceGrpc.getGetKpiDescriptorMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetKpiDescriptorMethod = MonitoringServiceGrpc.getGetKpiDescriptorMethod) == null) {
                    MonitoringServiceGrpc.getGetKpiDescriptorMethod = getGetKpiDescriptorMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetKpiDescriptor")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiDescriptor.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetKpiDescriptor")).build();
                }
            }
        }
        return getGetKpiDescriptorMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList> getGetKpiDescriptorListMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetKpiDescriptorList", requestType = context.ContextOuterClass.Empty.class, responseType = monitoring.Monitoring.KpiDescriptorList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList> getGetKpiDescriptorListMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList> getGetKpiDescriptorListMethod;
        if ((getGetKpiDescriptorListMethod = MonitoringServiceGrpc.getGetKpiDescriptorListMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetKpiDescriptorListMethod = MonitoringServiceGrpc.getGetKpiDescriptorListMethod) == null) {
                    MonitoringServiceGrpc.getGetKpiDescriptorListMethod = getGetKpiDescriptorListMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetKpiDescriptorList")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiDescriptorList.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetKpiDescriptorList")).build();
                }
            }
        }
        return getGetKpiDescriptorListMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty> getIncludeKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "IncludeKpi", requestType = monitoring.Monitoring.Kpi.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty> getIncludeKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty> getIncludeKpiMethod;
        if ((getIncludeKpiMethod = MonitoringServiceGrpc.getIncludeKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getIncludeKpiMethod = MonitoringServiceGrpc.getIncludeKpiMethod) == null) {
                    MonitoringServiceGrpc.getIncludeKpiMethod = getIncludeKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "IncludeKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.Kpi.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("IncludeKpi")).build();
                }
            }
        }
        return getIncludeKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty> getMonitorKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "MonitorKpi", requestType = monitoring.Monitoring.MonitorKpiRequest.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty> getMonitorKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty> getMonitorKpiMethod;
        if ((getMonitorKpiMethod = MonitoringServiceGrpc.getMonitorKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getMonitorKpiMethod = MonitoringServiceGrpc.getMonitorKpiMethod) == null) {
                    MonitoringServiceGrpc.getMonitorKpiMethod = getMonitorKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "MonitorKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.MonitorKpiRequest.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("MonitorKpi")).build();
                }
            }
        }
        return getMonitorKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable> getQueryKpiDataMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "QueryKpiData", requestType = monitoring.Monitoring.KpiQuery.class, responseType = monitoring.Monitoring.RawKpiTable.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable> getQueryKpiDataMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable> getQueryKpiDataMethod;
        if ((getQueryKpiDataMethod = MonitoringServiceGrpc.getQueryKpiDataMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getQueryKpiDataMethod = MonitoringServiceGrpc.getQueryKpiDataMethod) == null) {
                    MonitoringServiceGrpc.getQueryKpiDataMethod = getQueryKpiDataMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "QueryKpiData")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiQuery.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.RawKpiTable.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("QueryKpiData")).build();
                }
            }
        }
        return getQueryKpiDataMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse> getSetKpiSubscriptionMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetKpiSubscription", requestType = monitoring.Monitoring.SubsDescriptor.class, responseType = monitoring.Monitoring.SubsResponse.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse> getSetKpiSubscriptionMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse> getSetKpiSubscriptionMethod;
        if ((getSetKpiSubscriptionMethod = MonitoringServiceGrpc.getSetKpiSubscriptionMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getSetKpiSubscriptionMethod = MonitoringServiceGrpc.getSetKpiSubscriptionMethod) == null) {
                    MonitoringServiceGrpc.getSetKpiSubscriptionMethod = getSetKpiSubscriptionMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetKpiSubscription")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubsDescriptor.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubsResponse.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("SetKpiSubscription")).build();
                }
            }
        }
        return getSetKpiSubscriptionMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor> getGetSubsDescriptorMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetSubsDescriptor", requestType = monitoring.Monitoring.SubscriptionID.class, responseType = monitoring.Monitoring.SubsDescriptor.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor> getGetSubsDescriptorMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor> getGetSubsDescriptorMethod;
        if ((getGetSubsDescriptorMethod = MonitoringServiceGrpc.getGetSubsDescriptorMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetSubsDescriptorMethod = MonitoringServiceGrpc.getGetSubsDescriptorMethod) == null) {
                    MonitoringServiceGrpc.getGetSubsDescriptorMethod = getGetSubsDescriptorMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetSubsDescriptor")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubscriptionID.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubsDescriptor.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetSubsDescriptor")).build();
                }
            }
        }
        return getGetSubsDescriptorMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList> getGetSubscriptionsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetSubscriptions", requestType = context.ContextOuterClass.Empty.class, responseType = monitoring.Monitoring.SubsList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList> getGetSubscriptionsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList> getGetSubscriptionsMethod;
        if ((getGetSubscriptionsMethod = MonitoringServiceGrpc.getGetSubscriptionsMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetSubscriptionsMethod = MonitoringServiceGrpc.getGetSubscriptionsMethod) == null) {
                    MonitoringServiceGrpc.getGetSubscriptionsMethod = getGetSubscriptionsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetSubscriptions")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubsList.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetSubscriptions")).build();
                }
            }
        }
        return getGetSubscriptionsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty> getDeleteSubscriptionMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteSubscription", requestType = monitoring.Monitoring.SubscriptionID.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty> getDeleteSubscriptionMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty> getDeleteSubscriptionMethod;
        if ((getDeleteSubscriptionMethod = MonitoringServiceGrpc.getDeleteSubscriptionMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getDeleteSubscriptionMethod = MonitoringServiceGrpc.getDeleteSubscriptionMethod) == null) {
                    MonitoringServiceGrpc.getDeleteSubscriptionMethod = getDeleteSubscriptionMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteSubscription")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.SubscriptionID.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("DeleteSubscription")).build();
                }
            }
        }
        return getDeleteSubscriptionMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID> getSetKpiAlarmMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "SetKpiAlarm", requestType = monitoring.Monitoring.AlarmDescriptor.class, responseType = monitoring.Monitoring.AlarmID.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID> getSetKpiAlarmMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID> getSetKpiAlarmMethod;
        if ((getSetKpiAlarmMethod = MonitoringServiceGrpc.getSetKpiAlarmMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getSetKpiAlarmMethod = MonitoringServiceGrpc.getSetKpiAlarmMethod) == null) {
                    MonitoringServiceGrpc.getSetKpiAlarmMethod = getSetKpiAlarmMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "SetKpiAlarm")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmDescriptor.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmID.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("SetKpiAlarm")).build();
                }
            }
        }
        return getSetKpiAlarmMethod;
    }

    private static volatile io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList> getGetAlarmsMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetAlarms", requestType = context.ContextOuterClass.Empty.class, responseType = monitoring.Monitoring.AlarmList.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList> getGetAlarmsMethod() {
        io.grpc.MethodDescriptor<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList> getGetAlarmsMethod;
        if ((getGetAlarmsMethod = MonitoringServiceGrpc.getGetAlarmsMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetAlarmsMethod = MonitoringServiceGrpc.getGetAlarmsMethod) == null) {
                    MonitoringServiceGrpc.getGetAlarmsMethod = getGetAlarmsMethod = io.grpc.MethodDescriptor.<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetAlarms")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmList.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetAlarms")).build();
                }
            }
        }
        return getGetAlarmsMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor> getGetAlarmDescriptorMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetAlarmDescriptor", requestType = monitoring.Monitoring.AlarmID.class, responseType = monitoring.Monitoring.AlarmDescriptor.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor> getGetAlarmDescriptorMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor> getGetAlarmDescriptorMethod;
        if ((getGetAlarmDescriptorMethod = MonitoringServiceGrpc.getGetAlarmDescriptorMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetAlarmDescriptorMethod = MonitoringServiceGrpc.getGetAlarmDescriptorMethod) == null) {
                    MonitoringServiceGrpc.getGetAlarmDescriptorMethod = getGetAlarmDescriptorMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetAlarmDescriptor")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmID.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmDescriptor.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetAlarmDescriptor")).build();
                }
            }
        }
        return getGetAlarmDescriptorMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse> getGetAlarmResponseStreamMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetAlarmResponseStream", requestType = monitoring.Monitoring.AlarmSubscription.class, responseType = monitoring.Monitoring.AlarmResponse.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse> getGetAlarmResponseStreamMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse> getGetAlarmResponseStreamMethod;
        if ((getGetAlarmResponseStreamMethod = MonitoringServiceGrpc.getGetAlarmResponseStreamMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetAlarmResponseStreamMethod = MonitoringServiceGrpc.getGetAlarmResponseStreamMethod) == null) {
                    MonitoringServiceGrpc.getGetAlarmResponseStreamMethod = getGetAlarmResponseStreamMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetAlarmResponseStream")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmSubscription.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmResponse.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetAlarmResponseStream")).build();
                }
            }
        }
        return getGetAlarmResponseStreamMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty> getDeleteAlarmMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "DeleteAlarm", requestType = monitoring.Monitoring.AlarmID.class, responseType = context.ContextOuterClass.Empty.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty> getDeleteAlarmMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty> getDeleteAlarmMethod;
        if ((getDeleteAlarmMethod = MonitoringServiceGrpc.getDeleteAlarmMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getDeleteAlarmMethod = MonitoringServiceGrpc.getDeleteAlarmMethod) == null) {
                    MonitoringServiceGrpc.getDeleteAlarmMethod = getDeleteAlarmMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "DeleteAlarm")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.AlarmID.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(context.ContextOuterClass.Empty.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("DeleteAlarm")).build();
                }
            }
        }
        return getDeleteAlarmMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetStreamKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetStreamKpi", requestType = monitoring.Monitoring.KpiId.class, responseType = monitoring.Monitoring.Kpi.class, methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetStreamKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetStreamKpiMethod;
        if ((getGetStreamKpiMethod = MonitoringServiceGrpc.getGetStreamKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetStreamKpiMethod = MonitoringServiceGrpc.getGetStreamKpiMethod) == null) {
                    MonitoringServiceGrpc.getGetStreamKpiMethod = getGetStreamKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetStreamKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.Kpi.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetStreamKpi")).build();
                }
            }
        }
        return getGetStreamKpiMethod;
    }

    private static volatile io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetInstantKpiMethod;

    @io.grpc.stub.annotations.RpcMethod(fullMethodName = SERVICE_NAME + '/' + "GetInstantKpi", requestType = monitoring.Monitoring.KpiId.class, responseType = monitoring.Monitoring.Kpi.class, methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
    public static io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetInstantKpiMethod() {
        io.grpc.MethodDescriptor<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi> getGetInstantKpiMethod;
        if ((getGetInstantKpiMethod = MonitoringServiceGrpc.getGetInstantKpiMethod) == null) {
            synchronized (MonitoringServiceGrpc.class) {
                if ((getGetInstantKpiMethod = MonitoringServiceGrpc.getGetInstantKpiMethod) == null) {
                    MonitoringServiceGrpc.getGetInstantKpiMethod = getGetInstantKpiMethod = io.grpc.MethodDescriptor.<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>newBuilder().setType(io.grpc.MethodDescriptor.MethodType.UNARY).setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetInstantKpi")).setSampledToLocalTracing(true).setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.KpiId.getDefaultInstance())).setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(monitoring.Monitoring.Kpi.getDefaultInstance())).setSchemaDescriptor(new MonitoringServiceMethodDescriptorSupplier("GetInstantKpi")).build();
                }
            }
        }
        return getGetInstantKpiMethod;
    }

    /**
     * Creates a new async stub that supports all call types for the service
     */
    public static MonitoringServiceStub newStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceStub> factory = new io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceStub>() {

            @java.lang.Override
            public MonitoringServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new MonitoringServiceStub(channel, callOptions);
            }
        };
        return MonitoringServiceStub.newStub(factory, channel);
    }

    /**
     * Creates a new blocking-style stub that supports unary and streaming output calls on the service
     */
    public static MonitoringServiceBlockingStub newBlockingStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceBlockingStub> factory = new io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceBlockingStub>() {

            @java.lang.Override
            public MonitoringServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new MonitoringServiceBlockingStub(channel, callOptions);
            }
        };
        return MonitoringServiceBlockingStub.newStub(factory, channel);
    }

    /**
     * Creates a new ListenableFuture-style stub that supports unary calls on the service
     */
    public static MonitoringServiceFutureStub newFutureStub(io.grpc.Channel channel) {
        io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceFutureStub> factory = new io.grpc.stub.AbstractStub.StubFactory<MonitoringServiceFutureStub>() {

            @java.lang.Override
            public MonitoringServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
                return new MonitoringServiceFutureStub(channel, callOptions);
            }
        };
        return MonitoringServiceFutureStub.newStub(factory, channel);
    }

    /**
     */
    public interface AsyncService {

        /**
         */
        default void setKpi(monitoring.Monitoring.KpiDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiId> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetKpiMethod(), responseObserver);
        }

        /**
         */
        default void deleteKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteKpiMethod(), responseObserver);
        }

        /**
         */
        default void getKpiDescriptor(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptor> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetKpiDescriptorMethod(), responseObserver);
        }

        /**
         */
        default void getKpiDescriptorList(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptorList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetKpiDescriptorListMethod(), responseObserver);
        }

        /**
         */
        default void includeKpi(monitoring.Monitoring.Kpi request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getIncludeKpiMethod(), responseObserver);
        }

        /**
         */
        default void monitorKpi(monitoring.Monitoring.MonitorKpiRequest request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getMonitorKpiMethod(), responseObserver);
        }

        /**
         */
        default void queryKpiData(monitoring.Monitoring.KpiQuery request, io.grpc.stub.StreamObserver<monitoring.Monitoring.RawKpiTable> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getQueryKpiDataMethod(), responseObserver);
        }

        /**
         */
        default void setKpiSubscription(monitoring.Monitoring.SubsDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsResponse> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetKpiSubscriptionMethod(), responseObserver);
        }

        /**
         */
        default void getSubsDescriptor(monitoring.Monitoring.SubscriptionID request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsDescriptor> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetSubsDescriptorMethod(), responseObserver);
        }

        /**
         */
        default void getSubscriptions(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetSubscriptionsMethod(), responseObserver);
        }

        /**
         */
        default void deleteSubscription(monitoring.Monitoring.SubscriptionID request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteSubscriptionMethod(), responseObserver);
        }

        /**
         */
        default void setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmID> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSetKpiAlarmMethod(), responseObserver);
        }

        /**
         */
        default void getAlarms(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmList> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetAlarmsMethod(), responseObserver);
        }

        /**
         */
        default void getAlarmDescriptor(monitoring.Monitoring.AlarmID request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmDescriptor> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetAlarmDescriptorMethod(), responseObserver);
        }

        /**
         */
        default void getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmResponse> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetAlarmResponseStreamMethod(), responseObserver);
        }

        /**
         */
        default void deleteAlarm(monitoring.Monitoring.AlarmID request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDeleteAlarmMethod(), responseObserver);
        }

        /**
         */
        default void getStreamKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetStreamKpiMethod(), responseObserver);
        }

        /**
         */
        default void getInstantKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi> responseObserver) {
            io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetInstantKpiMethod(), responseObserver);
        }
    }

    /**
     * Base class for the server implementation of the service MonitoringService.
     */
    public static abstract class MonitoringServiceImplBase implements io.grpc.BindableService, AsyncService {

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return MonitoringServiceGrpc.bindService(this);
        }
    }

    /**
     * A stub to allow clients to do asynchronous rpc calls to service MonitoringService.
     */
    public static class MonitoringServiceStub extends io.grpc.stub.AbstractAsyncStub<MonitoringServiceStub> {

        private MonitoringServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected MonitoringServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MonitoringServiceStub(channel, callOptions);
        }

        /**
         */
        public void setKpi(monitoring.Monitoring.KpiDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiId> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getKpiDescriptor(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptor> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetKpiDescriptorMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getKpiDescriptorList(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptorList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetKpiDescriptorListMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void includeKpi(monitoring.Monitoring.Kpi request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getIncludeKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void monitorKpi(monitoring.Monitoring.MonitorKpiRequest request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getMonitorKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void queryKpiData(monitoring.Monitoring.KpiQuery request, io.grpc.stub.StreamObserver<monitoring.Monitoring.RawKpiTable> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getQueryKpiDataMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setKpiSubscription(monitoring.Monitoring.SubsDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsResponse> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getSetKpiSubscriptionMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getSubsDescriptor(monitoring.Monitoring.SubscriptionID request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsDescriptor> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetSubsDescriptorMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getSubscriptions(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetSubscriptionsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteSubscription(monitoring.Monitoring.SubscriptionID request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteSubscriptionMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmID> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getSetKpiAlarmMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getAlarms(context.ContextOuterClass.Empty request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmList> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetAlarmsMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getAlarmDescriptor(monitoring.Monitoring.AlarmID request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmDescriptor> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetAlarmDescriptorMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request, io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmResponse> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetAlarmResponseStreamMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void deleteAlarm(monitoring.Monitoring.AlarmID request, io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getDeleteAlarmMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getStreamKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi> responseObserver) {
            io.grpc.stub.ClientCalls.asyncServerStreamingCall(getChannel().newCall(getGetStreamKpiMethod(), getCallOptions()), request, responseObserver);
        }

        /**
         */
        public void getInstantKpi(monitoring.Monitoring.KpiId request, io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi> responseObserver) {
            io.grpc.stub.ClientCalls.asyncUnaryCall(getChannel().newCall(getGetInstantKpiMethod(), getCallOptions()), request, responseObserver);
        }
    }

    /**
     * A stub to allow clients to do synchronous rpc calls to service MonitoringService.
     */
    public static class MonitoringServiceBlockingStub extends io.grpc.stub.AbstractBlockingStub<MonitoringServiceBlockingStub> {

        private MonitoringServiceBlockingStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected MonitoringServiceBlockingStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MonitoringServiceBlockingStub(channel, callOptions);
        }

        /**
         */
        public monitoring.Monitoring.KpiId setKpi(monitoring.Monitoring.KpiDescriptor request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteKpi(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.KpiDescriptor getKpiDescriptor(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetKpiDescriptorMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.KpiDescriptorList getKpiDescriptorList(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetKpiDescriptorListMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty includeKpi(monitoring.Monitoring.Kpi request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getIncludeKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getMonitorKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.RawKpiTable queryKpiData(monitoring.Monitoring.KpiQuery request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getQueryKpiDataMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getSetKpiSubscriptionMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.SubsDescriptor getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetSubsDescriptorMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.SubsList getSubscriptions(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetSubscriptionsMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteSubscriptionMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.AlarmID setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getSetKpiAlarmMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.AlarmList getAlarms(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetAlarmsMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.AlarmDescriptor getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetAlarmDescriptorMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetAlarmResponseStreamMethod(), getCallOptions(), request);
        }

        /**
         */
        public context.ContextOuterClass.Empty deleteAlarm(monitoring.Monitoring.AlarmID request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getDeleteAlarmMethod(), getCallOptions(), request);
        }

        /**
         */
        public java.util.Iterator<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.blockingServerStreamingCall(getChannel(), getGetStreamKpiMethod(), getCallOptions(), request);
        }

        /**
         */
        public monitoring.Monitoring.Kpi getInstantKpi(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.blockingUnaryCall(getChannel(), getGetInstantKpiMethod(), getCallOptions(), request);
        }
    }

    /**
     * A stub to allow clients to do ListenableFuture-style rpc calls to service MonitoringService.
     */
    public static class MonitoringServiceFutureStub extends io.grpc.stub.AbstractFutureStub<MonitoringServiceFutureStub> {

        private MonitoringServiceFutureStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
        }

        @java.lang.Override
        protected MonitoringServiceFutureStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MonitoringServiceFutureStub(channel, callOptions);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetKpiMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteKpiMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetKpiDescriptorMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetKpiDescriptorListMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getIncludeKpiMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getMonitorKpiMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getQueryKpiDataMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetSubsDescriptorMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetSubscriptionsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteSubscriptionMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getSetKpiAlarmMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetAlarmsMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetAlarmDescriptorMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getDeleteAlarmMethod(), getCallOptions()), request);
        }

        /**
         */
        public com.google.common.util.concurrent.ListenableFuture<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request) {
            return io.grpc.stub.ClientCalls.futureUnaryCall(getChannel().newCall(getGetInstantKpiMethod(), getCallOptions()), request);
        }
    }

    private static final int METHODID_SET_KPI = 0;

    private static final int METHODID_DELETE_KPI = 1;

    private static final int METHODID_GET_KPI_DESCRIPTOR = 2;

    private static final int METHODID_GET_KPI_DESCRIPTOR_LIST = 3;

    private static final int METHODID_INCLUDE_KPI = 4;

    private static final int METHODID_MONITOR_KPI = 5;

    private static final int METHODID_QUERY_KPI_DATA = 6;

    private static final int METHODID_SET_KPI_SUBSCRIPTION = 7;

    private static final int METHODID_GET_SUBS_DESCRIPTOR = 8;

    private static final int METHODID_GET_SUBSCRIPTIONS = 9;

    private static final int METHODID_DELETE_SUBSCRIPTION = 10;

    private static final int METHODID_SET_KPI_ALARM = 11;

    private static final int METHODID_GET_ALARMS = 12;

    private static final int METHODID_GET_ALARM_DESCRIPTOR = 13;

    private static final int METHODID_GET_ALARM_RESPONSE_STREAM = 14;

    private static final int METHODID_DELETE_ALARM = 15;

    private static final int METHODID_GET_STREAM_KPI = 16;

    private static final int METHODID_GET_INSTANT_KPI = 17;

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
                case METHODID_SET_KPI:
                    serviceImpl.setKpi((monitoring.Monitoring.KpiDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiId>) responseObserver);
                    break;
                case METHODID_DELETE_KPI:
                    serviceImpl.deleteKpi((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_KPI_DESCRIPTOR:
                    serviceImpl.getKpiDescriptor((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptor>) responseObserver);
                    break;
                case METHODID_GET_KPI_DESCRIPTOR_LIST:
                    serviceImpl.getKpiDescriptorList((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptorList>) responseObserver);
                    break;
                case METHODID_INCLUDE_KPI:
                    serviceImpl.includeKpi((monitoring.Monitoring.Kpi) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_MONITOR_KPI:
                    serviceImpl.monitorKpi((monitoring.Monitoring.MonitorKpiRequest) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_QUERY_KPI_DATA:
                    serviceImpl.queryKpiData((monitoring.Monitoring.KpiQuery) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.RawKpiTable>) responseObserver);
                    break;
                case METHODID_SET_KPI_SUBSCRIPTION:
                    serviceImpl.setKpiSubscription((monitoring.Monitoring.SubsDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsResponse>) responseObserver);
                    break;
                case METHODID_GET_SUBS_DESCRIPTOR:
                    serviceImpl.getSubsDescriptor((monitoring.Monitoring.SubscriptionID) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsDescriptor>) responseObserver);
                    break;
                case METHODID_GET_SUBSCRIPTIONS:
                    serviceImpl.getSubscriptions((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsList>) responseObserver);
                    break;
                case METHODID_DELETE_SUBSCRIPTION:
                    serviceImpl.deleteSubscription((monitoring.Monitoring.SubscriptionID) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_SET_KPI_ALARM:
                    serviceImpl.setKpiAlarm((monitoring.Monitoring.AlarmDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmID>) responseObserver);
                    break;
                case METHODID_GET_ALARMS:
                    serviceImpl.getAlarms((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmList>) responseObserver);
                    break;
                case METHODID_GET_ALARM_DESCRIPTOR:
                    serviceImpl.getAlarmDescriptor((monitoring.Monitoring.AlarmID) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmDescriptor>) responseObserver);
                    break;
                case METHODID_GET_ALARM_RESPONSE_STREAM:
                    serviceImpl.getAlarmResponseStream((monitoring.Monitoring.AlarmSubscription) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmResponse>) responseObserver);
                    break;
                case METHODID_DELETE_ALARM:
                    serviceImpl.deleteAlarm((monitoring.Monitoring.AlarmID) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver);
                    break;
                case METHODID_GET_STREAM_KPI:
                    serviceImpl.getStreamKpi((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi>) responseObserver);
                    break;
                case METHODID_GET_INSTANT_KPI:
                    serviceImpl.getInstantKpi((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi>) responseObserver);
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
        return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(getSetKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId>(service, METHODID_SET_KPI))).addMethod(getDeleteKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty>(service, METHODID_DELETE_KPI))).addMethod(getGetKpiDescriptorMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor>(service, METHODID_GET_KPI_DESCRIPTOR))).addMethod(getGetKpiDescriptorListMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList>(service, METHODID_GET_KPI_DESCRIPTOR_LIST))).addMethod(getIncludeKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty>(service, METHODID_INCLUDE_KPI))).addMethod(getMonitorKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty>(service, METHODID_MONITOR_KPI))).addMethod(getQueryKpiDataMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable>(service, METHODID_QUERY_KPI_DATA))).addMethod(getSetKpiSubscriptionMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse>(service, METHODID_SET_KPI_SUBSCRIPTION))).addMethod(getGetSubsDescriptorMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor>(service, METHODID_GET_SUBS_DESCRIPTOR))).addMethod(getGetSubscriptionsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList>(service, METHODID_GET_SUBSCRIPTIONS))).addMethod(getDeleteSubscriptionMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty>(service, METHODID_DELETE_SUBSCRIPTION))).addMethod(getSetKpiAlarmMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID>(service, METHODID_SET_KPI_ALARM))).addMethod(getGetAlarmsMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList>(service, METHODID_GET_ALARMS))).addMethod(getGetAlarmDescriptorMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor>(service, METHODID_GET_ALARM_DESCRIPTOR))).addMethod(getGetAlarmResponseStreamMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse>(service, METHODID_GET_ALARM_RESPONSE_STREAM))).addMethod(getDeleteAlarmMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty>(service, METHODID_DELETE_ALARM))).addMethod(getGetStreamKpiMethod(), io.grpc.stub.ServerCalls.asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>(service, METHODID_GET_STREAM_KPI))).addMethod(getGetInstantKpiMethod(), io.grpc.stub.ServerCalls.asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>(service, METHODID_GET_INSTANT_KPI))).build();
    }

    private static abstract class MonitoringServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {

        MonitoringServiceBaseDescriptorSupplier() {
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
            return monitoring.Monitoring.getDescriptor();
        }

        @java.lang.Override
        public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
            return getFileDescriptor().findServiceByName("MonitoringService");
        }
    }

    private static final class MonitoringServiceFileDescriptorSupplier extends MonitoringServiceBaseDescriptorSupplier {

        MonitoringServiceFileDescriptorSupplier() {
        }
    }

    private static final class MonitoringServiceMethodDescriptorSupplier extends MonitoringServiceBaseDescriptorSupplier implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {

        private final String methodName;

        MonitoringServiceMethodDescriptorSupplier(String methodName) {
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
            synchronized (MonitoringServiceGrpc.class) {
                result = serviceDescriptor;
                if (result == null) {
                    serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME).setSchemaDescriptor(new MonitoringServiceFileDescriptorSupplier()).addMethod(getSetKpiMethod()).addMethod(getDeleteKpiMethod()).addMethod(getGetKpiDescriptorMethod()).addMethod(getGetKpiDescriptorListMethod()).addMethod(getIncludeKpiMethod()).addMethod(getMonitorKpiMethod()).addMethod(getQueryKpiDataMethod()).addMethod(getSetKpiSubscriptionMethod()).addMethod(getGetSubsDescriptorMethod()).addMethod(getGetSubscriptionsMethod()).addMethod(getDeleteSubscriptionMethod()).addMethod(getSetKpiAlarmMethod()).addMethod(getGetAlarmsMethod()).addMethod(getGetAlarmDescriptorMethod()).addMethod(getGetAlarmResponseStreamMethod()).addMethod(getDeleteAlarmMethod()).addMethod(getGetStreamKpiMethod()).addMethod(getGetInstantKpiMethod()).build();
                }
            }
        }
        return result;
    }
}

package monitoring;

import static monitoring.MonitoringServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: monitoring.proto")
public final class MutinyMonitoringServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyMonitoringServiceGrpc() {
    }

    public static MutinyMonitoringServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyMonitoringServiceStub(channel);
    }

    public static class MutinyMonitoringServiceStub extends io.grpc.stub.AbstractStub<MutinyMonitoringServiceStub> implements io.quarkus.grpc.MutinyStub {

        private MonitoringServiceGrpc.MonitoringServiceStub delegateStub;

        private MutinyMonitoringServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = MonitoringServiceGrpc.newStub(channel);
        }

        private MutinyMonitoringServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = MonitoringServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyMonitoringServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyMonitoringServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setKpi);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteKpi);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getKpiDescriptor);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getKpiDescriptorList);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::includeKpi);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::monitorKpi);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::queryKpiData);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getSubsDescriptor);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getSubscriptions);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteSubscription);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setKpiAlarm);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getAlarms);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getAlarmDescriptor);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteAlarm);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getInstantKpi);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::setKpiSubscription);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getAlarmResponseStream);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getStreamKpi);
        }
    }

    public static abstract class MonitoringServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public MonitoringServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(monitoring.MonitoringServiceGrpc.getSetKpiMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiDescriptor, monitoring.Monitoring.KpiId>(this, METHODID_SET_KPI, compression))).addMethod(monitoring.MonitoringServiceGrpc.getDeleteKpiMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, context.ContextOuterClass.Empty>(this, METHODID_DELETE_KPI, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetKpiDescriptorMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.KpiDescriptor>(this, METHODID_GET_KPI_DESCRIPTOR, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetKpiDescriptorListMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.KpiDescriptorList>(this, METHODID_GET_KPI_DESCRIPTOR_LIST, compression))).addMethod(monitoring.MonitoringServiceGrpc.getIncludeKpiMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.Kpi, context.ContextOuterClass.Empty>(this, METHODID_INCLUDE_KPI, compression))).addMethod(monitoring.MonitoringServiceGrpc.getMonitorKpiMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.MonitorKpiRequest, context.ContextOuterClass.Empty>(this, METHODID_MONITOR_KPI, compression))).addMethod(monitoring.MonitoringServiceGrpc.getQueryKpiDataMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiQuery, monitoring.Monitoring.RawKpiTable>(this, METHODID_QUERY_KPI_DATA, compression))).addMethod(monitoring.MonitoringServiceGrpc.getSetKpiSubscriptionMethod(), asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.SubsDescriptor, monitoring.Monitoring.SubsResponse>(this, METHODID_SET_KPI_SUBSCRIPTION, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetSubsDescriptorMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SubscriptionID, monitoring.Monitoring.SubsDescriptor>(this, METHODID_GET_SUBS_DESCRIPTOR, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetSubscriptionsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.SubsList>(this, METHODID_GET_SUBSCRIPTIONS, compression))).addMethod(monitoring.MonitoringServiceGrpc.getDeleteSubscriptionMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.SubscriptionID, context.ContextOuterClass.Empty>(this, METHODID_DELETE_SUBSCRIPTION, compression))).addMethod(monitoring.MonitoringServiceGrpc.getSetKpiAlarmMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmDescriptor, monitoring.Monitoring.AlarmID>(this, METHODID_SET_KPI_ALARM, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetAlarmsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, monitoring.Monitoring.AlarmList>(this, METHODID_GET_ALARMS, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetAlarmDescriptorMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmID, monitoring.Monitoring.AlarmDescriptor>(this, METHODID_GET_ALARM_DESCRIPTOR, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetAlarmResponseStreamMethod(), asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.AlarmSubscription, monitoring.Monitoring.AlarmResponse>(this, METHODID_GET_ALARM_RESPONSE_STREAM, compression))).addMethod(monitoring.MonitoringServiceGrpc.getDeleteAlarmMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.AlarmID, context.ContextOuterClass.Empty>(this, METHODID_DELETE_ALARM, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetStreamKpiMethod(), asyncServerStreamingCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>(this, METHODID_GET_STREAM_KPI, compression))).addMethod(monitoring.MonitoringServiceGrpc.getGetInstantKpiMethod(), asyncUnaryCall(new MethodHandlers<monitoring.Monitoring.KpiId, monitoring.Monitoring.Kpi>(this, METHODID_GET_INSTANT_KPI, compression))).build();
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

        private final MonitoringServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(MonitoringServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_SET_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.KpiDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiId>) responseObserver, compression, serviceImpl::setKpi);
                    break;
                case METHODID_DELETE_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteKpi);
                    break;
                case METHODID_GET_KPI_DESCRIPTOR:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptor>) responseObserver, compression, serviceImpl::getKpiDescriptor);
                    break;
                case METHODID_GET_KPI_DESCRIPTOR_LIST:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.KpiDescriptorList>) responseObserver, compression, serviceImpl::getKpiDescriptorList);
                    break;
                case METHODID_INCLUDE_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.Kpi) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::includeKpi);
                    break;
                case METHODID_MONITOR_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.MonitorKpiRequest) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::monitorKpi);
                    break;
                case METHODID_QUERY_KPI_DATA:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.KpiQuery) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.RawKpiTable>) responseObserver, compression, serviceImpl::queryKpiData);
                    break;
                case METHODID_SET_KPI_SUBSCRIPTION:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((monitoring.Monitoring.SubsDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsResponse>) responseObserver, compression, serviceImpl::setKpiSubscription);
                    break;
                case METHODID_GET_SUBS_DESCRIPTOR:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.SubscriptionID) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsDescriptor>) responseObserver, compression, serviceImpl::getSubsDescriptor);
                    break;
                case METHODID_GET_SUBSCRIPTIONS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.SubsList>) responseObserver, compression, serviceImpl::getSubscriptions);
                    break;
                case METHODID_DELETE_SUBSCRIPTION:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.SubscriptionID) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteSubscription);
                    break;
                case METHODID_SET_KPI_ALARM:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.AlarmDescriptor) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmID>) responseObserver, compression, serviceImpl::setKpiAlarm);
                    break;
                case METHODID_GET_ALARMS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmList>) responseObserver, compression, serviceImpl::getAlarms);
                    break;
                case METHODID_GET_ALARM_DESCRIPTOR:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.AlarmID) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmDescriptor>) responseObserver, compression, serviceImpl::getAlarmDescriptor);
                    break;
                case METHODID_GET_ALARM_RESPONSE_STREAM:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((monitoring.Monitoring.AlarmSubscription) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.AlarmResponse>) responseObserver, compression, serviceImpl::getAlarmResponseStream);
                    break;
                case METHODID_DELETE_ALARM:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.AlarmID) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteAlarm);
                    break;
                case METHODID_GET_STREAM_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi>) responseObserver, compression, serviceImpl::getStreamKpi);
                    break;
                case METHODID_GET_INSTANT_KPI:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((monitoring.Monitoring.KpiId) request, (io.grpc.stub.StreamObserver<monitoring.Monitoring.Kpi>) responseObserver, compression, serviceImpl::getInstantKpi);
                    break;
                default:
                    throw new java.lang.AssertionError();
            }
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public io.grpc.stub.StreamObserver<Req> invoke(io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                default:
                    throw new java.lang.AssertionError();
            }
        }
    }
}

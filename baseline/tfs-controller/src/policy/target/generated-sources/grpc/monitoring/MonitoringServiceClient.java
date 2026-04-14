package monitoring;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: monitoring.proto")
public class MonitoringServiceClient implements MonitoringService, MutinyClient<MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub> {

    private final MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub stub;

    public MonitoringServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub, MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyMonitoringServiceGrpc.newMutinyStub(channel));
    }

    private MonitoringServiceClient(MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub stub) {
        this.stub = stub;
    }

    public MonitoringServiceClient newInstanceWithStub(MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub stub) {
        return new MonitoringServiceClient(stub);
    }

    @Override
    public MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request) {
        return stub.setKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request) {
        return stub.deleteKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request) {
        return stub.getKpiDescriptor(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request) {
        return stub.getKpiDescriptorList(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request) {
        return stub.includeKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
        return stub.monitorKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request) {
        return stub.queryKpiData(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
        return stub.getSubsDescriptor(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request) {
        return stub.getSubscriptions(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
        return stub.deleteSubscription(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
        return stub.setKpiAlarm(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request) {
        return stub.getAlarms(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
        return stub.getAlarmDescriptor(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request) {
        return stub.deleteAlarm(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request) {
        return stub.getInstantKpi(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request) {
        return stub.setKpiSubscription(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request) {
        return stub.getAlarmResponseStream(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request) {
        return stub.getStreamKpi(request);
    }
}

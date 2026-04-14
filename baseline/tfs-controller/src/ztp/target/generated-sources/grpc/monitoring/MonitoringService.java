package monitoring;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: monitoring.proto")
public interface MonitoringService extends MutinyService {

    io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request);

    io.smallrye.mutiny.Uni<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request);

    io.smallrye.mutiny.Multi<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request);

    io.smallrye.mutiny.Multi<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request);

    io.smallrye.mutiny.Multi<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request);
}

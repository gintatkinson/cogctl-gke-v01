package monitoring;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: monitoring.proto")
public class MonitoringServiceBean extends MutinyMonitoringServiceGrpc.MonitoringServiceImplBase implements BindableService, MutinyBean {

    private final MonitoringService delegate;

    MonitoringServiceBean(@GrpcService MonitoringService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiId> setKpi(monitoring.Monitoring.KpiDescriptor request) {
        try {
            return delegate.setKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteKpi(monitoring.Monitoring.KpiId request) {
        try {
            return delegate.deleteKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptor> getKpiDescriptor(monitoring.Monitoring.KpiId request) {
        try {
            return delegate.getKpiDescriptor(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.KpiDescriptorList> getKpiDescriptorList(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getKpiDescriptorList(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> includeKpi(monitoring.Monitoring.Kpi request) {
        try {
            return delegate.includeKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> monitorKpi(monitoring.Monitoring.MonitorKpiRequest request) {
        try {
            return delegate.monitorKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.RawKpiTable> queryKpiData(monitoring.Monitoring.KpiQuery request) {
        try {
            return delegate.queryKpiData(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsDescriptor> getSubsDescriptor(monitoring.Monitoring.SubscriptionID request) {
        try {
            return delegate.getSubsDescriptor(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.SubsList> getSubscriptions(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getSubscriptions(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteSubscription(monitoring.Monitoring.SubscriptionID request) {
        try {
            return delegate.deleteSubscription(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmID> setKpiAlarm(monitoring.Monitoring.AlarmDescriptor request) {
        try {
            return delegate.setKpiAlarm(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmList> getAlarms(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getAlarms(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.AlarmDescriptor> getAlarmDescriptor(monitoring.Monitoring.AlarmID request) {
        try {
            return delegate.getAlarmDescriptor(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteAlarm(monitoring.Monitoring.AlarmID request) {
        try {
            return delegate.deleteAlarm(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<monitoring.Monitoring.Kpi> getInstantKpi(monitoring.Monitoring.KpiId request) {
        try {
            return delegate.getInstantKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.SubsResponse> setKpiSubscription(monitoring.Monitoring.SubsDescriptor request) {
        try {
            return delegate.setKpiSubscription(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.AlarmResponse> getAlarmResponseStream(monitoring.Monitoring.AlarmSubscription request) {
        try {
            return delegate.getAlarmResponseStream(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<monitoring.Monitoring.Kpi> getStreamKpi(monitoring.Monitoring.KpiId request) {
        try {
            return delegate.getStreamKpi(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

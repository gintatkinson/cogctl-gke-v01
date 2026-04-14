package service;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: service.proto")
public class ServiceServiceBean extends MutinyServiceServiceGrpc.ServiceServiceImplBase implements BindableService, MutinyBean {

    private final ServiceService delegate;

    ServiceServiceBean(@GrpcService ServiceService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request) {
        try {
            return delegate.createService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request) {
        try {
            return delegate.updateService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.deleteService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request) {
        try {
            return delegate.recomputeConnections(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

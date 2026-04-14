package service;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: service.proto")
public interface ServiceService extends MutinyService {

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request);
}

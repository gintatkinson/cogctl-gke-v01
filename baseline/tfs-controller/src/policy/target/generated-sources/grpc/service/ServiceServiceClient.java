package service;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: service.proto")
public class ServiceServiceClient implements ServiceService, MutinyClient<MutinyServiceServiceGrpc.MutinyServiceServiceStub> {

    private final MutinyServiceServiceGrpc.MutinyServiceServiceStub stub;

    public ServiceServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyServiceServiceGrpc.MutinyServiceServiceStub, MutinyServiceServiceGrpc.MutinyServiceServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyServiceServiceGrpc.newMutinyStub(channel));
    }

    private ServiceServiceClient(MutinyServiceServiceGrpc.MutinyServiceServiceStub stub) {
        this.stub = stub;
    }

    public ServiceServiceClient newInstanceWithStub(MutinyServiceServiceGrpc.MutinyServiceServiceStub stub) {
        return new ServiceServiceClient(stub);
    }

    @Override
    public MutinyServiceServiceGrpc.MutinyServiceServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request) {
        return stub.createService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request) {
        return stub.updateService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request) {
        return stub.deleteService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request) {
        return stub.recomputeConnections(request);
    }
}

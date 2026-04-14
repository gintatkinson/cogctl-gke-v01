package service;

import static service.ServiceServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: service.proto")
public final class MutinyServiceServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyServiceServiceGrpc() {
    }

    public static MutinyServiceServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyServiceServiceStub(channel);
    }

    public static class MutinyServiceServiceStub extends io.grpc.stub.AbstractStub<MutinyServiceServiceStub> implements io.quarkus.grpc.MutinyStub {

        private ServiceServiceGrpc.ServiceServiceStub delegateStub;

        private MutinyServiceServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = ServiceServiceGrpc.newStub(channel);
        }

        private MutinyServiceServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = ServiceServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyServiceServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyServiceServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::createService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::updateService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::recomputeConnections);
        }
    }

    public static abstract class ServiceServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public ServiceServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> createService(context.ContextOuterClass.Service request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> updateService(context.ContextOuterClass.Service request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteService(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> recomputeConnections(context.ContextOuterClass.Service request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(service.ServiceServiceGrpc.getCreateServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(this, METHODID_CREATE_SERVICE, compression))).addMethod(service.ServiceServiceGrpc.getUpdateServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(this, METHODID_UPDATE_SERVICE, compression))).addMethod(service.ServiceServiceGrpc.getDeleteServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>(this, METHODID_DELETE_SERVICE, compression))).addMethod(service.ServiceServiceGrpc.getRecomputeConnectionsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.Empty>(this, METHODID_RECOMPUTE_CONNECTIONS, compression))).build();
        }
    }

    private static final int METHODID_CREATE_SERVICE = 0;

    private static final int METHODID_UPDATE_SERVICE = 1;

    private static final int METHODID_DELETE_SERVICE = 2;

    private static final int METHODID_RECOMPUTE_CONNECTIONS = 3;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final ServiceServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(ServiceServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_CREATE_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver, compression, serviceImpl::createService);
                    break;
                case METHODID_UPDATE_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver, compression, serviceImpl::updateService);
                    break;
                case METHODID_DELETE_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteService);
                    break;
                case METHODID_RECOMPUTE_CONNECTIONS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::recomputeConnections);
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

// Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package src.main.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 * <pre>
 * Defining a Service, a Service can have multiple RPC operations
 * </pre>
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.24.0)",
    comments = "Source: grpcService.proto")
public final class updateServiceGrpc {

  private updateServiceGrpc() {}

  public static final String SERVICE_NAME = "src.main.proto.updateService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<src.main.proto.GrpcService.updateRequest,
      src.main.proto.GrpcService.updateResponse> getUpdateMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "update",
      requestType = src.main.proto.GrpcService.updateRequest.class,
      responseType = src.main.proto.GrpcService.updateResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<src.main.proto.GrpcService.updateRequest,
      src.main.proto.GrpcService.updateResponse> getUpdateMethod() {
    io.grpc.MethodDescriptor<src.main.proto.GrpcService.updateRequest, src.main.proto.GrpcService.updateResponse> getUpdateMethod;
    if ((getUpdateMethod = updateServiceGrpc.getUpdateMethod) == null) {
      synchronized (updateServiceGrpc.class) {
        if ((getUpdateMethod = updateServiceGrpc.getUpdateMethod) == null) {
          updateServiceGrpc.getUpdateMethod = getUpdateMethod =
              io.grpc.MethodDescriptor.<src.main.proto.GrpcService.updateRequest, src.main.proto.GrpcService.updateResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "update"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  src.main.proto.GrpcService.updateRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  src.main.proto.GrpcService.updateResponse.getDefaultInstance()))
              .setSchemaDescriptor(new updateServiceMethodDescriptorSupplier("update"))
              .build();
        }
      }
    }
    return getUpdateMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static updateServiceStub newStub(io.grpc.Channel channel) {
    return new updateServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static updateServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new updateServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static updateServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new updateServiceFutureStub(channel);
  }

  /**
   * <pre>
   * Defining a Service, a Service can have multiple RPC operations
   * </pre>
   */
  public static abstract class updateServiceImplBase implements io.grpc.BindableService {

    /**
     * <pre>
     * MODIFY HERE: Update the return to streaming return.
     * </pre>
     */
    public void update(src.main.proto.GrpcService.updateRequest request,
        io.grpc.stub.StreamObserver<src.main.proto.GrpcService.updateResponse> responseObserver) {
      asyncUnimplementedUnaryCall(getUpdateMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getUpdateMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                src.main.proto.GrpcService.updateRequest,
                src.main.proto.GrpcService.updateResponse>(
                  this, METHODID_UPDATE)))
          .build();
    }
  }

  /**
   * <pre>
   * Defining a Service, a Service can have multiple RPC operations
   * </pre>
   */
  public static final class updateServiceStub extends io.grpc.stub.AbstractStub<updateServiceStub> {
    private updateServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private updateServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected updateServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new updateServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * MODIFY HERE: Update the return to streaming return.
     * </pre>
     */
    public void update(src.main.proto.GrpcService.updateRequest request,
        io.grpc.stub.StreamObserver<src.main.proto.GrpcService.updateResponse> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getUpdateMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * <pre>
   * Defining a Service, a Service can have multiple RPC operations
   * </pre>
   */
  public static final class updateServiceBlockingStub extends io.grpc.stub.AbstractStub<updateServiceBlockingStub> {
    private updateServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private updateServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected updateServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new updateServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * MODIFY HERE: Update the return to streaming return.
     * </pre>
     */
    public src.main.proto.GrpcService.updateResponse update(src.main.proto.GrpcService.updateRequest request) {
      return blockingUnaryCall(
          getChannel(), getUpdateMethod(), getCallOptions(), request);
    }
  }

  /**
   * <pre>
   * Defining a Service, a Service can have multiple RPC operations
   * </pre>
   */
  public static final class updateServiceFutureStub extends io.grpc.stub.AbstractStub<updateServiceFutureStub> {
    private updateServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private updateServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected updateServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new updateServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * MODIFY HERE: Update the return to streaming return.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<src.main.proto.GrpcService.updateResponse> update(
        src.main.proto.GrpcService.updateRequest request) {
      return futureUnaryCall(
          getChannel().newCall(getUpdateMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_UPDATE = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final updateServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(updateServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_UPDATE:
          serviceImpl.update((src.main.proto.GrpcService.updateRequest) request,
              (io.grpc.stub.StreamObserver<src.main.proto.GrpcService.updateResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class updateServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    updateServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return src.main.proto.GrpcService.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("updateService");
    }
  }

  private static final class updateServiceFileDescriptorSupplier
      extends updateServiceBaseDescriptorSupplier {
    updateServiceFileDescriptorSupplier() {}
  }

  private static final class updateServiceMethodDescriptorSupplier
      extends updateServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    updateServiceMethodDescriptorSupplier(String methodName) {
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
      synchronized (updateServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new updateServiceFileDescriptorSupplier())
              .addMethod(getUpdateMethod())
              .build();
        }
      }
    }
    return result;
  }
}

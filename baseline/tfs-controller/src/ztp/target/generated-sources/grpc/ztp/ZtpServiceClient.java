package ztp;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: ztp.proto")
public class ZtpServiceClient implements ZtpService, MutinyClient<MutinyZtpServiceGrpc.MutinyZtpServiceStub> {

    private final MutinyZtpServiceGrpc.MutinyZtpServiceStub stub;

    public ZtpServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyZtpServiceGrpc.MutinyZtpServiceStub, MutinyZtpServiceGrpc.MutinyZtpServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyZtpServiceGrpc.newMutinyStub(channel));
    }

    private ZtpServiceClient(MutinyZtpServiceGrpc.MutinyZtpServiceStub stub) {
        this.stub = stub;
    }

    public ZtpServiceClient newInstanceWithStub(MutinyZtpServiceGrpc.MutinyZtpServiceStub stub) {
        return new ZtpServiceClient(stub);
    }

    @Override
    public MutinyZtpServiceGrpc.MutinyZtpServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRole> ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request) {
        return stub.ztpGetDeviceRole(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleList> ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request) {
        return stub.ztpGetDeviceRolesByDeviceId(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpAdd(ztp.Ztp.DeviceRole request) {
        return stub.ztpAdd(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpUpdate(ztp.Ztp.DeviceRoleConfig request) {
        return stub.ztpUpdate(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpDelete(ztp.Ztp.DeviceRole request) {
        return stub.ztpDelete(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceDeletionResult> ztpDeleteAll(context.ContextOuterClass.Empty request) {
        return stub.ztpDeleteAll(request);
    }
}

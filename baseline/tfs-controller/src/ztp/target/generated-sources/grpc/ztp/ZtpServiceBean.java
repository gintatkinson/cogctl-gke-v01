package ztp;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: ztp.proto")
public class ZtpServiceBean extends MutinyZtpServiceGrpc.ZtpServiceImplBase implements BindableService, MutinyBean {

    private final ZtpService delegate;

    ZtpServiceBean(@GrpcService ZtpService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRole> ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request) {
        try {
            return delegate.ztpGetDeviceRole(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleList> ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request) {
        try {
            return delegate.ztpGetDeviceRolesByDeviceId(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpAdd(ztp.Ztp.DeviceRole request) {
        try {
            return delegate.ztpAdd(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpUpdate(ztp.Ztp.DeviceRoleConfig request) {
        try {
            return delegate.ztpUpdate(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpDelete(ztp.Ztp.DeviceRole request) {
        try {
            return delegate.ztpDelete(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<ztp.Ztp.DeviceDeletionResult> ztpDeleteAll(context.ContextOuterClass.Empty request) {
        try {
            return delegate.ztpDeleteAll(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

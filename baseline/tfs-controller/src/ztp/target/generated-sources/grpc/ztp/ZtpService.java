package ztp;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: ztp.proto")
public interface ZtpService extends MutinyService {

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRole> ztpGetDeviceRole(ztp.Ztp.DeviceRoleId request);

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleList> ztpGetDeviceRolesByDeviceId(context.ContextOuterClass.DeviceId request);

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpAdd(ztp.Ztp.DeviceRole request);

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpUpdate(ztp.Ztp.DeviceRoleConfig request);

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceRoleState> ztpDelete(ztp.Ztp.DeviceRole request);

    io.smallrye.mutiny.Uni<ztp.Ztp.DeviceDeletionResult> ztpDeleteAll(context.ContextOuterClass.Empty request);
}

package context;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context.proto")
public class ContextServiceClient implements ContextService, MutinyClient<MutinyContextServiceGrpc.MutinyContextServiceStub> {

    private final MutinyContextServiceGrpc.MutinyContextServiceStub stub;

    public ContextServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyContextServiceGrpc.MutinyContextServiceStub, MutinyContextServiceGrpc.MutinyContextServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyContextServiceGrpc.newMutinyStub(channel));
    }

    private ContextServiceClient(MutinyContextServiceGrpc.MutinyContextServiceStub stub) {
        this.stub = stub;
    }

    public ContextServiceClient newInstanceWithStub(MutinyContextServiceGrpc.MutinyContextServiceStub stub) {
        return new ContextServiceClient(stub);
    }

    @Override
    public MutinyContextServiceGrpc.MutinyContextServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request) {
        return stub.listContextIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request) {
        return stub.listContexts(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request) {
        return stub.getContext(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request) {
        return stub.setContext(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request) {
        return stub.removeContext(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request) {
        return stub.listTopologyIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request) {
        return stub.listTopologies(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request) {
        return stub.getTopology(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request) {
        return stub.getTopologyDetails(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request) {
        return stub.setTopology(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request) {
        return stub.removeTopology(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request) {
        return stub.listDeviceIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request) {
        return stub.listDevices(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request) {
        return stub.getDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request) {
        return stub.setDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request) {
        return stub.removeDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request) {
        return stub.selectDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
        return stub.listEndPointNames(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request) {
        return stub.listLinkIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request) {
        return stub.listLinks(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request) {
        return stub.getLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request) {
        return stub.setLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request) {
        return stub.removeLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request) {
        return stub.listServiceIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request) {
        return stub.listServices(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request) {
        return stub.getService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request) {
        return stub.setService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request) {
        return stub.unsetService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request) {
        return stub.removeService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request) {
        return stub.selectService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request) {
        return stub.listSliceIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request) {
        return stub.listSlices(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request) {
        return stub.getSlice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request) {
        return stub.setSlice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request) {
        return stub.unsetSlice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request) {
        return stub.removeSlice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request) {
        return stub.selectSlice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request) {
        return stub.listConnectionIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request) {
        return stub.listConnections(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request) {
        return stub.getConnection(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request) {
        return stub.setConnection(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request) {
        return stub.removeConnection(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request) {
        return stub.getOpticalConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
        return stub.setOpticalConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
        return stub.updateOpticalConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
        return stub.selectOpticalConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
        return stub.deleteOpticalConfig(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
        return stub.deleteOpticalChannel(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request) {
        return stub.setOpticalLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request) {
        return stub.getOpticalLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request) {
        return stub.deleteOpticalLink(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request) {
        return stub.getOpticalLinkList(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request) {
        return stub.getOpticalBand(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
        return stub.selectOpticalBand(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
        return stub.deleteServiceConfigRule(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request) {
        return stub.getContextEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request) {
        return stub.getTopologyEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request) {
        return stub.getDeviceEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request) {
        return stub.getLinkEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request) {
        return stub.getServiceEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request) {
        return stub.getSliceEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request) {
        return stub.getConnectionEvents(request);
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request) {
        return stub.getAllEvents(request);
    }
}

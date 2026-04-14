package context;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context.proto")
public interface ContextService extends MutinyService {

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request);

    /**
     * <pre>
     *  ------------------------------ Experimental -----------------------------
     * </pre>
     */
    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Multi<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request);
}

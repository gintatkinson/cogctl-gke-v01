package context;

import static context.ContextServiceGrpc.getServiceDescriptor;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context.proto")
public final class MutinyContextServiceGrpc implements io.quarkus.grpc.MutinyGrpc {

    private MutinyContextServiceGrpc() {
    }

    public static MutinyContextServiceStub newMutinyStub(io.grpc.Channel channel) {
        return new MutinyContextServiceStub(channel);
    }

    public static class MutinyContextServiceStub extends io.grpc.stub.AbstractStub<MutinyContextServiceStub> implements io.quarkus.grpc.MutinyStub {

        private ContextServiceGrpc.ContextServiceStub delegateStub;

        private MutinyContextServiceStub(io.grpc.Channel channel) {
            super(channel);
            delegateStub = ContextServiceGrpc.newStub(channel);
        }

        private MutinyContextServiceStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            super(channel, callOptions);
            delegateStub = ContextServiceGrpc.newStub(channel).build(channel, callOptions);
        }

        @Override
        protected MutinyContextServiceStub build(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
            return new MutinyContextServiceStub(channel, callOptions);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listContextIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listContexts);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getContext);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setContext);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeContext);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listTopologyIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listTopologies);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getTopology);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getTopologyDetails);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setTopology);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeTopology);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listDeviceIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listDevices);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::selectDevice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listEndPointNames);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listLinkIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listLinks);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listServiceIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listServices);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::unsetService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::selectService);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listSliceIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listSlices);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getSlice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setSlice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::unsetSlice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeSlice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::selectSlice);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listConnectionIds);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::listConnections);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getConnection);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setConnection);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::removeConnection);
        }

        /**
         * <pre>
         *  ------------------------------ Experimental -----------------------------
         * </pre>
         */
        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getOpticalConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setOpticalConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::updateOpticalConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::selectOpticalConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteOpticalConfig);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteOpticalChannel);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::setOpticalLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getOpticalLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteOpticalLink);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getOpticalLinkList);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::getOpticalBand);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::selectOpticalBand);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToOne(request, delegateStub::deleteServiceConfigRule);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getContextEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getTopologyEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getDeviceEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getLinkEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getServiceEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getSliceEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getConnectionEvents);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request) {
            return io.quarkus.grpc.stubs.ClientCalls.oneToMany(request, delegateStub::getAllEvents);
        }
    }

    public static abstract class ContextServiceImplBase implements io.grpc.BindableService {

        private String compression;

        /**
         * Set whether the server will try to use a compressed response.
         *
         * @param compression the compression, e.g {@code gzip}
         */
        public ContextServiceImplBase withCompression(String compression) {
            this.compression = compression;
            return this;
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        /**
         * <pre>
         *  ------------------------------ Experimental -----------------------------
         * </pre>
         */
        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        public io.smallrye.mutiny.Multi<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }

        @java.lang.Override
        public io.grpc.ServerServiceDefinition bindService() {
            return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor()).addMethod(context.ContextServiceGrpc.getListContextIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextIdList>(this, METHODID_LIST_CONTEXT_IDS, compression))).addMethod(context.ContextServiceGrpc.getListContextsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextList>(this, METHODID_LIST_CONTEXTS, compression))).addMethod(context.ContextServiceGrpc.getGetContextMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.Context>(this, METHODID_GET_CONTEXT, compression))).addMethod(context.ContextServiceGrpc.getSetContextMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Context, context.ContextOuterClass.ContextId>(this, METHODID_SET_CONTEXT, compression))).addMethod(context.ContextServiceGrpc.getRemoveContextMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_CONTEXT, compression))).addMethod(context.ContextServiceGrpc.getGetContextEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ContextEvent>(this, METHODID_GET_CONTEXT_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getListTopologyIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyIdList>(this, METHODID_LIST_TOPOLOGY_IDS, compression))).addMethod(context.ContextServiceGrpc.getListTopologiesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.TopologyList>(this, METHODID_LIST_TOPOLOGIES, compression))).addMethod(context.ContextServiceGrpc.getGetTopologyMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Topology>(this, METHODID_GET_TOPOLOGY, compression))).addMethod(context.ContextServiceGrpc.getGetTopologyDetailsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.TopologyDetails>(this, METHODID_GET_TOPOLOGY_DETAILS, compression))).addMethod(context.ContextServiceGrpc.getSetTopologyMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Topology, context.ContextOuterClass.TopologyId>(this, METHODID_SET_TOPOLOGY, compression))).addMethod(context.ContextServiceGrpc.getRemoveTopologyMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.TopologyId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_TOPOLOGY, compression))).addMethod(context.ContextServiceGrpc.getGetTopologyEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.TopologyEvent>(this, METHODID_GET_TOPOLOGY_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getListDeviceIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceIdList>(this, METHODID_LIST_DEVICE_IDS, compression))).addMethod(context.ContextServiceGrpc.getListDevicesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceList>(this, METHODID_LIST_DEVICES, compression))).addMethod(context.ContextServiceGrpc.getGetDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Device>(this, METHODID_GET_DEVICE, compression))).addMethod(context.ContextServiceGrpc.getSetDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Device, context.ContextOuterClass.DeviceId>(this, METHODID_SET_DEVICE, compression))).addMethod(context.ContextServiceGrpc.getRemoveDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_DEVICE, compression))).addMethod(context.ContextServiceGrpc.getGetDeviceEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.DeviceEvent>(this, METHODID_GET_DEVICE_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getSelectDeviceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.DeviceFilter, context.ContextOuterClass.DeviceList>(this, METHODID_SELECT_DEVICE, compression))).addMethod(context.ContextServiceGrpc.getListEndPointNamesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.EndPointIdList, context.ContextOuterClass.EndPointNameList>(this, METHODID_LIST_END_POINT_NAMES, compression))).addMethod(context.ContextServiceGrpc.getListLinkIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkIdList>(this, METHODID_LIST_LINK_IDS, compression))).addMethod(context.ContextServiceGrpc.getListLinksMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkList>(this, METHODID_LIST_LINKS, compression))).addMethod(context.ContextServiceGrpc.getGetLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Link>(this, METHODID_GET_LINK, compression))).addMethod(context.ContextServiceGrpc.getSetLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Link, context.ContextOuterClass.LinkId>(this, METHODID_SET_LINK, compression))).addMethod(context.ContextServiceGrpc.getRemoveLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_LINK, compression))).addMethod(context.ContextServiceGrpc.getGetLinkEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.LinkEvent>(this, METHODID_GET_LINK_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getListServiceIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceIdList>(this, METHODID_LIST_SERVICE_IDS, compression))).addMethod(context.ContextServiceGrpc.getListServicesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.ServiceList>(this, METHODID_LIST_SERVICES, compression))).addMethod(context.ContextServiceGrpc.getGetServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Service>(this, METHODID_GET_SERVICE, compression))).addMethod(context.ContextServiceGrpc.getSetServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(this, METHODID_SET_SERVICE, compression))).addMethod(context.ContextServiceGrpc.getUnsetServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Service, context.ContextOuterClass.ServiceId>(this, METHODID_UNSET_SERVICE, compression))).addMethod(context.ContextServiceGrpc.getRemoveServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_SERVICE, compression))).addMethod(context.ContextServiceGrpc.getGetServiceEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ServiceEvent>(this, METHODID_GET_SERVICE_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getSelectServiceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceFilter, context.ContextOuterClass.ServiceList>(this, METHODID_SELECT_SERVICE, compression))).addMethod(context.ContextServiceGrpc.getListSliceIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceIdList>(this, METHODID_LIST_SLICE_IDS, compression))).addMethod(context.ContextServiceGrpc.getListSlicesMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ContextId, context.ContextOuterClass.SliceList>(this, METHODID_LIST_SLICES, compression))).addMethod(context.ContextServiceGrpc.getGetSliceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceId, context.ContextOuterClass.Slice>(this, METHODID_GET_SLICE, compression))).addMethod(context.ContextServiceGrpc.getSetSliceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>(this, METHODID_SET_SLICE, compression))).addMethod(context.ContextServiceGrpc.getUnsetSliceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Slice, context.ContextOuterClass.SliceId>(this, METHODID_UNSET_SLICE, compression))).addMethod(context.ContextServiceGrpc.getRemoveSliceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_SLICE, compression))).addMethod(context.ContextServiceGrpc.getGetSliceEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.SliceEvent>(this, METHODID_GET_SLICE_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getSelectSliceMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.SliceFilter, context.ContextOuterClass.SliceList>(this, METHODID_SELECT_SLICE, compression))).addMethod(context.ContextServiceGrpc.getListConnectionIdsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionIdList>(this, METHODID_LIST_CONNECTION_IDS, compression))).addMethod(context.ContextServiceGrpc.getListConnectionsMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceId, context.ContextOuterClass.ConnectionList>(this, METHODID_LIST_CONNECTIONS, compression))).addMethod(context.ContextServiceGrpc.getGetConnectionMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Connection>(this, METHODID_GET_CONNECTION, compression))).addMethod(context.ContextServiceGrpc.getSetConnectionMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Connection, context.ContextOuterClass.ConnectionId>(this, METHODID_SET_CONNECTION, compression))).addMethod(context.ContextServiceGrpc.getRemoveConnectionMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ConnectionId, context.ContextOuterClass.Empty>(this, METHODID_REMOVE_CONNECTION, compression))).addMethod(context.ContextServiceGrpc.getGetConnectionEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.ConnectionEvent>(this, METHODID_GET_CONNECTION_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getGetAllEventsMethod(), asyncServerStreamingCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.AnyEvent>(this, METHODID_GET_ALL_EVENTS, compression))).addMethod(context.ContextServiceGrpc.getGetOpticalConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalConfigList>(this, METHODID_GET_OPTICAL_CONFIG, compression))).addMethod(context.ContextServiceGrpc.getSetOpticalConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>(this, METHODID_SET_OPTICAL_CONFIG, compression))).addMethod(context.ContextServiceGrpc.getUpdateOpticalConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.OpticalConfigId>(this, METHODID_UPDATE_OPTICAL_CONFIG, compression))).addMethod(context.ContextServiceGrpc.getSelectOpticalConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.OpticalConfig>(this, METHODID_SELECT_OPTICAL_CONFIG, compression))).addMethod(context.ContextServiceGrpc.getDeleteOpticalConfigMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfigId, context.ContextOuterClass.Empty>(this, METHODID_DELETE_OPTICAL_CONFIG, compression))).addMethod(context.ContextServiceGrpc.getDeleteOpticalChannelMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalConfig, context.ContextOuterClass.Empty>(this, METHODID_DELETE_OPTICAL_CHANNEL, compression))).addMethod(context.ContextServiceGrpc.getSetOpticalLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalLink, context.ContextOuterClass.Empty>(this, METHODID_SET_OPTICAL_LINK, compression))).addMethod(context.ContextServiceGrpc.getGetOpticalLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.OpticalLink>(this, METHODID_GET_OPTICAL_LINK, compression))).addMethod(context.ContextServiceGrpc.getDeleteOpticalLinkMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.LinkId, context.ContextOuterClass.Empty>(this, METHODID_DELETE_OPTICAL_LINK, compression))).addMethod(context.ContextServiceGrpc.getGetOpticalLinkListMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalLinkList>(this, METHODID_GET_OPTICAL_LINK_LIST, compression))).addMethod(context.ContextServiceGrpc.getGetOpticalBandMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.Empty, context.ContextOuterClass.OpticalBandList>(this, METHODID_GET_OPTICAL_BAND, compression))).addMethod(context.ContextServiceGrpc.getSelectOpticalBandMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.OpticalBandId, context.ContextOuterClass.OpticalBand>(this, METHODID_SELECT_OPTICAL_BAND, compression))).addMethod(context.ContextServiceGrpc.getDeleteServiceConfigRuleMethod(), asyncUnaryCall(new MethodHandlers<context.ContextOuterClass.ServiceConfigRule, context.ContextOuterClass.Empty>(this, METHODID_DELETE_SERVICE_CONFIG_RULE, compression))).build();
        }
    }

    private static final int METHODID_LIST_CONTEXT_IDS = 0;

    private static final int METHODID_LIST_CONTEXTS = 1;

    private static final int METHODID_GET_CONTEXT = 2;

    private static final int METHODID_SET_CONTEXT = 3;

    private static final int METHODID_REMOVE_CONTEXT = 4;

    private static final int METHODID_GET_CONTEXT_EVENTS = 5;

    private static final int METHODID_LIST_TOPOLOGY_IDS = 6;

    private static final int METHODID_LIST_TOPOLOGIES = 7;

    private static final int METHODID_GET_TOPOLOGY = 8;

    private static final int METHODID_GET_TOPOLOGY_DETAILS = 9;

    private static final int METHODID_SET_TOPOLOGY = 10;

    private static final int METHODID_REMOVE_TOPOLOGY = 11;

    private static final int METHODID_GET_TOPOLOGY_EVENTS = 12;

    private static final int METHODID_LIST_DEVICE_IDS = 13;

    private static final int METHODID_LIST_DEVICES = 14;

    private static final int METHODID_GET_DEVICE = 15;

    private static final int METHODID_SET_DEVICE = 16;

    private static final int METHODID_REMOVE_DEVICE = 17;

    private static final int METHODID_GET_DEVICE_EVENTS = 18;

    private static final int METHODID_SELECT_DEVICE = 19;

    private static final int METHODID_LIST_END_POINT_NAMES = 20;

    private static final int METHODID_LIST_LINK_IDS = 21;

    private static final int METHODID_LIST_LINKS = 22;

    private static final int METHODID_GET_LINK = 23;

    private static final int METHODID_SET_LINK = 24;

    private static final int METHODID_REMOVE_LINK = 25;

    private static final int METHODID_GET_LINK_EVENTS = 26;

    private static final int METHODID_LIST_SERVICE_IDS = 27;

    private static final int METHODID_LIST_SERVICES = 28;

    private static final int METHODID_GET_SERVICE = 29;

    private static final int METHODID_SET_SERVICE = 30;

    private static final int METHODID_UNSET_SERVICE = 31;

    private static final int METHODID_REMOVE_SERVICE = 32;

    private static final int METHODID_GET_SERVICE_EVENTS = 33;

    private static final int METHODID_SELECT_SERVICE = 34;

    private static final int METHODID_LIST_SLICE_IDS = 35;

    private static final int METHODID_LIST_SLICES = 36;

    private static final int METHODID_GET_SLICE = 37;

    private static final int METHODID_SET_SLICE = 38;

    private static final int METHODID_UNSET_SLICE = 39;

    private static final int METHODID_REMOVE_SLICE = 40;

    private static final int METHODID_GET_SLICE_EVENTS = 41;

    private static final int METHODID_SELECT_SLICE = 42;

    private static final int METHODID_LIST_CONNECTION_IDS = 43;

    private static final int METHODID_LIST_CONNECTIONS = 44;

    private static final int METHODID_GET_CONNECTION = 45;

    private static final int METHODID_SET_CONNECTION = 46;

    private static final int METHODID_REMOVE_CONNECTION = 47;

    private static final int METHODID_GET_CONNECTION_EVENTS = 48;

    private static final int METHODID_GET_ALL_EVENTS = 49;

    private static final int METHODID_GET_OPTICAL_CONFIG = 50;

    private static final int METHODID_SET_OPTICAL_CONFIG = 51;

    private static final int METHODID_UPDATE_OPTICAL_CONFIG = 52;

    private static final int METHODID_SELECT_OPTICAL_CONFIG = 53;

    private static final int METHODID_DELETE_OPTICAL_CONFIG = 54;

    private static final int METHODID_DELETE_OPTICAL_CHANNEL = 55;

    private static final int METHODID_SET_OPTICAL_LINK = 56;

    private static final int METHODID_GET_OPTICAL_LINK = 57;

    private static final int METHODID_DELETE_OPTICAL_LINK = 58;

    private static final int METHODID_GET_OPTICAL_LINK_LIST = 59;

    private static final int METHODID_GET_OPTICAL_BAND = 60;

    private static final int METHODID_SELECT_OPTICAL_BAND = 61;

    private static final int METHODID_DELETE_SERVICE_CONFIG_RULE = 62;

    private static final class MethodHandlers<Req, Resp> implements io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>, io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>, io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {

        private final ContextServiceImplBase serviceImpl;

        private final int methodId;

        private final String compression;

        MethodHandlers(ContextServiceImplBase serviceImpl, int methodId, String compression) {
            this.serviceImpl = serviceImpl;
            this.methodId = methodId;
            this.compression = compression;
        }

        @java.lang.Override
        @java.lang.SuppressWarnings("unchecked")
        public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
            switch(methodId) {
                case METHODID_LIST_CONTEXT_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextIdList>) responseObserver, compression, serviceImpl::listContextIds);
                    break;
                case METHODID_LIST_CONTEXTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextList>) responseObserver, compression, serviceImpl::listContexts);
                    break;
                case METHODID_GET_CONTEXT:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Context>) responseObserver, compression, serviceImpl::getContext);
                    break;
                case METHODID_SET_CONTEXT:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Context) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextId>) responseObserver, compression, serviceImpl::setContext);
                    break;
                case METHODID_REMOVE_CONTEXT:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeContext);
                    break;
                case METHODID_GET_CONTEXT_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ContextEvent>) responseObserver, compression, serviceImpl::getContextEvents);
                    break;
                case METHODID_LIST_TOPOLOGY_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyIdList>) responseObserver, compression, serviceImpl::listTopologyIds);
                    break;
                case METHODID_LIST_TOPOLOGIES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyList>) responseObserver, compression, serviceImpl::listTopologies);
                    break;
                case METHODID_GET_TOPOLOGY:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Topology>) responseObserver, compression, serviceImpl::getTopology);
                    break;
                case METHODID_GET_TOPOLOGY_DETAILS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyDetails>) responseObserver, compression, serviceImpl::getTopologyDetails);
                    break;
                case METHODID_SET_TOPOLOGY:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Topology) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyId>) responseObserver, compression, serviceImpl::setTopology);
                    break;
                case METHODID_REMOVE_TOPOLOGY:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.TopologyId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeTopology);
                    break;
                case METHODID_GET_TOPOLOGY_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.TopologyEvent>) responseObserver, compression, serviceImpl::getTopologyEvents);
                    break;
                case METHODID_LIST_DEVICE_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceIdList>) responseObserver, compression, serviceImpl::listDeviceIds);
                    break;
                case METHODID_LIST_DEVICES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList>) responseObserver, compression, serviceImpl::listDevices);
                    break;
                case METHODID_GET_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Device>) responseObserver, compression, serviceImpl::getDevice);
                    break;
                case METHODID_SET_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Device) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceId>) responseObserver, compression, serviceImpl::setDevice);
                    break;
                case METHODID_REMOVE_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.DeviceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeDevice);
                    break;
                case METHODID_GET_DEVICE_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceEvent>) responseObserver, compression, serviceImpl::getDeviceEvents);
                    break;
                case METHODID_SELECT_DEVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.DeviceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.DeviceList>) responseObserver, compression, serviceImpl::selectDevice);
                    break;
                case METHODID_LIST_END_POINT_NAMES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.EndPointIdList) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.EndPointNameList>) responseObserver, compression, serviceImpl::listEndPointNames);
                    break;
                case METHODID_LIST_LINK_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkIdList>) responseObserver, compression, serviceImpl::listLinkIds);
                    break;
                case METHODID_LIST_LINKS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkList>) responseObserver, compression, serviceImpl::listLinks);
                    break;
                case METHODID_GET_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Link>) responseObserver, compression, serviceImpl::getLink);
                    break;
                case METHODID_SET_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Link) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkId>) responseObserver, compression, serviceImpl::setLink);
                    break;
                case METHODID_REMOVE_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeLink);
                    break;
                case METHODID_GET_LINK_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.LinkEvent>) responseObserver, compression, serviceImpl::getLinkEvents);
                    break;
                case METHODID_LIST_SERVICE_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceIdList>) responseObserver, compression, serviceImpl::listServiceIds);
                    break;
                case METHODID_LIST_SERVICES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList>) responseObserver, compression, serviceImpl::listServices);
                    break;
                case METHODID_GET_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Service>) responseObserver, compression, serviceImpl::getService);
                    break;
                case METHODID_SET_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver, compression, serviceImpl::setService);
                    break;
                case METHODID_UNSET_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Service) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceId>) responseObserver, compression, serviceImpl::unsetService);
                    break;
                case METHODID_REMOVE_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeService);
                    break;
                case METHODID_GET_SERVICE_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceEvent>) responseObserver, compression, serviceImpl::getServiceEvents);
                    break;
                case METHODID_SELECT_SERVICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ServiceList>) responseObserver, compression, serviceImpl::selectService);
                    break;
                case METHODID_LIST_SLICE_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceIdList>) responseObserver, compression, serviceImpl::listSliceIds);
                    break;
                case METHODID_LIST_SLICES:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ContextId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList>) responseObserver, compression, serviceImpl::listSlices);
                    break;
                case METHODID_GET_SLICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.SliceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Slice>) responseObserver, compression, serviceImpl::getSlice);
                    break;
                case METHODID_SET_SLICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Slice) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId>) responseObserver, compression, serviceImpl::setSlice);
                    break;
                case METHODID_UNSET_SLICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Slice) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceId>) responseObserver, compression, serviceImpl::unsetSlice);
                    break;
                case METHODID_REMOVE_SLICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.SliceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeSlice);
                    break;
                case METHODID_GET_SLICE_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceEvent>) responseObserver, compression, serviceImpl::getSliceEvents);
                    break;
                case METHODID_SELECT_SLICE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.SliceFilter) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.SliceList>) responseObserver, compression, serviceImpl::selectSlice);
                    break;
                case METHODID_LIST_CONNECTION_IDS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionIdList>) responseObserver, compression, serviceImpl::listConnectionIds);
                    break;
                case METHODID_LIST_CONNECTIONS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionList>) responseObserver, compression, serviceImpl::listConnections);
                    break;
                case METHODID_GET_CONNECTION:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ConnectionId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Connection>) responseObserver, compression, serviceImpl::getConnection);
                    break;
                case METHODID_SET_CONNECTION:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Connection) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionId>) responseObserver, compression, serviceImpl::setConnection);
                    break;
                case METHODID_REMOVE_CONNECTION:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ConnectionId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::removeConnection);
                    break;
                case METHODID_GET_CONNECTION_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.ConnectionEvent>) responseObserver, compression, serviceImpl::getConnectionEvents);
                    break;
                case METHODID_GET_ALL_EVENTS:
                    io.quarkus.grpc.stubs.ServerCalls.oneToMany((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.AnyEvent>) responseObserver, compression, serviceImpl::getAllEvents);
                    break;
                case METHODID_GET_OPTICAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigList>) responseObserver, compression, serviceImpl::getOpticalConfig);
                    break;
                case METHODID_SET_OPTICAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId>) responseObserver, compression, serviceImpl::setOpticalConfig);
                    break;
                case METHODID_UPDATE_OPTICAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfigId>) responseObserver, compression, serviceImpl::updateOpticalConfig);
                    break;
                case METHODID_SELECT_OPTICAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalConfigId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalConfig>) responseObserver, compression, serviceImpl::selectOpticalConfig);
                    break;
                case METHODID_DELETE_OPTICAL_CONFIG:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalConfigId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteOpticalConfig);
                    break;
                case METHODID_DELETE_OPTICAL_CHANNEL:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalConfig) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteOpticalChannel);
                    break;
                case METHODID_SET_OPTICAL_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalLink) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::setOpticalLink);
                    break;
                case METHODID_GET_OPTICAL_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLink>) responseObserver, compression, serviceImpl::getOpticalLink);
                    break;
                case METHODID_DELETE_OPTICAL_LINK:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.LinkId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteOpticalLink);
                    break;
                case METHODID_GET_OPTICAL_LINK_LIST:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalLinkList>) responseObserver, compression, serviceImpl::getOpticalLinkList);
                    break;
                case METHODID_GET_OPTICAL_BAND:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.Empty) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBandList>) responseObserver, compression, serviceImpl::getOpticalBand);
                    break;
                case METHODID_SELECT_OPTICAL_BAND:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.OpticalBandId) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.OpticalBand>) responseObserver, compression, serviceImpl::selectOpticalBand);
                    break;
                case METHODID_DELETE_SERVICE_CONFIG_RULE:
                    io.quarkus.grpc.stubs.ServerCalls.oneToOne((context.ContextOuterClass.ServiceConfigRule) request, (io.grpc.stub.StreamObserver<context.ContextOuterClass.Empty>) responseObserver, compression, serviceImpl::deleteServiceConfigRule);
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

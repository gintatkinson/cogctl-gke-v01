package context;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context.proto")
public class ContextServiceBean extends MutinyContextServiceGrpc.ContextServiceImplBase implements BindableService, MutinyBean {

    private final ContextService delegate;

    ContextServiceBean(@GrpcService ContextService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextIdList> listContextIds(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listContextIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextList> listContexts(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listContexts(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Context> getContext(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.getContext(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ContextId> setContext(context.ContextOuterClass.Context request) {
        try {
            return delegate.setContext(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeContext(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.removeContext(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyIdList> listTopologyIds(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listTopologyIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyList> listTopologies(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listTopologies(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Topology> getTopology(context.ContextOuterClass.TopologyId request) {
        try {
            return delegate.getTopology(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyDetails> getTopologyDetails(context.ContextOuterClass.TopologyId request) {
        try {
            return delegate.getTopologyDetails(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.TopologyId> setTopology(context.ContextOuterClass.Topology request) {
        try {
            return delegate.setTopology(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeTopology(context.ContextOuterClass.TopologyId request) {
        try {
            return delegate.removeTopology(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceIdList> listDeviceIds(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listDeviceIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> listDevices(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listDevices(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Device> getDevice(context.ContextOuterClass.DeviceId request) {
        try {
            return delegate.getDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceId> setDevice(context.ContextOuterClass.Device request) {
        try {
            return delegate.setDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeDevice(context.ContextOuterClass.DeviceId request) {
        try {
            return delegate.removeDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.DeviceList> selectDevice(context.ContextOuterClass.DeviceFilter request) {
        try {
            return delegate.selectDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.EndPointNameList> listEndPointNames(context.ContextOuterClass.EndPointIdList request) {
        try {
            return delegate.listEndPointNames(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkIdList> listLinkIds(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listLinkIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkList> listLinks(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listLinks(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Link> getLink(context.ContextOuterClass.LinkId request) {
        try {
            return delegate.getLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.LinkId> setLink(context.ContextOuterClass.Link request) {
        try {
            return delegate.setLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeLink(context.ContextOuterClass.LinkId request) {
        try {
            return delegate.removeLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceIdList> listServiceIds(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listServiceIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> listServices(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listServices(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Service> getService(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.getService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> setService(context.ContextOuterClass.Service request) {
        try {
            return delegate.setService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceId> unsetService(context.ContextOuterClass.Service request) {
        try {
            return delegate.unsetService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeService(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.removeService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ServiceList> selectService(context.ContextOuterClass.ServiceFilter request) {
        try {
            return delegate.selectService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceIdList> listSliceIds(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listSliceIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> listSlices(context.ContextOuterClass.ContextId request) {
        try {
            return delegate.listSlices(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Slice> getSlice(context.ContextOuterClass.SliceId request) {
        try {
            return delegate.getSlice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> setSlice(context.ContextOuterClass.Slice request) {
        try {
            return delegate.setSlice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceId> unsetSlice(context.ContextOuterClass.Slice request) {
        try {
            return delegate.unsetSlice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeSlice(context.ContextOuterClass.SliceId request) {
        try {
            return delegate.removeSlice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.SliceList> selectSlice(context.ContextOuterClass.SliceFilter request) {
        try {
            return delegate.selectSlice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionIdList> listConnectionIds(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.listConnectionIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionList> listConnections(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.listConnections(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Connection> getConnection(context.ContextOuterClass.ConnectionId request) {
        try {
            return delegate.getConnection(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.ConnectionId> setConnection(context.ContextOuterClass.Connection request) {
        try {
            return delegate.setConnection(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removeConnection(context.ContextOuterClass.ConnectionId request) {
        try {
            return delegate.removeConnection(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigList> getOpticalConfig(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getOpticalConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> setOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
        try {
            return delegate.setOpticalConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfigId> updateOpticalConfig(context.ContextOuterClass.OpticalConfig request) {
        try {
            return delegate.updateOpticalConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalConfig> selectOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
        try {
            return delegate.selectOpticalConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalConfig(context.ContextOuterClass.OpticalConfigId request) {
        try {
            return delegate.deleteOpticalConfig(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalChannel(context.ContextOuterClass.OpticalConfig request) {
        try {
            return delegate.deleteOpticalChannel(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> setOpticalLink(context.ContextOuterClass.OpticalLink request) {
        try {
            return delegate.setOpticalLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLink> getOpticalLink(context.ContextOuterClass.LinkId request) {
        try {
            return delegate.getOpticalLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteOpticalLink(context.ContextOuterClass.LinkId request) {
        try {
            return delegate.deleteOpticalLink(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalLinkList> getOpticalLinkList(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getOpticalLinkList(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBandList> getOpticalBand(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getOpticalBand(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.OpticalBand> selectOpticalBand(context.ContextOuterClass.OpticalBandId request) {
        try {
            return delegate.selectOpticalBand(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> deleteServiceConfigRule(context.ContextOuterClass.ServiceConfigRule request) {
        try {
            return delegate.deleteServiceConfigRule(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ContextEvent> getContextEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getContextEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.TopologyEvent> getTopologyEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getTopologyEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.DeviceEvent> getDeviceEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getDeviceEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.LinkEvent> getLinkEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getLinkEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ServiceEvent> getServiceEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getServiceEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.SliceEvent> getSliceEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getSliceEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.ConnectionEvent> getConnectionEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getConnectionEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Multi<context.ContextOuterClass.AnyEvent> getAllEvents(context.ContextOuterClass.Empty request) {
        try {
            return delegate.getAllEvents(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

package policy;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: policy.proto")
public class PolicyServiceBean extends MutinyPolicyServiceGrpc.PolicyServiceImplBase implements BindableService, MutinyBean {

    private final PolicyService delegate;

    PolicyServiceBean(@GrpcService PolicyService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request) {
        try {
            return delegate.policyAddService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request) {
        try {
            return delegate.policyAddDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request) {
        try {
            return delegate.policyUpdateService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
        try {
            return delegate.policyUpdateDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request) {
        try {
            return delegate.policyDelete(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request) {
        try {
            return delegate.getPolicyService(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request) {
        try {
            return delegate.getPolicyDevice(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
        try {
            return delegate.getPolicyByServiceId(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

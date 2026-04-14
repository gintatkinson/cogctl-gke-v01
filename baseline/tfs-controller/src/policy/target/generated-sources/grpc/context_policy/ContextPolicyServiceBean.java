package context_policy;

import io.grpc.BindableService;
import io.quarkus.grpc.GrpcService;
import io.quarkus.grpc.MutinyBean;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context_policy.proto")
public class ContextPolicyServiceBean extends MutinyContextPolicyServiceGrpc.ContextPolicyServiceImplBase implements BindableService, MutinyBean {

    private final ContextPolicyService delegate;

    ContextPolicyServiceBean(@GrpcService ContextPolicyService delegate) {
        this.delegate = delegate;
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listPolicyRuleIds(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request) {
        try {
            return delegate.listPolicyRules(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request) {
        try {
            return delegate.getPolicyRule(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request) {
        try {
            return delegate.setPolicyRule(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request) {
        try {
            return delegate.removePolicyRule(request);
        } catch (UnsupportedOperationException e) {
            throw new io.grpc.StatusRuntimeException(io.grpc.Status.UNIMPLEMENTED);
        }
    }
}

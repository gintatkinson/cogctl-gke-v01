package context_policy;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context_policy.proto")
public class ContextPolicyServiceClient implements ContextPolicyService, MutinyClient<MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub> {

    private final MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub stub;

    public ContextPolicyServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub, MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyContextPolicyServiceGrpc.newMutinyStub(channel));
    }

    private ContextPolicyServiceClient(MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub stub) {
        this.stub = stub;
    }

    public ContextPolicyServiceClient newInstanceWithStub(MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub stub) {
        return new ContextPolicyServiceClient(stub);
    }

    @Override
    public MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request) {
        return stub.listPolicyRuleIds(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request) {
        return stub.listPolicyRules(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request) {
        return stub.getPolicyRule(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request) {
        return stub.setPolicyRule(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request) {
        return stub.removePolicyRule(request);
    }
}

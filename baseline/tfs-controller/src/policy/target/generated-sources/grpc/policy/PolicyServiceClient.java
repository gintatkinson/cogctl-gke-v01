package policy;

import java.util.function.BiFunction;
import io.quarkus.grpc.MutinyClient;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: policy.proto")
public class PolicyServiceClient implements PolicyService, MutinyClient<MutinyPolicyServiceGrpc.MutinyPolicyServiceStub> {

    private final MutinyPolicyServiceGrpc.MutinyPolicyServiceStub stub;

    public PolicyServiceClient(String name, io.grpc.Channel channel, BiFunction<String, MutinyPolicyServiceGrpc.MutinyPolicyServiceStub, MutinyPolicyServiceGrpc.MutinyPolicyServiceStub> stubConfigurator) {
        this.stub = stubConfigurator.apply(name, MutinyPolicyServiceGrpc.newMutinyStub(channel));
    }

    private PolicyServiceClient(MutinyPolicyServiceGrpc.MutinyPolicyServiceStub stub) {
        this.stub = stub;
    }

    public PolicyServiceClient newInstanceWithStub(MutinyPolicyServiceGrpc.MutinyPolicyServiceStub stub) {
        return new PolicyServiceClient(stub);
    }

    @Override
    public MutinyPolicyServiceGrpc.MutinyPolicyServiceStub getStub() {
        return stub;
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request) {
        return stub.policyAddService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request) {
        return stub.policyAddDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request) {
        return stub.policyUpdateService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request) {
        return stub.policyUpdateDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request) {
        return stub.policyDelete(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request) {
        return stub.getPolicyService(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request) {
        return stub.getPolicyDevice(request);
    }

    @Override
    public io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request) {
        return stub.getPolicyByServiceId(request);
    }
}

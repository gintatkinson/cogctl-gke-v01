package policy;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: policy.proto")
public interface PolicyService extends MutinyService {

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddService(policy.Policy.PolicyRuleService request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyAddDevice(policy.Policy.PolicyRuleDevice request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateService(policy.Policy.PolicyRuleService request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyUpdateDevice(policy.Policy.PolicyRuleDevice request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleState> policyDelete(policy.Policy.PolicyRuleId request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleService> getPolicyService(policy.Policy.PolicyRuleId request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleDevice> getPolicyDevice(policy.Policy.PolicyRuleId request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleServiceList> getPolicyByServiceId(context.ContextOuterClass.ServiceId request);
}

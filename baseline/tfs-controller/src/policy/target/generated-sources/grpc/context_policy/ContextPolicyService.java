package context_policy;

import io.quarkus.grpc.MutinyService;

@jakarta.annotation.Generated(value = "by Mutiny Grpc generator", comments = "Source: context_policy.proto")
public interface ContextPolicyService extends MutinyService {

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleIdList> listPolicyRuleIds(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleList> listPolicyRules(context.ContextOuterClass.Empty request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRule> getPolicyRule(policy.Policy.PolicyRuleId request);

    io.smallrye.mutiny.Uni<policy.Policy.PolicyRuleId> setPolicyRule(policy.Policy.PolicyRule request);

    io.smallrye.mutiny.Uni<context.ContextOuterClass.Empty> removePolicyRule(policy.Policy.PolicyRuleId request);
}

/*
 * Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.etsi.tfs.policy.common;

import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;

public class ApplicationProperties {

    public static final String INVALID_MESSAGE = "%s is invalid.";
    public static final String VALID_MESSAGE = "%s is valid.";

    public static final PolicyRuleState INSERTED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_INSERTED, "Successfully entered to INSERTED state");
    public static final PolicyRuleState VALIDATED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_VALIDATED, "Successfully transitioned to VALIDATED state");
    public static final PolicyRuleState PROVISIONED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_PROVISIONED,
                    "Successfully transitioned from VALIDATED to PROVISIONED state");
    public static final PolicyRuleState ACTIVE_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_ACTIVE,
                    "Successfully transitioned from PROVISIONED to ACTIVE state");
    public static final PolicyRuleState ENFORCED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_ENFORCED,
                    "Successfully transitioned from ACTIVE to ENFORCED state");
    public static final PolicyRuleState INEFFECTIVE_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_INEFFECTIVE,
                    "Transitioned from ENFORCED to INEFFECTIVE state");
    public static final PolicyRuleState EFFECTIVE_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_EFFECTIVE,
                    "Successfully transitioned from ENFORCED to EFFECTIVE state");
    public static final PolicyRuleState UPDATED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_UPDATED, "Successfully entered to UPDATED state");
    public static final PolicyRuleState REMOVED_POLICYRULE_STATE =
            new PolicyRuleState(
                    PolicyRuleStateEnum.POLICY_REMOVED, "Successfully entered to REMOVED state");
}

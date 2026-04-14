/*
 * Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.etsi.tfs.policy.policy.model;

public enum PolicyRuleActionEnum {
    POLICY_RULE_ACTION_NO_ACTION,
    POLICY_RULE_ACTION_SET_DEVICE_STATUS,
    POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
    POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT,
    POLICY_RULE_ACTION_CALL_SERVICE_RPC,
    // This is temporary
    POLICY_RULE_ACTION_RECALCULATE_PATH
}

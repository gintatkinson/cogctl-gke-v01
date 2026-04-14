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

import static com.google.common.base.Preconditions.checkArgument;

import java.util.ArrayList;
import java.util.List;
import org.etsi.tfs.policy.common.Util;

public class PolicyRuleDevice extends PolicyRuleBase {

    public PolicyRuleDevice(PolicyRuleBasic policyRuleBasic, List<String> deviceIds) {

        try {
            this.policyRuleBasic = policyRuleBasic;
            checkArgument(!deviceIds.isEmpty(), "Device Ids must not be empty.");
            this.deviceIds = deviceIds;
            this.isValid = true;
        } catch (Exception e) {
            this.policyRuleBasic = policyRuleBasic;
            this.deviceIds = new ArrayList<String>();
            this.isValid = false;
            this.exceptionMessage = e.getMessage();
        }
    }

    public boolean areArgumentsValid() {
        return isValid;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{%s, [%s]}", getClass().getSimpleName(), policyRuleBasic, Util.toString(deviceIds));
    }
}

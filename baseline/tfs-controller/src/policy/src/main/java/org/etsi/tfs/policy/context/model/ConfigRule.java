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

package org.etsi.tfs.policy.context.model;

public class ConfigRule {

    private final ConfigActionEnum configActionEnum;
    private final ConfigRuleType<?> configRuleType;

    public ConfigRule(ConfigActionEnum configActionEnum, ConfigRuleType<?> configRuleType) {
        this.configActionEnum = configActionEnum;
        this.configRuleType = configRuleType;
    }

    public ConfigActionEnum getConfigActionEnum() {
        return configActionEnum;
    }

    public ConfigRuleType getConfigRuleType() {
        return configRuleType;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{configActionEnum:\"%s\", %s}",
                getClass().getSimpleName(), configActionEnum.toString(), configRuleType);
    }
}

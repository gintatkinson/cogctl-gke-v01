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

package org.etsi.tfs.ztp.acl;

import java.util.List;
import org.etsi.tfs.ztp.common.Util;

public class AclRuleSet {

    private final String name;
    private final AclRuleTypeEnum type;
    private final String description;
    private final String userId;
    private final List<AclEntry> entries;

    public AclRuleSet(
            String name,
            AclRuleTypeEnum type,
            String description,
            String userId,
            List<AclEntry> entries) {
        this.name = name;
        this.type = type;
        this.description = description;
        this.userId = userId;
        this.entries = entries;
    }

    public String getName() {
        return name;
    }

    public AclRuleTypeEnum getType() {
        return type;
    }

    public String getDescription() {
        return description;
    }

    public String getUserId() {
        return userId;
    }

    public List<AclEntry> getEntries() {
        return entries;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{name:\"%s\", type:\"%s\", description:\"%s\", userId:\"%s\", [%s]}",
                getClass().getSimpleName(),
                name,
                type.toString(),
                description,
                userId,
                Util.toString(entries));
    }
}

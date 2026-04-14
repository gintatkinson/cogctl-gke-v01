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

package org.etsi.tfs.ztp;

import static org.assertj.core.api.Assertions.assertThat;

import io.quarkus.test.junit.QuarkusTest;
import java.util.List;
import org.etsi.tfs.ztp.acl.AclAction;
import org.etsi.tfs.ztp.acl.AclEntry;
import org.etsi.tfs.ztp.acl.AclForwardActionEnum;
import org.etsi.tfs.ztp.acl.AclLogActionEnum;
import org.etsi.tfs.ztp.acl.AclMatch;
import org.etsi.tfs.ztp.acl.AclRuleSet;
import org.etsi.tfs.ztp.acl.AclRuleTypeEnum;
import org.etsi.tfs.ztp.context.model.ConfigRuleAcl;
import org.etsi.tfs.ztp.context.model.ConfigRuleCustom;
import org.etsi.tfs.ztp.context.model.ConfigRuleTypeAcl;
import org.etsi.tfs.ztp.context.model.ConfigRuleTypeCustom;
import org.etsi.tfs.ztp.context.model.EndPointId;
import org.etsi.tfs.ztp.context.model.TopologyId;
import org.junit.jupiter.api.Test;

@QuarkusTest
class ConfigRuleTypeTest {

    private AclMatch createAclMatch() {

        return new AclMatch(1, 2, "192.168.3.52", "192.168.4.192", 3224, 3845, 5, 10);
    }

    private AclAction createAclAction() {

        return new AclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
    }

    private AclEntry createAclEntry(AclMatch aclMatch, AclAction aclAction) {

        return new AclEntry(1, "aclEntryDescription", aclMatch, aclAction);
    }

    @Test
    void shouldExtractConfigRuleCustomFromConfigRuleTypeCustom() {
        final var resourceKey = "resourceKey";
        final var resourceValue = "resourceValue";

        final var expectedConfigRuleCustom = new ConfigRuleCustom(resourceKey, resourceValue);
        final var configRuleTypeCustom = new ConfigRuleTypeCustom(expectedConfigRuleCustom);

        assertThat(configRuleTypeCustom.getConfigRuleType()).isEqualTo(expectedConfigRuleCustom);
    }

    @Test
    void shouldExtractConfigRuleAclFromConfigRuleTypeAcl() {
        final var contextIdUuid = "contextId";
        final var topologyIdUuid = "topologyUuid";
        final var deviceIdUuid = "deviceIdUuid";
        final var endpointIdUuid = "endpointIdUuid";

        final var topologyId = new TopologyId(contextIdUuid, topologyIdUuid);
        final var endPointId = new EndPointId(topologyId, deviceIdUuid, endpointIdUuid);

        final var aclMatch = createAclMatch();
        final var aclAction = createAclAction();
        final var aclEntry = createAclEntry(aclMatch, aclAction);

        final var aclRuleSet =
                new AclRuleSet(
                        "aclRuleName", AclRuleTypeEnum.IPV4, "AclRuleDescription", "userId", List.of(aclEntry));

        final var expectedConfigRuleAcl = new ConfigRuleAcl(endPointId, aclRuleSet);
        final var configRuleTypeAcl = new ConfigRuleTypeAcl(expectedConfigRuleAcl);

        assertThat(configRuleTypeAcl.getConfigRuleType()).isEqualTo(expectedConfigRuleAcl);
    }
}

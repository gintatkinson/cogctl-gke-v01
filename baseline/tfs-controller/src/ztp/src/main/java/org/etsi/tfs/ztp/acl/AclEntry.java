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

public class AclEntry {

    private final int sequenceId;
    private final String description;
    private final AclMatch match;
    private final AclAction action;

    public AclEntry(int sequenceId, String description, AclMatch match, AclAction action) {
        this.sequenceId = sequenceId;
        this.description = description;
        this.match = match;
        this.action = action;
    }

    public int getSequenceId() {
        return sequenceId;
    }

    public String getDescription() {
        return description;
    }

    public AclMatch getMatch() {
        return match;
    }

    public AclAction getAction() {
        return action;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{sequenceId:\"%d\", description:\"%s\", %s, %s}",
                getClass().getSimpleName(), sequenceId, description, match, action);
    }
}

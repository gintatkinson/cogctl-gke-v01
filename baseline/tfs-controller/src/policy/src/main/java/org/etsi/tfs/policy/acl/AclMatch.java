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

package org.etsi.tfs.policy.acl;

public class AclMatch {

    private final int dscp;
    private final int protocol;
    private final String srcAddress;
    private final String dstAddress;
    private final int srcPort;
    private final int dstPort;
    private final int startMplsLabel;
    private final int endMplsLabel;

    public AclMatch(
            int dscp,
            int protocol,
            String srcAddress,
            String dstAddress,
            int srcPort,
            int dstPort,
            int startMplsLabel,
            int endMplsLabel) {
        this.dscp = dscp;
        this.protocol = protocol;
        this.srcAddress = srcAddress;
        this.dstAddress = dstAddress;
        this.srcPort = srcPort;
        this.dstPort = dstPort;
        this.startMplsLabel = startMplsLabel;
        this.endMplsLabel = endMplsLabel;
    }

    public int getDscp() {
        return dscp;
    }

    public int getProtocol() {
        return protocol;
    }

    public String getSrcAddress() {
        return srcAddress;
    }

    public String getDstAddress() {
        return dstAddress;
    }

    public int getSrcPort() {
        return srcPort;
    }

    public int getDstPort() {
        return dstPort;
    }

    public int getStartMplsLabel() {
        return startMplsLabel;
    }

    public int getEndMplsLabel() {
        return endMplsLabel;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{dscp:\"%d\", protocol:\"%d\", srcAddress:\"%s\", dstAddress:\"%s\", srcPort:\"%d\", dstPort:\"%d\", startMplsLabel:\"%d\", endMplsLabel:\"%d\"}",
                getClass().getSimpleName(),
                dscp,
                protocol,
                srcAddress,
                dstAddress,
                srcPort,
                dstPort,
                startMplsLabel,
                endMplsLabel);
    }
}

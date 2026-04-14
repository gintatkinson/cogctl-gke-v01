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

package org.etsi.tfs.policy.monitoring.model;

import java.util.List;
import org.etsi.tfs.policy.common.Util;

public class AlarmResponse {

    private final String alarmId;

    private final List<Kpi> kpiList;

    public AlarmResponse(String alarmId, List<Kpi> kpiList) {
        this.alarmId = alarmId;
        this.kpiList = kpiList;
    }

    public String getAlarmId() {
        return alarmId;
    }

    public List<Kpi> getKpiList() {
        return kpiList;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{alarmId:\"%s\", %s}", getClass().getSimpleName(), alarmId, Util.toString(kpiList));
    }
}

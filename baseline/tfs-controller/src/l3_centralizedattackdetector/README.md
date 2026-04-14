# L3 Centralized Attack Detector

Receives snapshot statistics from Distributed Attack Detector component and performs an inference to detect attacks.
It then sends the detected attacks to the Attack Mitigator component for them to be mitigated.

## Functions: 
- AnalyzeConnectionStatistics(L3CentralizedattackdetectorMetrics) -> StatusMessage
- AnalyzeBatchConnectionStatistics(L3CentralizedattackdetectorBatchInput) -> StatusMessage
- GetFeaturesIds(Empty) -> AutoFeatures
- SetAttackIPs(AttackIPs) -> Empty

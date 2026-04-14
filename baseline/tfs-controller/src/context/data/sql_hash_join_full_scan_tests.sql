-- Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

-- When inserting config rules, for instance related to device
--   If we insert few rules (3~4 rows), does a lookup join with more rows does hash join which is less performant...
--   To be investigated...

-----------------------------------------------------------------------------------------------------
-- Scenario: tests database with device and device_configrule tables

CREATE DATABASE tests;
USE tests;

CREATE TYPE public.orm_deviceoperationalstatusenum AS ENUM ('UNDEFINED', 'DISABLED', 'ENABLED');
CREATE TYPE public.orm_devicedriverenum AS ENUM ('UNDEFINED', 'OPENCONFIG', 'TRANSPORT_API', 'P4', 'IETF_NETWORK_TOPOLOGY', 'ONF_TR_352', 'XR', 'IETF_L2VPN', 'SMARTNIC');
CREATE TYPE public.configrulekindenum AS ENUM ('CUSTOM', 'ACL');
CREATE TYPE public.orm_configactionenum AS ENUM ('UNDEFINED', 'SET', 'DELETE');

CREATE TABLE public.device (
  device_uuid UUID NOT NULL,
  device_name VARCHAR NOT NULL,
  device_type VARCHAR NOT NULL,
  device_operational_status public.orm_deviceoperationalstatusenum NOT NULL,
  device_drivers public.orm_devicedriverenum[] NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  CONSTRAINT device_pkey PRIMARY KEY (device_uuid ASC)
);

CREATE TABLE public.device_configrule (
  configrule_uuid UUID NOT NULL,
  device_uuid UUID NOT NULL,
  "position" INT8 NOT NULL,
  kind public.configrulekindenum NOT NULL,
  action public.orm_configactionenum NOT NULL,
  data VARCHAR NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  CONSTRAINT device_configrule_pkey PRIMARY KEY (configrule_uuid ASC),
  CONSTRAINT device_configrule_device_uuid_fkey FOREIGN KEY (device_uuid) REFERENCES public.device(device_uuid) ON DELETE CASCADE,
  INDEX device_configrule_device_uuid_rec_idx (device_uuid ASC) STORING ("position", kind, action, data, created_at, updated_at),
  CONSTRAINT check_position_value CHECK ("position" >= 0:::INT8)
);

-----------------------------------------------------------------------------------------------------
-- Populate devices

INSERT INTO device (device_uuid, device_name, device_type, device_operational_status, device_drivers, created_at, updated_at) VALUES
('a3645f8a-5f1f-4d91-8b11-af4104e57f52'::UUID, 'R1', 'router', 'ENABLED', ARRAY['UNDEFINED'], '2023-04-21 07:51:00.0', '2023-04-21 07:51:00.0'),
('7c1e923c-145c-48c5-8016-0d1f596cb4c1'::UUID, 'R2', 'router', 'ENABLED', ARRAY['UNDEFINED'], '2023-04-21 07:51:00.0', '2023-04-21 07:51:00.0')
ON CONFLICT (device_uuid) DO UPDATE SET
device_name=excluded.device_name,
device_operational_status=excluded.device_operational_status,
updated_at=excluded.updated_at
RETURNING device.created_at, device.updated_at;

-----------------------------------------------------------------------------------------------------
-- Examine insertion of config rules...

-- Helpful commands:
--   ANALYZE (VERBOSE, TYPES) <statement>
--   EXPLAIN (VERBOSE, TYPES) <statement>

-- Rows with realistic data
EXPLAIN (TYPES, VERBOSE) INSERT INTO device_configrule (configrule_uuid, device_uuid, position, kind, action, data, created_at, updated_at) VALUES
('5491b521-76a2-57c4-b622-829131374b4b', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 0, 'CUSTOM', 'SET', '{"resource_key": "_connect/address", "resource_value": "127.0.0.1"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('1f39fb84-2337-5735-a873-2bc7cd50bdd2', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 1, 'CUSTOM', 'SET', '{"resource_key": "_connect/port", "resource_value": "0"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('5d4c72f9-7acc-5ab2-a41e-0d4bc625943e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 2, 'CUSTOM', 'SET', '{"resource_key": "_connect/settings", "resource_value": "{\\n\\"endpoints\\": [\\n{\\n\\"sample_types\\": [],\\n\\"type\\": \\"copper\\",\\n\\"uuid\\ ... (573 characters truncated) ... "type\\": \\"copper\\",\\n\\"uuid\\": \\"2/5\\"\\n},\\n{\\n\\"sample_types\\": [],\\n\\"type\\": \\"copper\\",\\n\\"uuid\\": \\"2/6\\"\\n}\\n]\\n}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('d14c3fc7-4998-5707-b1c4-073d553a86ef', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 3, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[1/1]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"1/1\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('e3268fba-e695-59d0-b26e-014930f416fd', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 4, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[1/2]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"1/2\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('043eb444-81c8-5ac9-83df-0c6a74bad534', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 5, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[1/3]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"1/3\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('df79d0ea-bcda-57fc-8926-e9a9257628dd', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 6, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/1]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/1\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('94f41adc-1041-5a8a-81f5-1224d884ae57', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 7, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/2]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/2\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('b27c0207-dc43-59db-a856-74aaab4f1a19', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 8, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/3]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/3\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('5902903f-0be4-5ec6-a133-c3e2f9ae05a6', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 9, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/4]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/4\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('eb20a698-99f2-5369-a228-610cd289297a', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 10, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/5]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/5\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('3a73b766-195c-59ec-a66e-d32391bc35a3', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 11, 'CUSTOM', 'SET', '{"resource_key": "/endpoints/endpoint[2/6]", "resource_value": "{\\"sample_types\\": {}, \\"type\\": \\"copper\\", \\"uuid\\": \\"2/6\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('353ba35c-5ec6-5f38-8ca9-e6c024772282', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 12, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:126]", "resource_value": "{\\"name\\": \\"ELAN-AC:126\\", \\"type\\": \\"L2VSI\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('45582643-09a1-5ade-beac-2bf057549d38', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 13, 'CUSTOM', 'SET', '{"resource_key": "/interface[2/4.126]/subinterface[0]", "resource_value": "{\\"index\\": 0, \\"name\\": \\"2/4.126\\", \\"type\\": \\"l2vlan\\", \\"vlan_id\\": 26}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9484afcd-b010-561e-ba83-6b0654d8816c', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 14, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:126]/interface[2/4.126]", "resource_value": "{\\"id\\": \\"2/4.126\\", \\"interface\\": \\"2/4.126\\", \\"name\\": \\"ELAN-AC:126\\", \\"subinterface\\": 0}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('f1cc8161-eaee-5139-a3e5-207fbe11800d', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 15, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:126]/connection_point[VC-1]", "resource_value": "{\\"VC_ID\\": \\"126\\", \\"connection_point\\": \\"VC-1\\", \\"name\\": \\"ELAN-AC:126\\", \\"remote_system\\": \\"10.0.0.6\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('f1836e1d-74a1-51be-944f-a2cedc297812', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 16, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:128]", "resource_value": "{\\"name\\": \\"ELAN-AC:128\\", \\"type\\": \\"L2VSI\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('86f152ea-6abf-5bd4-b2c8-eddfe2826847', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 17, 'CUSTOM', 'SET', '{"resource_key": "/interface[1/2.128]/subinterface[0]", "resource_value": "{\\"index\\": 0, \\"name\\": \\"1/2.128\\", \\"type\\": \\"l2vlan\\", \\"vlan_id\\": 28}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('c36e9d88-0ee3-5826-9a27-3b25a7520121', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 18, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:128]/interface[1/2.128]", "resource_value": "{\\"id\\": \\"1/2.128\\", \\"interface\\": \\"1/2.128\\", \\"name\\": \\"ELAN-AC:128\\", \\"subinterface\\": 0}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('a9d4c170-ca55-5969-8329-5bbbceec5bd6', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 19, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:128]/connection_point[VC-1]", "resource_value": "{\\"VC_ID\\": \\"128\\", \\"connection_point\\": \\"VC-1\\", \\"name\\": \\"ELAN-AC:128\\", \\"remote_system\\": \\"10.0.0.3\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('d86ceb87-e87a-5b1d-b3d9-15af96233500', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 20, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:136]", "resource_value": "{\\"name\\": \\"ELAN-AC:136\\", \\"type\\": \\"L2VSI\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('cef724a0-3a51-5dd7-b9e5-bde174f4a8d2', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 21, 'CUSTOM', 'SET', '{"resource_key": "/interface[2/6.136]/subinterface[0]", "resource_value": "{\\"index\\": 0, \\"name\\": \\"2/6.136\\", \\"type\\": \\"l2vlan\\", \\"vlan_id\\": 36}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9a01ca29-4ef6-50f3-84f0-a219e7c1689e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 22, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:136]/interface[2/6.136]", "resource_value": "{\\"id\\": \\"2/6.136\\", \\"interface\\": \\"2/6.136\\", \\"name\\": \\"ELAN-AC:136\\", \\"subinterface\\": 0}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9212773d-6a4f-5cce-ae5b-85adfdf6674e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 23, 'CUSTOM', 'SET', '{"resource_key": "/network_instance[ELAN-AC:136]/connection_point[VC-1]", "resource_value": "{\\"VC_ID\\": \\"136\\", \\"connection_point\\": \\"VC-1\\", \\"name\\": \\"ELAN-AC:136\\", \\"remote_system\\": \\"10.0.0.2\\"}"}', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892')
ON CONFLICT (configrule_uuid) DO UPDATE SET position = excluded.position, action = excluded.action, data = excluded.data, updated_at = excluded.updated_at
RETURNING device_configrule.created_at, device_configrule.updated_at;


-- Rows with empty data (still does full scan and hash join)
-- If only 3~4 rows are inserted it does lookup join...
EXPLAIN INSERT INTO device_configrule (configrule_uuid, device_uuid, position, kind, action, data, created_at, updated_at) VALUES
('5491b521-76a2-57c4-b622-829131374b4b', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 0, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('1f39fb84-2337-5735-a873-2bc7cd50bdd2', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 1, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('5d4c72f9-7acc-5ab2-a41e-0d4bc625943e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 2, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('d14c3fc7-4998-5707-b1c4-073d553a86ef', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 3, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('e3268fba-e695-59d0-b26e-014930f416fd', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 4, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('043eb444-81c8-5ac9-83df-0c6a74bad534', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 5, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('df79d0ea-bcda-57fc-8926-e9a9257628dd', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 6, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('94f41adc-1041-5a8a-81f5-1224d884ae57', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 7, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('b27c0207-dc43-59db-a856-74aaab4f1a19', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 8, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('5902903f-0be4-5ec6-a133-c3e2f9ae05a6', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 9, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('eb20a698-99f2-5369-a228-610cd289297a', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 10, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('3a73b766-195c-59ec-a66e-d32391bc35a3', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 11, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('353ba35c-5ec6-5f38-8ca9-e6c024772282', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 12, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('45582643-09a1-5ade-beac-2bf057549d38', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 13, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9484afcd-b010-561e-ba83-6b0654d8816c', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 14, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('f1cc8161-eaee-5139-a3e5-207fbe11800d', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 15, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('f1836e1d-74a1-51be-944f-a2cedc297812', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 16, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('86f152ea-6abf-5bd4-b2c8-eddfe2826847', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 17, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('c36e9d88-0ee3-5826-9a27-3b25a7520121', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 18, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('a9d4c170-ca55-5969-8329-5bbbceec5bd6', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 19, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('d86ceb87-e87a-5b1d-b3d9-15af96233500', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 20, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('cef724a0-3a51-5dd7-b9e5-bde174f4a8d2', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 21, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9a01ca29-4ef6-50f3-84f0-a219e7c1689e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 22, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892'),
('9212773d-6a4f-5cce-ae5b-85adfdf6674e', 'a3645f8a-5f1f-4d91-8b11-af4104e57f52', 23, 'CUSTOM', 'SET', '', '2023-04-20 17:33:54.044892', '2023-04-20 17:33:54.044892')
ON CONFLICT (configrule_uuid) DO UPDATE SET position = excluded.position, action = excluded.action, data = excluded.data, updated_at = excluded.updated_at
RETURNING device_configrule.created_at, device_configrule.updated_at;

# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import hashlib
import uuid
import xml.dom.minidom, xmltodict

def xml_pretty_print(data : str):
    return xml.dom.minidom.parseString(data).toprettyxml()

def xml_to_file(data : str, file_path : str) -> None:
    with open(file_path, mode='w', encoding='UTF-8') as f:
        f.write(xml_pretty_print(data))

def xml_to_dict(data : str):
    return xmltodict.parse(data)

def generate_uuid_from_numbers(code:str) ->str:
    # Concatenate the numbers into a single string


    # Generate a hash value using MD5 algorithm
    hash_value = hashlib.md5(code.encode()).hexdigest()

    # Convert the hash value into a UUID
    generated_uuid = uuid.UUID(hash_value)

    return str(generated_uuid)

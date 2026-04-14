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

import requests

url = "http://localhost:8002/tfs-api/link/CSGW1_xe5-CSGW2_xe5"

payload = ""
headers = {"cookie": "session%3Aaa82129ced5debbb=eyJjc3JmX3Rva2VuIjoiZGI1ZjY5Yjg0MDgxMjk3YmU3ZTY2MDMxZTljYzdiYTZmMWVjZjc0NCJ9.ZijdlQ.xdcOryRyoRgXCJ2XYwczsHw4yIQ; session%3A53cf1bf28136ee51=eyJjc3JmX3Rva2VuIjoiMDFlNWQwNzUyNDM3MDU1NWZhZjE3MGFiYzg4NGY2YmE3Y2M5MjM4OCJ9.ZikGzQ.KkIdiPPvqaO2pyBi7-mnlTKnmWs; session%3Ae52730446648c30a=eyJjc3JmX3Rva2VuIjoiODI4NTUwOTc4MWMxYzVjNmQ2ZDBiNGViMmU4ZDJmMzYzMzUxY2M2OSJ9.ZyOPuA.LWyhgLGjWOCb1H6wKlsG0evCV-A"}

response = requests.request("DELETE", url, data=payload, headers=headers)

print(response.text)
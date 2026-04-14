#!/bin/bash -eu
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

# Make folder containing the script the root folder for its execution
cd $(dirname $0)

mkdir -p src/python
rm -rf src/python/*.py

tee src/python/__init__.py << EOF > /dev/null
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
EOF

# Generate Python code
python3 -m grpc_tools.protoc -I=./ --python_out=src/python/ --grpc_python_out=src/python/ *.proto

# new line added to generate protobuf for the `grpclib` library
python3 -m grpc_tools.protoc -I=./ --python_out=src/python/asyncio --grpclib_python_out=src/python/asyncio *.proto

# Arrange generated code imports to enable imports from arbitrary subpackages
find src/python -type f -iname *.py -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} \;

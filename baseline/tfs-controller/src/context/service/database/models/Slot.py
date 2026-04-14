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

from sqlalchemy.types import  TypeDecorator, Integer

class SlotType(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value, dialect):
        if value is not None:
            bin_num = "0b"
            for i,(key,val) in enumerate(value.items()):
                bin_num =bin_num + f"{val}"
            int_num = int(bin_num,2)  
        return int_num

    def process_result_value(self, value, dialect):
        if value is not None:
            slot = dict()
            bin_num = bin(value)
            sliced_num = bin_num[2:]
            for i in range(len(sliced_num)):
                slot[str(i+1)]=int(sliced_num[i])
        return slot

class C_Slot(SlotType):
    start_point = 0

    def process_result_value(self, value, dialect):
        if value is not None:
            slot = dict()
            bin_num = bin(value)
            sliced_num = bin_num[2:]
            if (len(sliced_num) != 20) :
                for i in range(0,20 - len(sliced_num)):
                    sliced_num = '0' + sliced_num
            for i in range(len(sliced_num)):
                slot[str(self.start_point+i+1)]=int(sliced_num[i])
        return slot

class L_Slot (SlotType):
    start_point = 100

    def process_result_value(self, value, dialect):
        if value is not None:
            slot = dict()
            bin_num = bin(value)
            sliced_num = bin_num[2:]
            if (len(sliced_num) != 20) :
                for i in range(0,20 - len(sliced_num)):
                    sliced_num='0'+sliced_num
            for i in range(len(sliced_num)):
                slot[str(self.start_point+i+1)]=int(sliced_num[i])
        return slot

class S_Slot (SlotType):
    start_point = 500

    def process_result_value(self, value, dialect):
        if value is not None:
            slot= dict()
            bin_num = bin(value)
            sliced_num=bin_num[2:]
            if (len(sliced_num) != 20) :
                for i in range(0,20 - len(sliced_num)):
                    sliced_num='0'+sliced_num
            for i in range(len(sliced_num)):
                slot[str(self.start_point+i+1)]=int(sliced_num[i])
        return slot

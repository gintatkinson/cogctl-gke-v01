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

import copy

def convert_to_dict(single_val:int)->dict:
    slot= dict()
    bin_num = bin(single_val)
    sliced_num=bin_num[2:]
    for i in range(len(sliced_num)):
        slot[str(i+1)]=int(sliced_num[i])
    return slot

def correct_slot(dic: dict) -> dict:
    _dict = copy.deepcopy(dic)
    keys_list = list(_dict.keys())
    if len(keys_list) < 20:
        num_keys = [int(i) for i in keys_list]
        if num_keys[-1] != 20:
            missed_keys = []
            diff = 20 - len(num_keys)
            #print(f"diff {diff}")
            for i in range(diff+1):
                missed_keys.append(num_keys[-1]+i)
            #print(f"missed_keys {missed_keys}")
            for key in missed_keys :
                _dict[key]=1
            #print(f"result {_dict}")
    return _dict


## To be deleted , needed now for development purpose ## 

def order_list (lst:list[tuple])->list:
    if (len(lst)<=1):
        return lst
    else :
        pivot,bit_val =lst[0]
        lst_smaller = []
        lst_greater = []
        for element in lst[1:]:
            key,val=element
            if (key <= pivot):
                lst_smaller.append(element)
            else :
                lst_greater.append(element)
        return order_list(lst_smaller) + [(pivot,bit_val)] + order_list(lst_greater)

def list_to_dict (lst:list[tuple[int,int]])->dict:
    dct = dict()
    for ele in lst :
        key,value = ele
        dct[str(key)]=value
    return dct

def order_dict (dct:dict)->dict:
    lst = list()
    for key,value in sorted(dct.items()):
        lst.append((int(key),value))
    ordered_lst= order_list(lst)
    if (len(ordered_lst)>0):
        return list_to_dict (ordered_lst)

def order_dict_v1 (dct:dict)->dict:
    lst = list()
    for key,value in dct.items():
        lst.append((int(key),value))
    ordered_lst= order_list(lst)
    if (len(ordered_lst)>0):
        return list_to_dict (ordered_lst)

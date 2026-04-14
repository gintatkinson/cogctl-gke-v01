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

import grpc, logging
from typing import Dict, List, Set, Tuple
from common.Checkers import chk_string
from common.exceptions.ServiceException import ServiceException
from common.proto.context_pb2 import Constraint

def check_constraint(
    logger : logging.Logger, constraint_number : int, parent_name : str, constraint : Constraint,
    add_constraints : Dict[str, Dict[str, Set[str]]]) -> Tuple[str, str]:

    try:
        constraint_type  = chk_string('constraint[#{}].constraint_type'.format(constraint_number),
                                      constraint.constraint_type,
                                      allow_empty=False)
        constraint_value = chk_string('constraint[#{}].constraint_value'.format(constraint_number),
                                      constraint.constraint_value,
                                      allow_empty=False)
    except Exception as e:
        logger.exception('Invalid arguments:')
        raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    if constraint_type in add_constraints:
        msg = 'Duplicated ConstraintType({}) in {}.'
        msg = msg.format(constraint_type, parent_name)
        raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, msg)

    add_constraints[constraint_type] = constraint_value
    return constraint_type, constraint_value

def check_constraints(logger : logging.Logger, parent_name : str, constraints):
    add_constraints : Dict[str, str] = {}
    constraint_tuples : List[Tuple[str, str]] = []
    for constraint_number,constraint in enumerate(constraints):
        _parent_name = 'Constraint(#{}) of {}'.format(constraint_number, parent_name)
        constraint_type, constraint_value = check_constraint(
            logger, constraint_number, _parent_name, constraint, add_constraints)
        constraint_tuples.append((constraint_type, constraint_value))
    return constraint_tuples

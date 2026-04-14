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

from sqlalchemy import Column, DateTime, String
from sqlalchemy import Column, Float, BigInteger, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base


class SubscriptionModel(_Base):
    __tablename__ = 'subscription'

    subscription_uuid = Column(UUID(as_uuid=False), primary_key=True,    server_default=text('gen_random_uuid()'))
    subscription_id   = Column(BigInteger,  nullable=False, unique=True, server_default=text('unique_rowid()'))
    datastore         = Column(String,      nullable=False, unique=False)
    xpath_filter      = Column(String,      nullable=False, unique=False)
    period            = Column(Float,       nullable=False, unique=False)
    created_at        = Column(DateTime,    nullable=False)
    updated_at        = Column(DateTime,    nullable=False)

    sub_subscriptions = relationship('SubSubscriptionModel')

    def dump(self) -> Dict:
        return {
            'subscription_uuid': self.subscription_uuid,
            'subscription_id'  : self.subscription_id,
            'datastore'        : self.datastore,
            'xpath_filter'     : self.xpath_filter,
            'period'           : self.period,
        }

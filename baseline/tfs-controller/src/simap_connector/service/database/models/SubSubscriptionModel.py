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

from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Dict
from ._Base import _Base


class SubSubscriptionModel(_Base):
    __tablename__ = 'sub_subscription'

    parent                = Column(ForeignKey('subscription.subscription_uuid', ondelete='CASCADE'), primary_key=True)
    sub_subscription_uuid = Column(UUID(as_uuid=False), primary_key=True, server_default=text('gen_random_uuid()'))
    controller_uuid       = Column(String,      nullable=False, unique=False)
    datastore             = Column(String,      nullable=False, unique=False)
    xpath_filter          = Column(String,      nullable=False, unique=False)
    period                = Column(Float,       nullable=False, unique=False)
    sub_subscription_id   = Column(BigInteger,  nullable=False, unique=False)
    sub_subscription_uri  = Column(String,      nullable=False, unique=False)
    collector_name        = Column(String,      nullable=False, unique=False)
    created_at            = Column(DateTime,    nullable=False)
    updated_at            = Column(DateTime,    nullable=False)

    subscription = relationship('SubscriptionModel', back_populates='sub_subscriptions')

    def dump(self) -> Dict:
        return {
            'parent_subscription_uuid' : self.parent,
            'sub_subscription_uuid'    : self.sub_subscription_uuid,
            'controller_uuid'          : self.controller_uuid,
            'datastore'                : self.datastore,
            'xpath_filter'             : self.xpath_filter,
            'period'                   : self.period,
            'sub_subscription_id'      : self.sub_subscription_id,
            'sub_subscription_uri'     : self.sub_subscription_uri,
            'collector_name'           : self.collector_name,
        }

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


# RFC 8639 - Subscription to YANG Notifications
# Ref: https://datatracker.ietf.org/doc/html/rfc8639

# RFC 8641 - Subscription to YANG Notifications for Datastore Updates
# Ref: https://datatracker.ietf.org/doc/html/rfc8641


from nbi.service.NbiApplication import NbiApplication
from .AffectSampleSynthesizer import AffectSampleSynthesizer
from .EstablishSubscription import EstablishSubscription
from .DeleteSubscription import DeleteSubscription
from .StreamSubscription import StreamSubscription

def register_telemetry_subscription(nbi_app: NbiApplication):
    nbi_app.add_rest_api_resource(
        EstablishSubscription,
        '/restconf/operations/subscriptions:establish-subscription',
        '/restconf/operations/subscriptions:establish-subscription/',
        endpoint='sse.establish',
    )
    nbi_app.add_rest_api_resource(
        DeleteSubscription,
        '/restconf/operations/subscriptions:delete-subscription',
        '/restconf/operations/subscriptions:delete-subscription/',
        endpoint='sse.delete',
    )
    nbi_app.add_rest_api_resource(
        StreamSubscription,
        '/restconf/stream/<int:subscription_id>',
        '/restconf/stream/<int:subscription_id>/',
        endpoint='sse.stream',
    )
    nbi_app.add_rest_api_resource(
        AffectSampleSynthesizer,
        '/restconf/operations/affect_sample_synthesizer',
        '/restconf/operations/affect_sample_synthesizer/',
        endpoint='sse.affect_sample_synthesizer',
    )

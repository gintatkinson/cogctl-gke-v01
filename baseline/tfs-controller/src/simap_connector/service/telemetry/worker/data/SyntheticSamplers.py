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


import math, random, sys, threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional
from .Sample import Sample


@dataclass
class SyntheticSampler:
    amplitude   : float = field(default=0.0)
    phase       : float = field(default=0.0)
    period      : float = field(default=1.0)
    offset      : float = field(default=0.0)
    noise_ratio : float = field(default=0.0)
    min_value   : float = field(default=-sys.float_info.max)
    max_value   : float = field(default=sys.float_info.max)

    @classmethod
    def create_random(
        cls, amplitude_scale : float, phase_scale : float, period_scale : float,
        offset_scale : float, noise_ratio : float,
        min_value : Optional[float] = None, max_value : Optional[float] = None
    ) -> 'SyntheticSampler':
        amplitude  = amplitude_scale * random.random()
        phase      = phase_scale     * random.random()
        period     = period_scale    * random.random()
        offset     = offset_scale    * random.random() + amplitude
        if min_value is None: min_value = -sys.float_info.max
        if max_value is None: max_value = sys.float_info.max
        return cls(amplitude, phase, period, offset, noise_ratio, min_value, max_value)

    def get_sample(self) -> Sample:
        timestamp = datetime.timestamp(datetime.utcnow())

        waveform = math.sin(2 * math.pi * timestamp / self.period + self.phase)
        waveform *= self.amplitude
        waveform += self.offset

        noise = self.amplitude * random.random()
        value = abs((1.0 - self.noise_ratio) * waveform + self.noise_ratio * noise)

        value = max(value, self.min_value)
        value = min(value, self.max_value)

        return Sample(timestamp, 0, value)


class SyntheticSamplers:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._samplers : Dict[str, SyntheticSampler] = dict()

    def add_sampler(
        self, sampler_name : str, amplitude_scale : float, phase_scale : float,
        period_scale : float, offset_scale : float, noise_ratio : float
    ) -> None:
        with self._lock:
            if sampler_name in self._samplers:
                MSG = 'SyntheticSampler({:s}) already exists'
                raise Exception(MSG.format(sampler_name))
            self._samplers[sampler_name] = SyntheticSampler.create_random(
                amplitude_scale, phase_scale, period_scale, offset_scale, noise_ratio
            )

    def remove_sampler(self, sampler_name : str) -> None:
        with self._lock:
            self._samplers.pop(sampler_name, None)

    def get_sample(self, sampler_name : str) -> Sample:
        with self._lock:
            sampler = self._samplers.get(sampler_name)
            if sampler_name not in self._samplers:
                MSG = 'SyntheticSampler({:s}) does not exist'
                raise Exception(MSG.format(sampler_name))
            return sampler.get_sample()

# Copyright 2020 Norwegian University of Science and Technology.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from dataclasses import dataclass


@dataclass
class JointTrajectoryPoint:
    position: List[float]
    velocity: List[float]
    acceleration: List[float]
    effort: List[float]
    time_from_start: float

    def __init__(
        self,
        position: List[float] = [],
        velocity: List[float] = [],
        acceleration: List[float] = [],
        effort: List[float] = [],
        time_from_start: float = 0.0,
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.effort = effort
        self.time_from_start = time_from_start


@dataclass
class JointTrajectory:
    joint_names: List[str]
    points: List[JointTrajectoryPoint]

    def __init__(
        self, joint_names: List[str] = [], points: List[JointTrajectoryPoint] = []
    ) -> None:
        self.joint_names = joint_names
        self.points = points
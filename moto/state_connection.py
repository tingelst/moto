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

from typing import List, Callable
from copy import deepcopy
from threading import Thread, Lock

from moto.simple_message_connection import SimpleMessageConnection
from moto.simple_message import (
    JointFeedback,
    JointFeedbackEx,
    MsgType, RobotStatus,
    SimpleMessage,
    MOT_MAX_GR,
)


class StateConnection(SimpleMessageConnection):

    TCP_PORT_STATE = 50241

    def __init__(self, ip_address: str):
        super().__init__((ip_address, self.TCP_PORT_STATE))

        self._joint_feedback: List[JointFeedback] = [
            None
        ] * MOT_MAX_GR  # Max controllable groups

        self._joint_feedback_ex = None
        self._robot_status = None
        self._lock: Lock = Lock()

        self._joint_feedback_callbacks: List[Callable] = []
        self._joint_feedback_ex_callbacks: List[Callable] = []

        self._worker_thread: Thread = Thread(target=self._worker)
        self._worker_thread.daemon = True

    def joint_feedback(self, groupno: int) -> JointFeedback:
        with self._lock:
            return deepcopy(self._joint_feedback[groupno])

    def joint_feedback_ex(self) -> JointFeedbackEx:
        with self._lock:
            return deepcopy(self._joint_feedback_ex)

    def robot_status(self) -> RobotStatus:
        with self._lock:
            return deepcopy(self._robot_status)

    def add_joint_feedback_msg_callback(self, callback: Callable):
        self._joint_feedback_callbacks.append(callback)

    def add_joint_feedback_ex_msg_callback(self, callback: Callable):
        self._joint_feedback_ex_callbacks.append(callback)

    def start(self) -> None:
        self._tcp_client.connect()
        self._worker_thread.start()

    def stop(self) -> None:
        pass

    def _worker(self) -> None:
        while True:
            msg: SimpleMessage = self.recv()
            if msg.header.msg_type == MsgType.JOINT_FEEDBACK:
                with self._lock:
                    self._joint_feedback[msg.body.groupno] = deepcopy(msg.body)
                    for callback in self._joint_feedback_callbacks:
                        callback(deepcopy(msg.body))

            elif msg.header.msg_type == MsgType.MOTO_JOINT_FEEDBACK_EX:
                with self._lock:
                    self._joint_feedback_ex = deepcopy(msg.body)
                    for callback in self._joint_feedback_ex_callbacks:
                        callback(deepcopy(msg.body))

            elif msg.header.msg_type == MsgType.ROBOT_STATUS:
                with self._lock:
                    self._robot_status = deepcopy(msg.body)



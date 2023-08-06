from dataclasses import dataclass
from typing import *
from enum import Enum

@dataclass
class CanMessage:
    timestamp: float
    msg_id: int
    data: bytearray
    is_extended_id: bool


class CanMessageCollection:

    def __init__(self, existing_messages=None):
        self.messages = [] if existing_messages is None else existing_messages

    def add(self, message: CanMessage):
        self.messages.append(message)

    def add_or_update(self, message: CanMessage):
        for i, data in enumerate(self.messages):
            if data.msg_id == message.msg_id:
                self.messages[i] = message
                break
        else:
            self.add(message)

    def clear(self, msg_ids=None):
        if msg_ids is None:
            # clear all
            self.messages = []
        else:
            self.messages = [message for message in self.messages if message.msg_id not in msg_ids]

    def filter(self, predicate):
        return CanMessageCollection([message for message in self.messages if predicate(message.msg_id)])

    @property
    def first(self) -> CanMessage:
        return self.messages[0]

    @property
    def last(self) -> CanMessage:
        return self.messages[-1]

    @property
    def sorted_by_id(self) -> List[CanMessage]:
        return sorted(self.messages, key=lambda x: x.msg_id)

    @property
    def is_valid(self) -> bool:
        first_is_sync = self.first.msg_id == 0
        received_within_window = self.window_us < 2500
        return True # first_is_sync and received_within_window

    @property
    def window_us(self) -> int:
        return int((self.last.timestamp - self.first.timestamp) * 1e6)

    @property
    def ids(self) -> List[int]:
        return set(i.msg_id for i in  self.messages)

    def __len__(self):
        return len(self.messages)


class SensorModel(Enum):

    SCHA63T = 1
    BMX160 = 2
    SCLxxxx = 3
    PI48 = 4
    NotApplicable = 999

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class SensorDataType(Enum):

    Accelerometer = 1
    Gyroscope = 2
    Magnetometer = 3
    Temperature = 4
    Position = 5
    Pose1 = 6
    Pose2 = 7
    Pose3 = 8
    Velocity = 9
    Innovation = 10
    ImuPosition = 11
    PoseRPY = 12
    NotApplicable = 999

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < self.value
        return NotImplemented


class ProcessedCanDataItem:
    
    def __init__(self, nodeid: int, sensor: SensorModel, data_type: SensorDataType, data: List[Any]):
        self.nodeid = nodeid
        self.sensor = sensor
        self.data_type = data_type
        self.data = data


class ProcessedCanDataBlock:
    
    def __init__(self, timestamp, reception_window_us):
        self.timestamp = timestamp
        self.reception_window_us = reception_window_us
        self.items = []

    def add(self, item: ProcessedCanDataItem):
        self.items.append(item)

    def get_nodeids(self) -> Set[int]:
        return {d.nodeid for d in self.items}  # removes duplicates by returning a set

    def get_messages_for_nodeid(self, nodeid: int) -> List[ProcessedCanDataItem]:
        return [d for d in self.items]

    def has_message(self, nodeid: int, sensor: SensorModel, data_type: SensorDataType):
        try:
            self.get_message(nodeid, sensor, data_type)
            return True
        except:
            return False

    def get_message(self, nodeid: int, sensor: SensorModel, data_type: SensorDataType):
        return next(d for d in self.items if d.nodeid == nodeid and d.sensor == sensor and d.data_type == data_type)

    def get_messages(self) -> List[ProcessedCanDataItem]:
        """Returns a list of messages contained in one CAN epoch.
        """
        return sorted(self.items, key=lambda x: (x.nodeid, x.sensor, x.data_type))

    def __str__(self):
        return f'{self.timestamp} {self.reception_window_us} {self.items}'

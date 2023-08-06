import math
from nimutool.canbus.can_message import *


rad2deg = lambda x: x * (180 / math.pi)
rad2dph = lambda x: (x * (180 / math.pi)) * 3600
acc2g = lambda x: x / 9.81
acc2mg = lambda x: x / (9.81 / 1e3)
acc2ug = lambda x: x / (9.81 / 1e6)


def calculate_rpy_if_possible(processed_block: ProcessedCanDataBlock):
    for nodeid in processed_block.get_nodeids():
        dcm = []
        if processed_block.has_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose1) and \
            processed_block.has_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose2) and \
            processed_block.has_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose3):
            dcm1 = processed_block.get_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose1).data[0]
            dcm2 = processed_block.get_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose2).data[0]
            dcm3 = processed_block.get_message(nodeid, SensorModel.NotApplicable, SensorDataType.Pose3).data[0]
            dcm.append(dcm1)
            dcm.append(dcm2)
            dcm.append(dcm3)
            # Titterton, Strapdown Inertial Navigation Technology
            roll = math.degrees(math.atan2(dcm[2][1], dcm[2][2]))
            pitch = math.degrees(math.asin(-dcm[2][0]))
            yaw = math.degrees(math.atan2(dcm[1][0], dcm[0][0]))
            processed_block.add(ProcessedCanDataItem(nodeid, SensorModel.NotApplicable, SensorDataType.PoseRPY, [roll, pitch, yaw]))

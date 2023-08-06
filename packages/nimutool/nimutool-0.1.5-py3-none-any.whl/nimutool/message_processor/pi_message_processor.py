from struct import unpack
from .message_processor import *
import math

def unpack_21b_float(val, fraction_bits):
    return twos_comp(val, 21) / 2**fraction_bits

def parse_pi_fixpoint(data, fraction_bits):
    val = unpack('<Q', data)[0]
    vals = [unpack_21b_float((val >> shift) & 0x1fffff, fraction_bits) for shift in [0, 21, 42]]
    return vals, [True, True, True]

def parse_pi_fixpoint_fraction11(data):
    return parse_pi_fixpoint(data, 11)

def parse_pi_fixpoint_fraction9(data):
    values, statuses = parse_pi_fixpoint(data, 9)
    values = list(map(math.radians, values))
    return values, statuses

def parse_pi_tempvolt(data):
    packet_number, temperature, voltage = unpack('<IhH', data)
    temperature /= 2**8
    voltage /= 2**8
    return packet_number, temperature, voltage

def parse_pi_firmware(data):
    build_date, firmware_version, git_hash = unpack('<HHI', data)
    return build_date, firmware_version, git_hash

def parse_pi_device(data):
    serial_number, human_serial_number, product_id = unpack('<IHH', data)
    return serial_number, human_serial_number, product_id

def parse_pi_proto(data):
    status, gfraction, afraction, packet_rate = unpack('<HxxBBH', data)
    return [status]


class PIMessageProcessor(MessageProcessorBase):

    MSG_HANDLERS = {
        0x0c501000: {'name': 'temp, voltage', 'sensor': SensorModel.PI48, 'type': SensorDataType.NotApplicable, 'frequency': 10, 'is_extended': True, 'parser': None, 'priority': 3},
        0x0c501001: {'name': 'firmware', 'sensor': SensorModel.PI48, 'type': SensorDataType.NotApplicable, 'frequency': 10, 'is_extended': True, 'parser': None, 'priority': 3},
        0x0c501002: {'name': 'device info', 'sensor': SensorModel.PI48, 'type': SensorDataType.NotApplicable, 'frequency': 10, 'is_extended': True, 'parser': None, 'priority': 3},
        0x0c501003: {'name': 'protocol info', 'sensor': SensorModel.PI48, 'type': SensorDataType.NotApplicable, 'frequency': 10, 'is_extended': True, 'parser': None, 'priority': 3},
        0x0c501010: {'name': 'gyro', 'sensor': SensorModel.PI48, 'type': SensorDataType.Gyroscope, 'frequency': 1, 'is_extended': True, 'parser': parse_pi_fixpoint_fraction9, 'priority': 1},
        0x0c501011: {'name': 'acc', 'sensor': SensorModel.PI48, 'type': SensorDataType.Accelerometer, 'frequency': 1, 'is_extended': True, 'parser': parse_pi_fixpoint_fraction11, 'priority': 2},
    }

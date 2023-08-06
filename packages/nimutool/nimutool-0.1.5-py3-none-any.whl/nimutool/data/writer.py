from typing import *
from nimutool.canbus.can_message import *
from nimutool.data.conversion import *
from math import *

SEP = ';'

def format_imuloc(vals):
    nid, x, y, z = vals
    return [f'{nid}', f'{x / 100:2.2f}', f'{y / 100:2.2f}', f'{z / 100:2.2f}']

def format_fixpoint(vals):
    return format_list_of_floats(vals[0])

def format_list_of_floats(vals):
    return [f'{v:7.4f}' for v in vals]

def format_fixpoint_err(vals):
    return format_fixpoint(vals) + ['1' if not e else '0' for e in vals[1]]

def format_temps(vals):
    return [f'{vals[0] / 10:.1f}', f'{vals[1] / 10:.1f}']

def formatter_csv(elems):
    return SEP.join(arg.strip() for arg in elems)

def formatter_console(elems):
    return ' '.join(elems)

FORMATTERS = {
    (SensorModel.SCHA63T, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['hax', 'hay', 'haz']},
    (SensorModel.SCHA63T, SensorDataType.Gyroscope): {'formatter': format_fixpoint_err, 'header': ['hgx', ' hgy', 'hgz', 'hgxe', 'hgye', 'hgze']},
    (SensorModel.BMX160, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['bax', 'bay', 'baz']},
    (SensorModel.BMX160, SensorDataType.Gyroscope): {'formatter': format_fixpoint, 'header': ['bgx', 'bgy', 'bgz']},
    (SensorModel.SCLxxxx, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['pax', 'pay', 'paz']},
    (SensorModel.PI48, SensorDataType.Accelerometer): {'formatter': format_fixpoint, 'header': ['pi48ax', 'pi48ay', 'pi48az']},
    (SensorModel.PI48, SensorDataType.Gyroscope): {'formatter': format_fixpoint, 'header': ['pi48gx', 'pi48gy', 'pi48gz']},
    (SensorModel.NotApplicable, SensorDataType.Pose1): {'formatter': format_fixpoint, 'header': ['dcm11', 'dcm12', 'dcm13']},
    (SensorModel.NotApplicable, SensorDataType.Pose2): {'formatter': format_fixpoint, 'header': ['dcm21', 'dcm22', 'dcm23']},
    (SensorModel.NotApplicable, SensorDataType.Pose3): {'formatter': format_fixpoint, 'header': ['dcm31', 'dcm32', 'dcm33']},
    (SensorModel.NotApplicable, SensorDataType.Position): {'formatter': format_fixpoint, 'header': ['posx', 'posy', 'posz']},
    (SensorModel.NotApplicable, SensorDataType.Velocity): {'formatter': format_fixpoint, 'header': ['velx', 'vely', 'velz']},
    (SensorModel.NotApplicable, SensorDataType.Innovation): {'formatter': format_fixpoint, 'header': ['innox', 'innoy', 'innoz']},
    (SensorModel.NotApplicable, SensorDataType.ImuPosition): {'formatter': format_imuloc, 'header': ['id', 'imuposx', 'imuposy', 'imuposz']},
    (SensorModel.NotApplicable, SensorDataType.PoseRPY): {'formatter': format_list_of_floats, 'header': ['roll', 'pitch', 'yaw']},
}

class CsvWriter:

    def __init__(self, filename, write_every_nth=1):
        self.f = open(filename, "w")
        self.write_every_nth = write_every_nth
        self.cnt = 0

    def _add_header_if_needed(self, processed_block: ProcessedCanDataBlock):
        hdr = ['timestamp', 'window_us']
        for msg in processed_block.get_messages():
            fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
            hdr += [hdr_item + str(msg.nodeid) for hdr_item in fmtr['header']]
        if self.f.tell() == 0:
            self.f.write(formatter_csv(hdr) + '\n')

    def write(self, processed_block: ProcessedCanDataBlock):
        self.cnt += 1
        if self.cnt % self.write_every_nth != 0:
            return
        calculate_rpy_if_possible(processed_block)
        self._add_header_if_needed(processed_block)
        formatted_data_items = [str(processed_block.timestamp), str(processed_block.reception_window_us)]
        for msg in processed_block.get_messages():
            fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
            formatted_data_items += fmtr['formatter'](msg.data)
        self.f.write(formatter_csv(formatted_data_items) + '\n')


class ConsoleWriter:

    def write(self, processed_block: ProcessedCanDataBlock):
        calculate_rpy_if_possible(processed_block)
        formatted_data_items = [str(processed_block.timestamp), str(processed_block.reception_window_us)]
        for msg in processed_block.get_messages():
            fmtr = FORMATTERS[(msg.sensor, msg.data_type)]
            formatted_data_items += fmtr['formatter'](msg.data)
        print(formatter_console(formatted_data_items))

from nimutool.canbus import *
from typing import *

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


class MessageProcessorBase:

    def on_datacollection_ready(self, data_collection: CanMessageCollection) -> ProcessedCanDataBlock:
        synced_collection = data_collection.filter(lambda x: self.canid2dataid(x) in self.get_synchronized_frames())
        processed_block = ProcessedCanDataBlock(synced_collection.first.timestamp, synced_collection.window_us)
        for message in data_collection.sorted_by_id:
            processed_item = self.process_message(message, data_collection)
            if processed_item:
                processed_block.add(processed_item)
        if not data_collection.is_valid:
            raise Exception('data collection is not valid!')
        return processed_block

    def process_message(self, message: CanMessage, data_collection: CanMessageCollection) -> ProcessedCanDataItem:
        data_id, node_id = self.split_canid_to_msgid_and_nodeid(message.msg_id)
        hdlr = self.MSG_HANDLERS[data_id]
        parser = hdlr['parser']
        if parser:
            data = parser(message.data)
            return ProcessedCanDataItem(node_id, hdlr['sensor'], hdlr['type'], data)
        return None
    
    def canid2dataid(self, can_id):
        return can_id

    def split_canid_to_msgid_and_nodeid(self, can_id):
        return can_id, 0

    def get_highest_priority_frame(self, set_of_canids):
        highest_prio_canid = -1
        highest_prio = 999
        for canid in set_of_canids:
            dataid = self.canid2dataid(canid)
            prio = self.MSG_HANDLERS[dataid]['priority']
            if prio < highest_prio:
                highest_prio = prio
                highest_prio_canid = canid
        return highest_prio_canid

    def get_synchronized_frames(self) -> List[int]:
        return [can_id for can_id, frame_opts in self.MSG_HANDLERS.items() if frame_opts['frequency'] == 1]

    def get_latched_frames(self) -> List[int]:
        return [can_id for can_id, frame_opts in self.MSG_HANDLERS.items() if frame_opts['frequency'] != 1]

    def is_supported(self, message: CanMessage):
        data_id = self.canid2dataid(message.msg_id)
        if data_id in self.MSG_HANDLERS:
            return self.MSG_HANDLERS[data_id]['is_extended'] == message.is_extended_id
        return False

    def get_msg_name(self, can_id):
        data_id = self.canid2dataid(can_id)
        return self.MSG_HANDLERS[data_id]["name"]


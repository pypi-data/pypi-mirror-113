from nimutool.canbus import *
from nimutool.data import *
from nimutool.message_processor import *
import threading
from pathlib import Path


class NimuReader:

    def __init__(self, bus, traffic_study_period=0.5):
        self.bus = bus
        processor = NimuMessageProcessor()
        self.synchronizer = BusSynchronizer(traffic_study_period, processor)

    def __iter__(self):
        return self

    def __next__(self) -> ProcessedCanDataBlock:
        for msg in self.bus:
            processed_block = self.synchronizer.synchronize(msg)
            if processed_block:
                return processed_block


class ThreadedNimuAndPI48ReaderWriter(threading.Thread):

    def __init__(self, bus, path: Path, file_prefix: str, extras=True, nimu_protocol=2, traffic_study_period=0.5,):
        super().__init__()
        self.running = True
        self.nifile = Path(path) / Path(f'{file_prefix}_ni_data.csv')
        self.pifile = Path(path) / Path(f'{file_prefix}_pi_data.csv')
        self.bus = bus
        niprocessor = NimuMessageProcessorOld() if nimu_protocol == 1 else NimuMessageProcessor()
        piprocessor = PIMessageProcessor()
        self.nisynchronizer = BusSynchronizer(traffic_study_period, niprocessor)
        self.pisynchronizer = BusSynchronizer(traffic_study_period, piprocessor, True)
        self.next_trace = 0
        self.extras = extras

    def run(self):
        niwriter = CsvWriter(self.nifile)
        piwriter = CsvWriter(self.pifile)
        for msg in self.bus:
            if not self.running:
                break
            block = self.nisynchronizer.synchronize(msg)
            if block: niwriter.write(block)
            block = self.pisynchronizer.synchronize(msg)
            if block: piwriter.write(block)

            if self.next_trace < msg.timestamp:
                print(f'NI: {self.nisynchronizer} PI: {self.pisynchronizer}')
                self.next_trace = msg.timestamp + 5
                #if self.extras and block:
                #    ConsoleWriter().write(block)
        if self.nisynchronizer.collection_monitor.count != 0:
            print(f'Written {self.nisynchronizer.collection_monitor.count} rows to {self.nifile}')
        if self.pisynchronizer.collection_monitor.count != 0:
            print(f'Written {self.pisynchronizer.collection_monitor.count} rows to {self.pifile}')

    def stop(self):
        self.running = False
        self.join()
        if self.bus:
            self.bus.stop()
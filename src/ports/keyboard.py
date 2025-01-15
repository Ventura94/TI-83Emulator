import keyboard

from src.ram import VirtualMemory
from src.singleton import Singleton


class Keyboard(Singleton):
    BUFFER_ADDRESS = 0x844C
    BUFFER_SIZE = 10

    def __init__(self):
        self.index_address = 0x844C
        self.buffer = VirtualMemory(self.BUFFER_ADDRESS, self.BUFFER_ADDRESS + self.BUFFER_SIZE)

    def key(self):
        if (self.BUFFER_ADDRESS - self.index_address) < self.BUFFER_SIZE:
            key = keyboard.read_event()
            if key.name.isdigit():
                self.buffer.write(self.index_address, key.name)
                self.index_address += 1
            else:
                pass
            return key

    def clear_buffer(self):
        self.clear_buffer()

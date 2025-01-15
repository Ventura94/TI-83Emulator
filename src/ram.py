from src.singleton import Singleton


class RAM(Singleton):
    SIZE = 8192

    def __init__(self):
        self.memory = [0] * self.SIZE


class VirtualMemory:

    def __init__(self, start_address, end_address):
        self.start_address = start_address
        self.end_address = end_address
        self.physical_ram = RAM()
        if end_address - start_address > self.physical_ram.SIZE:
            raise ValueError("Address range exceeds physical memory size")
        self.virtual_memory = self.physical_ram.memory[start_address:end_address]

    def map_address(self, virtual_address):
        if virtual_address < self.start_address or virtual_address >= self.end_address:
            raise ValueError(f"Virtual address {hex(virtual_address)} out of allowed range.")
        return virtual_address - self.start_address

    def read(self, virtual_address):
        physical_index = self.map_address(virtual_address)
        return self.physical_ram.memory[physical_index]

    def write(self, virtual_address, value):
        physical_index = self.map_address(virtual_address)
        self.physical_ram.memory[physical_index] = value

    def clean_virtual_memory(self):
        for i in range(self.start_address, self.end_address):
            self.physical_ram.memory[i] = 0

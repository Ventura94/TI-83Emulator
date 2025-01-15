import os

from src.singleton import Singleton

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ROM(Singleton):
    def __init__(self):
        self.BASE_DIR = BASE_DIR
        self.data = self._load()
        self.pc = 0

    def _load(self):
        rom_path = os.path.join(self.BASE_DIR, 'ti83pv103.bin')
        with open(rom_path, 'rb') as f:
            return f.read()

    def fetch_hex(self, pc: int):
        return self.data[pc]

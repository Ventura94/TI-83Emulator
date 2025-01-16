from abc import ABC, abstractmethod

from src.ports.screen import LCDController
from src.singleton import Singleton


class OUTPortBase(ABC):
    hex_op = None

    @abstractmethod
    def send(self, hex_op: int):
        pass


class OUTScreenPort(OUTPortBase):
    hex_op = hex(0x06)

    def send(self, hex_op: int):
        lcd_controller = LCDController()
        lcd_controller.execute_instruction(hex_op)


class OUTPorts(Singleton):
    PORTS = [
        OUTScreenPort
    ]

    def __init__(self):
        self.ports_mapper = {port.hex_op: port for port in self.PORTS}

    def get_port_by_hex(self, hex_op):
        port = self.ports_mapper.get(hex_op)
        if port:
            return port()
        raise ValueError(f"Port {hex_op} not found")

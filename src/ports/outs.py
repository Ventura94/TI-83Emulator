from src.ports.screen import LCDScreen
from src.singleton import Singleton


class OUTPortBase:
    hex_op = None

    def send(self, in_register: None):
        pass


class OUTScreenPort(OUTPortBase):
    hex_op = hex(0x06)

    def execute(self, in_register: None):
        lcd = LCDScreen()


class OUTPorts(Singleton):
    PORTS = [
        OUTScreenPort
    ]

    def __init__(self):
        self.ports_mapper = {port.hex_op: port for port in self.PORTS}

    def get_port(self, hex_op):
        port = self.ports_mapper.get(hex_op)
        if port:
            return port()
        raise ValueError(f"Port {hex_op} not found")

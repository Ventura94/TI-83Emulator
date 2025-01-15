from abc import ABC, abstractmethod

from src.ports.outs import OUTPorts


class BaseInstruction(ABC):
    hex_op = None

    def __init__(self, cpu):
        self.cpu = cpu

    @abstractmethod
    def execute(self, in_register: None):
        pass


class OUT(BaseInstruction):
    hex_op = hex(0xD3)

    def execute(self, in_register: None):
        out_port_rom_hex = self.cpu.fetch_rom_hex()
        out_port = OUTPorts().get_port_by_hex(out_port_rom_hex)





class LD_A(BaseInstruction):
    hex_op = hex(0x3E)

    def execute(self, in_register: None):
        rom_hex = self.cpu.fetch_rom_hex()
        self.cpu.register.set_register("A", int(rom_hex, 0))

# class IN_A(BaseInstruction):
#     hex_op = hex(0xDB)
#
#     def execute(self, in_register: None):
#         instruction = self.cpu.execute_instruction(in_register="A")
#
#
# class KEYBOARD_IN(BaseInstruction):
#     hex_op = hex(0x01)
#
#     def execute(self, in_register: None):
#         keyboard = Keyboard()
#         while True:
#             key = keyboard.key()
#             if key.isdigit():
#                 return key
#             else:
#                 raise ValueError("Solo se permiten teclas numéricas.")
#
#
# class SUM(BaseInstruction):
#     hex_op = hex(0x80)
#
#     def execute(self, in_register: None):
#         pass
#
#
# class SUB(BaseInstruction):
#     hex_op = hex(0x90)
#
#     def execute(self, in_register: None):
#         pass

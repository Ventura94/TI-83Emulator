from src.instructions.base import LD_A, OUT_A, JP_nn, INC_B, IY, CB, RL_D, AND_n, DEC_DE, NOP, CALL_nn
from src.registers import Registers
from src.rom.rom import ROM
from src.singleton import Singleton
from src.stack import Stack


class CPU(Singleton):
    INSTRUCTIONS = [
        LD_A,
        OUT_A,
        JP_nn,
        INC_B,
        IY,
        CB,
        RL_D,
        AND_n,
        DEC_DE,
        NOP,
        CALL_nn
        # ADD_A_IY_d,
        # LD_IY_d_n,
        # LD_IY_nn
    ]

    def __init__(self):
        self.rom = ROM()
        self.stack = Stack()
        self.register = Registers()
        self.instruction_mapper = {instruction.hex_op: instruction for instruction in self.INSTRUCTIONS}

    def fetch_rom_hex(self):
        pc = self.register.get_register('PC')
        instruction = self.rom.fetch_hex(pc)
        self.register.set_register('PC', pc + 1)
        return hex(instruction)

    def execute_instruction(self, in_register=None):
        instruction = self.fetch_rom_hex()
        instruction_class = self.instruction_mapper.get(instruction)
        if instruction_class:
            return instruction_class(self).execute(in_register)
        raise ValueError(f"Instruction {instruction} not found")

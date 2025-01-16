from abc import ABC, abstractmethod

from src.ports.outs import OUTPorts


class BaseInstruction(ABC):
    hex_op = None

    def __init__(self, cpu):
        self.cpu = cpu

    @abstractmethod
    def execute(self, in_register: None):
        pass


class CALL_nn(BaseInstruction):
    hex_op = hex(0xCD)

    def execute(self, in_register: None):
        lsb = self.cpu.fetch_rom_hex()  # LSB (Low Byte)
        msb = self.cpu.fetch_rom_hex()  # MSB (High Byte)
        jump_address = (int(msb, 0) << 8) | int(lsb, 0)
        return_address = self.cpu.register.get_register('PC') + 2
        self.cpu.stack.push(return_address)
        self.cpu.register.set_register('PC', jump_address)


class NOP(BaseInstruction):
    hex_op = hex(0x00)

    def execute(self, in_register: None = None):
        pass


class DEC_DE(BaseInstruction):
    hex_op = hex(0x1B)

    def execute(self, _):
        de = self.cpu.register.get_register('DE')
        de = (de - 1) & 0xFFFF
        self.cpu.register.set_register('DE', de)


class AND_n(BaseInstruction):
    hex_op = hex(0xf6)

    def execute(self, _):
        operand = self.cpu.fetch_rom_hex()
        accumulator = self.cpu.register.get_register('A')
        result = accumulator & int(operand, 0)
        self.cpu.register.set_register('A', result)
        self.cpu.register.set_flag('Z', result == 0)
        self.cpu.register.set_flag('S', (result & 0x80) != 0)
        self.cpu.register.set_flag('P/V', bin(result).count('1') % 2 == 0)
        self.cpu.register.set_flag('H', 1)
        self.cpu.register.set_flag('C', 0)


class RL_D(BaseInstruction):
    hex_op = hex(0xCB13)

    def execute(self, in_register=None):
        reg_value = self.cpu.register.get_register("D")
        msb = (reg_value & 0x80) >> 7
        carry = self.cpu.register.get_flag("C")
        result = ((reg_value << 1) | carry) & 0xFF
        self.cpu.register.set_register("D", result)
        self.cpu.register.set_flag("C", msb)
        self.cpu.register.set_flag("Z", result == 0)
        self.cpu.register.set_flag("S", (result & 0x80) != 0)
        self.cpu.register.set_flag("P/V", bin(result).count("1") % 2 == 0)
        self.cpu.register.set_flag("N", 0)
        self.cpu.register.set_flag("H", 0)


class CB(BaseInstruction):
    hex_op = hex(0xCB)

    def execute(self, in_register: None):
        opcode = self.cpu.fetch_rom_hex()
        instruction = (int(self.hex_op, 0) << 8) | int(opcode, 0)
        next_hex_op = hex(instruction)
        instruction_class = self.cpu.instruction_mapper.get(next_hex_op)
        if instruction_class:
            return instruction_class(self.cpu).execute(in_register)
        raise ValueError(f"Instruction {instruction} not found in OxCB")


class IY(BaseInstruction):
    hex_op = hex(0xfd)

    def execute(self, in_register: None):
        self.cpu.execute_instruction("IY")
        self.cpu.execute_instruction("IY")
        self.cpu.execute_instruction("IY")


# class ADD_A_IY_d(BaseInstruction):
#     hex_op = hex(0x86)
#
#     def execute(self, in_register: None):
#         displacement = self.cpu.fetch_rom_signed_byte()  # Leer desplazamiento como valor con signo
#         iy = self.cpu.register.get_register("IY")
#         address = (iy + displacement) & 0xFFFF  # Calcular dirección (asegurar 16 bits)
#         value = self.cpu.memory.read(address)  # Leer valor de memoria
#         a = self.cpu.register.get_register("A")  # Leer acumulador
#         result = (a + value) & 0xFF  # Sumar y asegurar 8 bits
#         self.cpu.register.set_register("A", result)
#
#         # Actualizar flags (Zero, Carry, etc.)
#         self.cpu.update_flags_add(a, value, result)
#         print(f"A actualizado a: {hex(result)} tras sumar {hex(value)} de {hex(address)}")
#
#
# class LD_IY_d_n(BaseInstruction):
#     hex_op = hex(0x36)
#
#     def execute(self, in_register: None):
#         displacement = self.cpu.fetch_rom_signed_byte()  # Leer desplazamiento como valor con signo
#         value = int(self.cpu.fetch_rom_hex(), 0)  # Valor inmediato
#         iy = self.cpu.register.get_register("IY")
#         address = (iy + displacement) & 0xFFFF  # Calcular dirección (asegurar 16 bits)
#         self.cpu.memory.write(address, value)
#         print(f"Memoria en {hex(address)} cargada con: {hex(value)}")
#
#
# class LD_IY_nn(BaseInstruction):
#     hex_op = hex(0x21)
#
#     def execute(self, in_register: None):
#         lsb = self.cpu.fetch_rom_hex()
#         msb = self.cpu.fetch_rom_hex()
#         iy_value = (int(msb, 0) << 8) | int(lsb, 0)
#         self.cpu.register.set_register("IY", iy_value)
#         print(f"IY cargado con: {hex(iy_value)}")


class OUT_A(BaseInstruction):
    hex_op = hex(0xD3)

    def execute(self, in_register: None):
        out_port_rom_hex = self.cpu.fetch_rom_hex()
        out_port = OUTPorts().get_port_by_hex(out_port_rom_hex)
        out_port.send(self.cpu.register.get_register("A"))


class JP_nn(BaseInstruction):
    hex_op = hex(0xc3)

    def execute(self, in_register: None):
        lsb = self.cpu.fetch_rom_hex()
        msb = self.cpu.fetch_rom_hex()
        jump_address = (int(msb, 0) << 8) | int(lsb, 0)
        self.cpu.register.set_register("PC", jump_address)


class INC_B(BaseInstruction):
    hex_op = hex(0x4)

    def execute(self, in_register: None):
        b_register = self.cpu.register.get_register("B")
        b_register_inc = (b_register + 1) & 0xFF
        self.cpu.register.clear_flag("N")
        if b_register_inc == 0:
            self.cpu.register.set_flag("Z")
        else:
            self.cpu.register.clear_flag("Z")
        if (b_register & 0x0F) == 0x0F:
            self.cpu.register.set_flag("H")
        else:
            self.cpu.register.clear_flag("H")
        self.cpu.register.set_register("B", b_register_inc)


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

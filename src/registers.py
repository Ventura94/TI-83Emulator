class Registers:
    def __init__(self):
        self.FLAG_POSITIONS = {
            "S": 7,  # Sign flag
            "Z": 6,  # Zero flag
            "H": 4,  # Half Carry flag
            "P/V": 2,  # Parity/Overflow flag
            "N": 1,  # Add/Subtract flag
            "C": 0  # Carry flag
        }
        self.cpu_registers = {
            'A': 0,
            'F': 0,
            'B': 0,
            'C': 0,
            'D': 0,
            'E': 0,
            'H': 0,
            'L': 0,
            'PC': 0,
            'SP': 0,
            'IX': 0,
            'IY': 0,
            'I': 0,
            'R': 0
        }
        self.combined_registers = {
            'AF': lambda: (self.cpu_registers['A'] << 8) | self.cpu_registers['F'],
            'BC': lambda: (self.cpu_registers['B'] << 8) | self.cpu_registers['C'],
            'DE': lambda: (self.cpu_registers['D'] << 8) | self.cpu_registers['E'],
            'HL': lambda: (self.cpu_registers['H'] << 8) | self.cpu_registers['L']
        }
        self.alternate_registers = {'AF\'': 0, 'BC\'': 0, 'DE\'': 0, 'HL\'': 0}

    def set_flag(self, flag_name, value):
        if flag_name not in self.FLAG_POSITIONS:
            raise ValueError(f"Flag no válido: {flag_name}")
        flag_bit = self.FLAG_POSITIONS[flag_name]
        self.cpu_registers['F'] |= (1 << flag_bit)
        if value == 1:
            self.cpu_registers['F'] |= (1 << flag_bit)  # Activar el flag
        elif value == 0:
            self.cpu_registers['F'] &= ~(1 << flag_bit)  # Desactivar el flag
        else:
            raise ValueError(f"El valor de 'value' debe ser 0 o 1, pero se pasó: {value}")

    def clear_flag(self, flag_name):
        if flag_name not in self.FLAG_POSITIONS:
            raise ValueError(f"Flag no válido: {flag_name}")
        flag_bit = self.FLAG_POSITIONS[flag_name]
        self.cpu_registers['F'] &= ~(1 << flag_bit)

    def get_flag(self, flag_name):
        if flag_name not in self.FLAG_POSITIONS:
            raise ValueError(f"Flag no válido: {flag_name}")
        flag_bit = self.FLAG_POSITIONS[flag_name]
        return (self.cpu_registers['F'] >> flag_bit) & 1

    def set_register(self, reg, value):
        if reg in self.cpu_registers:
            self.cpu_registers[reg] = value & 0xFF  # Asegurar 8 bits
        elif reg in self.combined_registers:
            self.combined_registers[reg] = value & 0xFFFF  # Asegurar 16 bits
        elif reg in self.alternate_registers:
            self.alternate_registers[reg] = value & 0xFFFF  # Asegurar 16 bits
        else:
            raise ValueError(f"Registro no válido: {reg}")

    def get_register(self, reg):
        if reg in self.cpu_registers:
            return self.cpu_registers[reg]
        elif reg in self.combined_registers:
            return self.combined_registers[reg]()
        elif reg in self.alternate_registers:
            return self.alternate_registers[reg]
        else:
            raise ValueError(f"Registro no válido: {reg}")

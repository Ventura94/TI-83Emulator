from src.cpu import CPU
from src.rom.rom import ROM


def main():
    rom = ROM()
    cpu = CPU()

    while cpu.register.get_register("PC") < len(rom.data):
        cpu.execute_instruction()


if __name__ == '__main__':
    main()

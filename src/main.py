from src.cpu import CPU
from src.ports.screen import LCDScreen
from src.rom.rom import ROM


def main():
    rom = ROM()
    cpu = CPU()
    screen = LCDScreen()
    screen.draw()

    while cpu.register.get_register("PC") < len(rom.data):
        cpu.execute_instruction()


if __name__ == '__main__':
    main()

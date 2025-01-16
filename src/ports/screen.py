from typing import Literal

import pygame

from src.ram import VirtualMemory
from src.singleton import Singleton


class LCDController(Singleton):
    def __init__(self):
        self.screen = LCDScreen()

    def execute_instruction(self, hex_op: int):
        self.screen.write_byte(0, 0, hex_op)


class LCDScreen(Singleton):
    WIDTH = 96
    HEIGHT = 64
    PIXEL_SIZE = 5
    INIT_BUFFER_ADDRESS = 0x844C
    END_BUFFER_ADDRESS = 0x8B17

    def __init__(self):
        self.buffer = VirtualMemory(0x844C, 0x8B17)
        self.bytes_per_row = (self.WIDTH + 7) // 8
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH * self.PIXEL_SIZE, self.HEIGHT * self.PIXEL_SIZE))
        pygame.display.set_caption("LCD Simulator")
        self.clock = pygame.time.Clock()

    def clear_buffer(self):
        self.buffer.clean_virtual_memory()

    def set_pixel(self, x, y, value: Literal[0, 1]):
        byte_index = y * self.bytes_per_row + (x // 8)
        bit_index = x % 8
        current_byte = self.buffer.read(self.INIT_BUFFER_ADDRESS + byte_index)
        if value == 0:
            current_byte &= ~(1 << (7 - bit_index))
        else:
            current_byte |= (1 << (7 - bit_index))
        self.buffer.write(self.INIT_BUFFER_ADDRESS + byte_index, current_byte)
        self.draw()

    def write_byte(self, x, y, byte_value):
        if not (0x00 <= byte_value <= 0xFF):
            raise ValueError("El byte_value debe estar entre 0x00 y 0xFF")
        if x % 8 != 0:
            raise ValueError("La columna x debe ser múltiplo de 8 para escribir un byte completo")
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            raise ValueError("Coordenadas fuera del rango de la pantalla")
        byte_index = y * self.bytes_per_row + (x // 8)
        memory_address = self.INIT_BUFFER_ADDRESS + byte_index
        self.buffer.write(memory_address, byte_value)
        self.draw()

    def get_pixel(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            raise ValueError("Coordinates out of screen range")
        byte_index = y * self.bytes_per_row + (x // 8)
        bit_index = x % 8
        return (self.buffer.read(self.INIT_BUFFER_ADDRESS + byte_index) >> (7 - bit_index)) & 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.get_pixel(x, y) == 1:
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        (x * self.PIXEL_SIZE, y * self.PIXEL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE),
                    )
        pygame.display.flip()
        self.clock.tick(30)

#
# running = True
# lcd = LCDScreen()
# lcd_2 = LCDScreen()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     lcd.set_pixel(10, 5, 1)  # Encender un píxel en (10, 5)
#     lcd.draw()
#     lcd_2.set_pixel(10, 6, 1)  # Encender un píxel en (10, 5)
#     lcd.draw()
#
# pygame.quit()

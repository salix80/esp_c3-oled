from micropython import const
import framebuf
from machine import Pin, I2C

# Standard-I2C-Pins für ESP32-C3
SDA_PIN = 5
SCL_PIN = 6

class Display(framebuf.FrameBuffer):
    def __init__(self, width=128, height=64, addr=0x3C):
        # I2C automatisch mit festen Pins initialisieren
        self.i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
        self.width = width
        self.height = height
        self.addr = addr
        self.buffer = bytearray(self.width * self.height // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        """Initialisiert das OLED-Display"""
        for cmd in (
            0xAE,  # Display OFF
            0xD5, 0x80,  # Clock
            0xA8, 0x3F,  # Höhe
            0xD3, 0x00,  # Offset
            0x40,  # Startlinie
            0xA1,  # X-Spiegelung
            0xC8,  # Y-Spiegelung
            0xDA, 0x12,  # COM-Konfiguration
            0x81, 0x7F,  # Kontrast
            0xA4,  # Normalmodus
            0xA6,  # Nicht invertiert
            0xD9, 0xF1,  # Ladepumpe
            0xDB, 0x20,  # VCOMH
            0x8D, 0x14,  # Ladepumpe aktivieren
            0xAF,  # Display ON
        ):
            self.write_cmd(cmd)

        # Display-Speicher leeren
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        """Sendet einen Befehl an das OLED-Display"""
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def show(self):
        """Zeigt den FrameBuffer auf dem Display an"""
        for i in range(0, 8):
            self.write_cmd(0xB0 + i)
            self.write_cmd(0x00)
            self.write_cmd(0x10)
            self.i2c.writeto(self.addr, b"\x40" + self.buffer[i * self.width:(i + 1) * self.width])

    def line(self, x1, y1, x2, y2, color):
        """Zeichnet eine Linie mit Bresenham-Algorithmus"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


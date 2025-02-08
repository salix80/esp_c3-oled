from micropython import const
import framebuf
from machine import Pin, I2C

# Standard-I2C-Pins für ESP32-C3
SDA_PIN = 5
SCL_PIN = 6

class Display(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.offset_x = 30  # Linke Grenze der sichtbaren Anzeige
        self.line_height = 12  # Abstand zwischen den Zeilen
        self.buffer = bytearray(self.width * self.height // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        """Initialisiert das SH1106 OLED-Display"""
        for cmd in (
            0xAE,  # Display aus
            0xD5, 0x80,  # Takt
            0xA8, 0x3F,  # Höhe
            0xD3, 0x00,  # Offset
            0x40,  # Startlinie
            0xA1,  # Spiegelung X
            0xC8,  # Spiegelung Y
            0xDA, 0x12,  # COM-Konfiguration
            0x81, 0x7F,  # Kontrast
            0xA4,  # Normalmodus
            0xA6,  # Nicht invertiert
            0xD9, 0xF1,  # Ladepumpe
            0xDB, 0x20,  # VCOMH
            0x8D, 0x14,  # Ladepumpe aktivieren
            0xAF,  # Display an
        ):
            self.write_cmd(cmd)

        # Display-Speicher löschen
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        """Sendet einen Befehl an das OLED-Display"""
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def show(self):
        """Zeigt den Inhalt des FrameBuffers auf dem Display an"""
        for i in range(0, 8):
            self.write_cmd(0xB0 + i)
            self.write_cmd(0x00)
            self.write_cmd(0x10)
            self.i2c.writeto(self.addr, b"\x40" + self.buffer[i * self.width:(i + 1) * self.width])

    def text(self, text, line):
        """Zeichnet Text in eine der drei sichtbaren Zeilen (1, 2 oder 3)"""
        line_positions = {1: 12, 2: 24, 3: 36}  # Richtige Y-Positionen
        if line in line_positions:
            self.text(text, self.offset_x, line_positions[line])

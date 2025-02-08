import time
from display_int import Display  # Verwende den neuen Treiber

# Display initialisieren
oled = Display()

# Startposition des Smileys
x = 0

while True:
    oled.fill(0)  # Bildschirm leeren

    # 👀 Augen zeichnen
    oled.fill_rect(x + 5, 20, 5, 5, 1)  # Linkes Auge
    oled.fill_rect(x + 20, 20, 5, 5, 1)  # Rechtes Auge

    #Mund als Bogen zeichnen
    oled.line(x + 8, 40, x + 22, 40, 1)  # Gerade Linie unten
    oled.pixel(x + 6, 39, 1)
    oled.pixel(x + 24, 39, 1)
    oled.pixel(x + 4, 38, 1)
    oled.pixel(x + 26, 38, 1)

    #Kopf als Kreis (vereinfacht mit einem Rechteck)
    oled.rect(x, 15, 30, 30, 1)  # Kopf als Quadrat

    oled.show()  # Alles anzeigen

    time.sleep(0.05)  # Kurze Pause für flüssige Bewegung

    x += 2  # Smiley nach rechts bewegen

    if x > 98:  # Falls Smiley aus dem Bild geht, zurücksetzen
        x = 0

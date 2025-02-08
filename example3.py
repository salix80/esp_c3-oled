import time
import math
import random
from display_int import Display  # Neuer Treibername mit festem I2C

# Display initialisieren (I2C-Pins sind bereits im Treiber festgelegt)
oled = Display()

# Anzahl der Sterne
num_stars = 40

# Bildschirmmitte als Ursprung der Sterne
center_x = 64
center_y = 32

# Sterne erstellen (radius, winkel, speed)
stars = [
    [random.uniform(1, 64), random.uniform(0, 2 * math.pi), random.uniform(0.5, 2)]
    for _ in range(num_stars)
]

while True:
    oled.fill(0)  # Bildschirm leeren

    for star in stars:
        r, angle, speed = star  # Radius, Winkel, Geschwindigkeit

        # Vorherige Position für sanfte Lichtspuren (kürzere und weichere Spuren)
        trail_factor = speed * 2  # Spuren sind proportional zur Geschwindigkeit
        prev_x = int(center_x + math.cos(angle) * (r - trail_factor))
        prev_y = int(center_y + math.sin(angle) * (r - trail_factor))

        # Stern nach außen bewegen (Warp-Effekt)
        r += speed  

        # Neue Position berechnen
        x = int(center_x + math.cos(angle) * r)
        y = int(center_y + math.sin(angle) * r)

        # Falls der Stern aus dem Bildschirm fliegt, neu in die Mitte setzen
        if x < 0 or x >= 128 or y < 0 or y >= 64:
            r = random.uniform(1, 5)  # Neuer Startpunkt nahe Zentrum
            angle = random.uniform(0, 2 * math.pi)  # Zufällige Richtung
            speed = random.uniform(0.5, 2)  # Neue Geschwindigkeit

        # **Sanfte Lichtspuren zeichnen**
        if r > 10:  # Erst Linien ziehen, wenn Sterne weiter entfernt sind
            oled.line(prev_x, prev_y, x, y, 1)  # Kürzere, weichere Spuren

        # **Stern zeichnen**
        size = 1 if r < 20 else 2  # Kleine Sterne sind weiter weg
        oled.fill_rect(x, y, size, size, 1)

        # Neue Position speichern
        star[0], star[1], star[2] = r, angle, speed

    oled.show()  # Alles auf dem Bildschirm anzeigen
    time.sleep(0.05)  # Animationsgeschwindigkeit

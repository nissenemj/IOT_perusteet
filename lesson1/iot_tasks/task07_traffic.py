# Liikennevalot: tilakone + ohitusnappi + summeri (ekstra)
import machine
import utime

# LED-määritykset
led_red = machine.Pin(15, machine.Pin.OUT)
led_yellow = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(13, machine.Pin.OUT)

# Nappi ja summeri
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Huom! PULL_UP
buzzer = machine.Pin(12, machine.Pin.OUT)

while True:

    if button.value() ==1:
        led_red.value(1)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        led_red.value(0)

    led_red.value(1)
    led_yellow.value(0)
    led_green.value(0)
    utime.sleep(2)
        
        # Punainen + keltainen (valmistautuminen)
    led_red.value(1)
    led_yellow.value(1)
    led_green.value(0)
    utime.sleep(1)
        
        # Vihreä valo
    led_red.value(0)
    led_yellow.value(0)
    led_green.value(1)
    utime.sleep(2)
        
        # Keltainen valo (varoitus)
    led_red.value(0)
    led_yellow.value(1)
    led_green.value(0)
    utime.sleep(1)
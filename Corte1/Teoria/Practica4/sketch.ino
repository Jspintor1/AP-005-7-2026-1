import machine
import time

pin_boton = machine.Pin(13, machine.Pin.IN)
pines_leds = [15, 2, 4, 16, 17, 5, 18, 19]
leds = [machine.Pin(p, machine.Pin.OUT) for p in pines_leds]

modo = 0
ultimo_estado_boton = 1
ultima_vez_parpadeo = time.ticks_ms()
estado_led_blink = 0

def controlar_leds(valor):
    for led in leds:
        led.value(valor)

while True:
    lectura_actual = pin_boton.value()

    if ultimo_estado_boton == 1 and lectura_actual == 0:
        modo = (modo + 1) % 3
        time.sleep(0.2)
    
    ultimo_estado_boton = lectura_actual

    if modo == 0:
        controlar_leds(0)
    elif modo == 1:
        controlar_leds(1)
    elif modo == 2:
        ahora = time.ticks_ms()
        if time.ticks_diff(ahora, ultima_vez_parpadeo) > 300:
            ultima_vez_parpadeo = ahora
            estado_led_blink = 1 - estado_led_blink
            controlar_leds(estado_led_blink)

    time.sleep(0.01)
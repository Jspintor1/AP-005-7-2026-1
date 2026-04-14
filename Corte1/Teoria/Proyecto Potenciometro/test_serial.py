#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la comunicación serial con el ESP32
Este script ayuda a identificar problemas de conexión y formato de datos.
"""

import serial
import time

PUERTO = "COM5"
BAUDIOS = 115200
TIMEOUT = 2

print("=" * 60)
print("DIAGNÓSTICO DE CONEXIÓN SERIAL CON ESP32")
print("=" * 60)

print(f"\n[1] Intentando conectar a {PUERTO} a {BAUDIOS} baudios...")

try:
    conexion = serial.Serial(PUERTO, BAUDIOS, timeout=TIMEOUT)
    time.sleep(2)  # Esperar a que el ESP32 se reinicie
    print(f"    ✓ Conexión establecida exitosamente")
    print(f"    Puerto: {conexion.name}")
    print(f"    Baudios: {conexion.baudrate}")
    print(f"    Timeout: {conexion.timeout}s\n")

except serial.SerialException as e:
    print(f"    ✗ ERROR: No se pudo conectar al puerto")
    print(f"    Detalles: {e}")
    print(f"    Verifica que:")
    print(f"      - El ESP32 está conectado al puerto {PUERTO}")
    print(f"      - No hay otra aplicación usando el puerto")
    print(f"      - El driver USB está instalado correctamente")
    exit(1)

print("[2] Leyendo datos del ESP32 durante 10 segundos...")
print("-" * 60)

datos_recibidos = []
tiempo_inicio = time.time()
timeout_general = 10  # segundos

try:
    while time.time() - tiempo_inicio < timeout_general:
        try:
            if conexion.in_waiting > 0:
                linea = conexion.readline().decode("utf-8", errors="ignore").strip()
                if linea:
                    print(f"RECIBIDO: {linea}")
                    datos_recibidos.append(linea)
            else:
                time.sleep(0.1)
        except UnicodeDecodeError:
            print("⚠ ERROR: Datos corruptos recibidos")
            continue

except KeyboardInterrupt:
    print("\n[!] Lectura interrumpida por el usuario")

print("-" * 60)

# Análisis de datos
print(f"\n[3] Análisis de datos recibidos:")
print(f"    Total de líneas: {len(datos_recibidos)}")

if len(datos_recibidos) == 0:
    print("\n    ✗ NO se recibieron datos del ESP32")
    print("    Posibles causas:")
    print("      - El ESP32 no tiene el código cargado correctamente")
    print("      - El ESP32 está en bootloader o no se reinició después de conectar")
    print("      - El baudrate no coincide (revisa que sea 115200)")
    print("      - Hay un problema con el cable USB o la conexión")

else:
    print(f"\n    ✓ Se recibieron {len(datos_recibidos)} líneas\n")
    
    # Verificar formato esperado
    lineas_validas = 0
    lineas_invalidas = 0
    
    for i, linea in enumerate(datos_recibidos):
        print(f"    Línea {i+1}: {linea}")
        
        if "ESP32 listo" in linea or "Enviando" in linea:
            print(f"             [INFO: Mensaje de inicialización]")
            continue
        
        partes = linea.split(",")
        if len(partes) == 3:
            try:
                lectura = int(partes[0])
                voltaje = float(partes[1])
                porcentaje = int(partes[2])
                print(f"             ✓ Formato válido: lectura={lectura}, voltaje={voltaje:.3f}V, %={porcentaje}%")
                lineas_validas += 1
            except ValueError as e:
                print(f"             ✗ Error al convertir valores: {e}")
                lineas_invalidas += 1
        else:
            print(f"             ✗ Formato inválido: esperaba 3 valores, recibió {len(partes)}")
            lineas_invalidas += 1
    
    print(f"\n    Resumen:")
    print(f"      - Líneas válidas: {lineas_validas}")
    print(f"      - Líneas inválidas: {lineas_invalidas}")
    
    if lineas_validas > 0:
        print("\n    ✓ Los datos se están recibiendo en el formato correcto")
        print("    El problema puede estar en el script serial_a_csv.py")

conexion.close()
print("\n[4] Conexión cerrada\n")
print("=" * 60)

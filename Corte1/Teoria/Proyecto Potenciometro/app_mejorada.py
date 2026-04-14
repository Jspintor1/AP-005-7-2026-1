"""
Aplicación Flask mejorada con captura de datos serial en tiempo real
- Captura datos del ESP32 en un thread separado
- Actualiza el CSV automáticamente
- Genera gráficas dinámicas
- Página web se actualiza cada 5 segundos
"""

import os
import csv
import time
import threading
from datetime import datetime
from queue import Queue

from flask import Flask, render_template
import pandas as pd
from pandas.errors import EmptyDataError
import serial
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Configuración
PUERTO_SERIAL = "COM5"
BAUDIOS = 115200
ARCHIVO_CSV = "datos_potenciometro.csv"
CARPETA_STATIC = "static"
RUTA_GRAFICA = os.path.join(CARPETA_STATIC, "grafica_potenciometro.png")

# Variables globales
conexion_serial = None
hilo_lectura = None
DETENER_LECTURA = False
datos_lock = threading.Lock()  # Para evitar conflictos entre threads

app = Flask(__name__)

def inicializar_csv():
    """Crea el CSV con encabezados si no existe"""
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["timestamp_pc", "lectura_cruda", "voltaje", "porcentaje"])
        print("[INFO] CSV creado exitosamente")

def conectar_serial():
    """Conecta al puerto serial del ESP32"""
    global conexion_serial
    try:
        conexion_serial = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        time.sleep(2)  # Esperar a que el ESP32 se reinicie
        print(f"[✓] Conexión establecida con {PUERTO_SERIAL} a {BAUDIOS} baudios")
        return True
    except serial.SerialException as e:
        print(f"[✗] Error al conectar al puerto serial: {e}")
        conexion_serial = None
        return False

def leer_datos_serial():
    """
    Thread que lee continuamente datos del puerto serial
    y los guarda en el CSV
    """
    global DETENER_LECTURA, conexion_serial
    
    print("\n[INFO] Iniciando lectura de datos del ESP32...\n")
    
    while not DETENER_LECTURA:
        try:
            if conexion_serial is None:
                # Intentar reconectar cada 5 segundos
                if not conectar_serial():
                    time.sleep(5)
                    continue
            
            if conexion_serial.in_waiting > 0:
                linea = conexion_serial.readline().decode("utf-8", errors="ignore").strip()
                
                if not linea:
                    continue
                
                # Ignorar mensajes de inicialización
                if "ESP32 listo" in linea or "Enviando" in linea:
                    continue
                
                print(f"[RECIBIDO] {linea}")
                
                # Dividir los datos
                partes = linea.split(",")
                if len(partes) != 3:
                    print("[⚠] Formato inválido, se omite")
                    continue
                
                try:
                    lectura_cruda = int(partes[0])
                    voltaje = float(partes[1])
                    porcentaje = float(partes[2])
                except ValueError as e:
                    print(f"[⚠] Error al convertir datos: {e}")
                    continue
                
                # Obtener timestamp actual
                timestamp_pc = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Guardar en CSV de forma segura (thread-safe)
                try:
                    with datos_lock:
                        with open(ARCHIVO_CSV, mode="a", newline="", encoding="utf-8") as archivo:
                            escritor = csv.writer(archivo)
                            escritor.writerow([timestamp_pc, lectura_cruda, voltaje, porcentaje])
                    print(f"[✓] Guardado en CSV")
                except Exception as e:
                    print(f"[✗] Error al escribir en CSV: {e}")
            else:
                time.sleep(0.1)
        
        except Exception as e:
            print(f"[✗] Error inesperado: {e}")
            conexion_serial = None
            time.sleep(1)

def iniciar_lectura_background():
    """Inicia el thread de lectura de datos en segundo plano"""
    global hilo_lectura, DETENER_LECTURA
    
    if hilo_lectura is not None and hilo_lectura.is_alive():
        print("[INFO] El hilo de lectura ya está activo")
        return
    
    DETENER_LECTURA = False
    hilo_lectura = threading.Thread(target=leer_datos_serial, daemon=True)
    hilo_lectura.start()
    print("[✓] Thread de lectura iniciado")

def detener_lectura_background():
    """Detiene el thread de lectura"""
    global DETENER_LECTURA, conexion_serial
    
    DETENER_LECTURA = True
    if conexion_serial is not None:
        try:
            conexion_serial.close()
            print("[✓] Conexión serial cerrada")
        except:
            pass

def cargar_datos():
    """Carga los datos del CSV"""
    if not os.path.exists(ARCHIVO_CSV):
        return pd.DataFrame()
    
    try:
        with datos_lock:
            df = pd.read_csv(ARCHIVO_CSV, parse_dates=["timestamp_pc"])
        
        if df.empty:
            return pd.DataFrame()
        
        # Convertir a tipos numéricos
        df["lectura_cruda"] = pd.to_numeric(df["lectura_cruda"], errors="coerce")
        df["voltaje"] = pd.to_numeric(df["voltaje"], errors="coerce")
        df["porcentaje"] = pd.to_numeric(df["porcentaje"], errors="coerce")
        df = df.dropna().reset_index(drop=True)
        return df
    except EmptyDataError:
        return pd.DataFrame()
    except Exception as e:
        print(f"[✗] Error al cargar CSV: {e}")
        return pd.DataFrame()

def generar_grafica(df):
    """Genera la gráfica con los datos más recientes"""
    os.makedirs(CARPETA_STATIC, exist_ok=True)
    try:
        if df.empty:
            plt.figure(figsize=(10, 4))
            plt.text(0.5, 0.5, "Aún no hay datos para graficar",
                     ha="center", va="center", fontsize=14, color="#666")
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(RUTA_GRAFICA, dpi=100, bbox_inches="tight")
            plt.close()
            return
        
        # Usar las últimas 100 muestras
        df_grafica = df.tail(100).copy()
        
        # Crear figura con mejor aspecto
        plt.figure(figsize=(14, 6))
        plt.plot(df_grafica["timestamp_pc"], df_grafica["lectura_cruda"], 
                marker="o", linewidth=2, markersize=4, color="#667eea", label="Lectura ADC")
        
        plt.title("Lecturas del Potenciómetro en Tiempo Real", fontsize=16, fontweight="bold", color="#2d3748")
        plt.xlabel("Tiempo", fontsize=12, color="#4a5568")
        plt.ylabel("Lectura ADC (0-4095)", fontsize=12, color="#4a5568")
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.grid(True, alpha=0.3, linestyle="--")
        plt.legend(fontsize=11, loc="best")
        plt.tight_layout()
        plt.savefig(RUTA_GRAFICA, dpi=100, bbox_inches="tight")
        plt.close()
    except Exception as e:
        print(f"[✗] Error al generar gráfica: {e}")

def construir_resumen(df):
    """Construye un resumen con estadísticas"""
    if df.empty:
        return {
            "total_muestras": 0,
            "ultima_lectura": "Sin datos",
            "ultimo_voltaje": "Sin datos",
            "ultimo_porcentaje": "Sin datos",
            "promedio": "Sin datos",
            "minimo": "Sin datos",
            "maximo": "Sin datos",
        }
    
    ultima = df.iloc[-1]
    return {
        "total_muestras": int(len(df)),
        "ultima_lectura": int(ultima["lectura_cruda"]),
        "ultimo_voltaje": round(float(ultima["voltaje"]), 3),
        "ultimo_porcentaje": round(float(ultima["porcentaje"]), 1),
        "promedio": round(float(df["lectura_cruda"].mean()), 2),
        "minimo": int(df["lectura_cruda"].min()),
        "maximo": int(df["lectura_cruda"].max()),
    }

@app.route("/")
def inicio():
    """Ruta principal que renderiza el dashboard"""
    try:
        df = cargar_datos()
        generar_grafica(df)
        resumen = construir_resumen(df)
        
        # Generar tabla HTML
        if df.empty:
            tabla_html = "<p>No hay datos todavía. Esperando datos del ESP32...</p>"
        else:
            tabla_html = (
                df.tail(10)
                .copy()
                .to_html(classes="tabla-datos", index=False, border=0)
            )
        
        actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return render_template(
            "index.html",
            resumen=resumen,
            tabla_html=tabla_html,
            actualizacion=actualizacion
        )
    except Exception as e:
        return f"""
        <html>
            <head><title>Error</title></head>
            <body>
                <h1>Error interno en la aplicación</h1>
                <p>Detalle: {e}</p>
            </body>
        </html>
        """, 500

@app.before_request
def antes_request():
    """Ejecuta antes de cada request"""
    pass

@app.teardown_appcontext
def al_cerrar(exception):
    """Se ejecuta cuando Flask se cierra"""
    pass

if __name__ == "__main__":
    # Preparar ambiente
    inicializar_csv()
    
    # Iniciar lectura de datos en segundo plano
    iniciar_lectura_background()
    
    try:
        # Iniciar servidor Flask
        print("\n" + "="*60)
        print("SERVIDOR FLASK INICIADO")
        print("="*60)
        print("Accede a: http://127.0.0.1:5000")
        print("Los datos se capturan automáticamente en segundo plano")
        print("="*60 + "\n")
        
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n[INFO] Apagando servidor...")
        detener_lectura_background()
        print("[✓] Aplicación cerrada correctamente")

import os
import serial
import time
import mysql.connector
from mysql.connector import Error
from colorama import init, Fore, Back, Style

# Inicialización de colorama
init(autoreset=True)

class EstacionDashboard:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.arduino = None
        self.db = None
        self.cursor = None
        self.total_lecturas = 0

    def limpiar_pantalla(self):
        """Limpia la terminal para generar el efecto de tablero en vivo"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def conectar_sistemas(self, db_host, db_user, db_pass, db_name, db_port):
        """Inicializa conexiones físicas (Serial) y relacionales (MySQL)"""
        print(Fore.CYAN + Style.BRIGHT + "==========================================================================")
        print(Fore.WHITE + Back.BLUE + Style.BRIGHT + "   ESTACION METEOROLOGICA Y AMBIENTAL - ESCUELAS PRoA (RIO III)   ".center(74))
        print(Fore.CYAN + Style.BRIGHT + "==========================================================================")
        
        # Conexión Serial con Arduino UNO
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            print(Fore.GREEN + Style.BRIGHT + f"  [SERIAL] Conectado exitosamente en puerto {self.port}")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"  [SERIAL] Error al abrir el puerto {self.port}: {e}")
            return False

        # Conexión MySQL Workbench
        try:
            self.db = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pass,
                database=db_name,
                autocommit=True
            )
            self.cursor = self.db.cursor()
            print(Fore.GREEN + Style.BRIGHT + f"  [MySQL] Conectado exitosamente a '{db_name}'")
            print(Fore.YELLOW + "\n  Inicializando panel de control en vivo...")
            time.sleep(1.5)
            return True
        except Error as e:
            print(Fore.RED + Style.BRIGHT + f"  [MySQL] Error de autenticacion/conexion: {e}")
            return False

    def obtener_evaluacion_alerta(self, temperatura, gas):
        """Determina la tarjeta de estado y nivel de riesgo ambiental"""
        if gas > 300:
            return (
                Fore.WHITE + Back.RED + Style.BRIGHT,
                "ALERTA CRITICA: Aire Impuro / Posible Fuga de Gas Detectada"
            )
        elif temperatura >= 35:
            return (
                Fore.WHITE + Back.RED + Style.BRIGHT,
                "ALERTA CLIMATICA: Ambiente con Calor Extremo"
            )
        elif temperatura <= 15:
            return (
                Fore.BLACK + Back.CYAN + Style.BRIGHT,
                "ALERTA CLIMATICA: Ambiente con Frio Extremo / Helada"
            )
        else:
            return (
                Fore.WHITE + Back.GREEN + Style.BRIGHT,
                "ESTADO OPERATIVO: Condiciones Ambientales Normales"
            )

    def renderizar_tablero(self, humedad, temperatura, gas, estado_db):
        """Dibuja la interfaz alineando con precisión milimétrica los márgenes"""
        self.limpiar_pantalla()
        self.total_lecturas += 1
        hora_actual = time.strftime("%H:%M:%S")
        fecha_actual = time.strftime("%d/%m/%Y")

        estilo_alerta, msj_alerta = self.obtener_evaluacion_alerta(temperatura, gas)

        # Ancho interno estricto en caracteres (66 de espacio útil)
        W = 66

        print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * W + "╗")
        
        # Titulo Principal
        t_title = "PANEL DE CONTROL EN VIVO - ESTACION METEOROLOGICA PRoA RIO III"
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + Back.BLUE + Style.BRIGHT + t_title.center(W) + Style.RESET_ALL + Fore.CYAN + Style.BRIGHT + "║")
        
        print(Fore.CYAN + Style.BRIGHT + "╠" + "═" * W + "╣")
        
        # Barra de estado del sistema
        t_sys = f"Fecha: {fecha_actual}  |  Hora: {hora_actual}  |  Muestras: #{self.total_lecturas}"
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.BLACK + Back.WHITE + Style.BRIGHT + t_sys.center(W) + Style.RESET_ALL + Fore.CYAN + Style.BRIGHT + "║")
        
        print(Fore.CYAN + Style.BRIGHT + "╠" + "═" * W + "╣")

        # METRICAS EN TIEMPO REAL
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + Style.BRIGHT + " METRICAS EN TIEMPO REAL:".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + f"   - HUMEDAD RELATIVA : {humedad}%".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + f"   - TEMPERATURA      : {temperatura} °C".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + f"   - CALIDAD AIRE/GAS : {gas} PPM".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        
        print(Fore.CYAN + Style.BRIGHT + "╠" + "═" * W + "╣")

        # DIAGNOSTICO AMBIENTAL
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + Style.BRIGHT + " DIAGNOSTICO AMBIENTAL:".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        print(Fore.CYAN + Style.BRIGHT + "║" + estilo_alerta + msj_alerta.center(W) + Style.RESET_ALL + Fore.CYAN + Style.BRIGHT + "║")

        print(Fore.CYAN + Style.BRIGHT + "╠" + "═" * W + "╣")

        # ESTADO DE PERSISTENCIA
        st_txt = "OK (Guardado)" if estado_db else "ERROR"
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + f"  Persistencia SQL : {st_txt} en 'mediciones'".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        print(Fore.CYAN + Style.BRIGHT + "║" + Fore.WHITE + f"  Puerto Serial    : {self.port} [OK] | Presiona Ctrl+C para salir".ljust(W) + Fore.CYAN + Style.BRIGHT + "║")
        
        print(Fore.CYAN + Style.BRIGHT + "╚" + "═" * W + "╝")

    def recibir_y_guardar(self):
        """Escucha la trama serial, actualiza BD y dispara el redibujado"""
        if not self.arduino or not self.db:
            return

        try:
            linea = self.arduino.readline().decode('utf-8', errors='ignore').strip()
            
            if linea and "ERROR" not in linea:
                datos = linea.split(',')
                
                if len(datos) == 3:
                    humedad_act = int(float(datos[0]))
                    temperatura_act = int(float(datos[1]))
                    gas_act = int(float(datos[2]))

                    # Inyección SQL
                    sql = "INSERT INTO mediciones (temperatura, humedad, gas, fecha_hora) VALUES (%s, %s, %s, NOW())"
                    valores = (temperatura_act, humedad_act, gas_act)
                    self.cursor.execute(sql, valores)
                    
                    # Render de la interfaz gráfica
                    self.renderizar_tablero(humedad_act, temperatura_act, gas_act, estado_db=True)

        except Exception as e:
            pass

    def cerrar_conexiones(self):
        """Finaliza el programa liberando recursos"""
        if self.cursor: self.cursor.close()
        if self.db: self.db.close()
        if self.arduino and self.arduino.is_open: self.arduino.close()
        self.limpiar_pantalla()
        print(Fore.WHITE + Back.BLUE + Style.BRIGHT + "\n Panel finalizado de forma segura. N²-EFMG Solutions \n")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    
    PUERTO_COM = 'COM7'
    
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASS = 'root'
    DB_NAME = 'estacionmetereologica_proa'

    mi_estacion = EstacionDashboard(port=PUERTO_COM)
    
    if mi_estacion.conectar_sistemas(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT):
        try:
            while True:
                mi_estacion.recibir_y_guardar()
                time.sleep(2)
        except KeyboardInterrupt:
            mi_estacion.cerrar_conexiones()
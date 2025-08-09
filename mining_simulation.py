"""
Author: Carlos Martín
Date: 2025-08-08
Description: Simulación de minado Bitcoin - Prueba 10.000.000 de valores nounce
"""

# Importamos las librerías que necesitamos
import hashlib  # Para calcular hashes SHA-256
import time  # Para medir el tiempo que tarda el proceso
from datetime import datetime, timezone, timedelta  # Para trabajar con fechas
import os  # Para leer variables de entorno del archivo .env
from dotenv import load_dotenv  # Para cargar el archivo .env

# Cargamos las variables del archivo .env
load_dotenv()

# DATOS DEL BLOQUE 909070 (valores fijos para el ejemplo)
# Estos son los datos reales del bloque 909070 de Bitcoin
version = 0x237d4000  # Versión del protocolo Bitcoin
hash_bloque_previo = 0x0000000000000000000083f7e2de7797878fb850ab2b606a81985bfa691b8b98  # Hash del bloque anterior
merkle_root = 0x67b44295ef9de4e6d393296aa066edf7cba0a8919d2aafd80715305173bacf0a  # Raíz del árbol Merkle
timestamp = int(datetime(2025, 8, 7, 21, 44, 54, tzinfo=timezone(timedelta(hours=2))).timestamp())  # Fecha y hora del bloque
bits = 0x1702349e  # Dificultad del minado

# CONVERSIÓN A BYTES
# Bitcoin usa formato little-endian (el byte menos significativo va primero)
version_bytes = version.to_bytes(4, byteorder='little')  # 4 bytes para la versión
hash_bloque_previo_bytes = hash_bloque_previo.to_bytes(32, byteorder='little')  # 32 bytes para el hash
merkle_root_bytes = merkle_root.to_bytes(32, byteorder='little')  # 32 bytes para merkle root
timestamp_bytes = timestamp.to_bytes(4, byteorder='little')  # 4 bytes para timestamp
bits_bytes = bits.to_bytes(4, byteorder='little')  # 4 bytes para bits

# CONSTRUCCIÓN DE LA CABECERA BASE
# Unimos todos los campos excepto el nounce (que cambiaremos en cada iteración)
cabecera_base = version_bytes + hash_bloque_previo_bytes + merkle_root_bytes + timestamp_bytes + bits_bytes

print("=== SIMULACIÓN DE MINADO BITCOIN ===")
print(f"Probando 10.000.000 valores de nounce...")
print(f"Bloque base: 909070")
print()

# PRIMERA SIMULACIÓN: MEDIR RENDIMIENTO
# Vamos a probar 10 millones de valores diferentes de nounce
# para ver qué tan rápido puede calcular hashes nuestro ordenador

# Empezamos a contar el tiempo
inicio = time.time()

# Probamos 10.000.000 valores de nounce (de 0 a 9.999.999)
for nounce in range(10000000):
    # Convertimos el nounce actual a 4 bytes en formato little-endian
    nounce_bytes = nounce.to_bytes(4, byteorder='little')
    
    # Construimos la cabecera completa añadiendo el nounce
    cabecera = cabecera_base + nounce_bytes
    
    # Calculamos el hash usando doble SHA-256 (como hace Bitcoin)
    sha256_hash = hashlib.sha256(hashlib.sha256(cabecera).digest()).digest()
    
    # Mostramos el progreso cada 100.000 intentos para no saturar la pantalla
    if nounce % 100000 == 0:
        print(f"Nounce: {nounce:_} - Hash: {sha256_hash[::-1].hex()}".replace('_', '.'))

# Paramos de contar el tiempo
fin = time.time()
tiempo_total = fin - inicio  # Calculamos cuánto tiempo ha tardado

print()
print("=== RESULTADOS ===")
# Mostramos los resultados de la simulación
print(f"Tiempo total: {tiempo_total:.2f} segundos".replace('.', ','))  # Tiempo en formato europeo
print(f"Hashes por segundo: {10000000/tiempo_total:_.0f}".replace('_', '.'))  # Velocidad de cálculo
print(f"Nounce final probado: 9.999.999")  # Último nounce que probamos
print(f"Hash final: {sha256_hash[::-1].hex()}")  # Último hash calculado

print()
print("=== BÚSQUEDA DE UN HASH VALIDO DEL BLOQUE 909070 ===")
print("Buscando el nounce correcto...")
print()

# CÁLCULO DE LA DIFICULTAD DE MINADO
# El campo 'bits' contiene la dificultad en un formato especial llamado "compacto"
# Necesitamos decodificarlo para entender qué tan difícil es minar este bloque

# Separamos el campo bits en dos partes:
exponente = (bits >> 24) & 0xFF  # Los 8 bits de la izquierda (exponente)
mantisa = bits & 0xFFFFFF  # Los 24 bits de la derecha (mantisa)

# Calculamos el "target" (objetivo): el hash debe ser menor que este número
target = mantisa * (256 ** (exponente - 3))

# Calculamos la dificultad: cuánto más difícil es que el target más fácil posible
dificultad = 0x00000000FFFF0000000000000000000000000000000000000000000000000000 / target

# Estimamos cuántos ceros debe tener el hash al principio
ceros_necesarios = len(hex(target)[2:].rjust(64, '0')) - len(hex(target)[2:].lstrip('0'))

# CONFIGURACIÓN DE LA BÚSQUEDA
# Leemos desde el archivo .env dónde empezar y cuántos valores probar
nounce_inicio = int(os.getenv('NOUNCE_START', '0x0'), 16)  # Nounce de inicio (por defecto 0)
nounce_rango = int(os.getenv('NOUNCE_RANGE', '10000000'))  # Cuántos valores probar
print(f"Iniciando búsqueda desde nounce: {nounce_inicio:_}".replace('_', '.'))
print(f"Rango de búsqueda: {nounce_rango:_} valores".replace('_', '.'))
print()

# Convertimos el target a formato hexadecimal para poder comparar
target_str_bytes = target.to_bytes(32, byteorder='big').hex()

# Mostramos información sobre la dificultad del bloque
print("Calculando dificultad y parámetros de búsqueda...")
print(f"Bits: 0x{bits:08x}")  # Campo bits original
print(f"Target: {target_str_bytes}")  # Target calculado (el hash debe ser menor que esto)
print(f"Dificultad: {dificultad:,.0f}".replace(',', '.'))  # Dificultad numérica
print(f"Ceros necesarios al inicio del hash: {ceros_necesarios}")  # Aproximación de ceros
print()

# SEGUNDA SIMULACIÓN: BUSCAR UN NOUNCE VÁLIDO
# Ahora vamos a buscar un nounce que produzca un hash válido para este bloque

# Empezamos a contar el tiempo de búsqueda
inicio_busqueda = time.time()
nounce_encontrado = None  # Variable para guardar el nounce cuando lo encontremos

# Probamos diferentes valores de nounce hasta encontrar uno válido
for nounce in range(nounce_inicio, nounce_inicio + nounce_rango):  
    # Convertimos el nounce actual a bytes
    nounce_bytes = nounce.to_bytes(4, byteorder='little')
    
    # Construimos la cabecera completa con este nounce
    cabecera = cabecera_base + nounce_bytes
    
    # Calculamos el hash de esta cabecera
    sha256_hash = hashlib.sha256(hashlib.sha256(cabecera).digest()).digest()
    hash_resultado = sha256_hash[::-1].hex()  # Lo invertimos para mostrarlo correctamente
    
    # Verificamos si este hash es menor que el target (es decir, si es válido)
    if hash_resultado < target_str_bytes:
        nounce_encontrado = nounce  # ¡Encontramos un nounce válido!
        break  # Salimos del bucle
    
    # Mostramos el progreso cada millón de intentos
    if nounce % 1000000 == 0:
        print(f"Probando nounce: {nounce:_} - Hash: {hash_resultado}".replace('_', '.'))

# Paramos de contar el tiempo de búsqueda
fin_busqueda = time.time()
tiempo_busqueda = fin_busqueda - inicio_busqueda  # Calculamos cuánto tiempo ha tardado la búsqueda

# RESULTADOS DE LA BÚSQUEDA
print()
if nounce_encontrado is not None:
    # ¡Hemos encontrado un nounce válido!
    print("¡HASH ENCONTRADO!")
    print(f"Nounce correcto: 0x{nounce_encontrado:08x} ({nounce_encontrado:_})".replace('_', '.'))
    print(f"Hash objetivo : {target_str_bytes}")  # El target que teníamos que superar
    print(f"Hash resultado: {hash_resultado}")  # El hash que hemos conseguido
    print(f"Tiempo de búsqueda: {tiempo_busqueda:.2f} segundos".replace('.', ','))
    print(f"Intentos realizados: {nounce - nounce_inicio + 1:_}".replace('_', '.'))
else:
    # No hemos encontrado ningún nounce válido en el rango que hemos probado
    print("Hash no encontrado en el rango probado")
    print("Prueba a aumentar NOUNCE_RANGE en el archivo .env o cambiar NOUNCE_START")
    print(f"Tiempo de búsqueda: {tiempo_busqueda:.2f} segundos".replace('.', ','))
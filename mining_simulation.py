"""
Author: Carlos Martín
Date: 2025-08-08
Description: Simulación de minado Bitcoin - Prueba 10.000.000 de valores nounce
"""

import hashlib
import time
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# DATOS DEL BLOQUE 909070 (fijos)
version = 0x237d4000
hash_bloque_previo = 0x0000000000000000000083f7e2de7797878fb850ab2b606a81985bfa691b8b98
merkle_root = 0x67b44295ef9de4e6d393296aa066edf7cba0a8919d2aafd80715305173bacf0a
timestamp = int(datetime(2025, 8, 7, 21, 44, 54, tzinfo=timezone(timedelta(hours=2))).timestamp())
bits = 0x1702349e

# Convertir campos fijos a bytes (little-endian)
version_bytes = version.to_bytes(4, byteorder='little')
hash_bloque_previo_bytes = hash_bloque_previo.to_bytes(32, byteorder='little')
merkle_root_bytes = merkle_root.to_bytes(32, byteorder='little')
timestamp_bytes = timestamp.to_bytes(4, byteorder='little')
bits_bytes = bits.to_bytes(4, byteorder='little')

# Cabecera base (sin nounce)
cabecera_base = version_bytes + hash_bloque_previo_bytes + merkle_root_bytes + timestamp_bytes + bits_bytes

print("=== SIMULACIÓN DE MINADO BITCOIN ===")
print(f"Probando 10.000.000 valores de nounce...")
print(f"Bloque base: 909070")
print()

# Iniciar cronómetro
inicio = time.time()

# Probar 1.000.000 valores de nounce
for nounce in range(10000000):
    # Convertir nounce actual a bytes
    nounce_bytes = nounce.to_bytes(4, byteorder='little')
    
    # Construir cabecera completa
    cabecera = cabecera_base + nounce_bytes
    
    # Calcular doble SHA-256
    sha256_hash = hashlib.sha256(hashlib.sha256(cabecera).digest()).digest()
    
    # Mostrar progreso cada 100.000 iteraciones
    if nounce % 100000 == 0:
        print(f"Nounce: {nounce:_} - Hash: {sha256_hash[::-1].hex()}".replace('_', '.'))

# Finalizar cronómetro
fin = time.time()
tiempo_total = fin - inicio

print()
print("=== RESULTADOS ===")
print(f"Tiempo total: {tiempo_total:.2f} segundos".replace('.', ','))
print(f"Hashes por segundo: {10000000/tiempo_total:_.0f}".replace('_', '.'))
print(f"Nounce final probado: 9.999.999")
print(f"Hash final: {sha256_hash[::-1].hex()}")

print()
print("=== BÚSQUEDA DEL HASH EXACTO DEL BLOQUE 909070 ===")
hash_objetivo = "00000000000000000002300fc2687557b68f1d2b2f4b617c42c998d23a66c63f"
print(f"Hash objetivo: {hash_objetivo}")
print("Buscando el nounce correcto...")
print()

# Iniciar cronómetro para la búsqueda
inicio_busqueda = time.time()
nounce_encontrado = None

# Leer variables de entorno
nounce_inicio = int(os.getenv('NOUNCE_START', '0x0'), 16)
nounce_rango = int(os.getenv('NOUNCE_RANGE', '10000000'))
print(f"Iniciando búsqueda desde nounce: {nounce_inicio:_}".replace('_', '.'))
print(f"Rango de búsqueda: {nounce_rango:_} valores".replace('_', '.'))
print()

# Buscar el nounce que produce el hash exacto
for nounce in range(nounce_inicio, nounce_inicio + nounce_rango):  
    # Convertir nounce actual a bytes
    nounce_bytes = nounce.to_bytes(4, byteorder='little')
    
    # Construir cabecera completa
    cabecera = cabecera_base + nounce_bytes
    
    # Calcular doble SHA-256
    sha256_hash = hashlib.sha256(hashlib.sha256(cabecera).digest()).digest()
    hash_resultado = sha256_hash[::-1].hex()
    
    # Verificar si coincide con el hash objetivo
    if hash_resultado == hash_objetivo:
        nounce_encontrado = nounce
        break
    
    # Mostrar progreso cada 1.000.000 iteraciones
    if nounce % 1000000 == 0:
        print(f"Probando nounce: {nounce:_} - Hash: {hash_resultado}".replace('_', '.'))

# Finalizar cronómetro de búsqueda
fin_busqueda = time.time()
tiempo_busqueda = fin_busqueda - inicio_busqueda

print()
if nounce_encontrado is not None:
    print("¡HASH ENCONTRADO!")
    print(f"Nounce correcto: 0x{nounce_encontrado:08x} ({nounce_encontrado:_})".replace('_', '.'))
    print(f"Hash obtenido: {hash_resultado}")
    print(f"Tiempo de búsqueda: {tiempo_busqueda:.2f} segundos".replace('.', ','))
    print(f"Intentos realizados: {nounce - nounce_inicio + 1:_}".replace('_', '.'))
else:
    print("Hash no encontrado en el rango probado")
    print(f"Tiempo de búsqueda: {tiempo_busqueda:.2f} segundos".replace('.', ','))
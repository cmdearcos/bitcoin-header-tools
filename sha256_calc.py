"""
Author: Carlos Martín
Date: 2025-08-08
Description: Script para calcular el hash SHA-256 de un bloque de Bitcoin.
"""


# Importamos las librerías necesarias
import hashlib  # Para calcular hashes SHA-256
from datetime import datetime, timezone, timedelta  # Para trabajar con fechas
import os  # Para leer variables de entorno
from dotenv import load_dotenv  # Para cargar el archivo .env

# Cargamos las variables del archivo .env
load_dotenv()

# DATOS DEL BLOQUE DE BITCOIN (valores por defecto del bloque 909070)
version = int(os.getenv('VERSION', '0x237d4000'), 16)  # Versión del protocolo Bitcoin
hash_bloque_previo = int(os.getenv('HASH_BLOQUE_PREVIO', '0x0000000000000000000083f7e2de7797878fb850ab2b606a81985bfa691b8b98'), 16)  # Hash del bloque anterior
merkle_root = int(os.getenv('MERKLE_ROOT', '0x67b44295ef9de4e6d393296aa066edf7cba0a8919d2aafd80715305173bacf0a'), 16)  # Raíz del árbol Merkle
timestamp = int(os.getenv('TIMESTAMP', str(int(datetime(2025, 8, 7, 21, 44, 54, tzinfo=timezone(timedelta(hours=2))).timestamp()))))  # Fecha y hora del bloque
bits = int(os.getenv('BITS', '0x1702349e'), 16)  # Dificultad del minado
nounce = int(os.getenv('NOUNCE', '0x1858a28d'), 16)  # Número usado una sola vez (para el minado)

# CONVERSIÓN A BYTES
# Bitcoin usa formato little-endian (el byte menos significativo va primero)
version_bytes = version.to_bytes(4, byteorder='little')  # 4 bytes para la versión
hash_bloque_previo_bytes = hash_bloque_previo.to_bytes(32, byteorder='little')  # 32 bytes para el hash
merkle_root_bytes = merkle_root.to_bytes(32, byteorder='little')  # 32 bytes para merkle root
timestamp_bytes = timestamp.to_bytes(4, byteorder='little')  # 4 bytes para timestamp
bits_bytes = bits.to_bytes(4, byteorder='little')  # 4 bytes para bits
nounce_bytes = nounce.to_bytes(4, byteorder='little')  # 4 bytes para nounce

# Mostramos cada campo en formato hexadecimal
print(f"Version: {version_bytes.hex()}")
print(f"Hash del bloque previo: {hash_bloque_previo_bytes.hex()}")
print(f"Merkle root: {merkle_root_bytes.hex()}")
print(f"Timestamp: {timestamp_bytes.hex()}")
print(f"Bits: {bits_bytes.hex()}")
print(f"Nounce: {nounce_bytes.hex()}")

# CONSTRUCCIÓN DE LA CABECERA
# Concatenamos (unimos) todos los campos en el orden correcto
cabecera = version_bytes + hash_bloque_previo_bytes + merkle_root_bytes + timestamp_bytes + bits_bytes + nounce_bytes

print(f"Cabecera (bytes): {cabecera.hex()}")
print(f"Cabecera (longitud): {len(cabecera)} bytes")  # Debe ser 80 bytes en total

# CÁLCULO DEL HASH DEL BLOQUE
# Bitcoin usa doble SHA-256: SHA-256(SHA-256(cabecera))
sha256_hash = hashlib.sha256(hashlib.sha256(cabecera).digest()).digest()

# El resultado se muestra en orden inverso (little-endian)
print(f"SHA-256: {sha256_hash[::-1].hex()}")

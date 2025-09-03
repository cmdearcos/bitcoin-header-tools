#!/usr/bin/env python3
"""
Bitcoin Wallet Address Generator - Genera direcciones P2PKH de Bitcoin
"""

import hashlib
import base58
import argparse
import os
import secrets

def hash160(data):
    """Aplica SHA256 seguido de RIPEMD160"""
    sha256_hash = hashlib.sha256(data).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    return ripemd160_hash

def generate_private_key():
    """Genera una clave privada aleatoria de 32 bytes"""
    return secrets.randbits(256).to_bytes(32, 'big')

def private_key_to_public_key(private_key):
    """Convierte clave privada a clave pública (versión simplificada)"""
    # NOTA: Esta es una implementación simplificada
    # En producción se debe usar una librería como ecdsa o cryptography
    import ecdsa
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    
    # Clave pública no comprimida
    uncompressed = b'\x04' + vk.to_string()
    
    # Clave pública comprimida
    x, y = vk.to_string()[:32], vk.to_string()[32:]
    prefix = b'\x02' if int.from_bytes(y, 'big') % 2 == 0 else b'\x03'
    compressed = prefix + x
    
    return uncompressed, compressed

def public_key_to_address(public_key):
    """Convierte clave pública a dirección Bitcoin P2PKH"""
    # Paso 1: Hash160 de la clave pública
    pubkey_hash = hash160(public_key)
    
    # Paso 2: Añadir byte de versión (0x00 para mainnet)
    versioned_hash = b'\x00' + pubkey_hash
    
    # Paso 3: Doble SHA256 para checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
    
    # Paso 4: Concatenar y codificar en Base58
    address_bytes = versioned_hash + checksum
    address = base58.b58encode(address_bytes).decode('utf-8')
    
    return address

def generate_wallet():
    """Genera una wallet completa (clave privada, pública y dirección)"""
    # Generar clave privada
    private_key = generate_private_key()
    
    # Generar claves públicas (no comprimida y comprimida)
    public_key_uncompressed, public_key_compressed = private_key_to_public_key(private_key)
    
    # Generar SHA256 de la clave pública comprimida (estándar moderno)
    sha256_hash = hashlib.sha256(public_key_compressed).digest()
    
    # Generar pubKeyHash (Hash160) usando clave comprimida
    pubkey_hash = hash160(public_key_compressed)
    
    # Calcular checksum del pubKeyHash
    versioned_hash = b'\x00' + pubkey_hash
    checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
    
    # Generar dirección usando clave comprimida
    address = public_key_to_address(public_key_compressed)
    
    return {
        'private_key': private_key.hex(),
        'public_key': public_key_uncompressed.hex(),
        'public_key_compressed': public_key_compressed.hex(),
        'sha256': sha256_hash.hex(),
        'pubKeyHash': pubkey_hash.hex(),
        'checksum': checksum.hex(),
        'address': address
    }

def compressed_pubkey_to_address(compressed_pubkey_hex):
    """Convierte una clave pública comprimida a dirección Bitcoin P2PKH"""
    try:
        compressed_pubkey = bytes.fromhex(compressed_pubkey_hex)
        if len(compressed_pubkey) != 33 or compressed_pubkey[0] not in [0x02, 0x03]:
            raise ValueError("Clave pública comprimida inválida")
        
        # Generar SHA256 de la clave pública comprimida
        sha256_hash = hashlib.sha256(compressed_pubkey).digest()
        
        pubkey_hash = hash160(compressed_pubkey)
        
        # Calcular checksum del pubKeyHash
        versioned_hash = b'\x00' + pubkey_hash
        checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
        
        address = public_key_to_address(compressed_pubkey)
        
        return {
            'public_key_compressed': compressed_pubkey_hex,
            'sha256': sha256_hash.hex(),
            'pubKeyHash': pubkey_hash.hex(),
            'checksum': checksum.hex(),
            'address': address
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generador de direcciones Bitcoin P2PKH')
    parser.add_argument('-n', '--number', type=int, default=1, help='Número de direcciones a generar')
    parser.add_argument('-o', '--output', help='Archivo de salida (opcional)')
    parser.add_argument('--from-pubkey', help='Generar dirección desde clave pública comprimida (hex)')
    
    args = parser.parse_args()
    
    # Generar dirección desde clave pública comprimida
    if args.from_pubkey:
        print("=== GENERADOR DESDE CLAVE PÚBLICA COMPRIMIDA ===\n")
        result = compressed_pubkey_to_address(args.from_pubkey)
        if result:
            print(f"Clave pública comprimida: {result['public_key_compressed']}")
            print(f"SHA256: {result['sha256']}")
            print(f"pubKeyHash: {result['pubKeyHash']}")
            print(f"Checksum: {result['checksum']}")
            print(f"Dirección: {result['address']}")
            
            if args.output:
                import json
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResultado guardado en {args.output}")
        return
    
    # Generar wallets completas
    wallets = []
    print("=== GENERADOR DE WALLETS BITCOIN P2PKH ===\n")
    
    for i in range(args.number):
        wallet = generate_wallet()
        wallets.append(wallet)
        
        print(f"Wallet {i+1}:")
        print(f"  Dirección: {wallet['address']}")
        print(f"  Clave privada: {wallet['private_key']}")
        print(f"  Clave pública: {wallet['public_key']}")
        print(f"  Clave pública comprimida: {wallet['public_key_compressed']}")
        print(f"  SHA256: {wallet['sha256']}")
        print(f"  pubKeyHash: {wallet['pubKeyHash']}")
        print(f"  Checksum: {wallet['checksum']}")
        print()
    
    # Guardar en archivo si se especifica
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(wallets, f, indent=2)
        print(f"Wallets guardadas en {args.output}")

if __name__ == "__main__":
    main()
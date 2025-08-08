# Calculadora de Hash SHA-256 para Bloques de Bitcoin

## ¿Qué hace este programa?

Este script de Python calcula el **hash SHA-256** de un bloque de Bitcoin. Es una herramienta educativa para entender cómo funciona la tecnología blockchain y el proceso de minado de Bitcoin.

Surge de los comentarios recibidos después de publicar el LinkedIn el artículo [¿Tiene sentido minar bitcoins desde casa? (part I)](https://www.linkedin.com/pulse/tiene-sentido-minar-bitcoins-desde-casa-part-i-carlos-mart%C3%ADn-de-arcos-qs25f/?trackingId=2s6K31FzTpi1qautzIsdSA%3D%3D)

## ¿Qué es un hash SHA-256?

Un hash SHA-256 es como una "huella digital" única de los datos. Si cambias aunque sea un solo bit de información, el hash resultante será completamente diferente. Bitcoin usa este sistema para:
- Identificar cada bloque de forma única
- Verificar que los datos no han sido modificados
- Realizar el proceso de minado

## ¿Cómo funciona?

### 1. Estructura de un bloque Bitcoin
Cada bloque de Bitcoin tiene una **cabecera** con 6 campos importantes:
- **Versión**: Versión del protocolo Bitcoin
- **Hash del bloque previo**: Enlace al bloque anterior
- **Merkle Root**: Resumen de todas las transacciones
- **Timestamp**: Fecha y hora del bloque
- **Bits**: Nivel de dificultad del minado
- **Nounce**: Número que cambian los mineros para encontrar el hash correcto

### 2. Proceso del script
1. **Lee los datos** del archivo `.env` (o usa los valores por defecto del bloque [909070](https://btcscan.org/block/00000000000000000002300fc2687557b68f1d2b2f4b617c42c998d23a66c63f))
2. **Convierte cada campo** a formato binario (bytes)
3. **Une todos los campos** para formar la cabecera completa (80 bytes)
4. **Calcula el hash** usando doble SHA-256
5. **Muestra el resultado** en formato hexadecimal

## Instalación y uso

### Requisitos
- Python 3.6 o superior
- Librería `python-dotenv`

### Instalación
```bash
pip install python-dotenv
```

### Configuración
1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` con los datos del bloque que quieras analizar:
   ```
   VERSION=0x237d4000
   HASH_BLOQUE_PREVIO=0x0000000000000000000083f7e2de7797878fb850ab2b606a81985bfa691b8b98
   MERKLE_ROOT=0x67b44295ef9de4e6d393296aa066edf7cba0a8919d2aafd80715305173bacf0a
   TIMESTAMP=1753710054
   BITS=0x1702349e
   NOUNCE=0x1858a28d
   ```

### Ejecución
```bash
python sha256_calc.py
```

## Ejemplo de salida
```
Version: 00407d23
Hash del bloque previo: 98b8b91b5f...
Merkle root: 0acf3b1751...
Timestamp: 36029568
Bits: 9e340217
Nounce: 8da25818
Cabecera (bytes): 00407d23...
Cabecera (longitud): 80 bytes
SHA-256: 00000000000000001e8d6829a8a21adc5d38d0a473b144b6765798e61f98bd1d
```

## Datos por defecto
Si no modificas el archivo `.env`, el script usará los datos del **bloque 909070** de Bitcoin como ejemplo.

## Conceptos importantes

### Little-endian vs Big-endian
Bitcoin usa formato **little-endian**, que significa que los bytes se almacenan "al revés". Por ejemplo:
- Número: `0x12345678`
- Little-endian: `78 56 34 12`
- Big-endian: `12 34 56 78`

### Doble SHA-256
Bitcoin no usa SHA-256 una sola vez, sino **dos veces seguidas**:
```
Hash final = SHA-256(SHA-256(cabecera))
```

Esto proporciona mayor seguridad contra ciertos tipos de ataques.

## Archivos del proyecto
- `sha256_calc.py` - Script principal
- `.env` - Configuración de variables (crear desde .env.example)
- `.env.example` - Ejemplo de configuración con datos del bloque 909070
- `README.md` - Este archivo de documentación

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes usar, modificar y distribuir este código libremente, pero debes:
- Mantener el aviso de copyright original
- Incluir la licencia MIT en cualquier copia o distribución
- Indicar claramente las modificaciones que hayas realizado

Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor
Carlos Martín - 2025-08-08
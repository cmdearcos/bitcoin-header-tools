# Changelog

Todas las modificaciones importantes de este proyecto serán documentadas en este archivo.

## [Unreleased] - 2025-08-08

### Agregado
- **Nuevo script `mining_simulation.py`**: Simulación completa del proceso de minado de Bitcoin
  - Prueba 10.000.000 valores de nounce secuenciales
  - Mide rendimiento (hashes por segundo)
  - Busca el hash exacto del bloque 909070
  - Configurable mediante variables de entorno
- **Variables de entorno para simulación**:
  - `NOUNCE_START`: Valor inicial del nounce
  - `NOUNCE_RANGE`: Cantidad de valores a probar
- **Soporte para variables de entorno** en `sha256_calc.py`
  - Carga configuración desde archivo `.env`
  - Valores por defecto del bloque 909070 si no se especifican
- **Archivos de configuración**:
  - `.env.example` con datos del bloque 909070
  - `.gitignore` para excluir archivos sensibles
- **Documentación completa**:
  - `README.md` expandido con ejemplos y explicaciones
  - Sección específica del bloque 909070 con imagen
  - Documentación de ambos scripts

### Mejorado
- **Comentarios educativos** en el código para alumnos de 1º FP
- **Formato europeo** para números:
  - Punto (.) como separador de miles
  - Coma (,) como separador decimal en tiempos
- **Salida más informativa** con progreso detallado
- **Manejo de errores** y validación de entrada

### Cambiado
- **Estructura del proyecto** reorganizada con múltiples scripts
- **Configuración centralizada** en archivo `.env`
- **Formato de salida** mejorado con separadores de miles

## [0.0.1](https://github.com/cmdearcos/bitcoin-header-tools/releases/tag/0.0.1) - Versión inicial

### Agregado
- Script básico `sha256_calc.py` para calcular hash SHA-256
- Cálculo de hash de un bloque Bitcoin con valores hardcodeados
- Funcionalidad básica de doble SHA-256
- Conversión a formato little-endian
- **Licencia MIT** (`LICENSE`)

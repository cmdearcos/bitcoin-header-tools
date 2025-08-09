# Changelog

Todas las modificaciones importantes de este proyecto serán documentadas en este archivo.

## [0.0.2](https://github.com/cmdearcos/bitcoin-header-tools/releases/tag/0.0.2) - Simulación de minado

### Agregado
- **Nuevo script `mining_simulation.py`**: Simulación completa del proceso de minado de Bitcoin
  - **Fase 1**: Prueba 10.000.000 valores de nounce para medir rendimiento
  - **Fase 2**: Busca un nounce que produzca un hash válido (menor que el target)
  - **Cálculo de dificultad**: Decodifica el campo bits y calcula target y dificultad
  - **Información detallada**: Muestra bits, target, dificultad y ceros necesarios
  - Configurable mediante variables de entorno
- **Variables de entorno para simulación**:
  - `NOUNCE_START`: Valor inicial del nounce (soporta hexadecimal)
  - `NOUNCE_RANGE`: Cantidad de valores a probar
- **Soporte para variables de entorno** en `sha256_calc.py`
  - Carga configuración desde archivo `.env`
  - Valores por defecto del bloque 909070 si no se especifican
- **Archivos de configuración**:
  - `.env.example` con datos del bloque 909070
  - `.gitignore` para excluir archivos sensibles
- **Documentación completa**:
  - `README.md` expandido con ejemplos y explicaciones actualizadas
  - Sección específica del bloque 909070 con imagen
  - Documentación de ambos scripts actualizada
  - `CHANGELOG.md` para historial de versiones

### Mejorado
- **Formato europeo** para números:
  - Punto (.) como separador de miles
  - Coma (,) como separador decimal en tiempos
- **Salida más informativa** con:
  - Progreso detallado cada millón de intentos
  - Comparación entre hash objetivo y resultado
  - Número de intentos realizados
  - Sugerencias si no se encuentra el hash
- **Algoritmo de búsqueda mejorado**: Busca hashes válidos en lugar del hash exacto

### Cambiado
- **Estructura del proyecto** reorganizada con múltiples scripts
- **Configuración centralizada** en archivo `.env`
- **Formato de salida** mejorado con separadores de miles
- **Lógica de búsqueda**: Cambiada de hash exacto a hash válido (< target)

## [0.0.1](https://github.com/cmdearcos/bitcoin-header-tools/releases/tag/0.0.1) - Versión inicial

### Agregado
- Script básico `sha256_calc.py` para calcular hash SHA-256
- Cálculo de hash de un bloque Bitcoin con valores hardcodeados
- Funcionalidad básica de doble SHA-256
- Conversión a formato little-endian
- **Licencia MIT** (`LICENSE`)

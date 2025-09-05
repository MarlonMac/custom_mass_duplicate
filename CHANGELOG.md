# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---
## [Unreleased]

---
## [2.2.1] - 2025-09-05

### Fixed
- **Error de Redondeo de Tasa de Cambio**: Se corrigió un error crítico donde la tasa de cambio se redondeaba a 2 decimales, causando cálculos de precios incorrectos. La precisión completa de la tasa ahora se mantiene en todo el proceso.
- **Diagnóstico de "Copiar Costo"**: Se añadió logging detallado para investigar por qué la función de copiar costo podría no estar funcionando como se espera en ciertos escenarios.

---
## [2.2.0] - 2025-09-05

### Added
- **Ajuste de Precio de Venta**: Se añadió una sección en el wizard para aplicar un ajuste porcentual al precio de venta en el destino.
- **Selección de Tipo de Tasa Manual**: El usuario ahora puede especificar si la tasa de cambio manual es un 'divisor' o un 'multiplicador', eliminando ambigüedad.

### Changed
- **UI del Wizard**: Se reestructuró la sección de conversión de moneda para mayor claridad y se corrigieron problemas de alineación.

---
## [2.1.1] - 2025-09-04

### Fixed
- **KeyError en `standard_price`**: Se solucionó un error fatal que ocurría al intentar convertir el precio de coste cuando la opción de copiar coste estaba desactivada.
- **Error de Vista (attrs)**: Se corrigió un `ValueError: malformed node or string` causado por una sintaxis incorrecta en la vista del wizard, que impedía su apertura.

---
## [2.1.0] - 2025-09-04

### Added
- **Soporte Multi-Moneda**: El job de duplicación ahora detecta si la compañía de origen y destino tienen monedas diferentes y convierte los precios.
- **Tasa de Cambio Manual**: Se añadió una opción en el asistente para que el usuario pueda introducir una tasa de cambio manual.
- **Opción para Copiar Coste**: El usuario ahora puede elegir explícitamente si desea copiar el precio de coste (`standard_price`).
- **Dependencia de Contabilidad**: Se añadió `account` a las dependencias.

### Changed
- **UX del Asistente Mejorada**: El asistente ahora muestra la moneda de origen, la de destino y la tasa de cambio que se aplicará, proporcionando mayor claridad al usuario.

---
## [2.0.0] - 2025-09-04

### Added
- **Procesamiento Asíncrono**: Implementación de un sistema de cola de trabajos (`product.duplication.job`).
- **Monitor de Trabajos**: Nueva vista en `Inventario > Operaciones > Duplication Jobs`.
- **Tarea Programada (Cron)** para procesar los trabajos pendientes.
- **Acción para Re-encolar** trabajos fallidos.

### Changed
- **Cambio Arquitectónico (MAJOR)**: El proceso pasa de ser síncrono a asíncrono.

---
## [1.0.0] - 2025-09-04

### Added
- Creación Inicial del Módulo y wizard para la duplicación masiva.
- Lógica de Dos Pasadas y grupo de permisos "Gestor de Duplicación de Productos".
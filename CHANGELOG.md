# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---
## [Unreleased]

---
## [2.0.0] - 2025-09-04

### Added
- **Procesamiento Asíncrono**: Se implementó un sistema de cola de trabajos (`product.duplication.job`) para manejar duplicaciones masivas en segundo plano, evitando timeouts del servidor.
- **Monitor de Trabajos**: Nueva vista en `Inventario > Operaciones > Duplication Jobs` para ver el estado de las duplicaciones.
- **Tarea Programada (Cron)**: Se añadió un cron que se ejecuta cada minuto para procesar los trabajos pendientes.
- **Acción para Re-encolar**: Los trabajos fallidos ahora pueden ser re-encolados para un nuevo intento desde la vista del job.
- **Vista de Lista Personalizada**: La lista de productos dentro del job ahora es simplificada y no muestra columnas de stock para evitar confusiones.

### Changed
- **Cambio Arquitectónico (MAJOR)**: El proceso de duplicación pasa de ser síncrono (bloqueante) a asíncrono (en segundo plano). El asistente ahora solo crea un job en lugar de realizar el trabajo directamente.

---
## [1.0.0] - 2025-09-04

### Added
- Creación Inicial del Módulo y wizard para la duplicación masiva.
- Lógica de Dos Pasadas para reconstruir relaciones de forma estable.
- Grupo de permisos "Gestor de Duplicación de Productos" para controlar el acceso.

### Fixed
- Resueltos errores de permisos multi-empresa utilizando `sudo()`.
- Corregido `KeyError` al manejar los modelos `product.template` y `product.product`.
- Solucionados errores de restricción de BD usando el método `copy_data()` + `create()`.

### Changed
- **Workaround para Productos Opcionales**: Se deshabilitó la duplicación de `optional_product_ids` para garantizar la funcionalidad.
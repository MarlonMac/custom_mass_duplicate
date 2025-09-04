# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] - 2025-09-04

### Added
- **Creación Inicial del Módulo:** Estructura de archivos y wizard para la duplicación masiva.
- **Lógica de Dos Pasadas:** Se crea primero los productos y luego se reconstruyen las relaciones para mayor estabilidad.
- **Seguridad:** Creado el grupo de permisos "Gestor de Duplicación de Productos" para controlar el acceso a la acción.
- **Notificaciones:** Se muestra un mensaje de éxito al usuario al finalizar el proceso.

### Fixed
- Resueltos errores de permisos multi-empresa utilizando `sudo()` de forma controlada.
- Corregido `KeyError` al manejar incorrectamente los modelos `product.template` y `product.product`.
- Solucionados errores de restricción de base de datos al adoptar el método `copy_data()` + `create()` para la creación de registros.

### Changed
- **Workaround para Productos Opcionales:** Se deshabilita la duplicación de `optional_product_ids` para evitar errores de base de datos y garantizar la funcionalidad del módulo. El log y la notificación al usuario informan de esta omisión.
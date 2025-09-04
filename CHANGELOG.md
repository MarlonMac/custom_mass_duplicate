# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- (Ninguno)

---

## [1.0.0] - 2025-09-04

### Added
- **Creación Inicial del Módulo:** Estructura de archivos base para `custom_mass_duplicate`.
- **Asistente de Duplicación:** Se añade el modelo transitorio `product.duplicate.wizard` que permite al usuario seleccionar una compañía y un sitio web de destino.
- **Acción de Servidor:** Se crea la acción `action_open_product_duplicate_wizard` que se vincula al modelo `product.template` y aparece en el menú "Acción" en las vistas de lista y formulario de productos.
- **Lógica de Duplicación:** El método `action_duplicate_products` gestiona la copia de los `product.template` seleccionados. Se asegura la preservación de todos los datos relevantes como nombre, imágenes, descripciones y variantes.
- **Manejo de Conflictos de Referencia Interna:** Implementada la estrategia inicial y segura: si un `product.product` con la misma referencia interna ya existe en la compañía de destino, el campo en el nuevo producto se deja vacío para prevenir errores de unicidad en la base de datos.
- **Permisos de Seguridad:** Añadido el archivo `ir.model.access.csv` para conceder acceso al asistente a los grupos de usuarios apropiados.
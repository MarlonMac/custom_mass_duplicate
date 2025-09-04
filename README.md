# Módulo de Duplicación Masiva de Productos v1.0.0

Este módulo para Odoo 16 Community Edition proporciona una herramienta para duplicar masivamente productos de una compañía a otra, manteniendo toda su información, incluyendo imágenes, descripciones y referencias internas.

## Propósito

Facilita la gestión de catálogos en un entorno multi-empresa, eliminando la necesidad de crear productos manualmente cuando ya existen en otra compañía de la misma base de datos.

## Instalación

1.  Coloca este módulo en tu carpeta de `addons`.
2.  Reinicia el servicio de Odoo.
3.  Ve a `Aplicaciones`, actualiza la lista y busca e instala "Duplicador Masivo de Productos Multi-Empresa".

## Uso

1.  Asegúrate de que el usuario que realizará la operación pertenezca al grupo de seguridad **"Gestor de Duplicación de Productos"**. Puedes asignarlo en `Ajustes > Usuarios y Compañías > Grupos`.
2.  Navega a la vista de lista de productos (en Inventario o Sitio Web).
3.  Selecciona los productos que deseas duplicar.
4.  Haz clic en el menú `Acción > Duplicate to Company`.
5.  En el asistente, selecciona la compañía y el sitio web de destino.
6.  Haz clic en el botón `Duplicate`.

## Limitaciones Conocidas (v1.0.0)

* **Productos Opcionales**: Debido a conflictos con restricciones de base de datos en ciertos entornos de Odoo, la duplicación de los "Productos Opcionales" (`optional_product_ids`) está desactivada. Estos deben ser reasignados manualmente después de la duplicación.
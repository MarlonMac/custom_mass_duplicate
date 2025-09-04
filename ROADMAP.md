# Roadmap del Módulo: Duplicación Masiva de Productos

Este documento describe la dirección futura y las características planificadas para el módulo.

---

## Versión 1.0.0 - Lanzamiento Inicial
**Estado:** Liberado ✔️

Versión base estable que permite la duplicación masiva de productos y sus relaciones principales entre compañías.

* **Funcionalidad Principal:** Duplicación de productos con imágenes, variantes, accesorios y alternativos.
* **Seguridad:** Acceso restringido por grupo de permisos.
* **Workaround Implementado:** Omite la duplicación de "Productos Opcionales" para garantizar la estabilidad.

---

## Versión 1.1.0 - Soporte Extendido
**Estado:** Planificado 📝

El objetivo de esta versión es resolver las limitaciones conocidas de la v1.0.0 y añadir soporte para escenarios empresariales más complejos.

* **Investigación y Soporte para Productos Opcionales:**
    * Analizar la causa raíz del conflicto de base de datos con el campo `optional_product_ids`.
    * Implementar una solución que permita la duplicación de este campo de forma segura, compatible con los módulos de eCommerce de Odoo.

* **Soporte Multi-Moneda:**
    * Detectar si la compañía de origen y destino usan diferentes monedas.
    * Si las monedas son diferentes, buscar el tipo de cambio configurado en Odoo.
    * Convertir los campos de precio (Precio de Venta, Coste, etc.) a la nueva moneda durante la duplicación.

---

## Futuras Mejoras (Sin Versión Asignada)
**Estado:** Ideas 💡

* **Asistente de Evaluación de Conflictos:** Implementar un modo "dry run" que analice los productos a duplicar y presente un resumen de posibles conflictos (referencias internas duplicadas, enlaces que se perderán) antes de ejecutar la duplicación.
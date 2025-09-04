# Roadmap del Módulo: Duplicación Masiva de Productos

Este documento describe la dirección futura y las características planificadas para el módulo.

---
## Versión 2.0.0 - Arquitectura Asíncrona
**Estado:** Liberado ✔️

Re-arquitectura completa del módulo para soportar grandes volúmenes de datos sin timeouts, mediante un sistema de trabajos en segundo plano.

* **Funcionalidad Principal:** Duplicación asíncrona con cola de trabajos y monitor de estado.
* **Workaround Implementado:** Sigue omitiendo la duplicación de "Productos Opcionales".

---
## Versión 2.1.0 - Soporte Multi-Moneda y UX
**Estado:** Planificado 📝

El objetivo de esta versión será robustecer el módulo para escenarios de negocio más complejos y mejorar la experiencia de usuario durante el procesamiento de los jobs.

* **PRIORIDAD: Soporte Multi-Moneda:**
    * Detectar si la compañía de origen y destino usan diferentes monedas.
    * Si las monedas son diferentes, buscar el tipo de cambio configurado en Odoo.
    * Convertir los campos de precio (Precio de Venta, Coste, etc.) a la nueva moneda durante la duplicación.

* **Mejoras de UX para Jobs:**
    * **Barra de Progreso:** Investigar e implementar un indicador visual en el formulario del job que muestre el progreso (ej. "Procesando producto 45 de 450").
    * **Botón de Cancelación:** Añadir una opción para que un administrador pueda detener un job que esté `Pendiente` o `En Progreso`.

---
## Futuras Mejoras (Sin Versión Asignada)
**Estado:** Ideas 💡

* **Soporte para Productos Opcionales:** Analizar la causa raíz del conflicto de base de datos con el campo `optional_product_ids` e implementar una solución compatible.
* **Asistente de Evaluación de Conflictos:** Implementar un modo "dry run" que analice los productos y presente un resumen de posibles conflictos antes de ejecutar la duplicación.
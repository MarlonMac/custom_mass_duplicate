# Roadmap del Módulo: Duplicación Masiva de Productos

Este documento describe la dirección futura y las características planificadas para el módulo.

---
## Versión 2.0.0 - Arquitectura Asíncrona
**Estado:** Liberado ✔️

Re-arquitectura completa del módulo para soportar grandes volúmenes de datos sin timeouts, mediante un sistema de trabajos en segundo plano.

---
## Versión 2.1.1 - Soporte Multi-Moneda y Correcciones
**Estado:** Liberado ✔️

Se robusteció el módulo para escenarios de negocio multi-moneda y se mejoró la experiencia de usuario en el asistente de duplicación.

* **Funcionalidad Principal:**
    * Conversión automática de precios entre diferentes monedas.
    * Opción para anular la tasa de Odoo con una tasa manual por operación.
    * Opción para incluir o excluir el precio de coste en la duplicación.
* **Correcciones (Parches):**
    * Solucionado `KeyError` al procesar precios de coste.
    * Solucionado error que impedía abrir el asistente (wizard).

---
## Versión 2.2.0 - Mejoras de UX para Jobs
**Estado:** Planificado 📝

El objetivo de esta versión será mejorar la monitorización y control de los trabajos de duplicación que ya están en la cola.

* **Barra de Progreso:** Investigar e implementar un indicador visual en el formulario del job que muestre el progreso en tiempo real (ej. "Procesando producto 45 de 450"). Esto probablemente requerirá el uso del bus de Odoo o polling desde el cliente.

* **Botón de Cancelación:** Añadir una opción para que un administrador pueda detener un job que esté `Pendiente` o `En Progreso`. Un job cancelado no podrá ser re-encolado y pasará a un estado `cancelled`.

---
## Futuras Mejoras (Sin Versión Asignada)
**Estado:** Ideas 💡

* **Soporte para Productos Opcionales:** Analizar la causa raíz del conflicto de base de datos con el campo `optional_product_ids` e implementar una solución compatible.
* **Asistente de Evaluación de Conflictos:** Implementar un modo "dry run" que analice los productos y presente un resumen de posibles conflictos antes de ejecutar la duplicación.
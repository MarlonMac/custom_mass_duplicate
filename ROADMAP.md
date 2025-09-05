# Roadmap del Módulo: Duplicación Masiva de Productos

Este documento describe la dirección futura y las características planificadas para el módulo.

---
## Versión 2.2.1 - Cálculo de Precios Avanzado
**Estado:** Liberado (con limitaciones conocidas) ✔️

Esta versión introduce un control granular y preciso sobre el cálculo de precios en la duplicación, incluyendo ajustes de margen y manejo flexible de tasas de cambio.

* **Funcionalidad Principal:**
    * Cálculo de precios con alta precisión decimal.
    * Opción para aplicar un margen porcentual sobre el precio de venta.
    * Control explícito sobre el tipo de tasa de cambio manual (divisor/multiplicador).
* **Limitación Conocida:** La copia del campo coste (`standard_price`) no funciona y se abordará en la siguiente versión.

---
## Versión 2.3.0 - Gestión de Conflictos y Correcciones
**Estado:** Planificado 📝

El objetivo de esta versión es solucionar el bug pendiente del coste y añadir una funcionalidad crítica para entornos maduros: la gestión de conflictos por duplicados.

* **PRIORIDAD: Corregir bug de Copia de Coste:**
    * Investigar y solucionar el problema de raíz por el cual `standard_price` se lee como `0.0` en el job de segundo plano. Se explorarán métodos alternativos de lectura de datos para eludir el problema de contexto del ORM.

* **Gestión de Conflictos por Referencia Interna:**
    * Añadir una opción en el wizard para que el usuario decida qué hacer si un producto con la misma Referencia Interna (`default_code`) ya existe en la compañía de destino. Las opciones serán:
        * **No copiar**: Omitir los productos que ya existen.
        * **Crear copia (Ref. vacía)**: Crear el duplicado pero dejar su campo de Referencia Interna en blanco.
        * **Crear copia (Sufijo)**: Crear el duplicado y añadir un sufijo (ej. "-COPIA") a su Referencia Interna para evitar conflictos.
        * **Sobrescribir datos**: Actualizar ciertos campos del producto existente en el destino con los valores del producto de origen (esta opción se analizará con cuidado por su potencial destructivo).

---
## Futuras Mejoras (Sin Versión Asignada)
**Estado:** Ideas 💡

El objetivo de esta versión será mejorar la monitorización y control de los trabajos de duplicación que ya están en la cola.

* **Barra de Progreso:** Investigar e implementar un indicador visual en el formulario del job que muestre el progreso en tiempo real (ej. "Procesando producto 45 de 450"). Esto probablemente requerirá el uso del bus de Odoo o polling desde el cliente.

* **Botón de Cancelación:** Añadir una opción para que un administrador pueda detener un job que esté `Pendiente` o `En Progreso`. Un job cancelado no podrá ser re-encolado y pasará a un estado `cancelled`.

* **Soporte para Productos Opcionales:** Analizar la causa raíz del conflicto de base de datos con el campo `optional_product_ids` e implementar una solución compatible.
* **Asistente de Evaluación de Conflictos:** Implementar un modo "dry run" que analice los productos y presente un resumen de posibles conflictos antes de ejecutar la duplicación.
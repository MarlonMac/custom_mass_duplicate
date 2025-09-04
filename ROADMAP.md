# Roadmap del Módulo: Duplicación Masiva de Productos

Este documento describe la dirección futura y las características planificadas para el módulo `custom_mass_duplicate`.

---

## Versión 1.0.0 - Lanzamiento Inicial
**Estado:** Liberado ✔️

Versión base que introduce la funcionalidad principal de duplicación de productos entre compañías.

* **Asistente de Duplicación:** Interfaz para seleccionar productos y definir la compañía/sitio web de destino.
* **Integración con UI:** La acción está disponible en el menú "Acción" de la vista de productos.
* **Duplicación Completa:** Se copian todos los datos del `product.template`, incluyendo imágenes principales, galería de imágenes, descripciones y relaciones.
* **Gestión de Conflictos Básica:** Implementada la estrategia "Ignorar si Existe". Si una referencia interna ya existe en la compañía de destino, el campo se deja en blanco en el nuevo producto para evitar errores.

---

## Versión 1.1.0 - Gestión Avanzada de Conflictos
**Estado:** Planificado 📝

El objetivo principal de esta versión es dar al usuario control total sobre cómo se gestionan los conflictos de Referencia Interna durante el proceso de duplicación.

* **Selector de Estrategia en el Asistente:**
    * Se añadirá un nuevo campo en el asistente para que el usuario elija una de las siguientes opciones:
        1.  **Ignorar Referencia (Opción Segura):** Comportamiento actual. Deja el campo vacío si hay conflicto.
        2.  **Actualizar Producto Existente (Opción Destructiva):** No crea un nuevo producto, sino que actualiza el producto encontrado con los datos del producto origen.
        3.  **Añadir Sufijo al Duplicado:** Crea el producto y añade un sufijo (ej. "-COPY") a la referencia para garantizar la unicidad.

* **Advertencias Dinámicas en la Interfaz:**
    * Junto al selector de estrategia, se mostrará un texto de ayuda que cambiará según la opción elegida, advirtiendo claramente al usuario sobre las consecuencias de su selección (ej. "¡Atención! Esta opción sobrescribirá los datos del producto existente en la empresa de destino.").

* **Refactorización del Código:**
    * Se modificará el método `action_duplicate_products` para que ejecute la lógica correspondiente a la estrategia seleccionada por el usuario.

---

## Futuras Mejoras (Sin Versión Asignada)
**Estado:** Ideas 💡

* **Informe de Resultados:** Al finalizar la operación, mostrar una notificación al usuario resumiendo el resultado (ej. "Proceso finalizado: 420 productos creados, 30 ignorados por conflicto.").
* **Ejecución en Segundo Plano (Jobs):** Para catálogos muy grandes (+1000 productos), la operación podría procesarse en segundo plano para no bloquear la interfaz del usuario.
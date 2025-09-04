# Módulo de Duplicación Masiva de Productos v2.0.0

Este módulo para Odoo 16 Community Edition proporciona una herramienta robusta para duplicar grandes volúmenes de productos de forma masiva y asíncrona entre diferentes compañías.

## Propósito

Facilita la gestión de catálogos en un entorno multi-empresa, eliminando la necesidad de crear productos manualmente y evitando timeouts del servidor al procesar lotes grandes, gracias a su arquitectura de trabajos en segundo plano.

## Instalación

1.  Coloca este módulo en tu carpeta de `addons`.
2.  Reinicia el servicio de Odoo.
3.  Ve a `Aplicaciones`, actualiza la lista y busca e instala "Duplicador Masivo de Productos Multi-Empresa".

## Uso

El proceso ahora es asíncrono, lo que significa que no bloquea tu pantalla.

1.  **Asignar Permisos**: Asegúrate de que el usuario que realizará la operación pertenezca al grupo de seguridad **"Gestor de Duplicación de Productos"**. Puedes asignarlo en `Ajustes > Usuarios y Compañías > Grupos`.

2.  **Iniciar la Duplicación**:
    * Navega a la vista de lista de productos (en Inventario o Sitio Web).
    * Selecciona los productos que deseas duplicar (pueden ser cientos).
    * Haz clic en el menú `Acción > Duplicate to Company`.
    * En el asistente, selecciona la compañía y el sitio web de destino y haz clic en `Duplicate`.

3.  **Monitorear el Progreso**:
    * Recibirás una notificación **instantánea** de que el trabajo ha sido programado.
    * Para ver el estado, ve a `Inventario > Operaciones > Duplication Jobs`.
    * Encontrarás tu trabajo en la lista con uno de los siguientes estados:
        * **Pending**: Esperando a ser procesado por el servidor (normalmente en menos de un minuto).
        * **In Progress**: El trabajo se está ejecutando.
        * **Done**: La duplicación se completó con éxito.
        * **Failed**: Ocurrió un error. Revisa el "Error Log" dentro del job para más detalles.

## Limitaciones Conocidas (v2.0.0)

* **Productos Opcionales**: Debido a conflictos con restricciones de base de datos en ciertos entornos de Odoo, la duplicación del campo "Productos Opcionales" (`optional_product_ids`) está desactivada. Estos deben ser reasignados manualmente después de la duplicación.
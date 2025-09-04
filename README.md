# Módulo de Duplicación Masiva de Productos v2.1.0

Este módulo para Odoo 16 Community Edition proporciona una herramienta robusta para duplicar grandes volúmenes de productos de forma masiva y asíncrona entre diferentes compañías.

## Propósito

Facilita la gestión de catálogos en un entorno multi-empresa, eliminando la necesidad de crear productos manualmente y evitando timeouts del servidor al procesar lotes grandes, gracias a su arquitectura de trabajos en segundo plano.

## Instalación

1.  Coloca este módulo en tu carpeta de `addons`.
2.  Reinicia el servicio de Odoo.
3.  Ve a `Aplicaciones`, actualiza la lista y busca e instala "Duplicador Masivo de Productos Multi-Empresa". Si ya lo tenías instalado, simplemente actualízalo desde el menú de aplicaciones.

## Uso

El proceso es asíncrono, lo que significa que no bloquea tu pantalla.

1.  **Asignar Permisos**: Asegúrate de que el usuario que realizará la operación pertenezca al grupo de seguridad **"Gestor de Duplicación de Productos"**.

2.  **Iniciar la Duplicación**:
    * Navega a la vista de lista de productos.
    * Selecciona los productos que deseas duplicar.
    * Haz clic en el menú `Acción > Duplicate to Company`.
    * En el asistente que aparece, configura la operación:
        * **Target Company y Website**: Elige el destino.
        * **Copy Cost Price**: Marca esta casilla si deseas que el coste de los productos se copie al destino.
        * **Currency Conversion**: Si las monedas son diferentes, el módulo te mostrará la tasa de cambio de Odoo. Si lo necesitas, puedes marcar **"Use Manual Exchange Rate"** para introducir tu propia tasa para esta operación específica.
    * Haz clic en `Duplicate`.

3.  **Monitorear el Progreso**:
    * Recibirás una notificación **instantánea** de que el trabajo ha sido programado.
    * Para ver el estado, ve a `Inventario > Operaciones > Duplication Jobs`.
    * Allí encontrarás tu trabajo con su estado: `Pending`, `In Progress`, `Done`, o `Failed`.

## Limitaciones Conocidas (v2.1.0)

* **Productos Opcionales**: La duplicación del campo "Productos Opcionales" (`optional_product_ids`) está desactivada. Deben ser reasignados manualmente.
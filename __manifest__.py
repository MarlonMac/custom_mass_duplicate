# -*- coding: utf-8 -*-
{
    'name': 'Duplicador Masivo de Productos Multi-Empresa',
    'summary': 'Duplica productos masivamente a otra empresa y sitio web de forma asíncrona.',
    
    'description': """
Herramienta de Productividad para Multi-Empresa v2.1.1
=====================================================

Este módulo proporciona una solución robusta para duplicar grandes volúmenes de productos
de forma masiva y asíncrona entre diferentes empresas.

Características Principales:
---------------------------
* **Procesamiento en Segundo Plano:** Las duplicaciones de lotes grandes se ejecutan como un trabajo en segundo plano para evitar timeouts y no bloquear la interfaz.
* **Monitor de Trabajos:** Incluye una vista para monitorear el estado (Pendiente, En Progreso, Hecho, Fallido) de cada operación.
* **Soporte Multi-Moneda Avanzado:**
    * Convierte automáticamente los precios si la empresa destino usa una moneda diferente.
    * Muestra la tasa de cambio de Odoo directamente en el asistente.
    * **Permite establecer una tasa de cambio manual** para la operación.
* **Copia de Coste Opcional:** El usuario puede decidir si desea copiar el precio de coste de los productos.
* **Duplicación Completa:** Conserva imágenes, variantes, descripciones y relaciones de productos accesorios y alternativos.
* **Seguridad Integrada:** La acción está restringida por un grupo de permisos.

**Nota Importante (v2.1.1):** La duplicación del campo "Productos Opcionales" sigue desactivada para garantizar la estabilidad.
    """,
    
    'author': 'Marlon Macario',
    'maintainer': 'Marlon Macario',
    'company': 'Link GT',
    'website': 'https://link-gt.com',
    'license': 'OPL-1',
    
    'category': 'Inventory/Products',
    'version': '16.0.2.1.1', 
    
    'depends': [
        'product',
        'website',
        'stock',
        'account',
    ],
    'data': [
        'security/mass_duplicate_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/product_duplication_job_views.xml',
        'views/product_duplicate_wizard_views.xml',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
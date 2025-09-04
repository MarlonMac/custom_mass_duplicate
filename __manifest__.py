# -*- coding: utf-8 -*-
{
    'name': 'Duplicador Masivo de Productos Multi-Empresa',
    'summary': 'Duplica productos masivamente a otra empresa y sitio web de forma asíncrona.',
    
    'description': """
Herramienta de Productividad para Multi-Empresa v2.1.0
=====================================================

Este módulo proporciona una solución robusta para duplicar grandes volúmenes de productos
de forma masiva y asíncrona entre diferentes empresas.

Características Principales:
---------------------------
* **Procesamiento en Segundo Plano:** Las duplicaciones de lotes grandes se ejecutan como un trabajo en segundo plano para evitar timeouts del servidor y no bloquear la interfaz del usuario.
* **Monitor de Trabajos:** Incluye una nueva vista para monitorear el estado (Pendiente, En Progreso, Hecho, Fallido) de cada operación de duplicación.
* **Soporte Multi-Moneda:** Convierte automáticamente los precios de venta y coste si la empresa de destino utiliza una moneda diferente (requiere tasas de cambio configuradas en Odoo).
* **Duplicación Completa:** Conserva imágenes, variantes, descripciones y relaciones de productos accesorios y alternativos.
* **Seguridad Integrada:** La acción está restringida por un grupo de permisos para un control total.

**Nota Importante (v2.1.0):** Para garantizar la estabilidad, la duplicación del campo "Productos Opcionales" está desactivada. Estos deben ser reasignados manualmente.
    """,
    
    'author': 'Marlon Macario',
    'maintainer': 'Marlon Macario',
    'company': 'Link GT',
    'website': 'https://link-gt.com',
    'license': 'OPL-1',
    
    'category': 'Inventory/Products',
    'version': '16.0.2.1.0', 
    
    'depends': [
        'product',
        'website',
        'stock',
        'account', # Necesario para la conversión de moneda
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
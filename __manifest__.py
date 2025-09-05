# -*- coding: utf-8 -*-
{
    'name': 'Duplicador Masivo de Productos Multi-Empresa',
    'summary': 'Duplica productos masivamente a otra empresa y sitio web de forma asíncrona.',
    
    'description': """
Herramienta de Productividad para Multi-Empresa v2.2.2
=====================================================

Este módulo proporciona una solución robusta para duplicar grandes volúmenes de productos
de forma masiva y asíncrona entre diferentes empresas.

Características Principales:
---------------------------
* **Cálculo de Precios Preciso**: Realiza la conversión de moneda y los ajustes de precio de venta con alta precisión decimal.
* **Procesamiento en Segundo Plano**: Evita timeouts del servidor al procesar grandes lotes.
* **Soporte Multi-Moneda Avanzado**:
    * Muestra la tasa de cambio de Odoo en el asistente.
    * Permite establecer una tasa de cambio manual, especificando si es un divisor o multiplicador.
* **Ajuste de Precio de Venta**: Opción para aplicar un margen porcentual al precio de venta en el destino.

**Limitación Conocida (v2.2.2):**
----------------------------------
* **Copia de Costo (`standard_price`)**: Existe un problema conocido donde el costo del producto de origen se lee como 0.0 durante el proceso en segundo plano, por lo que no se copia correctamente. Este problema está programado para ser resuelto en la siguiente versión.
* **Productos Opcionales**: La duplicación de este campo sigue desactivada.
    """,
    
    'author': 'Marlon Macario',
    'maintainer': 'Marlon Macario',
    'company': 'Link GT',
    'website': 'https://link-gt.com',
    'license': 'OPL-1',
    'category': 'Inventory/Products',
    'version': '16.0.2.2.2',
    
    'depends': [ 'product', 'website', 'stock', 'account' ],
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
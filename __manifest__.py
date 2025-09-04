# -*- coding: utf-8 -*-
{
    'name': 'Duplicador Masivo de Productos Multi-Empresa',
    'summary': 'Duplica productos masivamente a otra empresa y sitio web, conservando imágenes y datos.',
    
    'description': """
Herramienta de Productividad para Multi-Empresa
================================================

Este módulo proporciona una solución robusta para duplicar productos de forma masiva
entre diferentes empresas configuradas en su instancia de Odoo 16.

Características Principales:
---------------------------
* **Asistente Intuitivo:** Seleccione productos y elija la empresa/sitio web de destino fácilmente.
* **Duplicación Completa:** Conserva imágenes, variantes, descripciones y relaciones de productos accesorios y alternativos.
* **Manejo de Conflictos:** Evita errores de base de datos si un producto con la misma Referencia Interna ya existe.
* **Seguridad Integrada:** Una acción restringida por un grupo de permisos para un control total.

**Nota Importante (v1.0.0):** Para garantizar la estabilidad en todos los entornos, la duplicación del campo "Productos Opcionales" está desactivada. Estos deben ser reasignados manualmente.
    """,
    
    'author': 'Marlon Macario',
    'maintainer': 'Marlon Macario',
    'company': 'Link GT',
    'website': 'https://link-gt.com',
    'license': 'OPL-1',
    
    'category': 'Inventory/Products',
    'version': '16.0.1.0.0',
    
    'depends': [
        'product',
        'website'
    ],
    'data': [
        'security/mass_duplicate_groups.xml',
        'security/ir.model.access.csv',
        'views/product_duplicate_wizard_views.xml',
    ],
    
    'images': ['static/description/banner.png'],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
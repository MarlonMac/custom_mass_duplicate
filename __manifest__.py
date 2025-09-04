# -*- coding: utf-8 -*-
{
    'name': 'Duplicador Masivo de Productos Multi-Empresa',
    'summary': 'Duplica productos masivamente a otra empresa y sitio web, conservando imágenes y datos.',
    
    'description': """
Herramienta de Productividad para Multi-Empresa
================================================

Este módulo proporciona una solución robusta para duplicar productos de forma masiva
entre diferentes empresas configuradas en su instancia de Odoo 16.

Es la herramienta perfecta para administradores de catálogos que necesitan poblar
un nuevo sitio web o empresa con productos ya existentes, sin perder tiempo en la
creación manual.

Características Principales:
---------------------------
* **Asistente Intuitivo:** Seleccione productos y elija la empresa/sitio web de destino fácilmente.
* **Duplicación Completa:** Conserva imágenes, variantes, precios, descripciones de sitio web y más.
* **Manejo de Conflictos:** Evita errores de base de datos si un producto con la misma Referencia Interna ya existe.
* **Integrado en la Interfaz:** Acceda a la funcionalidad desde el menú "Acción" en la vista de productos.
    """,
    
    'author': 'Marlon Macario',
    'maintainer': 'Marlon Macario',
    'company': 'Link GT',
    'website': 'https://link-gt.com',
    'license': 'LGPL-3', 
    
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
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
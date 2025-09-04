# -*- coding: utf-8 -*-
{
    'name': 'Custom Mass Product Duplicator',
    'version': '16.0.1.0.0',
    'summary': 'Allows mass duplication of products to another company and website.',
    'author': 'Marlon Macario',
    'category': 'Inventory/Inventory',
    'depends': [
        'product',
        'website'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_duplicate_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
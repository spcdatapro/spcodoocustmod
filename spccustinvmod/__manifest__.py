# -*- coding: utf-8 -*-
{
    'name': "Invoice sequence changer",

    'summary': """
        Modify the sequence number of an invoice""",

    'description': """
        Module to change the number of an invoice and the journal. Use it carefully. In order to use this module, you need to manually add the field 'nuevo_numero' to the invoice form.
    """,

    'author': "SPC",
    'website': "http://spcdatapro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales Management',
    'version': '1.0',
    'support': 'jaragon@spcdatapro.com',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
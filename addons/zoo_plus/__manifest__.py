# -*- coding: utf-8 -*-
{
    'name': 'Zoo_plus',
    'summary': """Inheritance from Zoo""",
    'description': """Zoo plus""",
    'author': 'Phuc.info',
    'maintainer': 'Phuc.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized', # https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    'version': '0.1',
    'depends': ['zoo','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/zoo_animal_views.xml',  

        'views/sale_order_views.xml'
    ],
    'demo': [],
    'css': [],
    # 'qweb': [
    #     'static/src/xml/counter.xml'    # register qweb template
    # ],
    'installable': True, 
    'auto_install': False,
    'application': True,
}

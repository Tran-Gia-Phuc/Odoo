# -*- coding: utf-8 -*-
{
    'name': 'restaurant_product',
    'summary': """restaurant product""",
    'description': """restaurant product""",
    'author': 'Phuc.info',
    'maintainer': 'Phuc.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized', # https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    'version': '0.1',
    'depends': ['point_of_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_combo_views.xml',  
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

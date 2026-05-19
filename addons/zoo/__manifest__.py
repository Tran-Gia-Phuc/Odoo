# -*- coding: utf-8 -*-
{
    "name": "Zoo City",
    "summary": """Zoo City Tutorials""",
    "description": """Building my own zoo city""",
    "author": "minhng.info",
    "maintainer": "minhng.info",
    "website": "https://minhng.info",
    "category": "Uncategorized",  # https://github.com/odoo/odoo/blob/17.0/odoo/addons/base/data/ir_module_category_data.xml
    "version": "0.1",
    "depends": [
        "product",
    ],
    "data": [
        "security/zoo_security.xml",
        "security/ir.model.access.csv",
        "views/zoo_animal_views.xml",
        "wizard/toy_add_views.xml",
        "wizard/toy_clear_views.xml",
        "wizard/cage_update_views.xml",
        "views/zoo_creature_views.xml",
        "views/zoo_cage_views.xml",
        "dummy_data/categ.xml",
        "dummy_data/dummy.xml",
        "views/zoo_dummy_views.xml",
        "views/report_animal.xml",
        "views/zoo_report.xml",
        "views/report_animal_inherit.xml",
        "views/report_dummy.xml",
        "data/zoo_animal_data.xml",
        "data/cron_feed.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "zoo/static/src/components/counter/*",  # <-- khai báo widget sắp hiện thực
            "zoo/static/src/components/mytable/*",
            "zoo/static/src/components/myheader/*",
        ]
    },
    "demo": [],
    "css": [],
    # 'qweb': [
    #     'static/src/xml/counter.xml'    # register qweb template
    # ],
    "installable": True,
    "auto_install": False,
    "application": True,
}

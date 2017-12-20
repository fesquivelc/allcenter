# -*- coding: utf-8 -*-
{
    'name': "ALLCENTER - PROYECTOS MRP",

    'summary': u"""
        Modulo que permite generar una relación entre proyectos y manufactura""",

    'description': u"""
        Este módulo permite crear presupuestos previo a los proyectos
        
        - 
    """,

    'author': "Cumbre",
    'website': "http://www.cumbre.com.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'mrp', 'stock', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_budget.xml',
        'views/project_task.xml',
        'views/mrp_production.xml',
        'views/project_project.xml',
        'reports/presupuesto_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

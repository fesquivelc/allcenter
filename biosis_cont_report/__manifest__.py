# -*- coding: utf-8 -*-
{
    'name': "Biosis Contable - Libros Electronicost",

    'summary': """
         Apartado para generación de libros electrónicos de acuerdo a SUNAT""",

    'description': """
        Libros Electronicos para SUNAT
    """,

    'author': "Biosis",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx','account','biosis_cont'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/libros_electronicos.xml',
        'data/anexo3_tablas.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/biosis_cont_report.xml',
        #'wizard/account_b_c_report_view.xml',
        #'wizard/account_ple_report_view.xml',
        #'wizard/account_cuentas_report_view.xml',
        #'wizard/account_cuenta_c_p_report_view.xml',
        #'wizard/account_personalizado_report_view.xml',
        #'wizard/report_le_view.xml',
        'wizard/account_sunat_report_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
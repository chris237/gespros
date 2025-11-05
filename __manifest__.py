# -*- coding: utf-8 -*-
{
    'name': 'Gestion Operations',
    'version': '1.0.0',
    'category': 'Perso',
    'summary': 'Module',
    'description': """
        Module 
    """,
    'author': 'Christian Ferdinand fotie201@gmail.com',
    'website': 'https://',
    'depends': ['base', 'hr_expense','mail', 'fleet'],
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/projet.xml',
        'views/cate_expense.xml'
    ],
    'images': [
        'static/description/brains.png',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

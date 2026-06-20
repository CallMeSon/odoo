# -*- coding: utf-8 -*-
{
    'name': 'Mamma Roti Inter-Company PO to SO',
    'version': '1.0',
    'category': 'Sales/Purchase',
    'summary': 'Automate Sales Order creation in Mamma Roti when Purchase Order is confirmed in Mitra Demo',
    'description': """
        This module automates inter-company trade for Mamma Roti:
        When a Purchase Order is confirmed in Mitra Demo (Company ID 2) for vendor Mamma Roti (Partner ID 1),
        it automatically generates a matching Sales Order in Mamma Roti (Company ID 1) for customer Mitra Demo (Partner ID 32).
    """,
    'author': 'Kelompok 5',
    'depends': ['purchase', 'sale'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

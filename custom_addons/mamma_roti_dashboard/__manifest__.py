# -*- coding: utf-8 -*-
{
    'name': 'Mamma Roti KPI Dashboard',
    'version': '1.0',
    'category': 'Dashboard/Reporting',
    'summary': 'Native Odoo KPI Dashboard for Mamma Roti',
    'description': """
        This module provides a native Odoo dashboard visualizing the 5 key performance indicators (KPIs) for Mamma Roti:
        1. Total Daily Revenue
        2. Top Selling Products by Quantity
        3. Average Transaction Value (ATV)
        4. Stock Discrepancy Rate
        5. On-Time Delivery Rate (OTD)
    """,
    'author': 'Kelompok 5 / AI Assistant',
    'depends': ['sale', 'stock', 'board', 'mis_builder'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/mamma_roti_dashboard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

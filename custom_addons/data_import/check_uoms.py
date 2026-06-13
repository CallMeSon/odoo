
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    products = env['product.product'].search([('name', 'in', [
        'Tepung Bogasari - Adonan A',
        'Margarin Simas',
        'Ragi Instan',
        'Telur Ayam',
        'Gula Pasir',
        'Susu Cair UHT',
        'Cokelat Impor SG (Isian/Toping)'
    ])])
    
    for p in products:
        print(f"Product: {p.name:<30} | UoM: {p.uom_id.name:<10} | Purchase UoM: {p.uom_po_id.name}")

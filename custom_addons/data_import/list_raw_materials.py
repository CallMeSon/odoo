
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    raw_cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    products = env['product.product'].search([('categ_id', '=', raw_cat.id)])
    for p in products:
        print(f"Product: {p.name}")

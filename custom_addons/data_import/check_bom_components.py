
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
    bom = env['mrp.bom'].search([('product_tmpl_id', '=', product.product_tmpl_id.id)], limit=1)
    
    print(f"BoM: {bom.display_name}")
    for line in bom.bom_line_ids:
        qty = line.product_id.qty_available
        print(f"  - Component: {line.product_id.name:<30} | Needed: {line.product_qty} | Available: {qty}")

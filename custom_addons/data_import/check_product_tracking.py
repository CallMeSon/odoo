
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    product = env['product.product'].search([('name', '=', 'Tepung Bogasari - Adonan A')], limit=1)
    print(f"Product: {product.name}")
    print(f"Tracking: {product.tracking}")
    print(f"UoM: {product.uom_id.name}")
    
    # Check if there are LOTs for this product
    lots = env['stock.lot'].search([('product_id', '=', product.id)])
    print(f"Lots found: {len(lots)}")
    for lot in lots:
        print(f"  - Lot: {lot.name} | Expiry: {lot.expiration_date}")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    mo = env['mrp.production'].search([], order='id desc', limit=1)
    print(f"MO: {mo.name}")
    print(f"Location: {mo.location_src_id.complete_name}")
    print(f"Dest Location: {mo.location_dest_id.complete_name}")

    for move in mo.move_raw_ids:
        qty = move.product_id.with_context(location=mo.location_src_id.id).qty_available
        print(f"  - Product: {move.product_id.name:<30} | Qty in {mo.location_src_id.name}: {qty}")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    mo = env['mrp.production'].search([('name', '=', 'GUT/MO/00015')], limit=1)
    print(f"MO: {mo.name} | Status: {mo.state}")

    print("\nConsumed Components:")
    for move in mo.move_raw_ids:
        for line in move.move_line_ids:
            print(f"  - Product: {move.product_id.name:<30} | Lot: {line.lot_id.name} | Qty: {line.quantity}")
            
    print("\nFinished Product:")
    for move in mo.move_finished_ids:
        for line in move.move_line_ids:
            print(f"  - Product: {move.product_id.name:<30} | Lot: {line.lot_id.name} | Qty: {line.quantity}")

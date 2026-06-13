
import odoo
from datetime import datetime

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION FASE 3: INTERNAL DISTRIBUTION ===\n")

    # 1. Find Locations
    src_loc = env['stock.location'].search([('complete_name', '=', 'GUT/Stock')], limit=1)
    # Find Cold Storage
    dest_loc = env['stock.location'].search([('name', '=', 'Cold Storage')], limit=1)
    if not dest_loc:
        # Create if missing
        parent = env['stock.location'].search([('name', '=', 'GUT')], limit=1)
        dest_loc = env['stock.location'].create({
            'name': 'Cold Storage',
            'location_id': parent.id if parent else False,
        })
    
    print(f"Source: {src_loc.complete_name}")
    print(f"Destination: {dest_loc.complete_name}")

    # 2. Find Product and Lot
    product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
    # Get the latest produced lot
    lot = env['stock.lot'].search([('product_id', '=', product.id)], order='id desc', limit=1)
    
    print(f"Product: {product.name}")
    print(f"Lot to move: {lot.name}")

    # 3. Create Internal Transfer
    picking_type = env['stock.picking.type'].search([
        ('code', '=', 'internal'),
        ('warehouse_id.name', '=', 'Gudang Utama') # Or whichever warehouse
    ], limit=1)
    
    picking = env['stock.picking'].create({
        'picking_type_id': picking_type.id,
        'location_id': src_loc.id,
        'location_dest_id': dest_loc.id,
        'move_ids': [(0, 0, {
            'name': 'Simulation Transfer',
            'product_id': product.id,
            'product_uom_qty': 50.0,
            'product_uom': product.uom_id.id,
            'location_id': src_loc.id,
            'location_dest_id': dest_loc.id,
        })]
    })
    print(f"Transfer Created: {picking.name}")

    # 4. Assign Lot and Validate
    picking.action_confirm()
    picking.action_assign()
    
    for move in picking.move_ids:
        # If Odoo didn't create a move line, create one
        if not move.move_line_ids:
            env['stock.move.line'].create({
                'picking_id': picking.id,
                'move_id': move.id,
                'product_id': product.id,
                'lot_id': lot.id,
                'quantity': 50.0,
                'location_id': src_loc.id,
                'location_dest_id': dest_loc.id,
            })
        else:
            move.move_line_ids.write({
                'lot_id': lot.id,
                'quantity': 50.0
            })
    
    # In Odoo 17, we might also need to set quantity on move itself for some configurations
    # but move_line should be enough for tracked products
    
    picking.button_validate()
    print(f"Transfer {picking.name} Validated.")

    # 5. Check stock in destination
    qty = product.with_context(location=dest_loc.id).qty_available
    print(f"\nFinal Qty in {dest_loc.name}: {qty} {product.uom_id.name}")

    cr.commit()
print("\nFase 3 Simulation completed successfully.")

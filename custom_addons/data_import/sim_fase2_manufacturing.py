
import odoo
from datetime import datetime

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION FASE 2: MANUFACTURING & FEFO ===\n")

    # 1. Find Product and BoM
    product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
    if not product:
        print("Product 'Mexican Buns Chocolate' not found.")
        exit()
    
    bom = env['mrp.bom'].search([('product_tmpl_id', '=', product.product_tmpl_id.id)], limit=1)
    if not bom:
        print(f"BoM for {product.name} not found.")
        exit()
    
    print(f"Product: {product.name}")
    print(f"BoM: {bom.display_name}")

    # 2. Create Manufacturing Order
    mo = env['mrp.production'].create({
        'product_id': product.id,
        'product_qty': 100.0,
        'bom_id': bom.id,
    })
    print(f"MO Created: {mo.name}")

    # 3. Confirm MO (Triggers reservation)
    mo.action_confirm()
    print(f"MO Status: {mo.state}")

    # 4. Check & Force FEFO Reservation
    mo.action_assign() 
    print("\nFEFO Check & Manual Assignment:")
    for move in mo.move_raw_ids:
        if not move.move_line_ids or not any(l.lot_id for l in move.move_line_ids):
            print(f"  - Component: {move.product_id.name:<30} | No lots reserved. Manually picking oldest lot...")
            # Find oldest lot by expiration date or creation date
            lot = env['stock.lot'].search([
                ('product_id', '=', move.product_id.id),
                ('product_qty', '>', 0)
            ], order='expiration_date asc, id asc', limit=1)
            
            if lot:
                # Clear existing empty lines if any
                move.move_line_ids.unlink()
                env['stock.move.line'].create({
                    'move_id': move.id,
                    'product_id': move.product_id.id,
                    'lot_id': lot.id,
                    'quantity': move.product_uom_qty,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                })
                print(f"    -> Assigned Lot: {lot.name}")
            else:
                print(f"    -> WARNING: No available lots found for {move.product_id.name}!")
        else:
            reserved_lots = move.move_line_ids.mapped('lot_id.name')
            print(f"  - Component: {move.product_id.name:<30} | Reserved Lots: {', '.join(reserved_lots)}")

    # 5. Process Work Orders (Labor Cost)
    if mo.workorder_ids:
        print("\nProcessing Work Orders:")
        for wo in mo.workorder_ids:
            print(f"  - Starting Work Order: {wo.name} at {wo.workcenter_id.name}")
            wo.button_start()
            # Simulate some time (not possible in real-time script easily, 
            # but Odoo uses duration_expected if we finish immediately)
            wo.button_finish()
            print(f"  - Finished Work Order: {wo.name}. Duration: {wo.duration} mins")
    else:
        print("\nNo Work Orders found for this BoM.")

    # 6. Complete MO
    # Record producing
    mo.qty_producing = mo.product_qty
    
    # Assign finished goods lot
    ts = datetime.now().strftime('%H%M%S')
    fg_lot_name = f"FG-BUN-CHO-{datetime.now().strftime('%Y%m%d')}-{ts}"
    fg_lot = env['stock.lot'].create({
        'name': fg_lot_name,
        'product_id': product.id,
        'company_id': env.company.id,
    })
    
    # In Odoo 17, we need to ensure the producing move lines have the lot
    # mrp.production has move_finished_ids
    for move in mo.move_finished_ids:
        if move.product_id == product:
            # If no move lines, create one
            if not move.move_line_ids:
                env['stock.move.line'].create({
                    'move_id': move.id,
                    'product_id': product.id,
                    'lot_id': fg_lot.id,
                    'quantity': mo.product_qty,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                })
            else:
                move.move_line_ids.write({'lot_id': fg_lot.id, 'quantity': mo.product_qty})
    
    print(f"\nProduced Finished Good Lot: {fg_lot_name}")

    # For components, if they were not auto-assigned, we might need to manually pick lots
    # But with FEFO strategy set on Category/Product, action_assign() should pick the oldest lots.
    
    mo.button_mark_done()
    print(f"MO {mo.name} Status: {mo.state}")

    cr.commit()
print("\nFase 2 Simulation completed successfully.")

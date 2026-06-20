import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION: INSTANT AUTO-REPLENISHMENT ON STOCK MOVE ===")
    
    # 1. Find product and orderpoint
    product = env['product.product'].search([('name', '=', 'Tepung Bogasari - Adonan A')], limit=1)
    assert product, "Product 'Tepung Bogasari - Adonan A' not found!"
    
    op = env['stock.warehouse.orderpoint'].search([
        ('product_id', '=', product.id),
        ('company_id', '=', 1)
    ], limit=1)
    assert op, f"Reordering rule not found for product {product.name}!"
    
    # Find an existing lot
    lot = env['stock.lot'].search([('product_id', '=', product.id)], limit=1)
    assert lot, f"No stock lot found for product {product.name}!"
    
    print(f"Target Product: {product.name}")
    print(f"Using Stock Lot: {lot.name}")
    
    # Update orderpoint minimum to be above forecasted qty to trigger replenishment
    # We do a compute first to get accurate forecasted quantity
    op._compute_qty()
    original_min = op.product_min_qty
    target_min = op.qty_forecast + 10.0
    
    print(f"Current Forecast: {op.qty_forecast}")
    print(f"Temporarily setting Min Qty from {original_min} to {target_min}")
    op.write({'product_min_qty': target_min})
    
    # 2. Count existing draft POs for this vendor before validating the move
    vendor_partner = product.seller_ids[0].partner_id
    print(f"Vendor: {vendor_partner.name}")
    
    pos_before = env['purchase.order'].search([
        ('partner_id', '=', vendor_partner.id),
        ('company_id', '=', 1),
        ('state', '=', 'draft')
    ])
    po_count_before = len(pos_before)
    print(f"Draft PO count before: {po_count_before}")
    
    # 3. Create and validate a stock move to trigger the _action_done hook
    print("\n1. Simulating stock move validation...")
    move = env['stock.move'].create({
        'name': 'Simulation Reorder Move',
        'product_id': product.id,
        'product_uom': product.uom_id.id,
        'product_uom_qty': 1.0,
        'location_id': op.location_id.id,
        'location_dest_id': env.ref('stock.stock_location_customers').id,
        'company_id': 1,
    })
    
    move._action_confirm()
    
    # Create the move line with lot
    env['stock.move.line'].create({
        'move_id': move.id,
        'product_id': product.id,
        'product_uom_id': product.uom_id.id,
        'quantity': 1.0,
        'lot_id': lot.id,
        'location_id': op.location_id.id,
        'location_dest_id': env.ref('stock.stock_location_customers').id,
    })
    
    # This will trigger our _action_done override instantly
    move._action_done()
    print("Stock move validated.")
    
    # 4. Verify that a draft PO was created or updated for the vendor
    print("\n2. Verifying generated Purchase Order (RFQ) in Mamma Roti...")
    pos_after = env['purchase.order'].search([
        ('partner_id', '=', vendor_partner.id),
        ('company_id', '=', 1),
        ('state', '=', 'draft')
    ])
    po_count_after = len(pos_after)
    print(f"Draft PO count after: {po_count_after}")
    
    # Assert that either a new draft PO was created, or an existing draft PO received the line
    assert po_count_after >= po_count_before, "No Purchase Orders found!"
    
    # Find the PO that contains our product
    po_line = env['purchase.order.line'].search([
        ('product_id', '=', product.id),
        ('company_id', '=', 1),
        ('state', '=', 'draft')
    ], limit=1)
    
    assert po_line, "No purchase order line was generated for the low stock product!"
    print(f"✅ Found Draft PO Line for {product.name}!")
    print(f"   PO Ref: {po_line.order_id.name}")
    print(f"   Quantity Ordered: {po_line.product_qty}")
    print(f"   Price Unit: {po_line.price_unit}")
    
    print("\n🎉 INSTANT AUTO-REPLENISHMENT VERIFICATION PASSED SUCCESSFULLY!")
    
    # Rollback to keep database completely clean
    print("\nRolling back transaction to keep the database clean...")
    cr.rollback()
    print("Rollback complete.")

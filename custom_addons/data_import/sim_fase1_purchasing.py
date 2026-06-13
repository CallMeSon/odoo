
import odoo
from datetime import datetime, timedelta

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION FASE 1: PURCHASING & RECEIPT ===\n")

    # 1. Find Vendor
    vendor = env['res.partner'].search([('name', 'ilike', 'Bogasari')], limit=1)
    if not vendor:
        vendor = env['res.partner'].create({'name': 'PT Bogasari Flour Mills', 'is_company': True})
    print(f"Vendor: {vendor.name}")

    # 2. Find Products
    ingredients = [
        'Tepung Bogasari - Adonan A',
        'Margarin Simas',
        'Ragi Instan',
        'Telur Ayam',
        'Gula Pasir',
        'Susu Cair UHT',
        'Cokelat Impor SG (Isian/Toping)'
    ]
    
    products = env['product.product'].search([('name', 'in', ingredients)])
    if len(products) < len(ingredients):
        print(f"Only found {len(products)} of {len(ingredients)} ingredients.")
        # Optional: create missing if needed, but they should exist
    
    # 3. Create RFQ
    order_lines = []
    for p in products:
        # Buy 10kg (10000g) or 10L
        qty = 10000.0 if p.uom_id.name == 'g' else 10.0
        order_lines.append((0, 0, {
            'product_id': p.id,
            'product_qty': qty,
            'price_unit': 10000.0, # Dummy price
            'date_planned': datetime.now(),
        }))
        print(f"  - Adding to RFQ: {p.name} ({qty} {p.uom_id.name})")

    po = env['purchase.order'].create({
        'partner_id': vendor.id,
        'order_line': order_lines
    })
    print(f"RFQ Created: {po.name} (Total: {po.amount_total:,.2f})")

    # 4. Confirm Order (Test Double Validation)
    po.button_confirm()
    print(f"Status after confirm: {po.state}")
    
    if po.state == 'to_approve':
        print("Double Validation triggered! Manually approving as manager...")
        po.button_approve()
        print(f"Status after manager approval: {po.state}")

    # 5. Process Receipt
    picking = po.picking_ids[0]
    print(f"Receipt Document: {picking.name}")
    
    # Need to assign LOTs and Expiry Dates
    for move in picking.move_ids:
        # Add timestamp to make it unique in case of multiple runs
        ts = datetime.now().strftime('%H%M%S')
        lot_name = f"LOT-{move.product_id.name[:3].upper()}-{datetime.now().strftime('%Y%m%d')}-{ts}"
        expiry = datetime.now() + timedelta(days=180) # 6 months
        
        # Create Lot
        lot = env['stock.lot'].create({
            'name': lot_name,
            'product_id': move.product_id.id,
            'company_id': env.company.id,
            'expiration_date': expiry,
        })
        
        # Assign lot to move line
        # Odoo 17 uses move_line_ids directly
        move.move_line_ids.write({
            'lot_id': lot.id,
            'quantity': move.product_uom_qty,
        })
        print(f"  - Assigned Lot {lot_name} (Exp: {expiry.strftime('%Y-%m-%d')}) to {move.product_id.name}")

    # Validate picking
    picking.button_validate()
    print(f"Receipt {picking.name} Validated.")

    cr.commit()
print("\nFase 1 Simulation completed successfully.")

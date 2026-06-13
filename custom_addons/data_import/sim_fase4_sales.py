
import odoo
from datetime import datetime

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION FASE 4: SALES (POS & B2B) ===\n")

    # --- Scenario A: POS Sale ---
    print("--- Scenario A: POS Sale ---")
    pos_config = env['pos.config'].search([], limit=1)
    if not pos_config:
        print("No POS Configuration found.")
    else:
        # 1. Open Session
        session = env['pos.session'].create({
            'user_id': odoo.SUPERUSER_ID,
            'config_id': pos_config.id,
        })
        print(f"POS Session Opened: {session.name}")
        
        # 2. Create Order
        product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
        partner = env['res.partner'].search([('name', '!=', False)], limit=1) # Sample customer
        
        # POS Orders are usually created via pos.order.create_from_ui but let's do it directly
        pos_order = env['pos.order'].create({
            'session_id': session.id,
            'partner_id': partner.id,
            'amount_total': 5 * 10000.0,
            'amount_tax': 0.0,
            'amount_paid': 5 * 10000.0,
            'amount_return': 0.0,
            'lines': [(0, 0, {
                'product_id': product.id,
                'qty': 5.0,
                'price_unit': 10000.0,
                'price_subtotal': 50000.0,
                'price_subtotal_incl': 50000.0,
            })],
        })
        print(f"POS Order Created: {pos_order.name} for 5 units.")
        
        # 3. Add Payment
        payment_method = env['pos.payment.method'].search([], limit=1)
        pos_order.add_payment({
            'pos_order_id': pos_order.id,
            'amount': 50000.0,
            'payment_date': datetime.now(),
            'payment_method_id': payment_method.id,
        })
        
        # 4. Validate and Close Session
        pos_order.action_pos_order_paid()
        print("POS Order Paid.")
        
        # Closing session would normally happen here, 
        # but let's leave it open or close it if needed for accounting
        session.action_pos_session_closing_control()
        print(f"POS Session {session.name} Closed.")

    # --- Scenario B: B2B Sales Order ---
    print("\n--- Scenario B: B2B Sales Order ---")
    partner_b2b = env['res.partner'].search([('name', '=', 'Mitra Bandung 01')], limit=1)
    if not partner_b2b:
        partner_b2b = env['res.partner'].create({'name': 'Mitra Bandung 01', 'is_company': True})
    
    sale_order = env['sale.order'].create({
        'partner_id': partner_b2b.id,
        'order_line': [(0, 0, {
            'product_id': product.id,
            'product_uom_qty': 45.0,
            'price_unit': 8000.0,
        })]
    })
    print(f"Sales Order Created: {sale_order.name} for 45 units.")
    
    sale_order.action_confirm()
    print(f"Sales Order Confirmed: {sale_order.state}")
    
    # Process Delivery
    picking = sale_order.picking_ids[0]
    print(f"Delivery Order: {picking.name}")
    
    picking.action_assign()
    # Ensure LOT is assigned (latest produced lot)
    lot = env['stock.lot'].search([('product_id', '=', product.id)], order='id desc', limit=1)
    
    for move in picking.move_ids:
        if not move.move_line_ids:
            env['stock.move.line'].create({
                'picking_id': picking.id,
                'move_id': move.id,
                'product_id': product.id,
                'lot_id': lot.id,
                'quantity': 45.0,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
            })
        else:
            move.move_line_ids.write({'lot_id': lot.id, 'quantity': 45.0})
            
    picking.button_validate()
    print(f"Delivery {picking.name} Validated.")

    # Create Invoice
    invoice = sale_order._create_invoices()
    invoice.action_post()
    print(f"Invoice Posted: {invoice.name}")

    cr.commit()
print("\nFase 4 Simulation completed successfully.")

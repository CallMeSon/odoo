import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== RESETTING INVENTORY ON-HAND QUANTITIES ===")

    # Using direct SQL to bypass ORM delete constraints on completed/done transactions
    try:
        # 1. Clear stock levels
        print("Clearing stock quants...")
        cr.execute("DELETE FROM stock_quant;")
        
        # 2. Clear stock valuation layers
        print("Clearing stock valuation layers...")
        cr.execute("DELETE FROM stock_valuation_layer;")
        
        # 3. Clear stock move lines & moves
        print("Clearing stock move lines...")
        cr.execute("DELETE FROM stock_move_line;")
        print("Clearing stock moves...")
        # Since stock.move might be referenced by mrp or sales, we set those FKs to null or delete them first
        cr.execute("DELETE FROM stock_move;")
        
        # 4. Clear stock pickings
        print("Clearing stock pickings...")
        cr.execute("DELETE FROM stock_picking;")

        # 5. Clear manufacturing orders
        print("Clearing manufacturing workorders and productions...")
        cr.execute("DELETE FROM mrp_workorder;")
        cr.execute("DELETE FROM mrp_production;")

        # 6. Clear sales orders
        print("Clearing sales order lines and sales orders...")
        cr.execute("DELETE FROM sale_order_line;")
        cr.execute("DELETE FROM sale_order;")

        # 7. Reset sequence numbers for clean numbering
        print("Resetting transaction sequences...")
        sequences = env['ir.sequence'].search([
            ('code', 'in', ['purchase.order', 'sale.order', 'stock.picking', 'mrp.production'])
        ])
        for seq in sequences:
            seq.write({'number_next': 1})

        cr.commit()
        print("=== INVENTORY RESET SUCCESSFULLY COMPLETED ===")
    except Exception as e:
        cr.rollback()
        print(f"❌ Error during inventory reset: {e}")

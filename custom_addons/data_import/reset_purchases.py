import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== RESETTING PURCHASE MODULE TRANSACTIONS ===")
    
    # 1. Delete Vendor Bills (account.move)
    bills = env['account.move'].search([('move_type', '=', 'in_invoice')])
    if bills:
        print(f"Found {len(bills)} Vendor Bills. Resetting and deleting...")
        try:
            bills.button_draft()
            bills.unlink()
            print("Successfully deleted Vendor Bills via ORM.")
        except Exception as e:
            print(f"ORM delete failed for bills: {e}. Using SQL fallback.")
            cr.execute("DELETE FROM account_move WHERE id IN %s", (tuple(bills.ids),))
            print("Deleted Vendor Bills via SQL.")

    # 2. Delete Incoming Pickings (stock.picking) and stock moves
    pickings = env['stock.picking'].search([('picking_type_id.code', '=', 'incoming')])
    if pickings:
        print(f"Found {len(pickings)} Incoming Pickings. Deleting...")
        try:
            moves = pickings.mapped('move_ids')
            moves.mapped('move_line_ids').unlink()
            moves.unlink()
            pickings.unlink()
            print("Successfully deleted Incoming Pickings via ORM.")
        except Exception as e:
            print(f"ORM delete failed for pickings/moves: {e}. Using SQL fallback.")
            # Clear stock valuation layers linked to these moves
            move_ids = pickings.mapped('move_ids').ids
            if move_ids:
                cr.execute("DELETE FROM stock_valuation_layer WHERE stock_move_id IN %s", (tuple(move_ids),))
                cr.execute("DELETE FROM stock_move_line WHERE move_id IN %s", (tuple(move_ids),))
                cr.execute("DELETE FROM stock_move WHERE id IN %s", (tuple(move_ids),))
            cr.execute("DELETE FROM stock_picking WHERE id IN %s", (tuple(pickings.ids),))
            print("Deleted Incoming Pickings and stock moves via SQL.")

    # 3. Delete Purchase Orders (purchase.order)
    pos = env['purchase.order'].search([])
    if pos:
        print(f"Found {len(pos)} Purchase Orders. Deleting...")
        try:
            pos.write({'state': 'cancel'})
            pos.unlink()
            print("Successfully deleted Purchase Orders via ORM.")
        except Exception as e:
            print(f"ORM delete failed for POs: {e}. Using SQL fallback.")
            cr.execute("DELETE FROM purchase_order_line WHERE order_id IN %s", (tuple(pos.ids),))
            cr.execute("DELETE FROM purchase_order WHERE id IN %s", (tuple(pos.ids),))
            print("Deleted Purchase Orders via SQL.")

    cr.commit()
    print("=== RESET COMPLETED ===")

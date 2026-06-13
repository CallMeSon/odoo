
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- 1. CREATING POS CATEGORIES ---")
    pos_cat_roti = env['pos.category'].search([('name', '=', 'Roti')], limit=1)
    if not pos_cat_roti:
        pos_cat_roti = env['pos.category'].create({'name': 'Roti'})
        print("Created POS Category: Roti")
        
    pos_cat_minuman = env['pos.category'].search([('name', '=', 'Minuman')], limit=1)
    if not pos_cat_minuman:
        pos_cat_minuman = env['pos.category'].create({'name': 'Minuman'})
        print("Created POS Category: Minuman")

    print("\n--- 2. UPDATING PRODUCT AVAILABILITY & CATEGORIES ---")
    
    # Mexican Buns
    bun_cat = env['product.category'].search([('name', '=', 'Mexican Buns')], limit=1)
    if bun_cat:
        bun_prods = env['product.template'].search([('categ_id', '=', bun_cat.id)])
        for p in bun_prods:
            p.write({
                'available_in_pos': True,
                'pos_categ_ids': [(6, 0, [pos_cat_roti.id])]
            })
            print(f"Updated POS access for Roti: {p.name}")

    # Drinks
    drink_cats = env['product.category'].search([('name', 'in', ['Coffee', 'Non-Coffee'])])
    if drink_cats:
        drink_prods = env['product.template'].search([('categ_id', 'in', drink_cats.ids)])
        for p in drink_prods:
            p.write({
                'available_in_pos': True,
                'pos_categ_ids': [(6, 0, [pos_cat_minuman.id])]
            })
            print(f"Updated POS access for Drink: {p.name}")

    print("\n--- 3. SETTING UP PAYMENT METHODS ---")
    # Find a bank journal to link to QRIS
    bank_journal = env['account.journal'].search([('type', '=', 'bank')], limit=1)
    
    qris_payment = env['pos.payment.method'].search([('name', 'ilike', 'QRIS')], limit=1)
    if not qris_payment:
        qris_payment = env['pos.payment.method'].create({
            'name': 'QRIS / E-Wallet',
            'journal_id': bank_journal.id if bank_journal else None,
            'split_transactions': False
        })
        print("Created Payment Method: QRIS / E-Wallet")
    
    # Assign to POS 1
    pos_config = env['pos.config'].search([('name', 'ilike', 'POS 1')], limit=1)
    if pos_config and qris_payment:
        # Check if already assigned
        if qris_payment.id not in pos_config.payment_method_ids.ids:
            pos_config.write({
                'payment_method_ids': [(4, qris_payment.id)]
            })
            print("Added QRIS to POS 1 configuration.")

    cr.commit()
print("\nPOS configuration completed successfully.")

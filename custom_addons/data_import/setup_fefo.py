
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- 1. ENABLING SYSTEM FEATURES ---")
    
    # Enable Lots & Serial Numbers
    group_lot = env.ref('stock.group_production_lot')
    # Enable Multi-step routes (Multi-Locations and Multi-Warehouses)
    group_multi_loc = env.ref('stock.group_stock_multi_locations')
    group_multi_wh = env.ref('stock.group_stock_multi_warehouses')
    
    # Add root and admin users to these groups
    users = env['res.users'].search([('login', 'in', ['admin', 'warehouse@mammaroti.com', 'store.manager@mammaroti.com'])])
    for user in users:
        user.write({
            'groups_id': [
                (4, group_lot.id),
                (4, group_multi_loc.id),
                (4, group_multi_wh.id)
            ]
        })
        print(f"Assigned advanced groups to user: {user.login}")

    # Set parameters for Expiration Dates
    # Note: module_product_expiry is usually an installed module or a parameter.
    # In Odoo 17, it's a field in res.config.settings that triggers module installation or sets a flag.
    # Let's ensure the group for expiration date is also handled if it exists.
    try:
        group_expiry = env.ref('product_expiry.group_expiry_date_on_delivery_slip')
        for user in users:
            user.write({'groups_id': [(4, group_expiry.id)]})
        print("Assigned Expiry Date groups.")
    except Exception as e:
        print(f"Group expiry not found or module not installed yet: {e}")

    print("\n--- 2. UPDATING RAW MATERIALS FOR LOT TRACKING ---")
    raw_cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if raw_cat:
        raw_products = env['product.template'].search([('categ_id', '=', raw_cat.id)])
        for product in raw_products:
            product.write({
                'tracking': 'lot',
                'use_expiration_date': True
            })
            print(f"Updated product to LOT tracking: {product.name}")

    print("\n--- 3. SETTING FEFO REMOVAL STRATEGY ---")
    fefo_strategy = env.ref('stock.removal_fefo', raise_if_not_found=False)
    if not fefo_strategy:
        # Fallback to search if ref fails
        fefo_strategy = env['product.removal'].search([('method', '=', 'fefo')], limit=1)
    
    if fefo_strategy:
        # Update Central Kitchen locations
        ck_locs = env['stock.location'].search([('complete_name', 'ilike', 'CK')])
        for loc in ck_locs:
            if loc.usage == 'internal':
                loc.write({'removal_strategy_id': fefo_strategy.id})
                print(f"Set FEFO strategy for location: {loc.complete_name}")
    else:
        print("FEFO removal strategy not found in system.")

    cr.commit()
print("\nFEFO and LOT tracking configuration completed.")

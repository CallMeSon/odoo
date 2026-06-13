
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== AUDIT REPORT: POINT OF SALE (POS) ===\n")

    # 1. POS Configurations (Shops)
    print("--- 1. POS Configurations ---")
    pos_configs = env['pos.config'].search([])
    if not pos_configs:
        print("No POS Shop configurations found.")
    for config in pos_configs:
        print(f"Shop: {config.name} | Warehouse: {config.warehouse_id.name or 'Default'} | Picking Type: {config.picking_type_id.name}")

    # 2. Payment Methods
    print("\n--- 2. Payment Methods ---")
    payment_methods = env['pos.payment.method'].search([])
    if not payment_methods:
        print("No POS Payment Methods found.")
    for pm in payment_methods:
        print(f"Method: {pm.name} | Journal: {pm.journal_id.name if pm.journal_id else 'None'}")

    # 3. Product Availability in POS
    print("\n--- 3. Product Availability in POS ---")
    pos_products = env['product.template'].search([('available_in_pos', '=', True)])
    print(f"Products available in POS: {len(pos_products)}")
    
    target_cats = ['Mexican Buns', 'Coffee', 'Non-Coffee']
    cats = env['product.category'].search([('name', 'in', target_cats)])
    missing_pos = env['product.template'].search([
        ('categ_id', 'in', cats.ids),
        ('available_in_pos', '=', False)
    ])
    if missing_pos:
        print(f"Warning: {len(missing_pos)} Finished Goods are NOT available in POS.")
        for p in missing_pos: print(f"  - {p.name}")

    # 4. Inventory Integration (Picking Types)
    print("\n--- 4. Inventory Integration ---")
    # Check if POS points to a specific shop warehouse/location
    for config in pos_configs:
        print(f"POS '{config.name}' deducts stock from: {config.picking_type_id.default_location_src_id.complete_name or 'Default'}")

print("\nAudit query completed.")

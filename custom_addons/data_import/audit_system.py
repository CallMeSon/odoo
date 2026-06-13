
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== AUDIT REPORT: MAMMA ROTI ODOO INTEGRATION ===\n")

    # 1. Product Data Integrity
    print("--- 1. Data Integrity ---")
    raw_cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if raw_cat:
        # Check for products without prices
        no_price = env['product.template'].search([('categ_id', '=', raw_cat.id), ('standard_price', '=', 0)])
        print(f"Bahan Baku without cost: {len(no_price)}")
        for p in no_price: print(f"  - {p.name}")
        
        # Check for products without vendor links (Purchasing Gap)
        no_vendor = env['product.template'].search([('categ_id', '=', raw_cat.id), ('seller_ids', '=', False)])
        print(f"Bahan Baku without Vendor Link: {len(no_vendor)}")
        for p in no_vendor: print(f"  - {p.name}")

    # 2. Manufacturing & Costing
    print("\n--- 2. Manufacturing & Costing ---")
    boms = env['mrp.bom'].search([])
    for bom in boms:
        if not bom.operation_ids:
            print(f"Warning: BoM for {bom.product_tmpl_id.name} has NO operations (No labor cost tracking).")
        
    # 3. Accounting Integration
    print("\n--- 3. Accounting Integration ---")
    cats = env['product.category'].search([('name', 'in', ['Bahan Baku', 'Mexican Buns', 'Coffee', 'Non-Coffee'])])
    for cat in cats:
        if cat.property_valuation != 'real_time':
            print(f"Warning: Category {cat.name} is NOT set to Automated Valuation.")
        if not cat.property_stock_valuation_account_id:
            print(f"Warning: Category {cat.name} is missing Valuation Account.")

    # 4. Inventory & Routing
    print("\n--- 4. Inventory & Routing ---")
    # Check if 'Manufacture' route is correctly applied to finished goods
    mfg_route = env['stock.route'].search([('name', '=', 'Manufacture')], limit=1)
    if mfg_route:
        fg_no_mfg = env['product.template'].search([
            ('categ_id.name', 'in', ['Mexican Buns', 'Coffee']),
            ('route_ids', 'not in', [mfg_route.id])
        ])
        print(f"Finished Goods without Manufacture route: {len(fg_no_mfg)}")
        for p in fg_no_mfg: print(f"  - {p.name}")

    # 5. Reordering Rules
    print("\n--- 5. Automation (Reordering Rules) ---")
    ops = env['stock.warehouse.orderpoint'].search([])
    print(f"Total Reordering Rules active: {len(ops)}")
    # Check for items in Bahan Baku without rules
    if raw_cat:
        raw_no_rules = env['product.product'].search([
            ('categ_id', '=', raw_cat.id),
            ('orderpoint_ids', '=', False)
        ])
        print(f"Bahan Baku without Reorder Rules: {len(raw_no_rules)}")
        for p in raw_no_rules: print(f"  - {p.name}")

print("\nAudit query completed.")

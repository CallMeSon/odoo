
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- IDENTIFYING ROUTES ---")
    route_buy = env.ref('stock.route_warehouse0_buy', raise_if_not_found=False)
    if not route_buy:
        route_buy = env['stock.route'].search([('name', 'ilike', 'Buy')], limit=1)
        
    route_mfg = env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
    if not route_mfg:
        route_mfg = env['stock.route'].search([('name', 'ilike', 'Manufacture')], limit=1)
        
    route_ck_to_gut = env['stock.route'].search([('name', '=', 'Mamma Roti: CK to GUT Transfer')], limit=1)

    print(f"Buy Route: {route_buy.name if route_buy else 'NOT FOUND'}")
    print(f"Manufacture Route: {route_mfg.name if route_mfg else 'NOT FOUND'}")
    print(f"CK to GUT Route: {route_ck_to_gut.name if route_ck_to_gut else 'NOT FOUND'}")

    # 1. RAW MATERIALS (Bahan Baku) -> Route: BUY
    print("\n--- CONFIGURING RAW MATERIALS (BUY) ---")
    cat_raw = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if cat_raw and route_buy:
        raw_products = env['product.template'].search([('categ_id', '=', cat_raw.id)])
        for p in raw_products:
            p.write({'route_ids': [(6, 0, [route_buy.id])]})
            print(f"Set BUY route for: {p.name}")

    # 2. MEXICAN BUNS -> Route: MANUFACTURE + CK to GUT
    print("\n--- CONFIGURING MEXICAN BUNS (MFG + TRANSFER) ---")
    cat_buns = env['product.category'].search([('name', '=', 'Mexican Buns')], limit=1)
    if cat_buns and route_mfg and route_ck_to_gut:
        bun_products = env['product.template'].search([('categ_id', '=', cat_buns.id)])
        for p in bun_products:
            p.write({'route_ids': [(6, 0, [route_mfg.id, route_ck_to_gut.id])]})
            print(f"Set MFG + TRANSFER routes for: {p.name}")

    # 3. DRINKS (Coffee & Non-Coffee) -> Route: MANUFACTURE
    print("\n--- CONFIGURING DRINKS (MFG) ---")
    cat_drinks = env['product.category'].search([('name', 'in', ['Coffee', 'Non-Coffee'])])
    if cat_drinks and route_mfg:
        drink_products = env['product.template'].search([('categ_id', 'in', cat_drinks.ids)])
        for p in drink_products:
            p.write({'route_ids': [(6, 0, [route_mfg.id])]})
            print(f"Set MFG route for: {p.name}")

    cr.commit()
print("\nProduct routes automation completed successfully.")

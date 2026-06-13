
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Correct names based on debug
    ROUTE_BUY_NAME = 'Buy'
    ROUTE_MFG_NAME = 'Manufacture'
    ROUTE_TRANSFER_NAME = 'Mamma_Roti: CK to GUT Transfer'

    route_buy = env['stock.route'].search([('name', '=', ROUTE_BUY_NAME)], limit=1)
    route_mfg = env['stock.route'].search([('name', '=', ROUTE_MFG_NAME)], limit=1)
    route_transfer = env['stock.route'].search([('name', '=', ROUTE_TRANSFER_NAME)], limit=1)

    print(f"Routes: BUY({route_buy.id}), MFG({route_mfg.id}), TRANSFER({route_transfer.id})")

    # 1. RAW MATERIALS -> BUY
    cat_raw = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if cat_raw and route_buy:
        prods = env['product.template'].search([('categ_id', '=', cat_raw.id)])
        prods.write({'route_ids': [(6, 0, [route_buy.id])]})
        print(f"Updated {len(prods)} Raw Materials to 'Buy'")

    # 2. MEXICAN BUNS -> MFG + TRANSFER
    cat_buns = env['product.category'].search([('name', '=', 'Mexican Buns')], limit=1)
    if cat_buns and route_mfg and route_transfer:
        prods = env['product.template'].search([('categ_id', '=', cat_buns.id)])
        prods.write({'route_ids': [(6, 0, [route_mfg.id, route_transfer.id])]})
        print(f"Updated {len(prods)} Mexican Buns to 'Manufacture' + 'Transfer'")

    # 3. DRINKS -> MFG
    cat_drinks = env['product.category'].search([('name', 'in', ['Coffee', 'Non-Coffee'])])
    if cat_drinks and route_mfg:
        prods = env['product.template'].search([('categ_id', 'in', cat_drinks.ids)])
        prods.write({'route_ids': [(6, 0, [route_mfg.id])]})
        print(f"Updated {len(prods)} Drinks to 'Manufacture'")

    cr.commit()
print("\nProduct routes automation completed successfully.")

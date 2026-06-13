
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Locations
    loc_gut_cold = env['stock.location'].search([('complete_name', '=', 'GUT/Stock/Cold Storage')], limit=1)
    
    print("--- 1. SETTING REORDERING RULES FOR MEXICAN BUNS ---")
    cat_buns = env['product.category'].search([('name', '=', 'Mexican Buns')], limit=1)
    if cat_buns and loc_gut_cold:
        products = env['product.product'].search([('categ_id', '=', cat_buns.id)])
        for prod in products:
            # Check if orderpoint already exists
            existing_op = env['stock.warehouse.orderpoint'].search([('product_id', '=', prod.id), ('location_id', '=', loc_gut_cold.id)], limit=1)
            if not existing_op:
                env['stock.warehouse.orderpoint'].create({
                    'product_id': prod.id,
                    'location_id': loc_gut_cold.id,
                    'product_min_qty': 500,
                    'product_max_qty': 2000,
                    'trigger': 'auto',
                })
                print(f"Created production trigger for: {prod.name}")
            else:
                existing_op.write({'product_min_qty': 500, 'product_max_qty': 2000})
                print(f"Updated production trigger for: {prod.name}")
    else:
        print("Required category or location not found for Orderpoints.")

    print("\n--- 2. ENABLING AUTOMATED INVENTORY VALUATION ---")
    target_cats = ['Mexican Buns', 'Coffee', 'Non-Coffee', 'Bahan Baku']
    categories = env['product.category'].search([('name', 'in', target_cats)])
    
    # Find default accounts to ensure we don't crash if they are missing
    # Odoo 17 usually sets these on the category via 'property_stock_valuation_account_id', etc.
    # We will set the valuation mode first.
    for cat in categories:
        cat.write({
            'property_cost_method': 'standard',
            'property_valuation': 'real_time'
        })
        print(f"Enabled Automated Valuation for category: {cat.name}")

    cr.commit()
print("\nFinal MRP and Accounting integration completed successfully.")

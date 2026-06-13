
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Identify target categories
    target_categories = ['Mexican Buns', 'Coffee', 'Non-Coffee']
    categories = env['product.category'].search([('name', 'in', target_categories)])
    cat_ids = categories.ids
    
    print(f"--- UPDATING SALE/PURCHASE FLAGS FOR CATEGORIES: {target_categories} ---")
    
    # Search for all products in these categories
    products = env['product.template'].search([('categ_id', 'in', cat_ids)])
    
    if not products:
        print("No products found in the specified categories.")
    else:
        for product in products:
            product.write({
                'sale_ok': True,
                'purchase_ok': False
            })
            print(f"Updated product: {product.name} | Can be Sold: True | Can be Purchased: False")
            
    cr.commit()
print("\nProduct flags update completed successfully.")

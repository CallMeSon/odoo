
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

# Data from PRODUCT_BREAD.csv
csv_data = [
    {'flavor': 'Chocolate', 'id': 'prod_bun_chocolate', 'name': 'Mexican Buns Chocolate', 'price': 10800.0},
    {'flavor': 'Choco Cheese', 'id': 'prod_bun_choco_cheese', 'name': 'Mexican Buns Choco Cheese', 'price': 10800.0},
    {'flavor': 'Original Butter', 'id': 'prod_bun_ori_butter', 'name': 'Mexican Buns Original Butter', 'price': 9450.0},
    {'flavor': 'Vanilla Butter', 'id': 'prod_bun_van_butter', 'name': 'Mexican Buns Vanilla Butter', 'price': 9450.0},
    {'flavor': 'Cheese', 'id': 'prod_bun_cheese', 'name': 'Mexican Buns Cheese', 'price': 10800.0},
    {'flavor': 'Vanilla Strawberry', 'id': 'prod_bun_strawberry', 'name': 'Mexican Buns Vanilla Strawberry', 'price': 10800.0},
]

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Get the category ID for cat_pos_buns
    category = env['product.category'].search([('name', '=', 'Mexican Buns')], limit=1)
    if not category:
        category = env['product.category'].search([('name', '=', 'All')], limit=1)
    
    print("--- SYNCING PRODUCT DATA FROM CSV ---")
    for row in csv_data:
        # Search for the product we created in the previous step
        # They were named "Mexican Bun Chocolate", etc.
        search_name = f"Mexican Bun {row['flavor']}"
        product = env['product.template'].search([('name', '=', search_name)], limit=1)
        
        if product:
            print(f"Found product: {search_name}. Updating...")
            
            # 1. Update Name, Price, Category, and Type
            product.write({
                'name': row['name'],
                'list_price': row['price'],
                'categ_id': category.id,
                'detailed_type': 'product', # 'Storable Product' in Odoo 17
                'invoice_policy': 'order', # 'Ordered quantities'
            })
            
            # 2. Assign/Update External ID
            # Check if ext ID exists
            ir_model_data = env['ir.model.data'].search([
                ('model', '=', 'product.template'),
                ('res_id', '=', product.id)
            ], limit=1)
            
            if ir_model_data:
                ir_model_data.write({'name': row['id'], 'module': '__import__'})
            else:
                env['ir.model.data'].create({
                    'name': row['id'],
                    'module': '__import__',
                    'model': 'product.template',
                    'res_id': product.id,
                })
            print(f"  - Updated to: {row['name']} | ID: {row['id']} | Price: {row['price']}")
        else:
            print(f"Product '{search_name}' not found in inventory. Skipping.")

    cr.commit()
print("\nProduct sync completed successfully.")

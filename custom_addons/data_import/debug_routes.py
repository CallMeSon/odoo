
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- SEARCHING ALL ROUTES ---")
    routes = env['stock.route'].search([])
    for r in routes:
        print(f"ID: {r.id} | Name: {r.name}")
        
    print("\n--- CHECKING MEXICAN BUNS CATEGORY ---")
    cat = env['product.category'].search([('name', 'ilike', 'Mexican Buns')], limit=1)
    if cat:
        print(f"Category Found: {cat.name} (ID: {cat.id})")
        products = env['product.template'].search([('categ_id', '=', cat.id)])
        print(f"Products in category: {[p.name for p in products]}")
    else:
        print("Category 'Mexican Buns' NOT FOUND.")

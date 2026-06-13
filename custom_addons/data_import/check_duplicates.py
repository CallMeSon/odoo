
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- Detailed Product Categories Check ---")
    cats = env['product.category'].search([], order='name')
    for cat in cats:
        # Get External ID
        ext_id = env['ir.model.data'].search([('model', '=', 'product.category'), ('res_id', '=', cat.id)])
        ext_id_str = f"{ext_id.module}.{ext_id.name}" if ext_id else "None"
        
        # Check if products are using this category
        product_count = env['product.template'].search_count([('categ_id', '=', cat.id)])
        
        print(f"ID: {cat.id} | Name: {cat.name} | Parent: {cat.parent_id.name or 'None'} | Ext ID: {ext_id_str} | Products: {product_count}")

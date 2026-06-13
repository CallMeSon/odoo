
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Mapping: (Manual ID, Imported ID)
    merge_map = [
        (16, 24), # Bahan Baku
        (14, 22), # Coffee
        (13, 21), # Mexican Buns
        (15, 23), # Non-Coffee
    ]
    
    print("--- MERGING PRODUCT CATEGORIES ---")
    for manual_id, imported_id in merge_map:
        manual_cat = env['product.category'].browse(manual_id)
        imported_cat = env['product.category'].browse(imported_id)
        
        if manual_cat.exists() and imported_cat.exists():
            print(f"Merging '{manual_cat.name}' (ID {manual_id}) into (ID {imported_id})...")
            
            # 1. Move products
            products = env['product.template'].search([('categ_id', '=', manual_id)])
            if products:
                products.write({'categ_id': imported_id})
                print(f"  - Moved {len(products)} products.")
            
            # 2. Check for child categories (if any)
            children = env['product.category'].search([('parent_id', '=', manual_id)])
            if children:
                children.write({'parent_id': imported_id})
                print(f"  - Moved {len(children)} child categories.")
            
            # 3. Delete manual category
            try:
                manual_cat.unlink()
                print(f"  - Successfully deleted duplicate category ID {manual_id}.")
            except Exception as e:
                print(f"  - Error deleting category: {e}")
        else:
            print(f"Skipping merge for IDs {manual_id} -> {imported_id} (one or both don't exist).")

    cr.commit()
print("\nCategory cleanup completed successfully.")

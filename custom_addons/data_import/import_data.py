
import odoo
import csv
import os

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def import_csv(env, model, file_path):
    print(f"Importing {file_path} into {model}...")
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        fields = next(reader)
        data = [row for row in reader]
        
    result = env[model].load(fields, data)
    if result.get('messages'):
        for msg in result['messages']:
            print(f"[{msg['type'].upper()}] {msg['message']} in row {msg['record']}")
    else:
        print(f"Successfully imported {len(data)} records into {model}.")

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Pre-create attributes if they don't exist
    attr_name = 'Rasa / Toping'
    attr = env['product.attribute'].search([('name', '=', attr_name)])
    if not attr:
        attr = env['product.attribute'].create({
            'name': attr_name,
            'create_variant': 'always',
            'display_type': 'radio'
        })
        print(f"Created attribute: {attr_name}")

    # Base directory for data
    base_dir = '/mnt/extra-addons/data_import'
    
    # 1. Product Categories
    import_csv(env, 'product.category', os.path.join(base_dir, 'PRODUCT_CATEGORY.csv'))
    cr.commit()
    
    # 2. Vendors (Contacts)
    import_csv(env, 'res.partner', os.path.join(base_dir, 'VENDOR.csv'))
    cr.commit()
    
    # 3. Raw Materials
    import_csv(env, 'product.template', os.path.join(base_dir, 'RAW_MATERIAL.csv'))
    cr.commit()
    
    # 4. Product Drinks
    import_csv(env, 'product.template', os.path.join(base_dir, 'PRODUCT_DRINK.csv'))
    cr.commit()
    
    # 5. Product Bread Template (Base Product)
    import_csv(env, 'product.template', os.path.join(base_dir, 'PRODUCT_BREAD_TEMPLATE.csv'))
    cr.commit()
    
    # 6. Product Bread (Variants/Attributes)
    import_csv(env, 'product.template', os.path.join(base_dir, 'PRODUCT_BREAD.csv'))
    cr.commit()

print("Data import process completed.")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

# Mapping: { Vendor Name Keyword: [List of product name keywords] }
mapping = {
    'Bogasari': ['Tepung Bogasari'],
    'SG Cocoa': ['Cokelat Impor SG'],
    'Margarin Simas': ['Margarin Simas'],
    'Ragi Sejahtera': ['Ragi Instan'],
    'Telur Makmur': ['Telur Ayam'],
    'Gula Putih': ['Gula Pasir', 'Gula Aren Cair'],
    'Susu Sehat': ['Susu Cair UHT', 'Keju', 'Butter'],
    'Mamma Roastery': ['Biji Kopi Espresso', 'Bubuk Matcha', 'Selai Strawberry', 'Sirup'],
}

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- LINKING VENDORS TO RAW MATERIALS ---")
    
    for v_key, p_keys in mapping.items():
        # Find vendor
        vendor = env['res.partner'].search([('name', 'ilike', v_key)], limit=1)
        if not vendor:
            print(f"Vendor NOT FOUND for key: {v_key}")
            continue
            
        for p_key in p_keys:
            # Find products
            products = env['product.template'].search([('name', 'ilike', p_key)])
            
            for product in products:
                # Check if this vendor is already linked
                existing = env['product.supplierinfo'].search([
                    ('product_tmpl_id', '=', product.id),
                    ('partner_id', '=', vendor.id)
                ])
                
                if not existing:
                    env['product.supplierinfo'].create({
                        'partner_id': vendor.id,
                        'product_tmpl_id': product.id,
                        'min_qty': 1,
                        'price': product.standard_price,
                        'delay': 2 # 2 days lead time as per BRD
                    })
                    print(f"Linked: {vendor.name} -> {product.name}")
                else:
                    print(f"Already Linked: {vendor.name} -> {product.name}")

    cr.commit()
print("\nVendor linking completed successfully.")

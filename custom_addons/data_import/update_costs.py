
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

# Realistic Price Estimates per Gram/Unit (in IDR)
# Target COGS: Rp 2.500 - Rp 3.500 per bun
raw_material_prices = {
    'Tepung Bogasari': 15,        # Rp 15.000 / Kg
    'Margarin Simas': 30,         # Rp 30.000 / Kg
    'Ragi Instan': 80,            # Rp 80.000 / Kg
    'Telur Ayam': 35,             # Rp 35.000 / Kg (approx per gram)
    'Gula Pasir': 18,             # Rp 18.000 / Kg
    'Susu Cair UHT': 20000,       # Rp 20.000 / Liter
    'Cokelat Impor SG': 120,      # Rp 120.000 / Kg
    'Biji Kopi Espresso': 250,    # Rp 250.000 / Kg
    'Gula Aren Cair': 35000,      # Rp 35.000 / Liter
    'Butter': 150,                # Rp 150.000 / Kg
    'Keju': 100,                  # Rp 100.000 / Kg
    'Selai Strawberry': 60,       # Rp 60.000 / Kg
    'Sirup Vanilla': 80000,       # Rp 80.000 / Liter
    'Sirup Caramel': 80000,       # Rp 80.000 / Liter
    'Sirup Hazelnut': 85000,      # Rp 85.000 / Liter
    'Sirup Butterscotch': 90000,   # Rp 90.000 / Liter
    'Sirup Mangga Tropical': 75000, # Rp 75.000 / Liter
    'Bubuk Matcha': 200,          # Rp 200.000 / Kg
}

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- UPDATING RAW MATERIAL COSTS ---")
    
    # Get the 'Bahan Baku' category
    raw_cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if not raw_cat:
        print("Category 'Bahan Baku' not found.")
    else:
        # Search for all products in this category
        raw_products = env['product.template'].search([('categ_id', '=', raw_cat.id)])
        
        for product in raw_products:
            found_match = False
            for name_key, price in raw_material_prices.items():
                if name_key.lower() in product.name.lower():
                    product.write({'standard_price': price})
                    print(f"Updated: {product.name} | Price: Rp {price} per {product.uom_id.name}")
                    found_match = True
                    break
            
            if not found_match:
                # Default price for unknown raw materials
                product.write({'standard_price': 50.0})
                print(f"Updated (Default): {product.name} | Price: Rp 50.0")

    cr.commit()
print("\nRaw material costs updated successfully.")

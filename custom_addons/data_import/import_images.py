import odoo
import base64
import os

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

# Define directories
POS_IMAGE_DIR = '/mnt/extra-addons/assets/product/POS product'
RAW_IMAGE_DIR = '/mnt/extra-addons/assets/product/Raw Material'

def get_base64_image(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read())

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== STARTING PRODUCT IMAGE IMPORT ===")

    # 1. Import Raw Material Images
    # Mapping image name to raw material name (approximate match)
    raw_materials = env['product.template'].search([('categ_id.name', '=', 'Bahan Baku')])
    raw_images = {
        'Tepung Bogasari': 'Tepung_Bogasari .png', # note the space in user asset name
        'Margarin Simas': 'Margarin_Simas.png',
        'Ragi Instan': 'Ragi_Instan.png',
        'Telur Ayam': 'Telur_Ayam.png',
        'Gula Pasir': 'Gula_Pasir.png',
        'Susu Cair UHT': 'Susu_Cair_UHT.png',
        'Cokelat Impor SG': 'Cokelat_Impor.png',
        'Biji Kopi Espresso': 'Biji_Kopi_Espresso.png',
        'Gula Aren Cair': 'Gula_Aren_Cair.png',
        'Butter': 'Butter.png',
        'Keju': 'Keju.png',
        'Selai Strawberry': 'Selai_Strawberry.png',
        'Sirup Vanilla': 'Sirup_Vanilla.png',
        'Sirup Caramel': 'Sirup_Caramel.png',
        'Sirup Hazelnut': 'Sirup_Hazelnut.png',
        'Sirup Butterscotch': 'Sirup_Butterscotch.png',
        'Sirup Mangga Tropical': 'Sirup_Mangga_Tropical.png',
        'Bubuk Matcha': 'Bubuk_Matcha.png',
    }

    for p in raw_materials:
        # Find matching key in raw_images
        matched_filename = None
        for key, filename in raw_images.items():
            if key.lower() in p.name.lower():
                matched_filename = filename
                break
        
        if matched_filename:
            path = os.path.join(RAW_IMAGE_DIR, matched_filename)
            # Try with and without trailing space for Bogasari just in case
            if matched_filename == 'Tepung_Bogasari .png' and not os.path.exists(path):
                path = os.path.join(RAW_IMAGE_DIR, 'Tepung_Bogasari.png')

            img_base64 = get_base64_image(path)
            if img_base64:
                p.write({'image_1920': img_base64})
                print(f"✅ Loaded image for Raw Material: {p.name} from {matched_filename}")
            else:
                print(f"❌ Failed to read image for Raw Material: {p.name}")
        else:
            print(f"⚠️ No matching image definition for Raw Material: {p.name}")

    # 2. Import POS Drink / Template Images
    pos_products = env['product.template'].search([('categ_id.name', 'in', ['Coffee', 'Non-Coffee'])])
    pos_images = {
        'Americano Hot': 'Americano_Hot.png',
        'Iced Americano': 'Iced_Americano.png',
        'Iced Chocolate': 'Iced_Chocolate.png',
        'Iced Creamy Matcha': 'Iced_Creamy_Matcha.png',
        'Iced Mango Tropical': 'Iced_Mango_Tropical.png',
        'Kopi Susu Butterscotch': 'Kopi_Susu_Butterscotch.png',
        'Kopi Susu Gula Aren': 'Kopi_Susu_Gula_Aren.png',
        'Kopi Susu Hazelnut': 'Kopi_Susu_Hazelnut.png',
        'Kopi Susu Salted Caramel': 'Kopi_Susu_Salted_Caramel.png',
    }

    for p in pos_products:
        matched_filename = None
        for key, filename in pos_images.items():
            if key.lower() in p.name.lower():
                matched_filename = filename
                break
        
        if matched_filename:
            path = os.path.join(POS_IMAGE_DIR, matched_filename)
            img_base64 = get_base64_image(path)
            if img_base64:
                p.write({'image_1920': img_base64})
                print(f"✅ Loaded image for Product: {p.name} from {matched_filename}")
            else:
                print(f"❌ Failed to read image for Product: {p.name}")
        else:
            print(f"⚠️ No matching image definition for Product: {p.name}")

    # 3. Import Mexican Buns Template Images
    buns_products = env['product.template'].search([('name', 'ilike', 'Mexican Buns')])
    bun_images = {
        'Mexican Buns Cheese': 'Mexican_Buns_Cheese.png',
        'Mexican Buns Choco Cheese': 'Mexican_Buns_Choco_Cheese.png',
        'Mexican Buns Chocolate': 'Mexican_Buns_Chocolate.png',
        'Mexican Buns Vanilla Butter': 'Mexican_Buns_Vanilla_Butter.png',
    }

    for p in buns_products:
        matched_filename = None
        for key, filename in bun_images.items():
            if key.lower() == p.name.strip().lower():
                matched_filename = filename
                break
        
        if matched_filename:
            path = os.path.join(POS_IMAGE_DIR, matched_filename)
            img_base64 = get_base64_image(path)
            if img_base64:
                p.write({'image_1920': img_base64})
                print(f"✅ Loaded image for Bread: {p.name} from {matched_filename}")
            else:
                print(f"❌ Failed to read image for Bread: {p.name}")
        else:
            print(f"⚠️ No matching image definition for Bread: {p.name}")

    cr.commit()
    print("=== IMAGE IMPORT COMPLETE ===")

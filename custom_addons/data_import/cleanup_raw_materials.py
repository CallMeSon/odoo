
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

raw_material_prices = {
    'Tepung Bogasari': 15,        
    'Margarin Simas': 30,         
    'Ragi Instan': 80,            
    'Telur Ayam': 35,             
    'Gula Pasir': 18,             
    'Susu Cair UHT': 20000,       
    'Cokelat Impor SG': 120,      
    'Biji Kopi Espresso': 250,    
    'Gula Aren Cair': 35000,      
    'Butter': 150,                
    'Keju': 100,                  
    'Selai Strawberry': 60,       
    'Sirup Vanilla': 80000,       
    'Sirup Caramel': 80000,       
    'Sirup Hazelnut': 85000,      
    'Sirup Butterscotch': 90000,   
    'Sirup Mangga Tropical': 75000, 
    'Bubuk Matcha': 200,          
}

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    raw_cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
    if not raw_cat:
        print("Category 'Bahan Baku' not found.")
    else:
        print("--- IDENTIFYING PRODUCTS IN 'BAHAN BAKU' ---")
        all_raw = env['product.template'].search([('categ_id', '=', raw_cat.id)])
        
        # Group products by normalized name to find duplicates
        by_name = {}
        for p in all_raw:
            name = p.name.strip().lower()
            if name not in by_name:
                by_name[name] = []
            by_name[name].append(p)
            
        print(f"Found {len(by_name)} unique product names across {len(all_raw)} records.")

        for name, products in by_name.items():
            if len(products) > 1:
                print(f"\nMerging duplicates for: {products[0].name}")
                
                # Sort: Priority to product with External ID
                def has_ext_id(prod):
                    return bool(env['ir.model.data'].search([('model', '=', 'product.template'), ('res_id', '=', prod.id)]))
                
                products.sort(key=lambda x: has_ext_id(x), reverse=True)
                
                master = products[0]
                duplicates = products[1:]
                
                print(f"  MASTER: ID {master.id} (Ext ID: {has_ext_id(master)})")
                
                for dup in duplicates:
                    print(f"  DUPLICATE: ID {dup.id} (Ext ID: {has_ext_id(dup)})")
                    
                    # 1. Update BoM lines
                    bom_lines = env['mrp.bom.line'].search([('product_id', 'in', dup.product_variant_ids.ids)])
                    if bom_lines:
                        bom_lines.write({'product_id': master.product_variant_id.id})
                        print(f"    - Moved {len(bom_lines)} BoM lines.")
                    
                    # 2. Update Orderpoints
                    ops = env['stock.warehouse.orderpoint'].search([('product_id', 'in', dup.product_variant_ids.ids)])
                    if ops:
                        ops.write({'product_id': master.product_variant_id.id})
                        print(f"    - Moved {len(ops)} Orderpoints.")
                        
                    # 3. Update Stock Moves (History)
                    moves = env['stock.move'].search([('product_id', 'in', dup.product_variant_ids.ids)])
                    if moves:
                        moves.write({'product_id': master.product_variant_id.id})
                        print(f"    - Moved {len(moves)} Stock Moves.")

                    # 4. Delete duplicate
                    try:
                        dup.unlink()
                        print(f"    - Successfully deleted ID {dup.id}.")
                    except Exception as e:
                        print(f"    - Error deleting ID {dup.id} (archiving instead): {e}")
                        dup.write({'active': False})

        # Final Price and UoM fix for clean list
        print("\n--- RE-APPLYING PRICES AND FIXING UOMs ---")
        final_list = env['product.template'].search([('categ_id', '=', raw_cat.id)])
        for p in final_list:
            # Fix UoM for liquids if still weird
            if 'cair' in p.name.lower() or 'susu' in p.name.lower() or 'sirup' in p.name.lower():
                uom_l = env.ref('uom.product_uom_litre')
                if p.uom_id.id != uom_l.id:
                    p.write({'uom_id': uom_l.id, 'uom_po_id': uom_l.id})
            
            # Apply Price
            for key, price in raw_material_prices.items():
                if key.lower() in p.name.lower():
                    p.write({'standard_price': price})
                    print(f"Set Price: {p.name} -> Rp {price} / {p.uom_id.name}")
                    break

    cr.commit()
print("\nCleanup and price update completed.")

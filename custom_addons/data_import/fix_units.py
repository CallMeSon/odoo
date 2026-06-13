
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Target UoMs
    uom_litre = env.ref('uom.product_uom_litre')
    uom_gram = env.ref('uom.product_uom_gram')
    uom_unit = env.ref('uom.product_uom_unit')
    
    print("--- FIXING BILL OF MATERIALS LINES ---")
    bom_lines = env['mrp.bom.line'].search([('product_uom_id.name', 'ilike', 'fl oz')])
    for line in bom_lines:
        old_qty = line.product_qty
        old_uom = line.product_uom_id.name
        
        # Logic: If it was fl oz, it was likely meant to be ml (which is 0.001 L in Odoo)
        # 20 fl oz -> likely meant 20 ml -> 0.02 L
        # 150 fl oz -> likely meant 150 ml -> 0.15 L
        new_qty = old_qty / 1000.0
        line.write({
            'product_uom_id': uom_litre.id,
            'product_qty': new_qty
        })
        print(f"Updated BoM Line {line.id} ({line.product_id.name}): {old_qty} {old_uom} -> {new_qty} L")

    print("\n--- FIXING REORDERING RULES (ORDERPOINTS) ---")
    # Some orderpoints have massive numbers (500,000) which are likely grams.
    # Let's normalize them to Kg if they are weight-based or just keep as is if Grams is the base.
    # The user said they are in grams. 500,000 g = 500 kg.
    # However, let's check if any are using fl oz.
    op_floz = env['stock.warehouse.orderpoint'].search([('product_uom_id.name', 'ilike', 'fl oz')])
    for op in op_floz:
        old_qty_min = op.product_min_qty
        old_qty_max = op.product_max_qty
        # Convert to Litre
        op.write({
            'product_uom_id': uom_litre.id,
            'product_min_qty': old_qty_min / 1000.0,
            'product_max_qty': old_qty_max / 1000.0
        })
        print(f"Updated Orderpoint {op.product_id.name}: {old_qty_min} fl oz -> {op.product_min_qty} L")

    cr.commit()
print("\nUpdate completed successfully.")

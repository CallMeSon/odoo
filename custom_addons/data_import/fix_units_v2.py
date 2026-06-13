
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Target UoM for liquids (Litre)
    uom_litre = env.ref('uom.product_uom_litre')
    
    print("--- FIXING BILL OF MATERIALS LINES ---")
    # This part succeeded before but we commit it now
    bom_lines = env['mrp.bom.line'].search([])
    for line in bom_lines:
        if 'fl oz' in line.product_uom_id.name.lower():
            old_qty = line.product_qty
            old_uom = line.product_uom_id.name
            new_qty = old_qty / 1000.0
            line.write({
                'product_uom_id': uom_litre.id,
                'product_qty': new_qty
            })
            print(f"Updated BoM Line {line.id} ({line.product_id.name}): {old_qty} {old_uom} -> {new_qty} L")

    print("\n--- FIXING REORDERING RULES (ORDERPOINTS) ---")
    # Orderpoint uses 'qty_multiple_uom_id' or 'product_uom_id' depending on Odoo version/config
    # In Odoo 17, it's usually 'product_uom_id' on the related product, but the orderpoint itself has a UoM field.
    # Let's check the fields first via code to be sure.
    orderpoints = env['stock.warehouse.orderpoint'].search([])
    for op in orderpoints:
        # Check the UoM field on orderpoint
        uom = op.product_uom_id
        if uom and 'fl oz' in uom.name.lower():
            old_min = op.product_min_qty
            old_max = op.product_max_qty
            op.write({
                'product_uom_id': uom_litre.id,
                'product_min_qty': old_min / 1000.0,
                'product_max_qty': old_max / 1000.0
            })
            print(f"Updated Orderpoint {op.product_id.name}: {old_min} {uom.name} -> {op.product_min_qty} L")

    cr.commit()
print("\nUpdate completed successfully.")

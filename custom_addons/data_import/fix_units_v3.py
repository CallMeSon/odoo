
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    uom_litre = env.ref('uom.product_uom_litre')
    
    print("--- FIXING BILL OF MATERIALS LINES ---")
    bom_lines = env['mrp.bom.line'].search([])
    for line in bom_lines:
        if line.product_uom_id and 'fl oz' in line.product_uom_id.name.lower():
            old_qty = line.product_qty
            new_qty = old_qty / 1000.0
            line.write({'product_uom_id': uom_litre.id, 'product_qty': new_qty})
            print(f"Updated BoM Line {line.id}: {old_qty} -> {new_qty} L")

    print("\n--- FIXING REORDERING RULES (ORDERPOINTS) ---")
    orderpoints = env['stock.warehouse.orderpoint'].search([])
    for op in orderpoints:
        # Based on AttributeError, the correct field is 'product_uom'
        uom = op.product_uom
        if uom and 'fl oz' in uom.name.lower():
            old_min = op.product_min_qty
            old_max = op.product_max_qty
            op.write({
                'product_uom': uom_litre.id,
                'product_min_qty': old_min / 1000.0,
                'product_max_qty': old_max / 1000.0
            })
            print(f"Updated Orderpoint {op.product_id.name}: {old_min} -> {op.product_min_qty} L")

    cr.commit()
print("\nUpdate completed successfully.")

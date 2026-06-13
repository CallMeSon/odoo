
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- REORDERING RULES (Replenishment) ---")
    orderpoints = env['stock.warehouse.orderpoint'].search([])
    if not orderpoints:
        print("No reordering rules found in the database.")
    for op in orderpoints:
        print(f"Product: {op.product_id.name}, Min Qty: {op.product_min_qty}, Max Qty: {op.product_max_qty}")
        
    print("\n--- BILL OF MATERIALS (Manufacturing) ---")
    boms = env['mrp.bom'].search([])
    if not boms:
        print("No Bill of Materials found in the database.")
    for bom in boms:
        print(f"BoM for Product: {bom.product_tmpl_id.name}, Produces: {bom.product_qty} {bom.product_uom_id.name}")
        for line in bom.bom_line_ids:
            print(f"  - Component: {line.product_id.name}, Qty: {line.product_qty} {line.product_uom_id.name}")

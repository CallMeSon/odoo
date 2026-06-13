
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- WAREHOUSE LOCATIONS ---")
    locations = env['stock.location'].search([('usage', '=', 'internal')])
    for loc in locations:
        print(f"ID: {loc.id}, Name: {loc.complete_name}")
        
    print("\n--- WORK CENTERS ---")
    work_centers = env['mrp.workcenter'].search([])
    if not work_centers:
        print("No work centers found.")
    for wc in work_centers:
        print(f"ID: {wc.id}, Name: {wc.name}")

    print("\n--- ROUTINGS / OPERATIONS ---")
    operations = env['mrp.routing.workcenter'].search([])
    if not operations:
        print("No operations found.")
    for op in operations:
        print(f"ID: {op.id}, Name: {op.name}, Work Center: {op.workcenter_id.name}, BoM: {op.bom_id.display_name}")

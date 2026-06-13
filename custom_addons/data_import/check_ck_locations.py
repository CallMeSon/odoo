
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Search for locations related to CK (Central Kitchen)
    locs = env['stock.location'].search([('complete_name', 'ilike', 'CK')])
    print("--- CENTRAL KITCHEN LOCATIONS ---")
    for l in locs:
        print(f"ID: {l.id}, Name: {l.complete_name}, Usage: {l.usage}")

    # Also search for 'Production' type locations
    mfg_locs = env['stock.location'].search([('usage', '=', 'production')])
    print("\n--- SYSTEM PRODUCTION LOCATIONS ---")
    for l in mfg_locs:
        print(f"ID: {l.id}, Name: {l.complete_name}, Usage: {l.usage}")

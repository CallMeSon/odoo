
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- INSTALLING PRODUCT EXPIRY MODULE ---")
    module = env['ir.module.module'].search([('name', '=', 'product_expiry')], limit=1)
    if module and module.state != 'installed':
        print("Installing product_expiry...")
        module.button_immediate_install()
        cr.commit()
        print("Module installed successfully.")
    else:
        print("Module already installed or not found.")

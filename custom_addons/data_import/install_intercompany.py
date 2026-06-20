import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("Updating Odoo module list...")
    env['ir.module.module'].update_list()
    cr.commit()
    
    module = env['ir.module.module'].search([('name', '=', 'mamma_roti_intercompany')], limit=1)
    if not module:
        print("Error: Module 'mamma_roti_intercompany' not found in module list.")
    else:
        print(f"Module state before install: {module.state}")
        if module.state in ('installed', 'to upgrade'):
            print("Module is already installed. Upgrading...")
            module.button_immediate_upgrade()
            print("Module upgraded successfully.")
        else:
            print("Installing module 'mamma_roti_intercompany'...")
            module.button_immediate_install()
            print("Module installed successfully.")
            
    cr.commit()

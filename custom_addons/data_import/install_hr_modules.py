
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    modules = env['ir.module.module'].search([('name', 'in', ['hr_holidays', 'hr_attendance'])])
    for m in modules:
        if m.state != 'installed':
            print(f"Installing module: {m.name}")
            m.button_immediate_install()
    cr.commit()
print("Modules installed successfully.")

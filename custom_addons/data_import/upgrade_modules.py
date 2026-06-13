
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    modules = env['ir.module.module'].search([('name', 'in', ['hr', 'hr_holidays', 'hr_attendance', 'hr_skills'])])
    for m in modules:
        print(f"Updating module: {m.name}")
        m.button_immediate_upgrade()
    cr.commit()
print("Modules upgraded successfully.")

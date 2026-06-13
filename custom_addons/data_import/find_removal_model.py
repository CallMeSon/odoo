
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def find_model():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        models = env['ir.model'].search([('model', 'ilike', 'removal')])
        for m in models:
            print(f"Model: {m.model} | Name: {m.name}")

if __name__ == "__main__":
    find_model()

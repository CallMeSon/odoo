
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    model = env['stock.location']
    print(f"Fields for {model._name}:")
    for name, field in model._fields.items():
        if 'parent' in name or 'location' in name or 'name' in name:
            print(f"{name}: {field.type}")

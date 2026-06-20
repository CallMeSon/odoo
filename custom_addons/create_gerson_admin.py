
import odoo
import sys

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Find the main administrator user to copy permissions
    admin_user = env.ref('base.user_admin')
    
    # Check if user 'gerson' already exists
    user = env['res.users'].search([('login', '=', 'gerson')])
    
    user_vals = {
        'name': 'Gerson',
        'login': 'gerson',
        'password': 'gerson',
        'tz': 'Asia/Jakarta',
        'groups_id': [(6, 0, admin_user.groups_id.ids)]
    }
    
    if not user:
        user = env['res.users'].create(user_vals)
        print("User 'gerson' created successfully with full Administrator privileges.")
    else:
        user.write(user_vals)
        print("User 'gerson' updated successfully with full Administrator privileges.")
    
    cr.commit()

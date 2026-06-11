
import odoo
import sys

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

users_data = [
    {
        'name': 'Warehouse Manager',
        'login': 'warehouse@mammaroti.com',
        'groups': [
            'stock.group_stock_manager',
            'purchase.group_purchase_user'
        ]
    },
    {
        'name': 'Finance',
        'login': 'finance@mammaroti.com',
        'groups': [
            'account.group_account_manager',
            'sales_team.group_sale_salesman_all_leads' # Sales: All Documents
        ]
    },
    {
        'name': 'Cashier',
        'login': 'cashier@mammaroti.com',
        'groups': [
            'point_of_sale.group_pos_user',
            'sales_team.group_sale_salesman', # Sales: Own Documents Only
            'stock.group_stock_user'
        ]
    },
    {
        'name': 'Store Manager',
        'login': 'store.manager@mammaroti.com',
        'groups': [
            'point_of_sale.group_pos_manager',
            'sales_team.group_sale_salesman_all_leads', # Store manager needs to see all sales
            'sales_team.group_sale_manager',
            'stock.group_stock_user'
        ]
    }
]

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    for data in users_data:
        # Check if user exists
        user = env['res.users'].search([('login', '=', data['login'])])
        
        # Prepare groups
        group_ids = []
        for xml_id in data['groups']:
            group = env.ref(xml_id, raise_if_not_found=False)
            if group:
                group_ids.append((4, group.id))
            else:
                print(f"Warning: Group {xml_id} not found.")

        if not user:
            user = env['res.users'].create({
                'name': data['name'],
                'login': data['login'],
                'password': 'MammaRoti2026!',
                'tz': 'Asia/Jakarta',
                'groups_id': group_ids
            })
            print(f"User {data['name']} created successfully.")
        else:
            user.write({
                'name': data['name'],
                'password': 'MammaRoti2026!',
                'tz': 'Asia/Jakarta',
                'groups_id': group_ids
            })
            print(f"User {data['name']} updated successfully.")
    
    cr.commit()

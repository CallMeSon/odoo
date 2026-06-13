
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Find a proper Stock Interim (Output) account
    interim_out = env['account.account'].search([('code', 'ilike', '1103%'), ('name', 'ilike', 'Interim')], limit=1)
    if not interim_out:
        # Create a dummy one if missing
        interim_out = env['account.account'].create({
            'name': 'Stock Interim (Delivered)',
            'code': '11030099',
            'account_type': 'asset_current',
            'reconcile': True,
        })
    
    print(f"Using Interim Account: {interim_out.name} ({interim_out.code})")

    # 2. Fix the properties for categories
    # Categories IDs 21-24
    categories = env['product.category'].browse([21, 22, 23, 24])
    for cat in categories:
        print(f"Fixing Category: {cat.name}")
        # Update property
        prop = env['ir.property'].search([
            ('name', '=', 'property_stock_account_output_categ_id'),
            ('res_id', '=', f'product.category,{cat.id}')
        ])
        if prop:
            prop.value_reference = f'account.account,{interim_out.id}'
            print(f"  -> Fixed Stock Output Account for {cat.name}")

    cr.commit()
print("Inventory accounts fixed.")

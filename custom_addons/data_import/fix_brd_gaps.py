
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Configure PO Double Validation
    company = env['res.company'].browse(1)
    company.write({
        'po_double_validation': 'two_step',
        'po_double_validation_amount': 5000000.0 # 5 Million IDR
    })
    print("PO Double Validation configured.")

    # 2. Create Employees for Users
    users = env['res.users'].search([('login', '!=', 'admin')])
    for user in users:
        employee = env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if not employee:
            employee = env['hr.employee'].create({
                'name': user.name,
                'user_id': user.id,
                'work_email': user.login,
            })
            print(f"Employee created for user: {user.name}")
        else:
            print(f"Employee already exists for user: {user.name}")

    # 3. Create a Sample Sales Order from a Partner (Franchise)
    # Check if a partner exists
    partner = env['res.partner'].search([('name', '=', 'Mitra Bandung 01')], limit=1)
    if not partner:
        partner = env['res.partner'].create({
            'name': 'Mitra Bandung 01',
            'is_company': True,
            'email': 'bandung01@partner.com',
        })
    
    # Check for a product to sell (e.g., Mexican Buns Chocolate)
    product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
    if product:
        # Check if already exists to avoid duplicates
        existing_so = env['sale.order'].search([('partner_id', '=', partner.id)], limit=1)
        if not existing_so:
            sale_order = env['sale.order'].create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 100,
                    'price_unit': 8000.0,
                })]
            })
            print(f"Sample Sales Order created: {sale_order.name}")
            # Confirm the order to create a Delivery Order
            sale_order.action_confirm()
            print(f"Sales Order {sale_order.name} confirmed (Delivery Order created).")
        else:
            print(f"Sales Order for {partner.name} already exists.")
    else:
        print("Product 'Mexican Buns Chocolate' not found.")

    cr.commit()
print("Gap fixing completed.")

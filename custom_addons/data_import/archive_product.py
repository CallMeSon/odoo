
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def archive_product():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        product = env['product.product'].search([('name', '=', 'Mexican Buns')], limit=1)
        if not product:
            print("Product not found.")
            return

        product.write({'active': False})
        print(f"Product '{product.name}' (ID: {product.id}) has been ARCHIVED successfully.")

    cr.commit()

if __name__ == "__main__":
    archive_product()

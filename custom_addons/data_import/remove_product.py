
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def delete_or_archive():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        product = env['product.product'].search([('name', '=', 'Mexican Buns')], limit=1)
        if not product:
            print("Product not found.")
            return

        try:
            # Try to delete
            name = product.name
            product.unlink()
            print(f"Product '{name}' successfully DELETED.")
        except Exception as e:
            print(f"Could not delete product: {e}")
            print("Attempting to ARCHIVE instead...")
            product.write({'active': False})
            print(f"Product '{product.name}' has been ARCHIVED.")

    cr.commit()

if __name__ == "__main__":
    delete_or_archive()

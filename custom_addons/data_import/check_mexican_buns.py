
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def check_product():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # Search for exact name first
        product = env['product.product'].search([('name', '=', 'Mexican Buns')], limit=1)
        if not product:
            print("Product 'Mexican Buns' not found.")
            # Search for partial match just in case
            others = env['product.product'].search([('name', 'ilike', 'Mexican Buns')])
            print(f"Other similar products: {[p.name for p in others]}")
            return

        print(f"Found Product: {product.name} (ID: {product.id})")
        
        # Check for stock moves
        moves = env['stock.move'].search_count([('product_id', '=', product.id)])
        print(f"Stock Moves: {moves}")
        
        # Check for Sales Order Lines
        sol = env['sale.order.line'].search_count([('product_id', '=', product.id)])
        print(f"Sales Order Lines: {sol}")
        
        # Check for Purchase Order Lines
        pol = env['purchase.order.line'].search_count([('product_id', '=', product.id)])
        print(f"Purchase Order Lines: {pol}")

        if moves == 0 and sol == 0 and pol == 0:
            print("Product has no history. SAFE TO DELETE.")
        else:
            print("Product has transaction history. SHOULD BE ARCHIVED.")

if __name__ == "__main__":
    check_product()

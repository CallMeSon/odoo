
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION FASE 5: ACCOUNTING AUDIT ===\n")

    # 1. Check Journal Entries
    print("--- Journal Entries Check ---")
    # Latest 10 entries
    moves = env['account.move'].search([], order='id desc', limit=10)
    for m in moves:
        print(f"Move: {m.name:<20} | Ref: {m.ref:<20} | State: {m.state:<10} | Amount: {m.amount_total:,.2f}")

    # 2. Check COGS for Mexican Buns
    print("\n--- COGS & Profitability (Mexican Buns Chocolate) ---")
    product = env['product.product'].search([('name', '=', 'Mexican Buns Chocolate')], limit=1)
    print(f"Product: {product.name}")
    print(f"Standard Price (Cost): {product.standard_price:,.2f}")
    
    # Check latest sale
    sale_line = env['sale.order.line'].search([('product_id', '=', product.id)], order='id desc', limit=1)
    if sale_line:
        print(f"Latest Sale Price: {sale_line.price_unit:,.2f} per unit")
        margin = sale_line.price_unit - product.standard_price
        print(f"Estimated Margin: {margin:,.2f} per unit")

    # 3. Stock Valuation
    print("\n--- Stock Valuation Report ---")
    cats = env['product.category'].search([('name', 'in', ['Bahan Baku', 'Mexican Buns'])])
    for cat in cats:
        # Sum of valuation
        products = env['product.product'].search([('categ_id', '=', cat.id)])
        total_value = sum(p.qty_available * p.standard_price for p in products)
        print(f"Category: {cat.name:<20} | Total Inventory Value: {total_value:,.2f}")

print("\nFase 5 Accounting Audit completed.")

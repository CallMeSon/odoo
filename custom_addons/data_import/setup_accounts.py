
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Identify Standard Accounts
    # Usually: Inventory Valuation (Asset), Stock Interim Input (Liability), Stock Interim Output (Asset)
    
    # Heuristic for Valuation Account
    valuation_account = env['account.account'].search([('account_type', '=', 'asset_current'), ('name', 'ilike', 'Stock Valuation')], limit=1)
    if not valuation_account:
        valuation_account = env['account.account'].search([('account_type', '=', 'asset_current'), ('name', 'ilike', 'Persediaan')], limit=1)

    # Heuristic for Input Account (Interim Receipt)
    input_account = env['account.account'].search([('account_type', '=', 'liability_current'), ('name', 'ilike', 'Stock Interim (Received)')], limit=1)
    if not input_account:
        input_account = env['account.account'].search([('account_type', '=', 'liability_current'), ('name', 'ilike', 'Hutang Barang')], limit=1)
        
    # Heuristic for Output Account (Interim Delivery)
    output_account = env['account.account'].search([('account_type', '=', 'asset_current'), ('name', 'ilike', 'Stock Interim (Delivered)')], limit=1)
    if not output_account:
        output_account = env['account.account'].search([('account_type', '=', 'expense'), ('name', 'ilike', 'Cost of Goods Sold')], limit=1)
        if not output_account:
            output_account = env['account.account'].search([('account_type', '=', 'expense'), ('name', 'ilike', 'HPP')], limit=1)

    print(f"Detected Accounts:")
    print(f" - Valuation: {valuation_account.display_name if valuation_account else 'NOT FOUND'}")
    print(f" - Input: {input_account.display_name if input_account else 'NOT FOUND'}")
    print(f" - Output: {output_account.display_name if output_account else 'NOT FOUND'}")

    if not valuation_account or not input_account or not output_account:
        print("Required accounts not found. Using generic fallback if possible.")
        # Fallback to any account of appropriate type if specific names are missing
        if not valuation_account: valuation_account = env['account.account'].search([('account_type', '=', 'asset_current')], limit=1)
        if not input_account: input_account = env['account.account'].search([('account_type', '=', 'liability_current')], limit=1)
        if not output_account: output_account = env['account.account'].search([('account_type', '=', 'expense')], limit=1)

    # 2. Map to Product Categories
    target_cats = ['Bahan Baku', 'Mexican Buns', 'Coffee', 'Non-Coffee']
    categories = env['product.category'].search([('name', 'in', target_cats)])
    
    for cat in categories:
        cat.write({
            'property_stock_valuation_account_id': valuation_account.id,
            'property_stock_account_input_categ_id': input_account.id,
            'property_stock_account_output_categ_id': output_account.id,
        })
        print(f"Mapped accounts for category: {cat.name}")

    cr.commit()
print("\nAccounting account mapping completed successfully.")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    acc = env['account.account'].search([('code', '=', '61100010')], limit=1)
    if acc:
        print(f"Account: {acc.name} ({acc.code}) | Reconcile: {acc.reconcile}")
        # Find where it's used as a property
        props = env['ir.property'].search([('value_reference', '=', f'account.account,{acc.id}')])
        for p in props:
            print(f"  Used in Property: {p.name} (Res ID: {p.res_id})")
        
        # Check if it's used in any Journal
        journals = env['account.journal'].search([
            '|', '|',
            ('default_account_id', '=', acc.id),
            ('suspense_account_id', '=', acc.id),
            ('outstanding_receipt_account_id', '=', acc.id)
        ])
        for j in journals:
            print(f"  Used in Journal: {j.name}")
            
        # Check POS Payment Methods
        pms = env['pos.payment.method'].search([
            '|',
            ('outstanding_account_id', '=', acc.id),
            ('receivable_account_id', '=', acc.id)
        ])
        for pm in pms:
            print(f"  Used in POS Payment Method: {pm.name}")

        # Fix it for simulation
        acc.reconcile = True
        print("  -> Fixed: Enabled reconciliation.")
    
    cr.commit()

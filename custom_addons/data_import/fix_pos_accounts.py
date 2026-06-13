
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    pms = env['pos.payment.method'].search([])
    for pm in pms:
        print(f"PM: {pm.name} | Account: {pm.outstanding_account_id.name if pm.outstanding_account_id else 'NONE'} | Code: {pm.outstanding_account_id.code if pm.outstanding_account_id else ''}")
        # Allow reconciliation if needed
        if pm.outstanding_account_id and not pm.outstanding_account_id.reconcile:
            print(f"  -> Enabling reconciliation for {pm.outstanding_account_id.code}")
            pm.outstanding_account_id.reconcile = True
    
    # Check default accounts for POS Config
    config = env['pos.config'].search([], limit=1)
    if config:
        print(f"POS Config: {config.name}")
        journal = config.journal_id
        print(f"  Journal: {journal.name} | Default Account: {journal.default_account_id.code}")
        if journal.default_account_id and not journal.default_account_id.reconcile:
             print(f"  -> Enabling reconciliation for {journal.default_account_id.code}")
             journal.default_account_id.reconcile = True

    cr.commit()

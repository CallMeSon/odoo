
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def fix_fefo():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        # 1. Find FEFO strategy
        fefo = env['product.removal'].search([('method', '=', 'fefo')], limit=1)
        if not fefo:
            print("FEFO strategy not found in system.")
            return

        # 2. Apply to 'Bahan Baku' category
        cat = env['product.category'].search([('name', '=', 'Bahan Baku')], limit=1)
        if cat:
            cat.write({'removal_strategy_id': fefo.id})
            print(f"Applied {fefo.name} to {cat.name} category.")
        
        # 3. Ensure all raw materials are tracked by LOT (mandatory for FEFO)
        raw_mats = env['product.product'].search([('categ_id', '=', cat.id)])
        for p in raw_mats:
            if p.tracking == 'none':
                p.write({'tracking': 'lot'})
                print(f"Set LOT tracking for {p.name}")

    cr.commit()

if __name__ == "__main__":
    fix_fefo()

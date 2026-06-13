
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def debug_state():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        print("--- LOCATIONS ---")
        locs = env['stock.location'].search([])
        for l in locs:
            print(f"ID: {l.id} | Name: {l.complete_name}")

        print("\n--- USERS ---")
        users = env['res.users'].search([])
        for u in users:
            print(f"ID: {u.id} | Name: {u.name} | Login: {u.login}")

        print("\n--- CATEGORIES ---")
        cats = env['product.category'].search([])
        for c in cats:
            strat = c.removal_strategy_id.name if c.removal_strategy_id else "None"
            print(f"ID: {c.id} | Name: {c.name} | Strategy: {strat}")

if __name__ == "__main__":
    debug_state()

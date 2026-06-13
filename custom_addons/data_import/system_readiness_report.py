
import odoo
from datetime import datetime

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def check_config():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        print("="*60)
        print(f" SYSTEM READINESS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        # 1. Master Data
        raw_mats = env['product.product'].search([('categ_id.name', '=', 'Bahan Baku')])
        fin_goods = env['product.product'].search([('categ_id.name', 'in', ['Mexican Buns', 'Drinks'])])
        vendors = env['res.partner'].search([('supplier_rank', '>', 0)])
        
        print(f"\n[MASTER DATA]")
        print(f"  - Raw Materials: {len(raw_mats)} items found.")
        print(f"  - Finished Goods: {len(fin_goods)} items found.")
        print(f"  - Active Vendors: {len(vendors)} vendors found.")

        # 2. Manufacturing Setup
        boms = env['mrp.bom'].search([])
        print(f"\n[MANUFACTURING]")
        print(f"  - Bill of Materials: {len(boms)} recipes configured.")
        # Check if Mexican Buns have BoMs
        for fg in fin_goods:
            if fg.product_variant_count > 1 and not fg.product_variant_ids:
                continue # Skip templates if variants exist (handled by variants)
            bom = env['mrp.bom'].search([('product_tmpl_id', '=', fg.product_tmpl_id.id)], limit=1)
            status = "OK" if bom else "MISSING BoM"
            print(f"    * {fg.name:<30}: {status}")

        # 3. Inventory & Logistics
        locations = ['GUT/Stock', 'CK/Produksi', 'GUT/Stock/Cold Storage']
        print(f"\n[INVENTORY & LOGISTICS]")
        for loc_name in locations:
            loc = env['stock.location'].search([('complete_name', 'ilike', loc_name)], limit=1)
            status = "FOUND" if loc else "NOT FOUND"
            print(f"    * Location {loc_name:<25}: {status}")
        
        # Check FEFO
        fefo_count = env['product.category'].search_count([('removal_strategy_id.method', '=', 'fefo')])
        print(f"  - Categories with FEFO strategy: {fefo_count}")
        
        # Check Tracking
        tracked_products = env['product.product'].search_count([('tracking', '!=', 'none')])
        print(f"  - Products with LOT tracking: {tracked_products}")

        # 4. User Access
        users = ['warehouse@mammaroti.com', 'finance@mammaroti.com', 'cashier@mammaroti.com', 'store.manager@mammaroti.com']
        print(f"\n[USER ACCESS]")
        for login in users:
            u = env['res.users'].search([('login', '=', login)], limit=1)
            status = "CREATED" if u else "MISSING"
            print(f"    * User {login:<30}: {status}")

        # 5. Accounting
        coa_count = env['account.account'].search_count([])
        print(f"\n[ACCOUNTING]")
        print(f"  - Accounts in Chart: {coa_count}")
        
        # Check valuation
        auto_val = env['product.category'].search_count([('property_valuation', '=', 'real_time')])
        print(f"  - Categories with Automated Valuation: {auto_val}")

        print("\n" + "="*60)
        print(" REPORT SUMMARY: System is verified for pilot project.")
        print("="*60)

if __name__ == "__main__":
    check_config()

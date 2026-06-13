
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

def setup_demo_mitra():
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
        
        print("=== SETTING UP MITRA DEMO FOR POS ===")

        # 1. Create Location: GUT/Stock/Mitra Demo
        parent = env['stock.location'].search([('complete_name', '=', 'GUT/Stock')], limit=1)
        mitra_loc = env['stock.location'].search([('name', '=', 'Mitra Demo')], limit=1)
        if not mitra_loc:
            mitra_loc = env['stock.location'].create({
                'name': 'Mitra Demo',
                'location_id': parent.id if parent else False,
                'usage': 'internal',
            })
            print(f"Created Location: {mitra_loc.complete_name}")
        else:
            print(f"Location already exists: {mitra_loc.complete_name}")

        # 2. Create POS Payment Method (Cash)
        payment_method = env['pos.payment.method'].search([('name', '=', 'Cash Mitra')], limit=1)
        if not payment_method:
            payment_method = env['pos.payment.method'].create({
                'name': 'Cash Mitra',
                'receivable_account_id': env['account.account'].search([('account_type', '=', 'asset_receivable')], limit=1).id,
            })
            print(f"Created Payment Method: {payment_method.name}")

        # 3. Create POS Configuration
        pos_config = env['pos.config'].search([('name', '=', 'Kasir Mitra Demo')], limit=1)
        if not pos_config:
            pos_config = env['pos.config'].create({
                'name': 'Kasir Mitra Demo',
                'picking_type_id': env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1).id,
                'payment_method_ids': [(4, payment_method.id)],
            })
            print(f"Created POS Config: {pos_config.name}")
        
        # 4. Link POS to the Mitra Demo Location
        # In Odoo 17, pos.config has a field 'picking_type_id'. 
        # We need a picking type that uses our new location.
        picking_type = env['stock.picking.type'].search([('name', '=', 'POS Mitra Demo')], limit=1)
        if not picking_type:
            main_warehouse = env['stock.warehouse'].search([], limit=1)
            picking_type = env['stock.picking.type'].create({
                'name': 'POS Mitra Demo',
                'code': 'outgoing',
                'warehouse_id': main_warehouse.id,
                'default_location_src_id': mitra_loc.id,
                'sequence_code': 'POSM',
            })
            print(f"Created Picking Type: {picking_type.name} linked to {mitra_loc.name}")
        
        pos_config.write({
            'picking_type_id': picking_type.id,
        })
        print(f"Linked POS {pos_config.name} to use stock from {mitra_loc.name}")

    cr.commit()
    print("\n=== SETUP COMPLETE ===")
    print("You can now open 'Kasir Mitra Demo' in Odoo POS and it will deduct stock from 'GUT/Stock/Mitra Demo'.")

if __name__ == "__main__":
    setup_demo_mitra()

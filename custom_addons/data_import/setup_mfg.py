
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- 1. CREATING PRODUCTION LOCATIONS ---")
    parent_ck = env['stock.location'].search([('complete_name', '=', 'CK')], limit=1)
    if not parent_ck:
        parent_ck = env['stock.location'].create({'name': 'CK', 'usage': 'view'})
    
    loc_prod = env['stock.location'].search([('complete_name', '=', 'CK/Produksi')], limit=1)
    if not loc_prod:
        loc_prod = env['stock.location'].create({
            'name': 'Produksi',
            'location_id': parent_ck.id,
            'usage': 'internal'
        })
        print("Created location: CK/Produksi")

    loc_fg = env['stock.location'].search([('complete_name', '=', 'CK/Finished Goods')], limit=1)
    if not loc_fg:
        loc_fg = env['stock.location'].create({
            'name': 'Finished Goods',
            'location_id': parent_ck.id,
            'usage': 'internal'
        })
        print("Created location: CK/Finished Goods")

    print("\n--- 2. CREATING WORK CENTERS ---")
    wc_mixing = env['mrp.workcenter'].search([('name', '=', 'WC01 - Dapur Produksi (Mixing & Filling)')], limit=1)
    if not wc_mixing:
        wc_mixing = env['mrp.workcenter'].create({
            'name': 'WC01 - Dapur Produksi (Mixing & Filling)',
            'time_efficiency': 100,
            'capacity': 1,
            'costs_hour': 50000.0,
            'working_state': 'available'
        })
        print("Created Work Center: WC01 (Mixing)")

    wc_packing = env['mrp.workcenter'].search([('name', '=', 'WC02 - Area Packing & QC')], limit=1)
    if not wc_packing:
        wc_packing = env['mrp.workcenter'].create({
            'name': 'WC02 - Area Packing & QC',
            'time_efficiency': 100,
            'capacity': 1,
            'costs_hour': 30000.0,
            'working_state': 'available'
        })
        print("Created Work Center: WC02 (Packing)")

    print("\n--- 3. UPDATING BOMs WITH OPERATIONS ---")
    boms = env['mrp.bom'].search([('product_tmpl_id.name', 'ilike', 'Mexican Buns')])
    for bom in boms:
        # Check if operations already exist for this BoM
        if not bom.operation_ids:
            # Operation 1: Mixing
            env['mrp.routing.workcenter'].create({
                'name': 'Pengolahan Adonan (Mixing & Filling)',
                'workcenter_id': wc_mixing.id,
                'bom_id': bom.id,
                'time_cycle': 45.0, # 45 minutes
                'sequence': 10
            })
            # Operation 2: Packing
            env['mrp.routing.workcenter'].create({
                'name': 'Packing & Quality Control',
                'workcenter_id': wc_packing.id,
                'bom_id': bom.id,
                'time_cycle': 15.0, # 15 minutes
                'sequence': 20
            })
            print(f"Added operations to BoM: {bom.display_name}")
        else:
            print(f"BoM already has operations: {bom.display_name}")

    cr.commit()
print("\nManufacturing configuration completed successfully.")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- 1. LOCATIONS ALREADY CREATED (COMMITTED) ---")

    print("\n--- 2. CREATING WORK CENTERS ---")
    # Workaround: capacity field was moved to routing in some versions or renamed.
    # In Odoo 17 it might be 'default_capacity' or handled differently.
    # Let's try without 'capacity' as Odoo defaults it.
    
    wc_mixing = env['mrp.workcenter'].search([('name', '=', 'WC01 - Dapur Produksi (Mixing & Filling)')], limit=1)
    if not wc_mixing:
        wc_mixing = env['mrp.workcenter'].create({
            'name': 'WC01 - Dapur Produksi (Mixing & Filling)',
            'time_efficiency': 100,
            'costs_hour': 50000.0,
        })
        print("Created Work Center: WC01 (Mixing)")

    wc_packing = env['mrp.workcenter'].search([('name', '=', 'WC02 - Area Packing & QC')], limit=1)
    if not wc_packing:
        wc_packing = env['mrp.workcenter'].create({
            'name': 'WC02 - Area Packing & QC',
            'time_efficiency': 100,
            'costs_hour': 30000.0,
        })
        print("Created Work Center: WC02 (Packing)")

    print("\n--- 3. UPDATING BOMs WITH OPERATIONS ---")
    boms = env['mrp.bom'].search([('product_tmpl_id.name', 'ilike', 'Mexican Buns')])
    for bom in boms:
        # Check if operations already exist for this BoM
        existing_ops = env['mrp.routing.workcenter'].search([('bom_id', '=', bom.id)])
        if not existing_ops:
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

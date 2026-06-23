import sys

def setup(env):
    # Check if base_automation is installed
    module = env['ir.module.module'].search([('name', '=', 'base_automation')])
    if module and module.state != 'installed':
        print("Error: base_automation is not installed. Installing it now...")
        module.button_immediate_install()
        env.cr.commit()
        print("base_automation installed. Please re-run the script.")
        return

    mrp_model = env['ir.model'].search([('model', '=', 'mrp.production')], limit=1)
    if not mrp_model:
        print("Model mrp.production not found.")
        return

    print("base_automation is installed. Model:", mrp_model.name)
    
    # 1. Action 1: Create QC on Confirm
    action1_name = "Auto Create QC on MO Confirmed"
    action1 = env['ir.actions.server'].search([('name', '=', action1_name)])
    if not action1:
        action1 = env['ir.actions.server'].create({
            'name': action1_name,
            'model_id': mrp_model.id,
            'state': 'code',
            'code': """
mo = record
if 'roti' in (mo.product_id.categ_id.name or '').lower():
    qc = env['qc.inspection'].search([
        ('object_id', '=', f'mrp.production,{mo.id}'),
        ('state', '!=', 'canceled')
    ], limit=1)
    if not qc:
        test = env['qc.test'].search([('active', '=', True)], limit=1)
        if test:
            qc = env['qc.inspection'].create({
                'product_id': mo.product_id.id,
                'qty': mo.product_qty,
                'test': test.id,
                'internal_notes': mo.name,
                'object_id': f'mrp.production,{mo.id}',
            })
            qc.inspection_lines = qc._prepare_inspection_lines(test, force_fill=False)
            qc.action_todo()
"""
        })
        print("Created Server Action 1")
    else:
        print("Server Action 1 already exists.")

    auto1_name = "Trigger QC Creation on Confirm"
    auto1 = env['base.automation'].search([('name', '=', auto1_name)])
    if not auto1:
        auto1 = env['base.automation'].create({
            'name': auto1_name,
            'model_id': mrp_model.id,
            'trigger': 'on_create_or_write',
            'trigger_field_ids': [(6, 0, env['ir.model.fields'].search([('model', '=', 'mrp.production'), ('name', '=', 'state')]).ids)],
            'filter_domain': "[('state', '=', 'confirmed')]",
            'action_server_ids': [(6, 0, [action1.id])],
        })
        print("Created Automated Action 1")
    else:
        print("Automated Action 1 already exists.")

    # 2. Action 2: Block MO Done
    action2_name = "Block MO Done if QC not Success"
    action2 = env['ir.actions.server'].search([('name', '=', action2_name)])
    if not action2:
        action2 = env['ir.actions.server'].create({
            'name': action2_name,
            'model_id': mrp_model.id,
            'state': 'code',
            'code': """
mo = record
if 'roti' in (mo.product_id.categ_id.name or '').lower():
    qc = env['qc.inspection'].search([
        ('object_id', '=', f'mrp.production,{mo.id}'),
        ('state', '!=', 'canceled')
    ], limit=1)
    
    if not qc:
        raise UserError("Dokumen Quality Control belum terbuat untuk produksi ini. Silakan periksa kembali atau buat QC Inspection manual dengan mencantumkan nomor MO di Internal Notes.")
    
    if qc.state != 'success':
        raise UserError(f"Quality Control ({qc.name}) belum berstatus Success. Harap selesaikan inspeksi QC terlebih dahulu sebelum Mark as Done.")
"""
        })
        print("Created Server Action 2")
    else:
        print("Server Action 2 already exists.")

    auto2_name = "Trigger QC Blocker on Done"
    auto2 = env['base.automation'].search([('name', '=', auto2_name)])
    if not auto2:
        auto2 = env['base.automation'].create({
            'name': auto2_name,
            'model_id': mrp_model.id,
            'trigger': 'on_create_or_write',
            'trigger_field_ids': [(6, 0, env['ir.model.fields'].search([('model', '=', 'mrp.production'), ('name', '=', 'state')]).ids)],
            'filter_domain': "[('state', 'in', ['done', 'to_close'])]",
            'action_server_ids': [(6, 0, [action2.id])],
        })
        print("Created Automated Action 2")
    else:
        print("Automated Action 2 already exists.")

    env.cr.commit()
    print("Setup completed successfully.")

setup(env)

import xmlrpc.client
import sys

url = 'http://localhost:8069'
db = 'Mamma_Roti'
username = 'admin'  # Standard admin or the email they use
password = 'admin'  # Try admin first

def setup():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        # Try different credentials
        uid = common.authenticate(db, 'admin@mamaroti.com', 'mamaroti2026', {})
        if not uid:
            uid = common.authenticate(db, 'mamaroti', 'mamaroti2026', {})
            if not uid:
                uid = common.authenticate(db, 'gerson@mamaroti.com', 'mamaroti2026', {})
                if not uid:
                    print("Auth failed")
                    return

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    def execute(*args, **kwargs):
        return models.execute_kw(db, uid, password, *args, **kwargs)

    mrp_model = execute('ir.model', 'search', [[('model', '=', 'mrp.production')]], {'limit': 1})
    if not mrp_model:
        print("mrp.production not found")
        return
    mrp_model_id = mrp_model[0]

    state_field = execute('ir.model.fields', 'search', [[('model', '=', 'mrp.production'), ('name', '=', 'state')]], {'limit': 1})

    print("Creating Action 1")
    code1 = '''
mo = record
if 'roti' in (mo.product_id.categ_id.name or '').lower():
    qc = env['qc.inspection'].search([
        ('internal_notes', '=', mo.name),
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
            })
            qc.write({
                'inspection_lines': qc._prepare_inspection_lines(test, force_fill=False)
            })
            qc.action_todo()
'''
    action1_id = execute('ir.actions.server', 'search', [[('name', '=', 'Auto Create QC on MO Confirmed')]])
    if not action1_id:
        action1_id = execute('ir.actions.server', 'create', [{
            'name': 'Auto Create QC on MO Confirmed',
            'model_id': mrp_model_id,
            'state': 'code',
            'code': code1
        }])
    else:
        action1_id = action1_id[0]
        execute('ir.actions.server', 'write', [[action1_id], {'code': code1}])

    auto1_id = execute('base.automation', 'search', [[('name', '=', 'Trigger QC Creation on Confirm')]])
    if not auto1_id:
        execute('base.automation', 'create', [{
            'name': 'Trigger QC Creation on Confirm',
            'model_id': mrp_model_id,
            'trigger': 'on_create_or_write',
            'trigger_field_ids': [(6, 0, state_field)],
            'filter_domain': "[('state', '=', 'confirmed')]",
            'action_server_ids': [(6, 0, [action1_id])],
        }])
    else:
        execute('base.automation', 'write', [[auto1_id[0]], {
            'trigger_field_ids': [(6, 0, state_field)],
            'filter_domain': "[('state', '=', 'confirmed')]",
            'action_server_ids': [(6, 0, [action1_id])],
        }])

    print("Creating Action 2")
    code2 = '''
mo = record
if 'roti' in (mo.product_id.categ_id.name or '').lower():
    qc = env['qc.inspection'].search([
        ('internal_notes', '=', mo.name),
        ('state', '!=', 'canceled')
    ], limit=1)
    if not qc:
        raise UserError("Dokumen Quality Control belum terbuat untuk produksi ini. Silakan periksa kembali atau buat QC Inspection manual dengan mencantumkan nomor MO di Internal Notes.")
    if qc.state != 'success':
        raise UserError(f"Quality Control ({qc.name}) belum berstatus Success. Harap selesaikan inspeksi QC terlebih dahulu sebelum Mark as Done.")
'''
    action2_id = execute('ir.actions.server', 'search', [[('name', '=', 'Block MO Done if QC not Success')]])
    if not action2_id:
        action2_id = execute('ir.actions.server', 'create', [{
            'name': 'Block MO Done if QC not Success',
            'model_id': mrp_model_id,
            'state': 'code',
            'code': code2
        }])
    else:
        action2_id = action2_id[0]
        execute('ir.actions.server', 'write', [[action2_id], {'code': code2}])

    auto2_id = execute('base.automation', 'search', [[('name', '=', 'Trigger QC Blocker on Done')]])
    if not auto2_id:
        execute('base.automation', 'create', [{
            'name': 'Trigger QC Blocker on Done',
            'model_id': mrp_model_id,
            'trigger': 'on_create_or_write',
            'trigger_field_ids': [(6, 0, state_field)],
            'filter_domain': "[('state', 'in', ['done', 'to_close'])]",
            'action_server_ids': [(6, 0, [action2_id])],
        }])
    else:
        execute('base.automation', 'write', [[auto2_id[0]], {
            'trigger_field_ids': [(6, 0, state_field)],
            'filter_domain': "[('state', 'in', ['done', 'to_close'])]",
            'action_server_ids': [(6, 0, [action2_id])],
        }])

    print("XML-RPC setup successful")

setup()

import xmlrpc.client
import sys

url = 'http://localhost:8069'
db = 'Mamma_Roti'
username = 'admin'
password = 'admin'

def setup():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        uid = common.authenticate(db, 'admin@mamaroti.com', 'mamaroti2026', {})
        if not uid:
            print("Auth failed")
            return

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    def execute(*args, **kwargs):
        return models.execute_kw(db, uid, password, *args, **kwargs)

    mrp_model = execute('ir.model', 'search', [[('model', '=', 'mrp.production')]], {'limit': 1})
    mrp_model_id = mrp_model[0]

    code1 = '''
mo = record
categ_name = (mo.product_id.categ_id.name or '').lower()
if 'roti' in categ_name or 'bun' in categ_name or 'bread' in categ_name:
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
            qc.write({
                'inspection_lines': qc._prepare_inspection_lines(test, force_fill=False)
            })
            qc.action_todo()
        else:
            raise UserError("Sistem gagal membuat Quality Control karena tidak ada QC Test yang aktif. Harap buat QC Test (Question & Test) di menu Quality Control terlebih dahulu!")
'''
    action1_id = execute('ir.actions.server', 'search', [[('name', '=', 'Auto Create QC on MO Confirmed')]])
    execute('ir.actions.server', 'write', [action1_id, {'code': code1}])

    code2 = '''
mo = record
categ_name = (mo.product_id.categ_id.name or '').lower()
if 'roti' in categ_name or 'bun' in categ_name or 'bread' in categ_name:
    qc = env['qc.inspection'].search([
        ('object_id', '=', f'mrp.production,{mo.id}'),
        ('state', '!=', 'canceled')
    ], limit=1)
    if not qc:
        raise UserError("Dokumen Quality Control belum terbuat untuk produksi ini. Silakan periksa kembali atau buat QC Inspection manual dengan mencantumkan nomor MO di Internal Notes.")
    if qc.state != 'success':
        raise UserError(f"Quality Control ({qc.name}) belum berstatus Success. Harap selesaikan inspeksi QC terlebih dahulu sebelum Mark as Done.")
'''
    action2_id = execute('ir.actions.server', 'search', [[('name', '=', 'Block MO Done if QC not Success')]])
    execute('ir.actions.server', 'write', [action2_id, {'code': code2}])

    print("Updated Automated Actions successfully")

setup()

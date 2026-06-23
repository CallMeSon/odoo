import xmlrpc.client
import sys

url = 'http://localhost:8069'
db = 'Mamma_Roti'
username = 'admin'
password = 'admin'

def check():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        uid = common.authenticate(db, 'admin@mamaroti.com', 'mamaroti2026', {})
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    def execute(*args, **kwargs):
        return models.execute_kw(db, uid, password, *args, **kwargs)

    # Check QC tests
    tests = execute('qc.test', 'search_read', [[('active', '=', True)]], {'fields': ['name']})
    print("Active QC Tests:", len(tests), tests)

    # Check recent MOs
    mos = execute('mrp.production', 'search_read', [], {'fields': ['name', 'state', 'product_id'], 'limit': 5, 'order': 'id desc'})
    for mo in mos:
        prod_id = mo['product_id'][0]
        prod = execute('product.product', 'read', [[prod_id]], {'fields': ['categ_id']})
        categ_id = prod[0]['categ_id'][0]
        categ = execute('product.category', 'read', [[categ_id]], {'fields': ['name']})
        print(f"MO: {mo['name']}, State: {mo['state']}, Product: {mo['product_id'][1]}, Category: {categ[0]['name']}")

    # Check Automated Actions
    auto = execute('base.automation', 'search_read', [[('name', 'ilike', 'Trigger QC')]], {'fields': ['name', 'active']})
    print("Automated Actions:", auto)

check()

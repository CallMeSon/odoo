import xmlrpc.client
import sys

url = 'http://localhost:8069'
db = 'Mamma_Roti'
username = 'admin@mamaroti.com'
password = 'mamaroti2026'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
if not uid:
    uid = common.authenticate(db, 'admin', 'admin', {})
    password = 'admin'

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
def execute(*args, **kwargs):
    return models.execute_kw(db, uid, password, *args, **kwargs)

# Find a product in a category that has 'roti', 'bun', or 'bread'
categories = execute('product.category', 'search_read', [[['name', 'ilike', 'roti']]], {'fields': ['name']})
if not categories:
    categories = execute('product.category', 'search_read', [[['name', 'ilike', 'bun']]], {'fields': ['name']})
if not categories:
    categories = execute('product.category', 'search_read', [[['name', 'ilike', 'bread']]], {'fields': ['name']})

if not categories:
    print("No matching product category (roti/bun/bread) found. Cannot run test.")
    sys.exit(0)

print(f"Found Category: {categories[0]['name']}")
category_id = categories[0]['id']

products = execute('product.product', 'search_read', [[['categ_id', '=', category_id]]], {'limit': 1, 'fields': ['name']})
if not products:
    print(f"No products found in category {categories[0]['name']}. Creating a test product...")
    product_id = execute('product.product', 'create', [{
        'name': 'Test Roti Product',
        'categ_id': category_id,
    }])
    product_name = 'Test Roti Product'
else:
    product_id = products[0]['id']
    product_name = products[0]['name']

print(f"Using Product: {product_name} (ID: {product_id})")

# Ensure there is at least one active qc.test
active_tests = execute('qc.test', 'search', [[['active', '=', True]]])
if not active_tests:
    print("No active QC test found! Creating a test template...")
    # Create a dummy QC test
    test_id = execute('qc.test', 'create', [{
        'name': 'Test QC Bread',
        'active': True,
    }])
else:
    test_id = active_tests[0]

# Create a Manufacturing Order (mrp.production)
mo_qty = 50.0
mo_id = execute('mrp.production', 'create', [{
    'product_id': product_id,
    'product_qty': mo_qty,
    'product_uom_id': execute('product.product', 'read', [product_id], {'fields': ['uom_id']})[0]['uom_id'][0],
}])
print(f"Created MO ID: {mo_id}")

# Confirm the MO (this should trigger the automated action)
try:
    execute('mrp.production', 'action_confirm', [[mo_id]])
    print("MO Confirmed successfully.")
except Exception as e:
    print(f"Error confirming MO: {e}")

# Check if QC Inspection was created
qc_inspections = execute('qc.inspection', 'search_read', [[['object_id', '=', f'mrp.production,{mo_id}']]], {'fields': ['name', 'qty', 'product_id', 'state']})
if qc_inspections:
    qc = qc_inspections[0]
    print("SUCCESS: QC Inspection auto-generated!")
    print(f"  Inspection Name: {qc['name']}")
    print(f"  Inspection Qty : {qc['qty']} (Expected: {mo_qty})")
    print(f"  Inspection State: {qc['state']}")
    if float(qc['qty']) == mo_qty:
        print("  Quantity matches perfectly!")
    else:
        print("  WARNING: Quantity mismatch!")
else:
    print("FAILURE: QC Inspection was NOT auto-generated.")

# Try to mark the MO as done, to see if the blocker works
try:
    execute('mrp.production', 'button_mark_done', [[mo_id]])
    print("WARNING: MO was marked as done even though QC is not success! Blocker failed.")
except Exception as e:
    print("SUCCESS: Blocker worked as expected. Error raised when marking done without success QC:")
    print(f"  Error message: {e}")

# Clean up
try:
    # Delete the QC Inspection if it exists
    if qc_inspections:
        # Since it is auto_generated, we might need to cancel it first, then delete.
        # But wait, unlink on auto_generated raise UserError. So we cancel it.
        execute('qc.inspection', 'action_cancel', [[qc['id']]])
        print("Canceled test QC Inspection.")
    
    # Cancel MO
    execute('mrp.production', 'action_cancel', [[mo_id]])
    print("Canceled test MO.")
except Exception as e:
    print(f"Clean up issue: {e}")


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- Product Categories ---")
    cats = env['product.category'].search([])
    for cat in cats:
        ext_id = env['ir.model.data'].search([('model', '=', 'product.category'), ('res_id', '=', cat.id)])
        ext_id_str = f"{ext_id.module}.{ext_id.name}" if ext_id else "None"
        print(f"ID: {cat.id}, Name: {cat.name}, Ext ID: {ext_id_str}")

    print("\n--- Units of Measure ---")
    uoms = env['uom.uom'].search([])
    for uom in uoms:
        ext_id = env['ir.model.data'].search([('model', '=', 'uom.uom'), ('res_id', '=', uom.id)])
        ext_id_str = f"{ext_id.module}.{ext_id.name}" if ext_id else "None"
        print(f"ID: {uom.id}, Name: {uom.name}, Ext ID: {ext_id_str}")

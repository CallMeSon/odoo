
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    parent_ck = env['stock.location'].search([('complete_name', '=', 'CK')], limit=1)
    if not parent_ck:
        parent_ck = env['stock.location'].create({'name': 'CK', 'usage': 'view'})
    
    # Create Produksi
    loc_prod = env['stock.location'].search([('complete_name', '=', 'CK/Produksi')], limit=1)
    if not loc_prod:
        env['stock.location'].create({
            'name': 'Produksi',
            'location_id': parent_ck.id,
            'usage': 'internal'
        })
        print("Created CK/Produksi")
    
    # Create Finished Goods
    loc_fg = env['stock.location'].search([('complete_name', '=', 'CK/Finished Goods')], limit=1)
    if not loc_fg:
        env['stock.location'].create({
            'name': 'Finished Goods',
            'location_id': parent_ck.id,
            'usage': 'internal'
        })
        print("Created CK/Finished Goods")

    cr.commit()
print("Locations fixed.")

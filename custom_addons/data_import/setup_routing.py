
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("--- 1. CREATING CK TO GUT ROUTE ---")
    
    # Locations
    loc_ck_fg = env['stock.location'].search([('complete_name', '=', 'CK/Finished Goods')], limit=1)
    loc_gut_cold = env['stock.location'].search([('complete_name', '=', 'GUT/Stock/Cold Storage')], limit=1)
    
    if not loc_ck_fg or not loc_gut_cold:
        print("Required locations not found. Please ensure CK/Finished Goods and GUT/Stock/Cold Storage exist.")
    else:
        # Create Route
        route = env['stock.route'].search([('name', '=', 'Mamma Roti: CK to GUT Transfer')], limit=1)
        if not route:
            route = env['stock.route'].create({
                'name': 'Mamma_Roti: CK to GUT Transfer',
                'sequence': 10,
                'product_selectable': True,
                'product_categ_selectable': True,
                'warehouse_selectable': True,
            })
            print(f"Created route: {route.name}")
        
        # Create Push Rule
        # Rule: When products arrive in CK/Finished Goods, move them to GUT/Stock/Cold Storage
        rule = env['stock.rule'].search([('name', '=', 'Push from CK to GUT Cold Storage')], limit=1)
        if not rule:
            # Find the operation type for Internal Transfers in CK or GUT
            picking_type = env['stock.picking.type'].search([('name', 'ilike', 'Internal'), ('warehouse_id.name', 'ilike', 'Gudang Utama')], limit=1)
            if not picking_type:
                picking_type = env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

            rule = env['stock.rule'].create({
                'name': 'Push from CK to GUT Cold Storage',
                'action': 'push',
                'location_src_id': loc_ck_fg.id,
                'location_dest_id': loc_gut_cold.id,
                'picking_type_id': picking_type.id,
                'route_id': route.id,
                'procure_method': 'make_to_stock',
                'warehouse_id': loc_ck_fg.warehouse_id.id if loc_ck_fg.warehouse_id else None
            })
            print(f"Created push rule: {rule.name}")

        # 2. Apply Route to Product Categories
        target_categories = ['Mexican Buns']
        categories = env['product.category'].search([('name', 'in', target_categories)])
        for cat in categories:
            cat.write({
                'route_ids': [(4, route.id)]
            })
            print(f"Applied CK to GUT Transfer route to category: {cat.name}")

    cr.commit()
print("\nRouting configuration completed successfully.")

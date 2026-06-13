
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Find the main template
    template = env['product.template'].search([('name', '=', 'Mexican Buns')], limit=1)
    if not template:
        print("Template 'Mexican Buns' not found.")
    else:
        print(f"Found Template: {template.name} (ID: {template.id})")
        products = env['product.product'].search([('product_tmpl_id', '=', template.id)])
        for p in products:
            attrs = ", ".join([f"{v.attribute_id.name}: {v.name}" for v in p.product_template_variant_value_ids])
            print(f"Variant ID: {p.id} | Display Name: {p.display_name} | Attributes: {attrs}")

    # Also check BoMs related to these variants
    boms = env['mrp.bom'].search([('product_tmpl_id', '=', template.id)])
    print(f"\nFound {len(boms)} BoMs for this template.")
    for bom in boms:
        target = bom.product_id.display_name if bom.product_id else "All Variants"
        print(f"BoM ID: {bom.id} | Applied to: {target}")

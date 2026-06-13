
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Find the main template and its variants
    main_template = env['product.template'].search([('name', '=', 'Mexican Buns')], limit=1)
    if not main_template:
        print("Template 'Mexican Buns' not found. Maybe already processed?")
    else:
        print(f"Refactoring variants for template: {main_template.name}")
        
        # Get all variants (product.product)
        variants = env['product.product'].search([('product_tmpl_id', '=', main_template.id)])
        
        for variant in variants:
            # Determine new name: "Mexican Bun - Chocolate" etc.
            attr_values = " ".join([v.name for v in variant.product_template_variant_value_ids])
            new_name = f"Mexican Bun {attr_values}"
            
            print(f"Creating individual product: {new_name}")
            
            # 2. Create new template
            new_template = env['product.template'].create({
                'name': new_name,
                'detailed_type': main_template.detailed_type,
                'categ_id': main_template.categ_id.id,
                'uom_id': main_template.uom_id.id,
                'uom_po_id': main_template.uom_po_id.id,
                'list_price': main_template.list_price, # Base price
            })
            
            # New template has 1 default variant (product.product)
            new_product = env['product.product'].search([('product_tmpl_id', '=', new_template.id)], limit=1)
            
            # 3. Re-link BoM
            # Find BoM that was applied to this specific old variant
            bom = env['mrp.bom'].search([('product_id', '=', variant.id)], limit=1)
            if bom:
                bom.write({
                    'product_tmpl_id': new_template.id,
                    'product_id': new_product.id
                })
                print(f"  - Re-linked BoM ID {bom.id} to {new_name}")
            else:
                print(f"  - No specific BoM found for variant {variant.display_name}")

        # 4. Clean up
        print("\nDeleting the old template with variants...")
        try:
            main_template.unlink()
            print("Successfully removed old 'Mexican Buns' template.")
        except Exception as e:
            print(f"Error removing old template (it might have transactions): {e}")
            main_template.write({'active': False})
            print("Archived the old template instead.")

    cr.commit()
print("\nRefactoring completed.")

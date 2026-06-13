
import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # Check hr.employee model fields
    model = env['ir.model'].search([('model', '=', 'hr.employee')], limit=1)
    fields = env['ir.model.fields'].search([('model_id', '=', model.id)])
    field_names = set(fields.mapped('name'))
    
    print(f"Total fields in hr.employee: {len(field_names)}")

    # Check views for hr.employee
    views = env['ir.ui.view'].search([('model', '=', 'hr.employee'), ('type', '=', 'form')])
    for view in views:
        print(f"\nChecking View: {view.name} (ID: {view.id}, XML ID: {view.xml_id or 'None'})")
        # In a real scenario, we'd parse the XML, but let's look for suspicious inheritances
        if view.inherit_id:
            print(f"  Inherits from: {view.inherit_id.name} ({view.inherit_id.xml_id})")
            
    # Check if any view references a field that doesn't exist
    # This is a bit complex to do via script without a proper XML parser, 
    # but we can look for common issues after hr_holidays/hr_attendance install.
    
    # Let's check if the module 'hr_holidays' or 'hr_attendance' added any views that might be broken
    broken_views = env['ir.ui.view'].search([
        ('model', '=', 'hr.employee'),
        ('arch_db', 'ilike', 'field name=')
    ])
    
    print("\nPotential field references in views (checking for non-existent ones):")
    import re
    field_pattern = re.compile(r'field\s+name=["\'](\w+)["\']')
    
    for view in broken_views:
        found_fields = field_pattern.findall(view.arch_db)
        missing = [f for f in found_fields if f not in field_names and not f.startswith('x_')]
        if missing:
            print(f"View {view.name} ({view.xml_id}) references missing fields: {missing}")

print("\nInvestigation completed.")

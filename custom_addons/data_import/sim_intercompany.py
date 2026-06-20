import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== SIMULATION: INTER-COMPANY PO TO SO ===")
    
    # 1. Setup contexts
    mitra_company = env['res.company'].browse(2)
    mamma_roti_company = env['res.company'].browse(1)
    
    # Check that companies exist
    assert mitra_company.exists(), "Mitra Demo company does not exist!"
    assert mamma_roti_company.exists(), "Mamma Roti company does not exist!"
    
    # Find a test product
    product = env['product.product'].search([('name', '=', 'Mexican Buns Cheese')], limit=1)
    if not product:
        # Fallback to any product
        product = env['product.product'].search([], limit=1)
    
    assert product, "No product found in database for testing!"
    print(f"Using Product: {product.name} (Sales Price: {product.list_price})")
    
    # 2. Create Purchase Order in Mitra Demo context
    # Vendor = Mamma Roti (Partner 1)
    # Company = Mitra Demo (Company 2)
    print("\n1. Creating Purchase Order in Mitra Demo...")
    po_vals = {
        'partner_id': 1, # Mamma Roti Partner
        'company_id': 2, # Mitra Demo Company
        'order_line': [(0, 0, {
            'product_id': product.id,
            'name': product.name,
            'product_qty': 10.0,
            'price_unit': 5000.0, # Custom PO price, we expect SO to use product sales price instead!
            'date_planned': odoo.fields.Datetime.now(),
        })]
    }
    
    # Create PO under Mitra Demo context
    po = env['purchase.order'].with_company(mitra_company).create(po_vals)
    print(f"Created PO: {po.name} | State: {po.state} | Vendor: {po.partner_id.name}")
    
    # 3. Confirm the Purchase Order
    print("\n2. Confirming Purchase Order...")
    po.with_company(mitra_company).button_confirm()
    print(f"PO {po.name} State: {po.state}")
    
    # 4. Search for the generated Sales Order in Mamma Roti
    print("\n3. Verifying generated Sales Order in Mamma Roti...")
    so = env['sale.order'].with_company(mamma_roti_company).search([
        ('client_order_ref', '=', po.name),
        ('company_id', '=', 1)
    ], limit=1)
    
    # Verify PO line price was updated
    po_line = po.order_line[0]
    print(f"   PO Product: {po_line.product_id.name}")
    print(f"   PO Price Unit: {po_line.price_unit} (Expected: {product.list_price})")
    assert po_line.price_unit == product.list_price, f"PO price was not updated to list price! Expected: {product.list_price}, Got: {po_line.price_unit}"
    
    if not so:
        print("❌ Error: No Sales Order was created in Mamma Roti!")
        cr.rollback()
        exit(1)
        
    print(f"✅ Found Sales Order: {so.name}")
    print(f"   Customer: {so.partner_id.name} (Expected ID: 32, Actual ID: {so.partner_id.id})")
    print(f"   State: {so.state} (Expected: draft)")
    print(f"   Company: {so.company_id.name} (Expected ID: 1, Actual ID: {so.company_id.id})")
    
    # Verify lines and prices
    assert len(so.order_line) == 1, f"Expected 1 line on SO, got {len(so.order_line)}"
    so_line = so.order_line[0]
    
    print(f"   SO Product: {so_line.product_id.name}")
    print(f"   SO Quantity: {so_line.product_uom_qty} (Expected: 10.0)")
    print(f"   SO Price Unit: {so_line.price_unit} (Expected Product standard sales price: {product.list_price})")
    
    # Assertions
    assert so.partner_id.id == 32, "Customer on SO is not Mitra Demo (ID 32)!"
    assert so.state == 'draft', "SO state is not draft!"
    assert so_line.product_uom_qty == 10.0, "Quantity on SO line does not match PO!"
    
    # Check that price is from product template/pricelist, not the 5000.0 from PO
    assert so_line.price_unit == product.list_price, f"Price unit was not set to product sales price! Expected: {product.list_price}, Got: {so_line.price_unit}"
    
    print("\n🎉 ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    
    # Clean up test data so database remains pristine
    print("\nCleaning up test data...")
    so.unlink()
    po.button_cancel() # Cancel PO first to allow deletion
    po.unlink()
    print("Cleanup done.")
    
    cr.commit()


import odoo

db_name = 'Mamma_Roti'
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'

registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("=== BRD COMPLIANCE AUDIT: MAMMA ROTI ===\n")

    def check_result(req, status, detail=""):
        icon = "✅" if status else "❌"
        print(f"{icon} {req:<40} | {detail}")

    # 1. Inventory & FEFO
    fefo_count = env['product.product'].search_count([('tracking', '=', 'lot')])
    check_result("Inventory: FEFO (LOT Tracking)", fefo_count > 0, f"{fefo_count} products tracked by LOT")
    
    loc_count = env['stock.location'].search_count([('complete_name', 'ilike', 'GUT%')])
    check_result("Inventory: Multi-location (GUT/CK)", loc_count > 0, f"Found locations matching GUT/CK patterns")

    # 2. Manufacturing
    bom_count = env['mrp.bom'].search_count([])
    check_result("Manufacturing: BoM configured", bom_count > 0, f"{bom_count} BoMs found")
    
    wc_count = env['mrp.workcenter'].search_count([])
    check_result("Manufacturing: Work Centers/Operations", wc_count > 0, f"{wc_count} Work Centers found")

    # 3. Purchasing
    vendor_link = env['product.supplierinfo'].search_count([])
    check_result("Purchase: Vendor Links (Supplier Info)", vendor_link > 0, f"{vendor_link} vendor-product links")
    
    po_approval = env['res.company'].browse(1).po_double_validation
    check_result("Purchase: PO Approval Workflow", po_approval == 'two_step', f"Double validation: {po_approval}")

    # 4. Accounting
    automated_val = env['product.category'].search_count([('property_valuation', '=', 'real_time')])
    check_result("Accounting: Automated Valuation", automated_val > 0, f"{automated_val} categories set to 'real_time'")

    # 5. POS
    pos_config = env['pos.config'].search_count([])
    check_result("POS: Configured", pos_config > 0, f"{pos_config} POS configs found")

    # 6. HR (Likely Gaps)
    emp_count = env['hr.employee'].search_count([])
    check_result("HR: Employee Master Data", emp_count > 1, f"{emp_count} employees found (Need more than just Admin)")
    
    if 'hr.leave.type' in env:
        leave_count = env['hr.leave.type'].search_count([])
        check_result("HR: Leave Management", leave_count > 0, f"{leave_count} leave types found")
    else:
        check_result("HR: Leave Management", False, "Module 'hr_holidays' not installed")

    # 7. Sales & Distribution
    partner_orders = env['sale.order'].search_count([('partner_id', '!=', 1)]) 
    check_result("Sales: Partner Orders", partner_orders > 0, f"{partner_orders} Sales Orders found")

    # 8. Dashboards
    if 'spreadsheet.dashboard' in env:
        dashboard_count = env['spreadsheet.dashboard'].search_count([])
        check_result("Reporting: Dashboards", dashboard_count > 0, f"{dashboard_count} dashboards found")
    else:
        check_result("Reporting: Dashboards", False, "Module 'spreadsheet_dashboard' not installed")

print("\nAudit completed.")

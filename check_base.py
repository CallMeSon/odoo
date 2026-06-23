import sys

def setup():
    module = env['ir.module.module'].search([('name', '=', 'base_automation')])
    if module and module.state != 'installed':
        print("Installing base_automation...")
        module.button_immediate_install()
        env.cr.commit()
        print("base_automation installed. Please re-run the script.")
        return

    print("base_automation fields:", env['base.automation']._fields.keys())

setup()

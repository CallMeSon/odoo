# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

class QcInspection(models.Model):
    _inherit = "qc.inspection"

    def object_selection_values(self):
        res = super(QcInspection, self).object_selection_values()
        # Add Manufacturing Order (mrp.production) to selection values
        res.append(("mrp.production", "Manufacturing Order"))
        return res

# -*- coding: utf-8 -*-
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        # 1. Before confirming, update PO lines to use Mamma Roti's product sales price (list_price)
        # if the PO is from Mitra Demo (ID 2) to Mamma Roti (ID 1)
        for po in self:
            if po.company_id.id == 2 and po.partner_id.id == 1:
                _logger.info("Updating PO %s lines to use Mamma Roti product list prices before confirmation...", po.name)
                for line in po.order_line:
                    if line.product_id:
                        line.write({
                            'price_unit': line.product_id.list_price
                        })

        # 2. Call the original method to confirm the PO
        res = super(PurchaseOrder, self).button_confirm()

        # 3. Create the Sales Order in Mamma Roti
        for po in self:
            if po.company_id.id == 2 and po.partner_id.id == 1:
                _logger.info("Intercompany PO confirmed: %s in Mitra Demo. Creating SO in Mamma Roti...", po.name)
                
                # Check if SO already exists for this PO reference to avoid double creation
                existing_so = self.env['sale.order'].sudo().search([
                    ('client_order_ref', '=', po.name),
                    ('company_id', '=', 1)
                ], limit=1)
                
                if existing_so:
                    _logger.warning("Sales Order for %s already exists: %s. Skipping creation.", po.name, existing_so.name)
                    continue

                # Prepare the sale order lines using the updated PO prices
                sale_lines = []
                for line in po.order_line:
                    # Skip descriptive lines / notes
                    if not line.product_id:
                        continue

                    sale_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,  # Copy updated PO price (which is now product list_price)
                    }))

                if not sale_lines:
                    _logger.warning("No products found in PO %s. Sales Order will not be created.", po.name)
                    continue

                # Create the Sales Order in Mamma Roti context (Company ID 1)
                mamma_roti_company = self.env['res.company'].browse(1)
                
                so_vals = {
                    'partner_id': 32, # Mitra Demo Partner ID
                    'company_id': 1, # Mamma Roti Company ID
                    'client_order_ref': po.name, # PO reference
                    'origin': po.name,
                    'order_line': sale_lines,
                }
                
                sale_order = self.env['sale.order'].with_company(mamma_roti_company).sudo().create(so_vals)
                _logger.info("Successfully created Sales Order %s in Mamma Roti for Purchase Order %s", sale_order.name, po.name)

        return res

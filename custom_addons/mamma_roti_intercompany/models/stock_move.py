# -*- coding: utf-8 -*-
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        # Call the original method to validate the stock moves
        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        
        # After stock moves are done, we check if any products in Mamma Roti (Company ID 1) need replenishment
        # We only check for products that were in the completed moves
        products = res.mapped('product_id')
        
        if products:
            # We search for orderpoints associated with these products in Mamma Roti (Company ID 1)
            # which have trigger = 'auto'
            orderpoints = self.env['stock.warehouse.orderpoint'].sudo().search([
                ('product_id', 'in', products.ids),
                ('company_id', '=', 1),
                ('trigger', '=', 'auto')
            ])
            
            if orderpoints:
                # Force compute quantities to reflect the stock change immediately
                orderpoints._compute_qty()
                ops_to_replenish = orderpoints.filtered(lambda op: op.qty_to_order > 0)
                
                if ops_to_replenish:
                    _logger.info("Auto-replenishment triggered instantly for orderpoints: %s", ops_to_replenish.mapped('display_name'))
                    # We run replenish under Mamma Roti context (Company ID 1)
                    mamma_roti_company = self.env['res.company'].browse(1)
                    ops_to_replenish.with_company(mamma_roti_company).action_replenish()
                    
        return res

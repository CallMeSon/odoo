# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, time, timedelta
from odoo import api, fields, models

class MammaRotiKpiReport(models.Model):
    _name = 'mamma_roti.kpi.report'
    _description = 'Mamma Roti Daily KPI Report'
    _order = 'date desc'

    name = fields.Char(string='Day Name', required=True)
    date = fields.Date(string='Date', required=True, index=True)
    revenue = fields.Float(string='Daily Revenue', digits=(16, 2))
    transaction_count = fields.Integer(string='Transactions')
    atv = fields.Float(string='Average Transaction Value (ATV)', digits=(16, 2))
    stock_discrepancy_rate = fields.Float(string='Stock Discrepancy Rate (%)', digits=(5, 2))
    otd_rate = fields.Float(string='On-Time Delivery Rate (%)', digits=(5, 2))

    _sql_constraints = [
        ('date_unique', 'unique(date)', 'A report already exists for this date!'),
    ]

    @api.model
    def refresh_kpis_cron(self):
        """Called by Cron to update the last 30 days of KPIs"""
        self.refresh_kpis_for_days(days=30)

    @api.model
    def refresh_kpis_for_days(self, days=30):
        """Calculate and store KPIs for the specified number of past days up to today"""
        tz = pytz.timezone('Asia/Jakarta')
        today = datetime.now(tz).date()
        
        for i in range(days):
            target_date = today - timedelta(days=i)
            
            # Local start and end times
            local_start = tz.localize(datetime.combine(target_date, time.min))
            local_end = tz.localize(datetime.combine(target_date, time.max))
            
            # Convert to UTC for database queries
            utc_start = local_start.astimezone(pytz.utc).replace(tzinfo=None)
            utc_end = local_end.astimezone(pytz.utc).replace(tzinfo=None)
            
            # Calculate KPIs
            kpis = self._calculate_kpis_for_period(utc_start, utc_end)
            
            # Find or create record
            record = self.search([('date', '=', target_date)], limit=1)
            vals = {
                'name': target_date.strftime('%d %b %Y'),
                'date': target_date,
                'revenue': kpis['revenue'],
                'transaction_count': kpis['transaction_count'],
                'atv': kpis['atv'],
                'stock_discrepancy_rate': kpis['stock_discrepancy_rate'],
                'otd_rate': kpis['otd_rate'],
            }
            if record:
                record.write(vals)
            else:
                self.create(vals)
        return True

    def _calculate_kpis_for_period(self, utc_start, utc_end):
        # 1. Revenue & Transactions (KPI-1 & KPI-3) - Combining B2B (sale.order) and POS (pos.order)
        orders = self.env['sale.order'].search([
            ('state', 'in', ('sale', 'done')),
            ('date_order', '>=', utc_start),
            ('date_order', '<=', utc_end)
        ])
        b2b_revenue = sum(orders.mapped('amount_total'))
        b2b_count = len(orders)

        pos_orders = self.env['pos.order'].search([
            ('state', 'in', ('paid', 'done', 'invoiced')),
            ('date_order', '>=', utc_start),
            ('date_order', '<=', utc_end)
        ])
        pos_revenue = sum(pos_orders.mapped('amount_total'))
        pos_count = len(pos_orders)

        revenue = b2b_revenue + pos_revenue
        transaction_count = b2b_count + pos_count
        atv = revenue / transaction_count if transaction_count > 0 else 0.0

        # 2. Stock Discrepancy Rate (KPI-4)
        # Find all stock moves that are inventory adjustments (loss or gain)
        discrepancy_moves = self.env['stock.move'].search([
            ('state', '=', 'done'),
            ('date', '>=', utc_start),
            ('date', '<=', utc_end),
            '|',
            ('location_id.usage', '=', 'inventory'),
            ('location_dest_id.usage', '=', 'inventory')
        ])
        discrepancy_qty = sum(discrepancy_moves.mapped('product_qty'))
        
        # Get total on-hand stock in internal locations
        quants = self.env['stock.quant'].search([
            ('location_id.usage', '=', 'internal')
        ])
        total_onhand_qty = sum(quants.mapped('quantity'))
        
        # Calculate rate
        stock_discrepancy_rate = (discrepancy_qty / total_onhand_qty * 100) if total_onhand_qty > 0 else 0.0

        # 3. On-Time Delivery Rate (OTD) (KPI-5)
        # Deliveries validated in this period
        deliveries = self.env['stock.picking'].search([
            ('state', '=', 'done'),
            ('date_done', '>=', utc_start),
            ('date_done', '<=', utc_end),
            ('picking_type_id.code', '=', 'outgoing')
        ])
        
        total_deliveries = 0
        on_time_deliveries = 0
        for picking in deliveries:
            sale = picking.sale_id
            if sale and sale.date_order:
                total_deliveries += 1
                # Limit is H+2 (48 hours)
                limit = sale.date_order + timedelta(days=2)
                if picking.date_done <= limit:
                    on_time_deliveries += 1
                    
        otd_rate = (on_time_deliveries / total_deliveries * 100) if total_deliveries > 0 else 100.0

        return {
            'revenue': revenue,
            'transaction_count': transaction_count,
            'atv': atv,
            'stock_discrepancy_rate': stock_discrepancy_rate,
            'otd_rate': otd_rate,
        }

    def action_refresh_dashboard(self):
        """Button on dashboard to manually refresh KPIs"""
        self.refresh_kpis_for_days(days=30)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

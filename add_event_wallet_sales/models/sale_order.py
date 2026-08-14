# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Confirmar pedido pero evitar facturación automática si es pago con monedero"""
        res = super().action_confirm()
        for order in self:
            if order.payment_term_id and order.payment_term_id.name == 'Wallet':
                # Evitar creación de factura automática
                order.invoice_status = 'no'
        return res

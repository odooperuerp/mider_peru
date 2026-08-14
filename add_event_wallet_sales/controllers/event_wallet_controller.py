# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class EventWalletController(http.Controller):

    @http.route(['/event/<int:event_id>/wallet_register'], type='http', auth="user", website=True)
    def wallet_register(self, event_id, **kwargs):
        event = request.env['event.event'].browse(event_id)
        partner = request.env.user.partner_id

        # Ticket especial
        ticket = event.ticket_ids.filtered(lambda t: t.name == 'Entrada (Test Saldo)')
        if not ticket:
            return request.redirect('/event/%s' % event_id)

        amount = ticket.price

        # Validar saldo
        if partner.wallet_balance >= amount:
            partner.wallet_balance -= amount

            # Crear pedido de venta (sin factura)
            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': ticket.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': amount,
                })],
                'payment_term_id': request.env.ref('account.account_payment_term_immediate').id,
            })
            order.action_confirm()

            # Crear registro de evento
            request.env['event.registration'].sudo().create({
                'event_id': event.id,
                'partner_id': partner.id,
                'sale_order_id': order.id,
                'ticket_id': ticket.id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone,
            })

            return request.redirect('/event/%s/confirmation' % event.id)
        else:
            return request.redirect('/event/%s?error=saldo_insuficiente' % event_id)

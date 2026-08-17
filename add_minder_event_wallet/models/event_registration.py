# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            ticket_id = vals.get('event_ticket_id')
            if ticket_id:
                ticket = self.env['event.event.ticket'].browse(ticket_id)
                
                # 1. Verificamos si la entrada que están comprando es la de "Saldo"
                if ticket and 'saldo' in ticket.name.lower():
                    
                    # 2. Buscamos el boleto oculto "Descontar recarga" en el MISMO evento
                    ticket_recarga = self.env['event.event.ticket'].search([
                        ('event_id', '=', ticket.event_id.id),
                        ('name', 'ilike', 'descontar recarga')
                    ], limit=1)
                    
                    # Si existe el boleto oculto, leemos el precio en USD
                    if ticket_recarga:
                        # Usamos tu campo personalizado price_usd
                        costo_entrada = ticket_recarga.price_usd 
                        
                        if costo_entrada > 0:
                            # Obtenemos el ID del cliente o del usuario logueado
                            partner_id = vals.get('partner_id') or self.env.user.partner_id.id
                            
                            # 3. Buscamos el monedero del usuario
                            card = self.env['loyalty.card'].sudo().search([
                                ('partner_id', '=', partner_id),
                                ('program_id.program_type', '=', 'ewallet')
                            ], limit=1)
                            
                            # 4. Validamos que el monedero exista y tenga saldo suficiente
                            if not card or card.points < costo_entrada:
                                raise UserError(_("Saldo insuficiente en tu monedero electrónico. Necesitas $ %s y tienes $ %s.") % (costo_entrada, card.points if card else 0))
                            
                            # 5. Descontamos el saldo
                            card.sudo().write({
                                'points': card.points - costo_entrada
                            })
                            
        return super().create(vals_list)
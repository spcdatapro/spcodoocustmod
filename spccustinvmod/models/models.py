# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class spccustinvmod_account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    nuevo_numero = fields.Char(string="Nuevo número")

    @api.multi
    def write(self, vals):
        if 'nuevo_numero' in vals:
            if self.number != vals['nuevo_numero']:
                if vals['nuevo_numero']:
                    vals['number'] = vals['nuevo_numero']
                    vals['move_name'] = vals['nuevo_numero']
                    account_move = self.move_id
                    if account_move.id:
                        self._cr.execute('UPDATE account_move ' \
                                         'SET name=%s ' \
                                         'WHERE id = %s', (vals['nuevo_numero'], account_move.id,))


        return super(spccustinvmod_account_invoice, self).write(vals)
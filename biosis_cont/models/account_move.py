# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    cuo = fields.Char(String=u"CUO")
    ple_generado = fields.Boolean(string=u'Ple Generado', default=False)

    @api.multi
    def post(self):
        super(AccountMove, self).post()
        for move in self:
            secuencia = self.env['ir.sequence'].search([('code','=','biosis_cont.cuo')],limit=1)
            if not move.cuo:
                move.write({'cuo': secuencia.next_by_id()})
        return self


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    numero_asiento = fields.Char(String=u'Número Asiento')
    ple_generado = fields.Boolean(string=u'Ple Generado', default=False)

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    itf_account = fields.Many2one('account.account',string=u'Cuenta para ITF')
    itf_porcentaje = fields.Float(string=u'Porcentaje para ITF')
    comisiones_account = fields.Many2one('account.account',string=u'Cuenta para Comisiones')
    comisiones_porcentaje = fields.Float(string=u'Porcentaje para Comisiones')


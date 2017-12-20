# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    presupuesto_id = fields.Many2one('biosis.project.budget', string='Presupuesto')

    monto_presupuestado = fields.Float(string='Monto presupuestado', related='presupuesto_id.monto_presupuestado')
    monto_real = fields.Float(string='Monto real', related='presupuesto_id.monto_real')

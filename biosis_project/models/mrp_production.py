# coding=utf-8
import math

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    budget_line_id = fields.Many2one('biosis.project.budget.line', 'Presupuesto')
    stage_id = fields.Many2one('project.task.type', related='budget_line_id.stage_id', string=u'Orígen')
    tarea_id = fields.Many2one('project.task', related='budget_line_id.tarea_id', string=u'Piso')
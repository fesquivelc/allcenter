# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTaskBudget(models.Model):
    _inherit = 'project.task'

    monto_presupuestado = fields.Float(string='Monto presupuestado', readonly=True, compute='_compute_montos')
    monto_real = fields.Float(string='Monto real', readonly=True, compute='_compute_montos')
    # presupuesto_id = fields.Many2one('biosis.project.budget', related='project_id.presupuesto_id')
    presupuesto_conteo = fields.Integer(compute='_compute_ppto_conteo', store=True)
    detalle_ppto_real = fields.One2many('biosis.project.budget.line', 'tarea_id', string='Detalle inicial',
                                        domain=[('tipo', '=', 'real')])
    detalle_ppto_inicial = fields.One2many('biosis.project.budget.line', 'tarea_id', string='Detalle real',
                                           domain=[('tipo', '=', 'presupuestado')])

    @api.multi
    def _compute_ppto_conteo(self):
        for task in self:
            conteo = self.env['biosis.project.budget.line'].search_count([('tarea_id', '=', task.id)])
            task.presupuesto_conteo = conteo

    @api.multi
    def _compute_montos(self):
        for task in self:
            task.monto_presupuestado = sum([linea.subtotal for linea in task.detalle_ppto_inicial])
            task.monto_real = sum([linea.subtotal for linea in task.detalle_ppto_real])

    @api.multi
    def fabricar(self):
        for task in self:
            for linea in task.detalle_ppto_real:
                if linea.ldm_id:
                    values = {
                        u'bom_id': linea.ldm_id.id,
                        u'company_id': 1,
                        u'date_planned_finished': fields.Datetime.now(),
                        u'date_planned_start': fields.Datetime.now(),
                        u'location_src_id': linea.presupuesto_id.ubicacion_origen_id.id,
                        u'location_dest_id': linea.presupuesto_id.ubicacion_destino_id.id,
                        u'message_follower_ids': False,
                        u'message_ids': False,
                        u'move_finished_ids': [],
                        u'move_raw_ids': [],
                        u'origin': False,
                        u'picking_type_id': linea.presupuesto_id.albaran_id.id,
                        u'state': u'confirmed',
                        u'product_id': linea.ldm_id.product_tmpl_id.id,
                        u'product_qty': linea.cantidad,
                        u'product_tmpl_id': linea.ldm_id.product_tmpl_id.id,
                        u'product_uom_id': linea.ldm_product_uom_id.id,
                        u'user_id': 1,

                        u'budget_line_id': linea.id
                    }
                    self.env['mrp.production'].create(values)


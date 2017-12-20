# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectBudget(models.Model):
    _inherit = ['mail.thread']
    _name = 'biosis.project.budget'

    proyecto_nombre = fields.Char('Nombre del proyecto', required=True)
    # proyecto_id = fields.Many2one('project.project', string='Proyecto')
    ubicacion_origen_id = fields.Many2one('stock.location', string=u'Ubicación de orígen')
    ubicacion_destino_id = fields.Many2one('stock.location', string=u'Ubicación destino')
    albaran_id = fields.Many2one('stock.picking.type', string=u'Tipo de albarán')

    detalle_presupuestado_ids = fields.One2many('biosis.project.budget.line', 'presupuesto_id',
                                                string='Detalle Presupuestado', required=True,
                                                domain=[('tipo', '=', 'presupuestado')])
    detalle_real_ids = fields.One2many('biosis.project.budget.line', 'presupuesto_id', string='Detalle real',
                                       domain=[('tipo', '=', 'real')])
    monto_presupuestado = fields.Float(string='Monto presupuestado', storage=True, compute='_compute_monto')
    monto_real = fields.Float(string='Monto real', storage=False, compute='_compute_monto')
    proyecto_generado = fields.Boolean(default=False)
    proyecto_ids = fields.One2many('project.project', 'presupuesto_id')

    @api.multi
    def name_get(self):
        result = []
        nombre = u'Presupuesto de %s'
        for presupuesto in self:
            l_name = presupuesto.proyecto_nombre
            result.append((presupuesto.id, nombre % l_name))
        return result

    @api.multi
    @api.depends('detalle_presupuestado_ids')
    def _compute_monto(self):
        for presupuesto in self:
            presupuesto.monto_presupuestado = sum(
                [linea.subtotal for linea in presupuesto.detalle_presupuestado_ids])
            presupuesto.monto_real = sum(
                [linea.subtotal for linea in presupuesto.detalle_real_ids])

    @api.multi
    def obtener_presupuesto(self):
        for presupuesto in self:
            return sum([linea.subtotal for linea in presupuesto.budget_lines_id])

    @api.multi
    def crear_proyecto(self):
        """
        Este método permite crear un proyecto con los parámetros especificados.
        Así como también permite copiar este presupuesto para que sirva como presupuesto REAL,
        de esa manera controlar mejor lo planificado y lo no planificado
        :return: None
        """
        for presupuesto in self:
            # Generamos todas las tareas que se van a relacionar con el proyecto
            if not presupuesto.proyecto_generado:

                # presupuesto.write({'proyecto_id': proyecto.id})

                # presupuesto_real = presupuesto.copy()
                # real_write = {
                #     'tipo': 'real',
                #     'budget_lines_id': []
                # }
                detalle_real_ids = []
                proy_vals = {
                    'name': presupuesto.proyecto_nombre,
                    'use_tasks': True,
                    'presupuesto_id': presupuesto.id,
                }
                proyecto = self.env['project.project'].create(proy_vals)
                secuencia = 1
                for linea in presupuesto.detalle_presupuestado_ids:
                    tarea_vals = {'stage_id': linea.stage_id.id, 'sequence': secuencia, 'project_id': proyecto.id}
                    stage_vals = {'project_ids': [proyecto.id, ]}

                    linea.tarea_id.write(tarea_vals)
                    linea.stage_id.write(stage_vals)
                    # linea.write({'tipo': 'presupuestada'})
                    linea2 = linea.copy()
                    linea2.write({'tipo': 'real'})
                    # linea2.write({'tipo': 'real'})
                    detalle_real_ids.append(linea2)

                    secuencia += 1
                presupuesto.write({'proyecto_generado': True, 'detalle_real_ids': detalle_real_ids})
                warning = {
                    'title': "Proyecto creado",
                    'message': "Se ha creado un proyecto con el presupuesto generado"
                }
            else:
                # Mensaje de error
                warning = {
                    'title': _("¡Proyecto existente!"),
                    'message': _("Ya existe un proyecto a partir de este presupuesto")
                }
            return {'warning': warning}

    @api.multi
    def fabricar(self):
        for presupuesto in self:
            for linea in presupuesto.budget_lines_id:
                linea.fabricar()

    @api.model
    def create(self, vals):
        vals['tipo'] = 'inicial'
        vals['proyecto_generado'] = False
        # for linea in vals['detalle_presupuestado_ids']:
        #     linea['tipo'] = 'presupuestado'
        # vals['monto_presupuestado'] = self.obtener_presupuesto()
        return super(ProjectBudget, self).create(vals)


TIPO_LINEA = (
    ('presupuestado', 'Presupuestado'),
    ('real', 'Real')
)


class ProjectBudgetLine(models.Model):
    _name = 'biosis.project.budget.line'

    presupuesto_id = fields.Many2one('biosis.project.budget')
    tarea_id = fields.Many2one('project.task', string='Dpto')
    stage_id = fields.Many2one('project.task.type', string='Piso')
    producto_id = fields.Many2one('product.product', required=True)
    producto_type = fields.Selection(related='producto_id.type')
    producto_bom_count = fields.Integer(related='producto_id.bom_count')
    producto_precio = fields.Float(string='Precio de venta', store=True, related='producto_id.list_price')
    ldm_id = fields.Many2one('mrp.bom', string='Producto a fabricar')
    ldm_product_uom_id = fields.Many2one('product.uom', related='ldm_id.product_uom_id')
    costo = fields.Float(string='Costo', store=True, compute='_compute_costo')
    cantidad = fields.Float(string='Cantidad', required=True)
    subtotal = fields.Float(string='Subtotal', store=True, compute='_compute_subtotal')
    tipo = fields.Selection(TIPO_LINEA, string='Tipo de detalle', default='presupuestado')
    fabricado = fields.Boolean(default=True)

    @api.multi
    @api.depends('producto_id')
    def _compute_costo(self):
        for linea in self:
            total_unidad = linea.producto_id.standard_price
            if linea.producto_bom_count > 0:
                if linea.ldm_id:
                    total_unidad = sum(
                        [bom_line.product_id.standard_price * bom_line.product_qty for bom_line in
                         linea.ldm_id.bom_line_ids])
            linea.costo = total_unidad

    @api.multi
    @api.depends('ldm_id', 'cantidad')
    def _compute_subtotal(self):
        for linea in self:
            subtotal = 0.0
            if linea.cantidad and linea.cantidad > 0.0 and linea.costo > 0.0:
                subtotal = linea.costo * linea.cantidad
                # cantidad = linea.cantidad_fabricar / linea.ldm_id.product_qty
                # total_unidad = sum(
                #     [bom_line.product_id.standard_price * bom_line.product_qty for bom_line in
                #      linea.ldm_id.bom_line_ids])
                # linea.subtotal = cantidad * total_unidad
            linea.subtotal = subtotal

    @api.multi
    def fabricar(self):
        for linea in self:
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
                u'product_qty': linea.cantidad_fabricar,
                u'product_tmpl_id': linea.ldm_id.product_tmpl_id.id,
                u'product_uom_id': linea.ldm_product_uom_id.id,
                u'user_id': 1,

                u'budge_line_id': linea.id
            }
            self.env['mrp.production'].create(values)

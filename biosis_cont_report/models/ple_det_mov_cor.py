# -*- coding: utf-8 -*-
import datetime
import re
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PleDetalleMovimientoCorriente(models.Model):
    _name = 'account.ple.detalle.movimiento.corriente'
    _description = u'PLE para DETALLE DE LOS MOVIMIENTOS DE LA CUENTA CORRIENTE'

    periodo_1 = fields.Char(string=u'Periodo', required=True)
    cuo_2 = fields.Char(string=u'Codigo Único de Operación', required=True)
    move_cuo_3 = fields.Char(string=u'CUO-Asiento Contable', required=True)
    codigo_ef_4 = fields.Char(string=u'Código de la entidad financiera', required=True)
    codigo_cb_contri_5 = fields.Char(string=u'Código Cuenta Bancaria del Contribuyente')
    fecha_o_6 = fields.Char(string=u'Fecha de la Operación', required=True)
    medio_pago_7 = fields.Char(string=u'Medio de pago utilizado en la operación bancaria')
    descripcion_o_b_8 = fields.Char(string=u'Descripción de la operación bancaria')
    tipo_doc_gb_9 = fields.Char(string=u'Tipo documento Girador o Beneficiario', default=u'')
    numero_doc_gb_10 = fields.Char(string=u'Número documento Girador o Beneficiario', default=u'')
    ap_d_rz_gb_11 = fields.Char(string=u'Número documento Girador o Beneficiario', default=u'')
    nro_transc_bancaria_12 = fields.Char(string=u'Número de transacción bancaria, número de documento sustentatorio '
                                                u'o número de control interno de la operación bancaria', default=u'')
    mov_debe_13 = fields.Char(string=u'Movimiento del Debe', required=True)
    mov_haber_14 = fields.Char(string=u'Movimiento del Haber', required=True)
    estado_15 = fields.Char(string=u'Estado', required=True)

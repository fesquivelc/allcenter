# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api


class PleMayor(models.Model):
    _name = 'account.ple.mayor'
    _description = 'PLE para Mayor'

    periodo_1 = fields.Char(string=u'Periodo',required=True)
    cuo_2 = fields.Char(string=u'Codigo Único de Operación',required=True)
    move_cuo_3 = fields.Char(string=u'CUO-Asiento Contable',required=True)
    cuenta_cont_4 = fields.Char(string=u'Cuenta Contable',required=True)
    cunio_uea_un_up_5 = fields.Char(string=u'Codigo Unidad de Operación & Unidad Economica Adm & Unidad de Negocio',default=u'')
    ccc_cu_ci_6 = fields.Char(string=u'Código Centro de Costos & Centro Utilidades % Centro de Inversión', default=u'')
    codigo_moneda_7 = fields.Char(string=u'Código Moneda', default=u'0.000')
    tipo_doc_pro_8 = fields.Char(string=u'Tipo documento Emisor', default=u'')
    numero_doc_pro_9 = fields.Char(string=u'Número documento Emisor', default=u'')
    tipo_cpbt_10 = fields.Char(string=u'Tipo Comprobante', required=True)
    serie_cpbt_11 = fields.Char(string=u'Serie del Comprobante', default=u'-')
    numero_cpbt_12 = fields.Char(string=u'Número Comprobante', required=True)
    fecha_c_13 = fields.Char(string=u'Fecha Contable',required=True)
    fecha_v_14 = fields.Char(string=u'Fecha Vencimiento',default=u'01/01/0001')
    fecha_e_15 = fields.Char(string=u'Fecha Emisión', required=True)
    glosa_16 = fields.Char(string=u'Descripcion de la naturaleza de la operación registrada',required=True)
    glosa_referencial_17 = fields.Char(string=u'Descripción referencial',default=u'')
    mov_debe_18 = fields.Char(string=u'Movimiento del Debe', required=True)
    mov_haber_19 = fields.Char(string=u'Movimiento del Haber', required=True)
    dato_estructurado_20 = fields.Char(string=u'Dato Estructurado')
    estado_21 = fields.Char(string=u'Estado', required=True)

    @api.multi
    def get_ple_line(self):
        return self.periodo_1+'|'+self.cuo_2+'|'+self.move_cuo_3+'|'+self.cuenta_cont_4+'|'+self.cunio_uea_un_up_5+'|'\
               +self.ccc_cu_ci_6+'|'+self.codigo_moneda_7+'|'+self.tipo_doc_pro_8+'|'+self.numero_doc_pro_9+'|'\
               +self.tipo_cpbt_10+'|'+self.serie_cpbt_11+'|'+self.numero_cpbt_12+'|'+self.fecha_c_13+'|'\
               +self.fecha_v_14+'|'+self.fecha_e_15+'|'+self.glosa_16+'|'+self.glosa_referencial_17+'|'\
               +self.mov_debe_18+'|'+self.mov_haber_19+'|'+self.dato_estructurado_20+'|'+self.estado_21+'|'+'\n'

    @api.multi
    def get_ple_mayor(self, fecha_reporte, fecha_inicio, fecha_fin):
        ple_mayor_res = ''
        move_nuevos = self.env['account.move.line'].search([
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
            ('move_id.state', '!=', 'draft'),
            ('ple_generado', '=', False)
        ]).sorted(key=lambda r: int(r.account_id.code))

        move_old = self.env['account.move.line'].search([
            ('date', '>=', fecha_inicio),
            ('date', '<=', fecha_fin),
            ('move_id.state', '!=', 'draft'),
            ('ple_generado', '=', True)
        ]).sorted(key=lambda r: int(r.account_id.code))

        if len(move_nuevos) > 0:
            ple_nuevos = self.create_ple_items_mayor(move_nuevos, fecha_reporte, fecha_inicio, fecha_fin)
            ple_mayor_res = ple_mayor_res + ple_nuevos

        if len(move_old) > 0:
            ple_modificados = self.update_ple_items_mayor(move_old, fecha_reporte, fecha_inicio, fecha_fin)
            ple_mayor_res = ple_mayor_res + ple_modificados

        return ple_mayor_res

    @api.multi
    def create_ple_items_mayor(self, move_nuevos, fecha_reporte, fecha_inicio, fecha_fin):
        ple_items = ''
        ple_diario = self.env['account.ple.mayor']
        i = 1
        for move_line in move_nuevos:
            if datetime.datetime.strptime(move_line.date,
                                          '%Y-%m-%d').date() >= fecha_inicio and datetime.datetime.strptime(
                    move_line.date, '%Y-%m-%d').date() <= fecha_fin:
                ple_item_estado_21 = u'1'
            elif datetime.datetime.strptime(move_line.date, '%Y-%m-%d').date() <= fecha_inicio:
                ple_item_estado_21 = u'8'
            ##for move_line in move.line_ids:
            codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
            ple_item_vals = {
                'periodo_1': fecha_reporte,
                'cuo_2': move_line.move_id.cuo,
                'move_cuo_3': 'M' + str(i),
                'cuenta_cont_4': move_line.account_id.code,
                'cunio_uea_un_up_5': '2',  # SE APLICARA CUANDO ESTE COMPLETADO UNIDAD DE NEGOCIOS
                'ccc_cu_ci_6': '2',  # SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
                'codigo_moneda_7': 'PEN',
                'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
                'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
                'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code if move_line.invoice_id.tipo_documento.code else '00',
                'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
                'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
                'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime('%d/%m/%Y'),
                'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                'fecha_e_15': '01/01/0001',
                'glosa_16': move_line.name,  # move_line.invoice_id.name if move_line.invoice_id.name else '',
                'glosa_referencial_17': '',
                'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
                'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
                'dato_estructurado_20': codigo_libro + '&' + fecha_reporte + '&' + move_line.move_id.cuo + '&' + 'M' + str(
                    i),
                'estado_21': ple_item_estado_21
            }
            move_line.write({'numero_asiento': 'M' + str(i)})
            move_line.write({'ple_generado': True})
            ple_item = ple_diario.create(ple_item_vals)
            ple_items = ple_items + ple_item.get_ple_line()
            i = i + 1
            # despues de proceso
            move_line.move_id.write({'ple_generado': True})

        return ple_items

    @api.multi
    def update_ple_items_mayor(self, move_olds, fecha_reporte, fecha_inicio, fecha_fin):
        ple_items = ''
        for move_line in move_olds:
            ple_actual = self.env['account.ple.diario'].search([
                ('cuo_2', '=', move_line.move_id.cuo),
                ('move_cuo_3', '=', move_line.numero_asiento)
            ], limit=1)
            if ple_actual.write_date < move_line.write_date:
                codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
                ple_item_vals = {
                    'periodo_1': ple_actual.periodo_1,
                    'cuo_2': move_line.move_id.cuo,
                    'move_cuo_3': 'M' + move_line.move_id.cuo,
                    'cuenta_cont_4': move_line.account_id.code,
                    'cunio_uea_un_up_5': '2',  # SE APLICARA CUANDO ESTE COMPLETADO UNIDAD DE NEGOCIOS
                    'ccc_cu_ci_6': '2',  # SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
                    'codigo_moneda_7': 'PEN',
                    'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
                    'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
                    'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code,
                    'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
                    'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
                    'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime(
                        '%d/%m/%Y'),
                    'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'fecha_e_15': '01/01/0001',
                    'glosa_16': move_line.name,  # move_line.invoice_id.name if move_line.invoice_id.name else '',
                    'glosa_referencial_17': '',
                    'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
                    'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
                    'dato_estructurado_20': codigo_libro + '&' + fecha_reporte + '&' + move_line.move_id.cuo + '&' + move_line.numero_asiento,
                    'estado_21': '9'
                }
                ple_actual.write(ple_item_vals)
                # despues de proceso
                ple_items = ple_items + ple_actual.get_ple_line()
            else:
                ple_items = ple_items + ple_actual.get_ple_line()
        return ple_items
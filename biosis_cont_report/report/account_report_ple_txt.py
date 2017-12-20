# -*- coding: utf-8 -*-
import datetime
import calendar
from odoo import api, models

TIPO_REPORTE_SUNAT = {
    '010100':u'010100',
    '010200':u'010200',
    '030100':u'030100',
    '030200':u'030200',
    '030300':u'030300',
    '030400':u'030400',
    '030500':u'030500',
    '030600':u'030600',
    '030700':u'030700',
    '030800':u'030800',
    '030900':u'030900',
    '031100':u'031100',
    '031200':u'031200',
    '031300':u'031300',
    '031400':u'031400',
    '031500':u'031500',
    '031601':u'031601',
    '031602':u'031602',
    '031700':u'031700',
    '031800':u'031800',
    '031900':u'031900',
    '032000':u'032000',
    '032300':u'032300',
    '032400':u'032400',
    '032500':u'032500',
    '040100':u'040100',
    '050100':u'050100',
    '050300':u'050300',
    '050200':u'050200',
    '050400':u'050400',
    '060100':u'060100',
    '070100':u'070100',
    '070300':u'070300',
    '070400':u'070400',
    '080100':u'080100',
    '080200':u'080200',
    '080300':u'080300',
    '090100':u'090100',
    '090200':u'090200',
    '100100':u'100100',
    '100200':u'100200',
    '100300':u'100300',
    '100400':u'100400',
    '120100':u'120100',
    '130100':u'130100',
    '140100':u'140100',
    '140200':u'140200'
}

class BiosisContReportPLE(models.AbstractModel):
    _name = 'report.biosis_cont_report.report_ple'
    def generate_txt_report(self,mes_int,year_int,tipo_r):
        #Obtener fechas de busqueda
        year = str(year_int)
        if mes_int != 'False':
            mes = str(mes_int)
        else:
            mes = '01'
        date1 = year+'-'+mes+'-'+'01'
        fecha_inicio = datetime.datetime.strptime(date1,"%Y-%m-%d").date()

        if mes_int != 'False':
            date2 = "%s-%s-%s" % (fecha_inicio.year,fecha_inicio.month,calendar.monthrange(fecha_inicio.year,fecha_inicio.month)[1])
        else:
            date2 = "%s-%s-%s" % (fecha_inicio.year, 12, calendar.monthrange(fecha_inicio.year, fecha_inicio.month)[1])
        fecha_fin = datetime.datetime.strptime(date2,"%Y-%m-%d").date()

        company_name = self.env.user.company_id.partner_id.vat
        fecha_reporte = year+('0'+mes if len(mes)==1 else mes)+'00'

        if tipo_r == TIPO_REPORTE_SUNAT['010100']:
            nombre_ple = u'LE' + company_name + year + ('0' + mes if len(mes) == 1 else mes) + u'00' + u'010100' + u'00' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.detalle.movimiento.efectivo'].get_ple(fecha_reporte, fecha_inicio,fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['080100']:
            nombre_ple = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'080100' + u'00' + u'1111'
            nombre_ple_v = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'080200' + u'00' + u'1011'
            #return nombre_ple, nombre_ple_v, self.get_ple_compras(fecha_reporte,fecha_inicio,fecha_fin)
            return nombre_ple, nombre_ple_v, self.env['account.ple.compras'].get_ple_compras(fecha_reporte, fecha_inicio, fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['140100']:
            nombre_ple = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'140100' + u'00' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.ventas'].get_ple_ventas(fecha_reporte,fecha_inicio,fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['030100']:
            nombre_ple = u'LE' + company_name + year + u'12' + u'31' + u'030100' + u'01' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.estado.situacion.finaciera'].get_ple(fecha_reporte, fecha_inicio,fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['031700']:
            #nombre_ple = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'031700' + u'01' + u'1111'
            nombre_ple = u'LE' + company_name + year + u'12' + u'31' + u'031700' + u'01' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.balancecomprobacion'].get_ple_bc(fecha_reporte, fecha_inicio, fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['050100']:
            nombre_ple = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'050100' + u'00' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.diario'].get_ple_diario(fecha_reporte,fecha_inicio,fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['050300']:
            nombre_ple = u'LE' + company_name + year + ('0' + mes if len(mes) == 1 else mes) + u'00' + u'050300' + u'00' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.diario.detalle'].get_ple_diario_detalle(fecha_reporte, fecha_inicio, fecha_fin)
        elif tipo_r == TIPO_REPORTE_SUNAT['060100']:
            nombre_ple = u'LE' + company_name + year + ('0'+mes if len(mes)==1 else mes) + u'00' + u'060100' + u'00' + u'1111'
            nombre_ple_v = False
            return nombre_ple, nombre_ple_v, self.env['account.ple.mayor'].get_ple_mayor(fecha_reporte,fecha_inicio,fecha_fin)


    # def get_ple_compras(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_compras_res = ''
    #     #ED sin ple
    #     invoices_nuevos = self.env['account.invoice'].search([
    #         ('date_due','>=',fecha_inicio),
    #         ('date_due','<=',fecha_fin),
    #         ('type','=','in_invoice'),
    #         ('state','!=','draft'),
    #         ('tipo_documento.code','in',['01','03','07','08']),
    #         ('ple_generado','=',False)
    #     ]).sorted(key= lambda r: r.date_due)
    #
    #     invoices_old = self.env['account.invoice'].search([
    #         ('date_due','>=',fecha_inicio),
    #         ('date_due','<=',fecha_fin),
    #         ('type','=','in_invoice'),
    #         ('state', '!=', 'draft'),
    #         ('tipo_documento.code','in',['01','03','07','08']),
    #         ('ple_generado','=',True)
    #     ]).sorted(key= lambda r: r.date_due)
    #
    #     if len(invoices_nuevos) > 0:
    #         ple_nuevos = self.create_ple_items_compras(invoices_nuevos, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_compras_res = ple_compras_res + ple_nuevos
    #
    #     if len(invoices_old) > 0:
    #         ple_modificados = self.update_ple_items_compras(invoices_old)
    #         ple_compras_res = ple_compras_res + ple_modificados
    #
    #     return ple_compras_res
    #
    # def get_ple_ventas(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_ventas_res = ''
    #     invoices_nuevos = self.env['account.invoice'].search([
    #         ('date_due', '>=', fecha_inicio),
    #         ('date_due', '<=', fecha_fin),
    #         ('type', '=', 'out_invoice'),
    #         ('state', '!=', 'draft'),
    #         ('tipo_documento.code', 'in', ['01', '03', '07', '08']),
    #         ('ple_generado', '=', False)
    #     ]).sorted(key= lambda r: r.date_due)
    #
    #     invoices_old = self.env['account.invoice'].search([
    #         ('date_due', '>=', fecha_inicio),
    #         ('date_due', '<=', fecha_fin),
    #         ('type', '=', 'out_invoice'),
    #         ('state', '!=', 'draft'),
    #         ('tipo_documento.code', 'in', ['01', '03', '07', '08']),
    #         ('ple_generado', '=', True)
    #     ]).sorted(key= lambda r: r.date_due)
    #
    #     if len(invoices_nuevos) > 0:
    #         ple_nuevos = self.create_ple_items_ventas(invoices_nuevos, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_ventas_res = ple_ventas_res + ple_nuevos
    #
    #     if len(invoices_old) > 0:
    #         ple_modificados = self.update_ple_items_ventas(invoices_old, fecha_inicio, fecha_fin)
    #         ple_ventas_res = ple_ventas_res + ple_modificados
    #
    #     return ple_ventas_res
    #
    # def get_ple_diario(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_diario_res = ''
    #     move_nuevos = self.env['account.move'].search([
    #         ('date', '>=', fecha_inicio),
    #         ('date', '<=', fecha_fin),
    #         ('state', '!=', 'draft'),
    #         ('ple_generado', '=', False)
    #     ]).sorted(key=lambda r: int(r.cuo))
    #
    #     move_old = self.env['account.move'].search([
    #         ('date', '>=', fecha_inicio),
    #         ('date', '<=', fecha_fin),
    #         ('state', '!=', 'draft'),
    #         ('ple_generado', '=', True)
    #     ]).sorted(key=lambda r: int(r.cuo))
    #
    #     if len(move_nuevos) > 0:
    #         ple_nuevos = self.create_ple_items_diario(move_nuevos, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_diario_res = ple_diario_res + ple_nuevos
    #
    #     if len(move_old) > 0:
    #         ple_modificados = self.update_ple_items_diario(move_old, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_diario_res = ple_diario_res + ple_modificados
    #
    #     return ple_diario_res
    #
    # def get_ple_diario_detalle(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_diario_detalle_res = ''
    #     diario_detalle_list = []
    #     cuentas_list_move = []  #Lista cuentas de moves
    #     cuentas_list_dd = []    #Lista cuentas de ple diario detalle
    #     cuentas_list_new = []
    #
    #     move_list = self.env['account.move.line'].search([
    #         ('date', '>=', fecha_inicio),
    #         ('date', '<=', fecha_fin),
    #     ])
    #
    #     diario_detalle_list = self.env['account.ple.diario.detalle'].search([
    #         ('periodo_1', '=', fecha_reporte)
    #     ])
    #
    #     #Lista de cuentas moves lines
    #     if move_list:
    #         for line in move_list:
    #             if not(line.account_id.code in cuentas_list_move):
    #                 cuentas_list_move.append(line.account_id.code)
    #
    #     # Lista de cuentas diario detalle
    #     if diario_detalle_list:
    #         for line in diario_detalle_list:
    #             if not (line.cuenta_cont_2 in cuentas_list_dd):
    #                 cuentas_list_dd.append(line.cuenta_cont_2)
    #
    #
    #     # Verificamos si existen nuevas cuentas
    #     if len(cuentas_list_move) > 0 and len(cuentas_list_dd) > 0:
    #         for cuenta in cuentas_list_move:
    #             if not (cuenta in cuentas_list_dd):
    #                 cuentas_list_new.append(cuenta)
    #
    #     if len(cuentas_list_move) > 0 and len(cuentas_list_dd) == 0:
    #         cuentas_list_new = cuentas_list_move
    #
    #     if len(cuentas_list_new)>0:
    #         """
    #            Pasos para agregar lineas Diario Detalle al res
    #         """
    #         ple_nuevos = self.create_ple_items_diario_detalle(cuentas_list_new,fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_diario_detalle_res = ple_diario_detalle_res + ple_nuevos
    #
    #     if len(diario_detalle_list)>0:
    #         """
    #            Pasos para crear lineas Diario Detalle con cuentas_list_new
    #         """
    #         ple_old = self.update_ple_items_diario_detalle(diario_detalle_list,fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_diario_detalle_res = ple_diario_detalle_res + ple_old
    #
    #     return ple_diario_detalle_res
    #
    # def get_ple_mayor(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_mayor_res = ''
    #     move_nuevos = self.env['account.move.line'].search([
    #         ('date', '>=', fecha_inicio),
    #         ('date', '<=', fecha_fin),
    #         ('move_id.state','!=','draft'),
    #         ('ple_generado', '=', False)
    #     ]).sorted(key=lambda r: int(r.account_id.code))
    #
    #     move_old = self.env['account.move.line'].search([
    #         ('date', '>=', fecha_inicio),
    #         ('date', '<=', fecha_fin),
    #         ('move_id.state', '!=', 'draft'),
    #         ('ple_generado', '=', True)
    #     ]).sorted(key=lambda r: int(r.account_id.code))
    #
    #     if len(move_nuevos) > 0:
    #         ple_nuevos = self.create_ple_items_mayor(move_nuevos, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_mayor_res = ple_mayor_res + ple_nuevos
    #
    #     if len(move_old) > 0:
    #         ple_modificados = self.update_ple_items_mayor(move_old, fecha_reporte, fecha_inicio, fecha_fin)
    #         ple_mayor_res = ple_mayor_res + ple_modificados
    #
    #     return ple_mayor_res
    #
    # def get_ple_bc(self, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_bc_res = ''
    #
    #
    #
    # """Funcion CREATE COMPRAS PLE
    # """
    # def create_ple_items_compras(self, invoices, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_compras = self.env['account.ple.compras']
    #     for invoice in invoices:
    #         print invoice.write_date
    #         # Buscar item ple previo
    #         ple_item_prev = self.env['account.ple.compras'].search([
    #             ('cuo_2', '=', invoice.cuo_invoice)
    #         ], limit=1)
    #         if ple_item_prev:
    #             print ple_item_prev
    #         """
    #             TRABAJAR CON LAS FECHAS MAXIMAS PARA ATRASO QUE ESTAN DISPONIBLES EN SUNAT
    #         """
    #         if datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').date() >= fecha_inicio and datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').date()  <= fecha_fin:
    #             ple_item_estado_41 = u'1'
    #         elif datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').date() <= fecha_inicio:
    #             ple_item_estado_41 = u'6'
    #
    #         ple_item_vals = {
    #             'periodo_1': fecha_reporte,
    #             'cuo_2': invoice.cuo_invoice,
    #             'move_cuo_3': 'M' + invoice.cuo_invoice,
    #             'fecha_e_4': datetime.datetime.strptime(invoice.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #             'fecha_v_5': datetime.datetime.strptime(invoice.date_due, '%Y-%m-%d').strftime(
    #                 '%d/%m/%Y') if invoice.date_due else '01/01/0001',
    #             'tipo_cpbt_6': invoice.tipo_documento.code,
    #             'serie_cpbt_7': invoice.numero.split('-')[0],
    #             # ple_item.anio_emision_dua_dsi_8 -> no implementado
    #             'numero_cpbt_9': invoice.numero.split('-')[1],
    #             # ple_item.importe_total_diario_10 - no implementado
    #             'tipo_doc_pro_11': invoice.partner_id.catalog_06_id.code,
    #             'numero_doc_pro_12': invoice.partner_id.vat,
    #             'razon_social_pro_13': invoice.partner_id.registration_name if invoice.partner_id.registration_name else invoice.partner_id.name,
    #             'base_adq_gravadas_14': str(invoice.amount_untaxed),
    #             'monto_igv_1_15': str(invoice.amount_tax),
    #             # ple_item.base_adq_no_gravadas_16 - por consultar
    #             # ple_item.monto_igv_2_17
    #             # ple_item.base_adq_sin_df_18
    #             # ple_item.monto_igv_3_19
    #             # ple_item.valor_adq_no_gravadas_20
    #             # ple_item.monto_isc_21
    #             # ple_item.otros_conceptos_22
    #             'importe_total_23': str(invoice.amount_total_signed),
    #             'codigo_moneda_24': invoice.currency_id.name,
    #             'tipo_cambio_25': '1.000',  # agregar campo a invoice str(invoice.valor_tipo_cambio)
    #             'fecha_emision_doc_mod_26': datetime.datetime.strptime(invoice.invoice_id.date_due,
    #                                                                    '%Y-%m-%d').strftime('%d/%m/%Y') if (
    #             invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else '01/01/0001',
    #             'tipo_cpbt_mod_27': invoice.invoice_id.tipo_documento.code if (
    #             invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'00',
    #             'serie_cpbt_mod_28': invoice.invoice_id.numero.split('-')[0] if (
    #             invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #             # ple_item.codigo_dep_aduanera_29
    #             'numero_cpbt_mod_30': invoice.invoice_id.numero.split('-')[1] if (
    #             invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #             'fecha_emision_cdd_31': datetime.datetime.strptime(invoice.fecha_emision_detraccion,'%Y-%m-%d').strftime('%d/%m/%Y') if invoice.fecha_emision_detraccion else u'01/01/0001',
    #             'numero_cdd_32' : invoice.numero_detraccion if invoice.numero_detraccion else u'0',
    #             # ple_item.marca_cpbt_33
    #             # ple_item.clasif_bienes_34
    #             # ple_item.identif_contrato_s_i_35
    #             # ple_item.error_tipo1_36
    #             # ple_item.error_tipo2_37
    #             # ple_item.error_tipo3_38
    #             # ple_item.error_tipo4_39
    #             # ple_item.indicador_cpbt_40
    #             'estado_41': ple_item_estado_41
    #         }
    #         ple_item = ple_compras.create(ple_item_vals)
    #         invoice.write({'ple_generado':True})
    #         # despues de proceso
    #         ple_items = ple_items + ple_item.get_ple_line()
    #     return ple_items
    #
    # """Funcion FIND, UPDATE COMPRAS PLE
    # """
    # def update_ple_items_compras(self, invoices):
    #     ple_items = ''
    #     for invoice in invoices:
    #         ple_actual = self.env['account.ple.compras'].search([
    #             ('cuo_2', '=', invoice.cuo_invoice)
    #         ], limit=1)
    #
    #         if ple_actual.write_date < invoice.write_date:
    #             ple_item_vals = {
    #                 'periodo_1': ple_actual.periodo_1,
    #                 'cuo_2': invoice.cuo_invoice,
    #                 'move_cuo_3': 'M' + invoice.cuo_invoice,
    #                 'fecha_e_4': datetime.datetime.strptime(invoice.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                 'fecha_v_5': datetime.datetime.strptime(invoice.date_due, '%Y-%m-%d').strftime(
    #                     '%d/%m/%Y') if invoice.date_due else '01/01/0001',
    #                 'tipo_cpbt_6': invoice.tipo_documento.code,
    #                 'serie_cpbt_7': invoice.numero.split('-')[0],
    #                 # ple_item.anio_emision_dua_dsi_8 -> no implementado
    #                 'numero_cpbt_9': invoice.numero.split('-')[1],
    #                 # ple_item.importe_total_diario_10 - no implementado
    #                 'tipo_doc_pro_11': invoice.partner_id.catalog_06_id.code,
    #                 'numero_doc_pro_12': invoice.partner_id.vat,
    #                 'razon_social_pro_13': invoice.partner_id.registration_name,
    #                 'base_adq_gravadas_14': str(invoice.amount_untaxed),
    #                 'monto_igv_1_15': str(invoice.amount_tax),
    #                 # ple_item.base_adq_no_gravadas_16 - por consultar
    #                 # ple_item.monto_igv_2_17
    #                 # ple_item.base_adq_sin_df_18
    #                 # ple_item.monto_igv_3_19
    #                 # ple_item.valor_adq_no_gravadas_20
    #                 # ple_item.monto_isc_21
    #                 # ple_item.otros_conceptos_22
    #                 'importe_total_23': str(invoice.amount_total_signed),
    #                 'codigo_moneda_24': invoice.currency_id.name,
    #                 'tipo_cambio_25': '1.000',  # agregar campo a invoice str(invoice.valor_tipo_cambio)
    #                 # 'fecha_emision_doc_mod_26': (invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') if invoice.invoice_id.date_due.strftime('%d/%m/%Y') else '01/01/0001',
    #                 'fecha_emision_doc_mod_26': datetime.datetime.strptime(invoice.invoice_id.date_due,
    #                                                                        '%Y-%m-%d').strftime('%d/%m/%Y') if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'01/01/0001',
    #                 'tipo_cpbt_mod_27': invoice.invoice_id.tipo_documento.code if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'00',
    #                 'serie_cpbt_mod_28': invoice.invoice_id.numero.split('-')[0] if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #                 # ple_item.codigo_dep_aduanera_29
    #                 'numero_cpbt_mod_30': invoice.invoice_id.numero.split('-')[1] if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #                 'fecha_emision_cdd_31': datetime.datetime.strptime(invoice.fecha_emision_detraccion,'%Y-%m-%d').strftime('%d/%m/%Y') if invoice.fecha_emision_detraccion else u'01/01/0001',
    #                 'numero_cdd_32': invoice.numero_detraccion if invoice.numero_detraccion else u'0',
    #                 # ple_item.marca_cpbt_33
    #                 # ple_item.clasif_bienes_34
    #                 # ple_item.identif_contrato_s_i_35
    #                 # ple_item.error_tipo1_36
    #                 # ple_item.error_tipo2_37
    #                 # ple_item.error_tipo3_38
    #                 # ple_item.error_tipo4_39
    #                 # ple_item.indicador_cpbt_40
    #                 'estado_41': u'9'
    #             }
    #             ple_actual.write(ple_item_vals)
    #             # despues de proceso
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #         else:
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #     return ple_items
    #
    # """Funcion CREATE VENTAS PLE
    # """
    # def create_ple_items_ventas(self, invoices, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_ventas = self.env['account.ple.ventas']
    #     for invoice in invoices:
    #         print invoice.write_date
    #         # Buscar item ple previo
    #         ple_item_prev = self.env['account.ple.ventas'].search([
    #             ('cuo_2', '=', invoice.cuo_invoice)
    #         ], limit=1)
    #         if ple_item_prev:
    #             print ple_item_prev
    #         # if invoice.date_due:
    #         #    ple_item.fecha_v_5 = invoice.date_due.strftime('%d/%m/%Y')
    #         #if invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08':
    #         #    ple_item.fecha_emision_doc_mod_26 = datetime.datetime.strptime(invoice.invoice_id.date_due,
    #         #                                                                   '%Y-%m-%d').strftime('%d/%m/%Y')
    #         #    ple_item.tipo_cpbt_mod_27 = invoice.invoice_id.tipo_documento.code
    #         #    ple_item.serie_cpbt_mod_28 = u'F001'
    #         if datetime.datetime.strptime(invoice.date_invoice,'%Y-%m-%d').date() >= fecha_inicio and datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').date() <= fecha_fin:
    #             ple_item_estado_34 = u'1'
    #         elif datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d').date() <= fecha_inicio:
    #             ple_item_estado_34 = u'8'
    #
    #         ple_item_vals = {
    #             'periodo_1': fecha_reporte,
    #             'cuo_2': invoice.cuo_invoice,
    #             'move_cuo_3': 'M' + invoice.cuo_invoice,
    #             'fecha_e_4': datetime.datetime.strptime(invoice.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #             'fecha_v_5': datetime.datetime.strptime(invoice.date_due, '%Y-%m-%d').strftime(
    #                 '%d/%m/%Y') if invoice.date_due else '01/01/0001',
    #             'tipo_cpbt_6': invoice.tipo_documento.code,
    #             'serie_cpbt_7': invoice.numero.split('-')[0],
    #             'numero_cpbt_8': invoice.numero.split('-')[1],
    #             # ple_item.importe_total_diario_9 - no implementado
    #             'tipo_doc_pro_10': invoice.partner_id.catalog_06_id.code,
    #             'numero_doc_pro_11': invoice.partner_id.vat,
    #             'razon_social_pro_12': invoice.partner_id.registration_name,
    #             # ple_item.valor_facturado_13 - no implementado
    #             'base_adq_gravadas_14': str(invoice.amount_untaxed),
    #             # ple_item.descuento_base_imponible_15 - por revisar
    #             'monto_igv_16': str(invoice.amount_tax),
    #             # ple_item.descuento_igv_17 - por revisar
    #             # ple_item.importe_operacion_exonerada_18 - por consultar
    #             # ple_item.importe_operacion_inafecta_19 - por consultar
    #             # ple_item.isc_20 - por consultar
    #             # ple_item.base_adq_gravadas_arroz_pilado_21 - por consultar
    #             # ple_item.impuesto_ventas_arroz_pilado_22 - por consultar
    #             # ple_item.otros_conceptos_23
    #             'importe_total_24': str(invoice.amount_total_signed),
    #             'codigo_moneda_25': invoice.currency_id.name,
    #             'tipo_cambio_26': '1.000',  # agregar campo a invoice str(invoice.valor_tipo_cambio)
    #             #'fecha_emision_doc_mod_26': (invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') if invoice.invoice_id.date_due.strftime('%d/%m/%Y') else '01/01/0001',
    #             'fecha_emision_doc_mod_27': datetime.datetime.strptime(invoice.invoice_id.date_due,
    #                                                                    '%Y-%m-%d').strftime('%d/%m/%Y') if (
    #                 invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else '01/01/0001',
    #             'tipo_cpbt_mod_28': invoice.invoice_id.tipo_documento.code if (
    #                 invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'00',
    #             'serie_cpbt_mod_29': invoice.invoice_id.numero.split('-')[0] if (
    #                 invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #             # ple_item.codigo_dep_aduanera_29
    #             'numero_cpbt_mod_codigo_dep_aduanera_30': invoice.invoice_id.numero.split('-')[1] if (
    #                 invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #             # ple_item.identificacion_contrato_31
    #             # ple_item.error_tipo1_32
    #             # ple_item.indicador_cpbt_33
    #             'estado_34': ple_item_estado_34
    #         }
    #         ple_item = ple_ventas.create(ple_item_vals)
    #         invoice.write({'ple_generado': True})
    #         # despues de proceso
    #         ple_items = ple_items + ple_item.get_ple_line()
    #     return ple_items
    #
    # """Funcion FIND, UPDATE VENTAS PLE
    # """
    # def update_ple_items_ventas(self, invoices, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     for invoice in invoices:
    #         ple_actual = self.env['account.ple.ventas'].search([
    #             ('cuo_2', '=', invoice.cuo_invoice)
    #         ], limit=1)
    #
    #         if ple_actual.write_date < invoice.write_date:
    #
    #             if invoice.state == 'cancel':
    #                 ple_item_estado_34 = u'2'
    #             else:
    #                 ple_item_estado_34 = u'9'
    #
    #             ple_item_vals = {
    #                 'periodo_1': ple_actual.periodo_1,
    #                 'cuo_2': invoice.cuo_invoice,
    #                 'move_cuo_3': 'M' + invoice.cuo_invoice,
    #                 'fecha_e_4': datetime.datetime.strptime(invoice.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                 'fecha_v_5': datetime.datetime.strptime(invoice.date_due, '%Y-%m-%d').strftime(
    #                     '%d/%m/%Y') if invoice.date_due else '01/01/0001',
    #                 'tipo_cpbt_6': invoice.tipo_documento.code,
    #                 'serie_cpbt_7': invoice.numero.split('-')[0],
    #                 'numero_cpbt_8': invoice.numero.split('-')[1],
    #                 # ple_item.importe_total_diario_9 - no implementado
    #                 'tipo_doc_pro_10': invoice.partner_id.catalog_06_id.code,
    #                 'numero_doc_pro_11': invoice.partner_id.vat,
    #                 'razon_social_pro_12': invoice.partner_id.registration_name,
    #                 # ple_item.valor_facturado_13 - no implementado
    #                 'base_adq_gravadas_14': str(invoice.amount_untaxed),
    #                 # ple_item.descuento_base_imponible_15 - por revisar
    #                 'monto_igv_1_16': str(invoice.amount_tax),
    #                 # ple_item.descuento_igv_17 - por revisar
    #                 # ple_item.importe_operacion_exonerada_18 - por consultar
    #                 # ple_item.importe_operacion_inafecta_19 - por consultar
    #                 # ple_item.isc_20 - por consultar
    #                 # ple_item.base_adq_gravadas_arroz_pilado_21 - por consultar
    #                 # ple_item.impuesto_ventas_arroz_pilado_22 - por consultar
    #                 # ple_item.otros_conceptos_23
    #                 'importe_total_24': str(invoice.amount_total_signed),
    #                 'codigo_moneda_25': invoice.currency_id.name,
    #                 'tipo_cambio_26': str(invoice.valor_tipo_cambio),
    #                 # 'fecha_emision_doc_mod_26': (invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') if invoice.invoice_id.date_due.strftime('%d/%m/%Y') else '01/01/0001',
    #                 'fecha_emision_doc_mod_27': datetime.datetime.strptime(invoice.invoice_id.date_due,
    #                                                                        '%Y-%m-%d').strftime('%d/%m/%Y') if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else '01/01/0001',
    #                 'tipo_cpbt_mod_28': invoice.invoice_id.tipo_documento.code if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'00',
    #                 'serie_cpbt_mod_29': invoice.invoice_id.numero.split('-')[0] if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #                 # ple_item.codigo_dep_aduanera_29
    #                 'numero_cpbt_mod_codigo_dep_aduanera_30': invoice.invoice_id.numero.split('-')[1] if (
    #                     invoice.tipo_documento.code == '07' or invoice.tipo_documento.code == '08') else u'-',
    #                 # ple_item.identificacion_contrato_31
    #                 # ple_item.error_tipo1_32
    #                 # ple_item.indicador_cpbt_33
    #                 'estado_34': ple_item_estado_34
    #             }
    #             ple_actual.write(ple_item_vals)
    #             # despues de proceso
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #         else:
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #     return ple_items
    #
    # """Funcion CREATE DIARIO PLE
    # """
    # def create_ple_items_diario(self, move_nuevos, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_diario = self.env['account.ple.diario']
    #     for move in move_nuevos:
    #         i = 1
    #         if datetime.datetime.strptime(move.date,'%Y-%m-%d').date() >= fecha_inicio and datetime.datetime.strptime(move.date, '%Y-%m-%d').date() <= fecha_fin:
    #             ple_item_estado_21 = u'1'
    #         elif datetime.datetime.strptime(move.date, '%Y-%m-%d').date() <= fecha_inicio:
    #             ple_item_estado_21 = u'8'
    #         for move_line in move.line_ids:
    #             codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
    #             ple_item_vals = {
    #                 'periodo_1': fecha_reporte,
    #                 'cuo_2': move.cuo,
    #                 'move_cuo_3': 'M' + str(i),
    #                 'cuenta_cont_4': move_line.account_id.code,
    #                 'cunio_uea_un_up_5': '2', #SE APLICARA CUANDO ESTE COMPLETADO U.E
    #                 'ccc_cu_ci_6': '2', #SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
    #                 'codigo_moneda_7': 'PEN',
    #                 'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                 'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                 'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code if move_line.invoice_id.tipo_documento.code else '00',
    #                 'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
    #                 'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
    #                 'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                 'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                 'fecha_e_15': '01/01/0001',
    #                 'glosa_16': move_line.name, #move_line.invoice_id.name if move_line.invoice_id.name else '',
    #                 'glosa_referencial_17': '',
    #                 'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
    #                 'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
    #                 'dato_estructurado_20': codigo_libro+'&'+fecha_reporte+'&'+move.cuo+'&'+'M' + str(i),
    #                 'estado_21': ple_item_estado_21
    #             }
    #             move_line.write({'numero_asiento': 'M' + str(i)})
    #             move_line.write({'ple_generado': True})
    #             ple_item = ple_diario.create(ple_item_vals)
    #             ple_items = ple_items + ple_item.get_ple_line()
    #             i = i + 1
    #         # despues de proceso
    #         move.write({'ple_generado': True})
    #
    #     return ple_items
    #
    # """Funcion FIND, UPDATE DIARIO PLE
    # """
    # def update_ple_items_diario(self, move_olds, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     for move in move_olds:
    #         for move_line in move.line_ids:
    #             ple_actual = self.env['account.ple.diario'].search([
    #                 ('cuo_2','=',move.cuo),
    #                 ('move_cuo_3', '=', move_line.numero_asiento)
    #             ], limit=1)
    #             if ple_actual.write_date < move_line.write_date:
    #                 codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
    #                 ple_item_vals = {
    #                     'periodo_1': ple_actual.periodo_1,
    #                     'cuo_2': move.cuo,
    #                     'move_cuo_3': move_line.numero_asiento,
    #                     'cuenta_cont_4': move_line.account_id.code,
    #                     'cunio_uea_un_up_5': '2', #SE APLICARA CUANDO ESTE COMPLETADO U.N
    #                     'ccc_cu_ci_6': '2', #SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
    #                     'codigo_moneda_7': 'PEN',
    #                     'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                     'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                     'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code,
    #                     'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
    #                     'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
    #                     'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                     'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                     'fecha_e_15': '01/01/0001',
    #                     'glosa_16': move_line.name, #move_line.invoice_id.name if move_line.invoice_id.name else '',
    #                     'glosa_referencial_17': '',
    #                     'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
    #                     'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
    #                     'dato_estructurado_20': codigo_libro+'&'+fecha_reporte+'&'+move.cuo+'&'+move_line.numero_asiento,
    #                     'estado_21': '9'
    #                 }
    #                 ple_actual.write(ple_item_vals)
    #                 # despues de proceso
    #                 ple_items = ple_items + ple_actual.get_ple_line()
    #             else:
    #                 ple_items = ple_items + ple_actual.get_ple_line()
    #     return ple_items
    #
    # """Funcion CREATE DIARIO DETALLE PLE
    # """
    #
    # def create_ple_items_diario_detalle(self, cuentas_list_new, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_diario = self.env['account.ple.diario.detalle']
    #     date_now = datetime.date.today()
    #     for cuenta in cuentas_list_new:
    #         if date_now >= fecha_inicio and date_now <= fecha_fin:
    #             ple_item_estado_8 = u'1'
    #         elif date_now >= fecha_fin:
    #             ple_item_estado_8 = u'8'
    #
    #         ple_item_vals = {
    #             'periodo_1': fecha_reporte,
    #             'cuenta_cont_2': cuenta,
    #             'descripcion_cuenta_3': self.env['account.account'].search([('code','=',cuenta)], limit=1).name,
    #             'cod_plan_cuenta_4': u'01',
    #             'desc_plan_cuenta_5': u'',
    #             'cod_cuenta_corp_6': u'',  # Cuenta corporativa SBS
    #             'desc_cuenta_corp_7': u'', # Cuenta corporativa SBS
    #             'estado_8': ple_item_estado_8
    #         }
    #         ple_item = ple_diario.create(ple_item_vals)
    #         ple_items = ple_items + ple_item.get_ple_line()
    #
    #     return ple_items
    #
    # """Funcion UPDATE DIARIO DETALLE PLE
    #     """
    #
    # def update_ple_items_diario_detalle(self, diario_detalle_list, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_diarios = self.env['account.ple.diario.detalle'].search([
    #         ('periodo_1','=',fecha_reporte)
    #     ])
    #
    #     for diario in ple_diarios:
    #         ple_items = ple_items + diario.get_ple_line()
    #
    #     return ple_items
    #
    # """Funcion CREATE MAYOR PLE
    # """
    # def create_ple_items_mayor(self, move_nuevos, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     ple_diario = self.env['account.ple.mayor']
    #     i = 1
    #     for move_line in move_nuevos:
    #         if datetime.datetime.strptime(move_line.date, '%Y-%m-%d').date() >= fecha_inicio and datetime.datetime.strptime(
    #                 move_line.date, '%Y-%m-%d').date() <= fecha_fin:
    #             ple_item_estado_21 = u'1'
    #         elif datetime.datetime.strptime(move_line.date, '%Y-%m-%d').date() <= fecha_inicio:
    #             ple_item_estado_21 = u'8'
    #         ##for move_line in move.line_ids:
    #         codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
    #         ple_item_vals = {
    #             'periodo_1': fecha_reporte,
    #             'cuo_2': move_line.move_id.cuo,
    #             'move_cuo_3': 'M' + str(i),
    #             'cuenta_cont_4': move_line.account_id.code,
    #             'cunio_uea_un_up_5': '2', #SE APLICARA CUANDO ESTE COMPLETADO UNIDAD DE NEGOCIOS
    #             'ccc_cu_ci_6': '2', #SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
    #             'codigo_moneda_7': 'PEN',
    #             'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #             'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #             'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code if move_line.invoice_id.tipo_documento.code else '00',
    #             'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
    #             'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
    #             'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #             'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #             'fecha_e_15': '01/01/0001',
    #             'glosa_16': move_line.name, #move_line.invoice_id.name if move_line.invoice_id.name else '',
    #             'glosa_referencial_17': '',
    #             'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
    #             'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
    #             'dato_estructurado_20': codigo_libro + '&' + fecha_reporte + '&' + move_line.move_id.cuo + '&' + 'M' + str(i),
    #             'estado_21': ple_item_estado_21
    #         }
    #         move_line.write({'numero_asiento': 'M' + str(i)})
    #         move_line.write({'ple_generado': True})
    #         ple_item = ple_diario.create(ple_item_vals)
    #         ple_items = ple_items + ple_item.get_ple_line()
    #         i = i + 1
    #         # despues de proceso
    #         move_line.move_id.write({'ple_generado': True})
    #
    #     return ple_items
    #
    # """Funcion FIND, UPDATE MAYOR PLE
    # """
    # def update_ple_items_mayor(self, move_olds, fecha_reporte, fecha_inicio, fecha_fin):
    #     ple_items = ''
    #     for move_line in move_olds:
    #         ple_actual = self.env['account.ple.diario'].search([
    #             ('cuo_2', '=', move_line.move_id.cuo),
    #             ('move_cuo_3', '=', move_line.numero_asiento)
    #         ], limit=1)
    #         if ple_actual.write_date < move_line.write_date:
    #             codigo_libro = '140100' if move_line.invoice_id.type == 'out_invoice' else '080100'
    #             ple_item_vals = {
    #                 'periodo_1': ple_actual.periodo_1,
    #                 'cuo_2': move_line.move_id.cuo,
    #                 'move_cuo_3': 'M' + move_line.move_id.cuo,
    #                 'cuenta_cont_4': move_line.account_id.code,
    #                 'cunio_uea_un_up_5': '2', #SE APLICARA CUANDO ESTE COMPLETADO UNIDAD DE NEGOCIOS
    #                 'ccc_cu_ci_6': '2', #SE APLICARA CUANDO ESTE COMPLETADO CENTRO DE COSTOS
    #                 'codigo_moneda_7': 'PEN',
    #                 'tipo_doc_pro_8': move_line.invoice_id.partner_id.catalog_06_id.code if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                 'numero_doc_pro_9': move_line.invoice_id.partner_id.vat if move_line.invoice_id.partner_id and move_line.invoice_id.type == 'in_invoice' else '',
    #                 'tipo_cpbt_10': move_line.invoice_id.tipo_documento.code,
    #                 'serie_cpbt_11': move_line.invoice_id.numero.split('-')[0] if move_line.invoice_id.numero else '-',
    #                 'numero_cpbt_12': move_line.invoice_id.numero.split('-')[1] if move_line.invoice_id.numero else '-',
    #                 'fecha_c_13': datetime.datetime.strptime(move_line.date_maturity, '%Y-%m-%d').strftime(
    #                     '%d/%m/%Y'),
    #                 'fecha_v_14': datetime.datetime.strptime(move_line.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
    #                 'fecha_e_15': '01/01/0001',
    #                 'glosa_16': move_line.name, #move_line.invoice_id.name if move_line.invoice_id.name else '',
    #                 'glosa_referencial_17': '',
    #                 'mov_debe_18': str(move_line.credit) if move_line.debit == 0 else '0.00',
    #                 'mov_haber_19': str(move_line.debit) if move_line.credit == 0 else '0.00',
    #                 'dato_estructurado_20': codigo_libro+'&'+fecha_reporte+'&'+move_line.move_id.cuo+'&'+move_line.numero_asiento,
    #                 'estado_21': '9'
    #             }
    #             ple_actual.write(ple_item_vals)
    #             # despues de proceso
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #         else:
    #             ple_items = ple_items + ple_actual.get_ple_line()
    #     return ple_items
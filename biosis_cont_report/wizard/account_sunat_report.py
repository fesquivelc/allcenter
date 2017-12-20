# -*- coding: utf-8 -*-
import calendar

from odoo import api, fields, models
from datetime import date, datetime

class AccountingReportSunat(models.TransientModel):
    _name = "account.sunatreport"
    _description = u"Reportes Sunat"

    date_from = fields.Date(string='Desde:')
    date_to = fields.Date(string='Hasta:')
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True, default=lambda self: self.env['account.journal'].search([]))
    libro_electronico = fields.Many2one('biosis_cont_report.libro.electronico', string='Reportes Sunat', required=True)
    por_rango = fields.Boolean(string=u'Por rango de fechas')
    por_mes = fields.Boolean(string=u'Por mes')
    mes = fields.Selection([('1', u'Enero'),
                            ('2', u'Febrero'),
                            ('3', u'Marzo'),
                            ('4', u'Abril'),
                            ('5', u'Mayo'),
                            ('6', u'Junio'),
                            ('7', u'Julio'),
                            ('8', u'Agosto'),
                            ('9', u'Setiembre'),
                            ('10', u'Octubre'),
                            ('11', u'Noviembre'),
                            ('12', u'Diciembre')], 'Mes')
    year = fields.Selection([(num, str(num)) for num in range((datetime.now().year), 1900, -1)], u'Año',required=True)

    # Metodo para crear xlsx
    @api.multi
    def print_report_xls(self):
        nombre_reporte = self.libro_electronico.descripcion
        report_balance = self.libro_electronico.account_report_id
        data = {}
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids','libro_electronico','por_rango','por_mes','mes','year'])[0]
        data['form']['debit_credit'] = True
        data['form']['tipo_reporte'] = self.libro_electronico.codigo_le
        if report_balance:
            data['form']['account_report_id'] = (report_balance.id, report_balance.name)
        else:
            data['form']['account_report_id'] = False
        data['form']['enable_filter'] = False
        if self.por_mes:
            date1 = str(self.year) + '-' + str(self.mes) + '-' + '01'
            fecha_inicio = datetime.strptime(date1, "%Y-%m-%d").date()
            date2 = "%s-%s-%s" % (fecha_inicio.year, fecha_inicio.month, calendar.monthrange(fecha_inicio.year, fecha_inicio.month)[1])
            fecha_fin = datetime.strptime(date2, "%Y-%m-%d").date()
            data['form']['date_from'] = fecha_inicio.strftime("%Y-%m-%d")
            data['form']['date_to'] = fecha_fin.strftime("%Y-%m-%d")
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return {'type': 'ir.actions.report.xml',
                'report_name': 'biosis_cont_report.report_sunat_xls.xlsx',
                'datas': data['form'],
                'name': nombre_reporte
                }

    #Metodo para crear txt PLE
    @api.multi
    def get_ple_file(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/biosis_cont/contabilidad/ple?mes=%s&year=%s&tipo_reporte=%s&filename=Reporte_PLE.txt' % (
            self.mes, self.year, self.libro_electronico.codigo_le),
            'target': 'self',
        }

    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'posted'
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result

    @api.multi
    @api.onchange('por_rango')
    def onchange_por_rango(self):
        if self.por_rango:
            self.por_mes = False

    @api.multi
    @api.onchange('por_mes')
    def onchange_por_mes(self):
        if self.por_mes:
            self.por_rango = False

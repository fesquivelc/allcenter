# -*- coding: utf-8 -*-
import calendar
from datetime import date, datetime
from odoo import models, fields, api

# class customaddons/biosis_cont_report(models.Model):
#     _name = 'customaddons/biosis_cont_report.customaddons/biosis_cont_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class LibroElectronico(models.Model):
    _name = 'biosis_cont_report.libro.electronico'
    _description = 'Libro Electronicos'
    _rec_name = 'descripcion'
    name = fields.Char(string=u'Nombre',required=True)
    descripcion = fields.Char(string=u'Descripción',required=True)
    codigo_le = fields.Char(string=u'Código LE',required=True)
    state = fields.Selection([('enable','Disponible'),('disable','No disponible')],string=u'Estado Libro')
    nro_orden = fields.Char(string=u'Número Orden')
    account_report_id = fields.Many2one('account.financial.report', 'Reporte Asignado')
    grupo_libro_id = fields.Many2one('biosis_cont_report.grupolibroelectronico', string=u'Grupo Libro Electrónico')

    @api.multi
    @api.depends('descripcion')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.descripcion
            result.append((table.id, l_name))
        return result

class AccountFinancialReport(models.Model):
    _inherit = 'account.financial.report'
    code = fields.Char(string=u'Código')


class FechasMaximasAtraso(models.Model):
    _name = 'biosis_cont_report.fechasatraso'
    _description = 'Tabla para almacenar fechas para definir atraso en entrega de libros e.'
    _rec_name = 'year'
    year = fields.Selection([(num, str(num)) for num in range(datetime.now().year, datetime.now().year-10, -1)], u'Año', required=True)
    january = fields.Date(string=u'Enero:', required=True)
    february = fields.Date(string=u'Febrero:', required=True)
    march = fields.Date(string=u'Marzo:', required=True)
    april = fields.Date(string=u'Abril:', required=True)
    may = fields.Date(string=u'Mayo:', required=True)
    june = fields.Date(string=u'Junio:', required=True)
    july = fields.Date(string=u'Julio:', required=True)
    august = fields.Date(string=u'Agosto:', required=True)
    september = fields.Date(string=u'Setiembre:', required=True)
    october = fields.Date(string=u'Octubre:', required=True)
    november = fields.Date(string=u'Noviembre:', required=True)
    december = fields.Date(string=u'Diciembre:', required=True)

class GrupoLibroElectronico(models.Model):
    _name = 'biosis_cont_report.grupolibroelectronico'
    _descripcion = 'Grupo Libro Electronico'

    name = fields.Char(string=u'Nombre Grupo Libro',required=True)
    code = fields.Char(string=u'Código', required=True)
    type_time = fields.Selection([('MES','MES'),('DIA','DIA')],string=u'Tipo de tiempo', required=True)
    quantity = fields.Integer(string=u'Cantidad', required=True)


"""
    Tablas ANEXO 3 SUNAT
"""
class PleAnexo3Tabla1(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla1'
    _description = u'TABLA 1: TIPO DE MEDIO DE PAGO'

    num_order = fields.Char(string=u'N°',required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla2(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla2'
    _description = u'TABLA 2: TIPO DE DOCUMENTO DE IDENTIDAD'

    num_order = fields.Char(string=u'N°',required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla3(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla3'
    _description = u'TABLA 3: ENTIDAD FINANCIERA'

    num_order = fields.Char(string=u'N°',required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla4(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla4'
    _description = u'TABLA 4: TIPO DE MONEDA'

    cod = fields.Char(string=u'Código')
    descripcion = fields.Char(string=u'Descripción',required=True)
    pais_zona = fields.Char(string=u'País o zona de referencia', required=True)

class PleAnexo3Tabla5(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla5'
    _description = u'TABLA 5: TIPO DE EXISTENCIA'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla6(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla6'
    _description = u'TABLA 6: CÓDIGO DE LA UNIDAD DE MEDIDA'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla10(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla10'
    _description = u'TABLA 10: TIPO DE COMPROBANTE DE PAGO O DOCUMENTO'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla11(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla11'
    _description = u'TABLA 11: CÓDIGO DE LA ADUANA'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla12(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla12'
    _description = u'TABLA 12: TIPO DE OPERACIÓN'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla13(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla13'
    _description = u'TABLA 13: CATÁLOGO DE EXISTENCIAS'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla14(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla14'
    _description = u'TABLA 14: MÉTODO DE VALUACIÓN'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla15(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla15'
    _description = u'TABLA 15: TIPO DE TÍTULO'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla16(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla16'
    _description = u'TABLA 16: TIPO DE ACCIONES O PARTICIPACIONES'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla17(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla17'
    _description = u'TABLA 17: PLAN DE CUENTAS'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla18(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla18'
    _description = u'TABLA 18: TIPO DE ACTIVO FIJO'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla19(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla19'
    _description = u'TABLA 19: ESTADO DEL ACTIVO FIJO'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla20(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla20'
    _description = u'TABLA 20: MÉTODO DE DEPRECIACIÓN'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla21(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla21'
    _description = u'TABLA 21: CÓDIGO DE AGRUPAMIENTO DEL COSTO DE PRODUCCIÓN VALORIZADO ANUAL'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla22(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla22'
    _description = u'TABLA 22: CATÁLOGO DE ESTADOS FINANCIEROS'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)

class PleAnexo3Tabla25(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla25'
    _description = u'TABLA 25 "CONVENIOS PARA EVITAR LA DOBLE TRIBUTACIÓN"'

    num_order = fields.Char(string=u'N°', required=True)
    descripcion = fields.Char(string=u'Descripción', required=True)


class PleAnexo3Tabla34(models.Model):
    _name = 'biosis.report.ple.anexo3.tabla34'
    _description = u'TABLA 34: CÓDIGO DE LOS RUBROS DE LOS ESTADOS FINANCIEROS'

    codigo = fields.Char(string=u'Código')
    descripcion = fields.Char(string=u'Descripción', required=True)
    estado_financiero_id = fields.Many2one('biosis.report.ple.anexo3.tabla22',string=u'Estado Finaciero')
    cuentas = fields.Char(string=u'Cuentas a aplicar')
    excepciones = fields.Char(string=u'Cuentas a quitar')
    tipo = fields.Char(string=u'Tipo',required=True)
    padre = fields.Char(string=u'Padre')
    codigo_le = fields.Char(string=u'Libro Electronico',required=True)



# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    impuesto = fields.Boolean(string=u'Operación')
    type_journal = fields.Selection(related='journal_id.type', string=u'Tipo Diario')

    #tipo_impuesto = fields.Many2one('account.tax', string=u'Descripción tipo operación', domain=[('type_tax_use', '=', 'none')])
    tipo_impuesto = fields.Many2one('account.gastos_bancarios', string=u'Tipo de  operación')

    #payment_type = fields.Selection(selection_add=[('impuestos', 'Entrada de Impuestos')])

    @api.multi
    def post(self):
        """
        Se extiende el metodo post() de account_payment, el cual contendra la logic para crear el asiento contable donde
        se incluya el ITF.
        """
        super(AccountPayment, self).post()
        if self.journal_id.type == 'bank':
            if self.payment_type == 'outbound':
                if self.has_invoices == False:
                    account_move = self.env['account.move']
                    for rec in self:
                        ctx = dict(self._context, lang=rec.partner_id.lang)

                        date_payment = fields.Date.context_today(self)
                        company_currency = rec.company_id.currency_id

                        pml = rec.itf_line_move_get(rec, company_currency)
                        part = self.env['res.partner']._find_accounting_partner(rec.partner_id)
                        line = [(0, 0, self.env['account.invoice'].line_get_convert(l, part.id)) for l in pml]

                        # 1er Asiento
                        line1 = []
                        line1.append(line[0])
                        line1.append(line[1])
                        # 2do Asiento
                        line2 = []
                        line2.append(line[2])
                        line2.append(line[3])


                        journal = rec.journal_id.with_context(ctx)
                        date = date_payment
                        move_vals_1 = {
                            'line_ids': line1,
                            'journal_id': journal.id,
                            'date': date,
                        }

                        move_vals_2 = {
                            'line_ids': line2,
                            'journal_id': journal.id,
                            'date': date,
                        }

                        ctx['company_id'] = rec.company_id.id
                        ctx_nolang = ctx.copy()
                        ctx_nolang.pop('lang', None)

                        move1 = account_move.with_context(ctx_nolang).create(move_vals_1)
                        move1.post()

                        move2 = account_move.with_context(ctx_nolang).create(move_vals_2)
                        move2.post()
                    return True


    @api.multi
    def post_transfer(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconciliable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconciliable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            if rec.state != 'draft':
                raise UserError(
                    _("Only a draft payment can be posted. Trying to post a payment in state %s.") % rec.state)

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # Use the right sequence to set the name
            if rec.payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if rec.partner_type == 'customer':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if rec.partner_type == 'supplier':
                    if rec.payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if rec.payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
                sequence_code)

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            # cambios implementados
            # if rec.payment_type != 'transfer':

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.journal_id.type == 'bank':
                if rec.payment_type == 'transfer':
                    if rec.impuesto == True:
                        transfer_debit_aml = rec._create_transfer_itf(amount)
                    else:
                        transfer_debit_aml =  rec._create_transfer_entry_transfer(amount)
                else:
                    transfer_debit_aml = rec._create_transfer_entry_transfer(amount)
            else:
                if rec.payment_type == 'transfer':
                    transfer_debit_aml = rec._create_transfer_entry_transfer(amount)



            rec.state = 'posted'

    def _create_transfer_entry_transfer(self, amount):
        """ Create the journal entry corresponding to the 'incoming money' part of an internal transfer, return the reconciliable move line
        """
        cuenta_efectivo = self.env['account.account'].search([('code', '=like', '101001%')], limit=1)
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        debit, credit, amount_currency, dummy = aml_obj.with_context(date=self.payment_date).compute_amount_fields(
            amount, self.currency_id, self.company_id.currency_id)
        amount_currency = self.destination_journal_id.currency_id and self.currency_id.with_context(
            date=self.payment_date).compute(amount, self.destination_journal_id.currency_id) or 0

        dst_move = self.env['account.move'].create(self._get_move_vals(self.destination_journal_id))

        dst_liquidity_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, dst_move.id)
        dst_liquidity_aml_dict.update({
            'name': _('Transfer from %s') % self.journal_id.name,
            'account_id': self.destination_journal_id.default_credit_account_id.id,
            'currency_id': self.destination_journal_id.currency_id.id,
            'payment_id': self.id,
            'journal_id': self.destination_journal_id.id})
        aml_obj.create(dst_liquidity_aml_dict)

        transfer_debit_aml_dict = self._get_shared_move_line_vals(credit, debit, 0, dst_move.id)
        transfer_debit_aml_dict.update({
            'name': _('Transfer to %s') % self.destination_journal_id.name,
            'payment_id': self.id,
            'account_id': cuenta_efectivo.id,
            'journal_id': self.destination_journal_id.id})
        if self.currency_id != self.company_id.currency_id:
            transfer_debit_aml_dict.update({
                'currency_id': self.currency_id.id,
                'amount_currency': -self.amount,
            })
        transfer_debit_aml = aml_obj.create(transfer_debit_aml_dict)
        dst_move.post()
        return transfer_debit_aml

    @api.multi
    def itf_line_move_get(self, rec, currency):
        res = []
        journal = rec.journal_id
        itf_tax = self.env['account.gastos_bancarios'].search([('name', '=like', 'ITF%')], limit=1)
        cargos_account = self.env['account.account'].search([('code', '=like', '791%')], limit=1)
        # Creacion 1er asiento contable
        move_line_itf = {
            'type': 'src',
            'name': 'ITF',
            'price_unit': rec.amount * (itf_tax.amount / 100),
            'price': rec.amount * (itf_tax.amount / 100),
            'quantity': 1,
            'account_id': journal.itf_account_id.id,
        }
        res.append(move_line_itf)
        move_line_efectivo = {
            'type': 'src',
            'name': journal.name,
            'price_unit': -(rec.amount * (itf_tax.amount / 100)),
            'price': -(rec.amount * (itf_tax.amount / 100)),
            'quantity': 1,
            'account_id': journal.default_debit_account_id.id,
        }
        res.append(move_line_efectivo)
        # Creacion 2do asiento contable
        move_line_destino_itf = {
            'type': 'src',
            'name': itf_tax.name,
            'price_unit': rec.amount * (itf_tax.amount / 100),
            'price': rec.amount * (itf_tax.amount / 100),
            'quantity': 1,
            'account_id': itf_tax.destino_cuenta.id,
        }
        res.append(move_line_destino_itf)
        move_line_cargas_itf = {
            'type': 'src',
            'name': cargos_account.name,
            'price_unit': -(rec.amount * (itf_tax.amount / 100)),
            'price': -(rec.amount * (itf_tax.amount / 100)),
            'quantity': 1,
            'account_id': cargos_account.id,
        }
        res.append(move_line_cargas_itf)

        return res

    def _create_transfer(self, amount):
        """ Create the journal entry corresponding to the 'incoming money' part of an internal transfer, return the reconciliable move line
        """
        cuenta_salida = self.journal_id.default_credit_account_id.id
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        debit, credit, amount_currency, dummy = aml_obj.with_context(date=self.payment_date).compute_amount_fields(
            amount, self.currency_id, self.company_id.currency_id)
        amount_currency = self.destination_journal_id.currency_id and self.currency_id.with_context(
            date=self.payment_date).compute(amount, self.destination_journal_id.currency_id) or 0

        dst_move = self.env['account.move'].create(self._get_move_vals(self.destination_journal_id))

        dst_liquidity_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, dst_move.id)
        dst_liquidity_aml_dict.update({
            'name': _('Transfer from %s') % self.journal_id.name,
            'account_id': self.destination_journal_id.default_credit_account_id.id,
            'currency_id': self.destination_journal_id.currency_id.id,
            'payment_id': self.id,
            'journal_id': self.destination_journal_id.id})
        aml_obj.create(dst_liquidity_aml_dict)

        transfer_debit_aml_dict = self._get_shared_move_line_vals(credit, debit, 0, dst_move.id)
        transfer_debit_aml_dict.update({
            'name': _('Transfer to %s') % self.destination_journal_id.name,
            'payment_id': self.id,
            'account_id': cuenta_salida,
            'journal_id': self.destination_journal_id.id})
        if self.currency_id != self.company_id.currency_id:
            transfer_debit_aml_dict.update({
                'currency_id': self.currency_id.id,
                'amount_currency': -self.amount,
            })
        transfer_debit_aml = aml_obj.create(transfer_debit_aml_dict)
        dst_move.post()

        # Inicio Segundo Asiento
        account_move = self.env['account.move']
        ctx = dict(self._context, lang=self.partner_id.lang)

        date_payment = fields.Date.context_today(self)
        company_currency = self.company_id.currency_id

        pml = self.itf_line_move()
        part = self.env['res.partner']._find_accounting_partner(self.partner_id)
        line = [(0, 0, self.env['account.invoice'].line_get_convert(l, part.id)) for l in pml]

        # 2do Asiento
        line1 = []
        line1.append(line[0])
        line1.append(line[1])
        journal = self.journal_id.with_context(ctx)
        date = date_payment
        move_vals_1 = {
            'line_ids': line1,
            'journal_id': journal.id,
            'date': date,
        }

        ctx['company_id'] = self.company_id.id
        ctx_nolang = ctx.copy()
        ctx_nolang.pop('lang', None)

        move1 = account_move.with_context(ctx_nolang).create(move_vals_1)
        move1.post()


        #return True

        #Fin Segundo Asiento
        return transfer_debit_aml

    @api.multi
    def itf_line_move(self):
        res = []
        journal = self.journal_id
        itf_tax = self.env['account.tax'].search([('name', '=like', 'ITF%')], limit=1)
        cargos_account = self.env['account.account'].search([('code', '=like', '791%')], limit=1)

        # Creacion 2do asiento contable
        move_line_destino_itf = {
            'type': 'src',
            'name': itf_tax.account_id.name,
            'price_unit': self.amount ,
            'price': self.amount ,
            'quantity': 1,
            'account_id': itf_tax.account_id.id,
        }
        res.append(move_line_destino_itf)
        move_line_cargas_itf = {
            'type': 'src',
            'name': cargos_account.name,
            'price_unit': -(self.amount ),
            'price': -(self.amount),
            'quantity': 1,
            'account_id': cargos_account.id,
        }
        res.append(move_line_cargas_itf)

        return res

    def _create_transfer_itf(self, amount):
        """ Create the journal entry corresponding to the 'incoming money' part of an internal transfer, return the reconciliable move line
        """
        cuenta_salida = self.tipo_impuesto.id_cuenta.id,
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        debit, credit, amount_currency, dummy = aml_obj.with_context(date=self.payment_date).compute_amount_fields(
            amount, self.currency_id, self.company_id.currency_id)
        amount_currency = self.journal_id.currency_id and self.currency_id.with_context(
            date=self.payment_date).compute(amount, self.journal_id.currency_id) or 0

        dst_move = self.env['account.move'].create(self._get_move_vals(self.journal_id))

        dst_liquidity_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, dst_move.id)
        dst_liquidity_aml_dict.update({
            'name': _('Transferido desde %s') % self.journal_id.name,
            'account_id': cuenta_salida,
            'currency_id': self.currency_id.id,
            'payment_id': self.id,
            'journal_id': self.journal_id.id})
        aml_obj.create(dst_liquidity_aml_dict)

        transfer_debit_aml_dict = self._get_shared_move_line_vals(credit, debit, 0, dst_move.id)
        transfer_debit_aml_dict.update({
            'name': _('Transferido a %s') % self.tipo_impuesto.id_cuenta.name,
            'payment_id': self.id,
            'account_id': self.journal_id.default_credit_account_id.id,
            'journal_id': self.journal_id.id})
        if self.currency_id != self.company_id.currency_id:
            transfer_debit_aml_dict.update({
                'currency_id': self.currency_id.id,
                'amount_currency': -self.amount,
            })
        transfer_debit_aml = aml_obj.create(transfer_debit_aml_dict)
        dst_move.post()

        #Validamos si tiene cuenta destino
        if self.tipo_impuesto.destino_cuenta.id != False:
            # Inicio Segundo Asiento
            account_move = self.env['account.move']
            ctx = dict(self._context, lang=self.partner_id.lang)

            date_payment = fields.Date.context_today(self)
            company_currency = self.company_id.currency_id

            pml = self.line_move_itf()
            part = self.env['res.partner']._find_accounting_partner(self.partner_id)
            line = [(0, 0, self.env['account.invoice'].line_get_convert(l, part.id)) for l in pml]

            # 2do Asiento
            line1 = []
            line1.append(line[0])
            line1.append(line[1])
            journal = self.journal_id.with_context(ctx)
            date = date_payment
            move_vals_1 = {
                'line_ids': line1,
                'journal_id': journal.id,
                'date': date,
            }

            ctx['company_id'] = self.company_id.id
            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)

            move1 = account_move.with_context(ctx_nolang).create(move_vals_1)
            move1.post()

            # return True

        # Fin Segundo Asiento
        return transfer_debit_aml

    def line_move_itf(self):
        res = []
        journal = self.journal_id
        #itf_tax = self.env['account.tax'].search([('name', '=like', 'ITF%')], limit=1)
        cargos_account = self.env['account.account'].search([('code', '=like', '791%')], limit=1)

        # Creacion 2do asiento contable
        move_line_destino_itf = {
            'type': 'src',
            'name': self.tipo_impuesto.destino_cuenta.name,
            'price_unit': self.amount,
            'price': self.amount,
            'quantity': 1,
            'account_id': self.tipo_impuesto.destino_cuenta.id,
        }
        res.append(move_line_destino_itf)
        move_line_cargas_itf = {
            'type': 'src',
            'name': cargos_account.name,
            'price_unit': -(self.amount),
            'price': -(self.amount),
            'quantity': 1,
            'account_id': cargos_account.id,
        }
        res.append(move_line_cargas_itf)

        return res
#class AccountPaymentAbstract(models.AbstractModel):
 #   _inherit = "account.abstract.payment"

#    type_journal = fields.Selection(related='journal_id.type', string='Tipo Diario')


# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recurring Consignment module for Odoo
#    Copyright (C) 2015 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    # TODO improve me
    # Please, I, don't like this kind of code
    # I'm so ashamed... (with french sentences..., bad boy...)
    def _get_commission_key(self, cr, uid, move_line, context=None):
        if move_line.tax_code_id:
            # That is Vat Excl Revenue
            if '5,5' in move_line.tax_code_id.name:
                return (
                    'revenue',
                    _("Encaissement de Chiffre d'affaire HT (TVA à 5,5%)"))
            else:
                return (
                    'revenue',
                    _("Encaissement de Chiffre d'affaire HT (TVA à 20%)"))
        else:
            # That is Tax
            if '5,5' in move_line.name:
                return ('tax', _('Encaissement de TVA à 5,5%'))
            else:
                return ('tax', _('Encaissement de TVA à 20%'))

    def _get_sorted_consignment_lines(
            self, cr, uid, move_lines, order, context=None):
        line_ids = [x.id for x in move_lines]
        move_line_obj = self.pool['account.move.line']
        ordered_line_ids = move_line_obj.search(
            cr, uid, [('id', 'in', line_ids)], order=order, context=context)
        res = move_line_obj.browse(cr, uid, ordered_line_ids, context=context)
        return res

    def _get_commission_information_summary(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            groups = {}
            invoice_res = []
            move_lines = self._get_sorted_consignment_lines(
                cr, uid, invoice.consignment_line_ids,
                'tax_code_id, name', context=context)
            for move_line in move_lines:
                key = self._get_commission_key(
                    cr, uid, move_line, context=context)
                groups.setdefault(key, [])
                groups[key].append(move_line)
            for key, value in groups.iteritems():
                (kind, name) = key
                amount = 0
                for move_line in value:
                    amount += move_line.credit - move_line.debit
                invoice_res.append({
                    'type': kind,
                    'name': name,
                    'amount': amount,
                    'is_commission': (kind == 'revenue')})
            res[invoice.id] = invoice_res
        return res

    def _get_commission_information_detail(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            invoice_res = []
            sorted_lines = self._get_sorted_consignment_lines(
                cr, uid, invoice.consignment_line_ids,
                'date, move_id, tax_code_id, name', context=context)
            for line in sorted_lines:
                tmp = self._get_commission_key(cr, uid, line, context=context)
                invoice_res.append({
                    'date': line.date,
                    'name': line.move_id.name,
                    'description': tmp[1],
                    'debit': line.debit,
                    'credit': line.credit,
                    'is_commission': not (not(line.tax_code_id))})
            res[invoice.id] = invoice_res
        return res

    def _get_product_detail(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        invoice_obj = self.pool['account.invoice']
        invoice_line_obj = self.pool['account.invoice.line']
        order_obj = self.pool['pos.order']
        order_line_obj = self.pool['pos.order.line']
        product_obj = self.pool['product.product']

        for invoice in self.browse(cr, uid, ids, context=context):
            groups = {}
            invoice_res = []

            # Get Product ids
            consignor_product_ids = product_obj.search(cr, uid, [
                ('consignor_partner_id', '=', invoice.partner_id.id)],
                context=context)

            # Get Account Move
            move_ids = list(
                set([x.move_id.id for x in invoice.consignment_line_ids]))

            # Get related invoice
            com_invoice_ids = invoice_obj.search(cr, uid, [
                ('move_id', 'in', move_ids)], context=context)

            com_invoice_line_ids = invoice_line_obj.search(cr, uid, [
                ('invoice_id', 'in', com_invoice_ids),
                ('product_id', 'in', consignor_product_ids)], context=context)

            for com_invoice_line in invoice_line_obj.browse(
                    cr, uid, com_invoice_line_ids, context=context):
                key = (
                    com_invoice_line.product_id.id,
                    com_invoice_line.price_unit,
                    com_invoice_line.discount,
                )
                groups.setdefault(key, {
                    'quantity': 0,
                    'total_vat_excl': 0,
                    'total_vat_incl': 0})
                groups[key] = {
                    'quantity': groups[key]['quantity'] +
                    com_invoice_line.quantity,
                    'total_vat_excl': groups[key]['total_vat_excl'] +
                    com_invoice_line. price_subtotal,
                    'total_vat_incl': groups[key]['total_vat_incl'] +
                    com_invoice_line. price_subtotal_taxinc,
                }

            # Get related pos order
            com_order_ids = order_obj.search(cr, uid, [
                ('account_move', 'in', move_ids)], context=context)

            com_order_line_ids = order_line_obj.search(cr, uid, [
                ('order_id', 'in', com_order_ids),
                ('product_id', 'in', consignor_product_ids)], context=context)

            for com_order_line in order_line_obj.browse(
                    cr, uid, com_order_line_ids, context=context):
                key = (
                    com_order_line.product_id.id,
                    com_order_line.price_unit,
                    com_order_line.discount,
                )
                groups.setdefault(key, {
                    'quantity': 0,
                    'total_vat_excl': 0,
                    'total_vat_incl': 0})
                groups[key] = {
                    'quantity': groups[key]['quantity'] +
                    com_order_line.qty,
                    'total_vat_excl': groups[key]['total_vat_excl'] +
                    com_order_line.price_subtotal,
                    'total_vat_incl': groups[key]['total_vat_incl'] +
                    com_order_line.price_subtotal_incl,
                }

            # Compute sum of each product
            for key, value in groups.iteritems():
                (product_id, price_unit, discount) = key
                product = product_obj.browse(
                    cr, uid, product_id, context=context)
                invoice_res.append({
                    'product_code': product.default_code,
                    'product_name': product.name,
                    'price_unit': price_unit,
                    'discount': discount,
                    'quantity': value['quantity'],
                    'total_vat_excl': value['total_vat_excl'],
                    'total_vat_incl': value['total_vat_incl'],
                })
            sorted_invoice_res = sorted(
                invoice_res,
                key=lambda k: (
                    k['product_name'], - k['price_unit'], k['discount']))
            res[invoice.id] = sorted_invoice_res
        return res

    # Columns Section
    _columns = {
        'commission_information_summary': fields.function(
            _get_commission_information_summary, type='char',
            string='Commission Information Summary'),
        'commission_information_detail': fields.function(
            _get_commission_information_detail, type='char',
            string='Commission Information Detail'),
        'product_detail': fields.function(
            _get_product_detail, type='char',
            string='Product Detail'),
        'is_consignment_invoice': fields.boolean(
            string='Is Consignment Invoice', readonly=True),
        'consignment_line_ids': fields.one2many(
            'account.move.line', 'consignment_invoice_id',
            'Commissionned Lines', readonly=True),
    }

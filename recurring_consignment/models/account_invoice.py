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
    # Please, I, don't right this kind of code
    # I'm so ashamed...
    def _get_commission_key(self, cr, uid, move_line, context=None):
        if move_line.tax_code_id:
            # That is Vat Excl Revenue
            if '5,5' in move_line.tax_code_id.name:
                return ('revenue', _("Chiffre d'affaire HT (TVA 5,5%)"))
            else:
                return ('revenue', _("Chiffre d'affaire à HT (TVA 20%)"))
        else:
            # That is Tax
            if '5,5' in move_line.name:
                return ('tax', _('Encaissement de TVA à 5,5%'))
            else:
                return ('tax', _('Encaissement de TVA à 20%'))

    def _get_commission_information(self, cr, uid, ids, a, bon, context=None):
        res = {}
        groups = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            groups = {}
            invoice_res = []
            for move_line in invoice.consignment_line_ids:
                key = self._get_commission_key(
                    cr, uid, move_line, context=context)
                groups.setdefault(key, [])
                groups[key].append(move_line)
            for key, value in groups.iteritems():
                (kind, name) = key
                amount = 0
                for move_line in value:
                    amount += move_line.credit - move_line.debit
                if kind == 'revenue':
                    commission_rate = invoice.partner_id.consignment_commission
                else:
                    commission_rate = 0
                invoice_res.append({
                    'type': kind,
                    'name': name,
                    'amount': amount,
                    'commission_rate': commission_rate})
            res[invoice.id] = invoice_res
        return res

    # Columns Section
    _columns = {
        'commission_information': fields.function(
            _get_commission_information, type='char',
            string='Commission Information'),
        'is_consignment_invoice': fields.boolean(
            string='Is Consignment Invoice', readonly=True),
        'consignment_line_ids': fields.one2many(
            'account.move.line', 'consignment_invoice_id',
            'Commissionned Lines', readonly=True),
    }

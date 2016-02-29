# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recurring Consignment module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime

from openerp.osv.osv import except_osv
from openerp.osv.orm import TransientModel
from openerp.osv import fields
from openerp.tools.translate import _


class InvoiceCommissionWizard(TransientModel):
    _name = 'invoice.commission.wizard'

    # Columns Section
    _columns = {
        'consignor_partner_id': fields.many2one(
            'res.partner', string='Consignor', required=True,
            domain="[('is_consignor', '=', True)]"),
        'period_id': fields.many2one(
            'account.period', string='Accounting Period', required=True,
            domain="[('special', '=', False), ('state', '=', 'draft')]"),
        'line_qty': fields.integer(
            string='Move Lines Quantity', readonly=True),
    }

    # Default values Section
    def _default_consignor_partner_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    def _default_period_id(self, cr, uid, context=None):
        "return the past accounting period"
        period_obj = self.pool['account.period']
        period_ids = period_obj.search(cr, uid, [
            ('date_stop', '<', datetime.now().strftime('%Y-%m-%d')),
            ('special', '=', False)],
            order='date_start desc', limit=1, context=context)
        return period_ids and period_ids[0] or False

    def _default_line_qty(self, cr, uid, context=None):
        consignor_partner_id = self._default_consignor_partner_id(
            cr, uid, context=context)
        period_id = self._default_period_id(cr, uid, context=context)
        line_ids = self._get_line_ids(
            cr, uid, consignor_partner_id, period_id, context=context)
        return line_ids and len(line_ids) or 0

    _defaults = {
        'consignor_partner_id': _default_consignor_partner_id,
        'period_id': _default_period_id,
        'line_qty': _default_line_qty,
    }

    # On Change Section
    def on_change_consignor_partner_id_period_id(
            self, cr, uid, ids, consignor_partner_id, period_id, context=None):
        line_ids = self._get_line_ids(
            cr, uid, consignor_partner_id, period_id, context=context)
        return {'value': {'line_qty': len(line_ids)}}

    # Action Section
    def invoice_commission(self, cr, uid, ids, context=None):
        model_data_obj = self.pool['ir.model.data']
        action_obj = self.pool['ir.actions.act_window']
        move_line_obj = self.pool['account.move.line']
        invoice_obj = self.pool['account.invoice']
        invoice_line_obj = self.pool['account.invoice.line']
        invoice_ids = []
        grouped_data = {}
        done_line_ids = []

        for wizard in self.browse(cr, uid, ids, context=context):
            rate = wizard.consignor_partner_id.consignment_commission
            # Get lines to commission
            # rate = wizard.consignor_partner_id.consignment_commission
            line_ids = self._get_line_ids(
                cr, uid, wizard.consignor_partner_id.id, wizard.period_id.id,
                context=context)
            if not line_ids:
                raise except_osv(_('Error!'), _(
                    "There is no move lines to commission for this consignor"
                    " and this accounting period."))

            for line in move_line_obj.browse(
                    cr, uid, line_ids, context=context):
                # If there is product commission on this line
                if line.tax_code_id.consignment_product_id:
                    key = self._get_line_key(cr, uid, line, context=context)
                    grouped_data.setdefault(key, [])
                    grouped_data[key].append(line)

            # Make Commission Invoice
            invoice_vals = {
                'partner_id': wizard.consignor_partner_id.id,
                'date_invoice': wizard.period_id.date_stop,
                'is_consignment_invoice': True,
                'type': 'out_invoice',
                'name': _('Commission Invoices (%s)') % wizard.period_id.code,
                'account_id':
                    wizard.consignor_partner_id.consignment_account_id.id,
            }
            invoice_id = invoice_obj.create(
                cr, uid, invoice_vals, context=context)
            invoice_ids.append(invoice_id)

            # Create lines
            for key, value in grouped_data.iteritems():
                current_line_ids = [x.id for x in value]
                invoice_line_vals = self._prepare_invoice_line(
                    cr, uid, key, value, wizard, invoice_id, context=context)
                invoice_line_obj.create(
                    cr, uid, invoice_line_vals, context=context)

                done_line_ids += current_line_ids

                # Mark Move lines as commisssioned
                move_line_obj.write(cr, uid, current_line_ids, {
                    'consignment_invoice_id': invoice_id,
                    'consignment_commission': rate,
                }, context=context)

            # Mark leaving Move lines as no commisssioned
            leaving_line_ids = [x for x in line_ids if x not in done_line_ids]
            move_line_obj.write(cr, uid, leaving_line_ids, {
                'consignment_invoice_id': invoice_id,
                'consignment_commission': 0,
            }, context=context)

        # Recompute Taxes
        invoice_obj.button_reset_taxes(cr, uid, invoice_ids, context=context)

        # Return action that displays new invoices
        action_id = model_data_obj.get_object_reference(
            cr, uid, 'account', 'action_invoice_tree1')[1]
        action = action_obj.read(cr, uid, [action_id], context=context)[0]
        action['domain'] =\
            "[('id', 'in', ["+','.join(map(str, invoice_ids))+"])]"
        return action

    def _prepare_invoice_line(
            self, cr, uid, key, value, wizard, invoice_id, context=None):
        invoice_line_obj = self.pool['account.invoice.line']
        rate = wizard.consignor_partner_id.consignment_commission
        total_credit = 0
        product = value[0].tax_code_id.consignment_product_id
        for line in value:
            total_credit += line.credit - line.debit
        res = invoice_line_obj.product_id_change(
            cr, uid, False, product.id, product.uom_id.id, qty=1,
            type='out_invoice', partner_id=wizard.consignor_partner_id.id,
            context=None)['value']
        res.update({
            'product_id': product.id,
            'invoice_id': invoice_id,
            'price_unit': total_credit * rate / 100,
            'invoice_line_tax_id': [(6, False, res['invoice_line_tax_id'])],
            'name':  _(
                "Commission on Sale or Refunds\n"
                "(Rate : %s %%; Base : %.2f € ; Period %s)") % (
                    rate, total_credit, value[0].period_id.code),

        })
        return res

    # Private Section
    def _get_line_key(self, cr, uid, move_line, context=None):
        return (
            move_line.period_id.id,
            move_line.tax_code_id.id)

    def _get_line_ids(
            self, cr, uid, consignor_partner_id, period_id, context=None):
        if not (consignor_partner_id and period_id):
            return []
        partner_obj = self.pool['res.partner']
        journal_obj = self.pool['account.journal']
        period_obj = self.pool['account.period']
        line_obj = self.pool['account.move.line']
        consignor_partner = partner_obj.browse(
            cr, uid, consignor_partner_id, context=context)
        period = period_obj.browse(cr, uid, period_id, context=context)
        journal_ids = journal_obj.search(
            cr, uid, [('type', 'in', ['sale', 'sale_refund'])],
            context=context)
        return line_obj.search(cr, uid, [
            ('period_id', '=', period.id),
            ('account_id', '=', consignor_partner.consignment_account_id.id),
            ('journal_id', 'in', journal_ids),
            ('consignment_invoice_id', '=', False),
            ('partner_id', '!=', consignor_partner.id),
        ], order='date, move_id, tax_code_id', context=context)

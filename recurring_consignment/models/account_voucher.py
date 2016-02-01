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


class AccountVoucher(Model):
    _inherit = 'account.voucher'

#    # Override section
#    def recompute_voucher_lines(
#            self, cr, uid, ids, partner_id, journal_id, price, currency_id,
#            ttype, date, context=None):
#        partner_obj = self.pool['res.partner']
#        move_line_obj = self.pool['account.move.line']
#        ctx = context.copy()
#        if partner_id:
#            partner = partner_obj.browse(cr, uid, partner_id, context=context)
#            if partner.is_consignor:
# #                ctx.update({
# #                    'partner_id': False,
# #                    'account_id': partner.consignment_account_id.id,
# #                })
#                move_line_ids = move_line_obj.search(
#                    cr, uid, [('state','=','valid'),
#                    ('account_id', '=', partner.consignment_account_id.id),
#                    ('reconcile_id', '=', False)], context=context)
#                ctx.update({
#                    'move_line_ids': move_line_ids,
#                })

#        res = super(AccountVoucher, self).recompute_voucher_lines(
#            cr, uid, ids, partner_id, journal_id, price, currency_id, ttype,
#            date, context=ctx)
#        print "**********>"
#        print "partner_id : %s" % partner_id
#        print "journal_id : %s" % journal_id
#        print "price : %s" % price
#        print "currency_id : %s" % currency_id
#        print "ttype %s" % ttype
#        print res
#        return res

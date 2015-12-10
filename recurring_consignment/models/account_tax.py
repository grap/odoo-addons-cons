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


class account_tax(Model):
    _inherit = 'account.tax'

    # Columns Section
    _columns = {
        'consignor_id': fields.many2one(
            'res.partner', string='Consignor',
            domain="[('is_consignor', '=', True)]"),
    }

    def on_change_consignor_id(self, cr, uid, ids, consignor_id, context=None):
        partner_obj = self.pool['res.partner']

        if not consignor_id:
            return {}
        else:
            partner = partner_obj.browse(
                cr, uid, consignor_id, context=context)
        return {'value': {
            'account_collected_id': partner.property_account_payable.id,
            'account_paid_id': partner.property_account_payable.id,
        }}


    # Constraint Section
    def _check_consignor_taxes(self, cr, uid, ids, context=None):
        for tax in self.browse(cr, uid, ids, context=context):
            if tax.consignor_id:
                if tax.consignor_id.property_account_payable.id !=\
                        tax.account_collected_id.id or\
                        tax.consignor_id.property_account_payable.id !=\
                        tax.account_paid_id.id:
                    return False
        return True

    _constraints = [
        (
            _check_consignor_taxes,
            "You have to set the same"
            " accounts as the supplier account of the selected consignor.",
            ['consignor_id', 'account_collected_id', 'account_paid_id'])
    ]

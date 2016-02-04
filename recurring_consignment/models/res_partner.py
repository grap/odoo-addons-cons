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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.osv import except_osv
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _


class res_partner(Model):
    _inherit = 'res.partner'

    _columns = {
        'is_consignor': fields.boolean('Is Consignor'),
        'consignment_commission': fields.float('Consignment Commission Rate'),
        'consignment_account_id': fields.many2one(
            'account.account', string='Consignment Account'),
    }

    # Constraint Section
    def _check_is_consignor_consignment_account_id(
            self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.is_consignor:
                if not (partner.consignment_account_id and
                        partner.consignment_commission != 0):
                    return False
            else:
                if (partner.consignment_account_id or
                        partner.consignment_commission != 0):
                    return False
        return True

    _constraints = [
        (
            _check_is_consignor_consignment_account_id,
            "A Consignor must have a not null 'Consignment Commission'"
            " and a 'Consignment Account' defined.\n\n"
            " a Non Consignor partner can not have 'Consignment Commission'"
            " neither 'Consignment Account' defined.",
            ['is_consignor', 'consignment_commission',
                'consignment_account_id'])
    ]

    # Create / write Overload Section
    def _update_vals_consignment(self, cr, uid, vals, context=None):
        vals.pop('simple_tax_type', False)
        vals.pop('property_account_payable', False)
        vals.pop('property_account_receivable', False)
        if vals.get('consignment_account_id', False):
            vals.update({
                'simple_tax_type': 'excluded',
                'property_account_payable': vals['consignment_account_id'],
                'property_account_receivable': vals['consignment_account_id'],
            })
        return vals

    def create(self, cr, uid, vals, context=None):
        vals = self._update_vals_consignment(cr, uid, vals, context=context)
        return super(res_partner, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'is_consignor' in vals and vals.get('is_consignor') is False:
            for partner in self.browse(cr, uid, ids, context=context):
                if partner.is_consignor:
                    raise except_osv(_('Error!'), _(
                        "You can not unset consignor setting on partner.\n"
                        " Please create a new one if you want to do so."))
        vals = self._update_vals_consignment(cr, uid, vals, context=context)
        return super(res_partner, self).write(
            cr, uid, ids, vals, context=context)

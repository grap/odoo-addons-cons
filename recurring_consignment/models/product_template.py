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

from openerp.osv.orm import Model
from openerp.osv import fields


class product_template(Model):
    _inherit = 'product.template'

    # Compute Section
    def get_is_consignment(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for template in self.browse(cr, uid, ids, context=context):
            res[template.id] = (template.consignor_partner_id.id is not False)
        return res

    # Columns Section
    _columns = {
        'consignor_partner_id': fields.many2one(
            'res.partner', string='Consignor',
            domain="[('is_consignor', '=', True)]",
            oldname='consignor_id'),
        'is_consignment': fields.function(
            get_is_consignment, type='boolean', string='Is Consignment',
            readonly=True, store=True),
        # Overload to update domain constraint
        'tax_group_id': fields.many2one(
            'tax.group', 'Tax Group',
            domain="[('company_id', '=', company_id),"
            "('consignor_partner_id', '=', consignor_partner_id)]",
            help="Specify the combination of taxes for this product."
            " This field is required. If you dont find the correct Tax"
            " Group, Please create a new one or ask to your account"
            " manager if you don't have the access right."),
    }

    # Constraint Section
    def _check_consignor_partner_id_fields(self, cr, uid, ids, context=None):
        for template in self.browse(cr, uid, ids, context=context):
            if template.consignor_partner_id:
                if template.standard_price:
                    return False
        return True

    _constraints = [
        (
            _check_consignor_partner_id_fields,
            "A consigned product must have null Cost Price.\n",
            # "A consigned product must have a uniq supplier.\n"
            # "The supplier of a consigned product should be the consignor.\n",
            ['consignor_partner_id', 'seller_ids']),
    ]

    def _update_vals_consignor(self, cr, uid, vals, context=None):
        partner_obj = self.pool['res.partner']
        if vals.get('consignor_partner_id', False):
            partner = partner_obj.browse(
                cr, uid, vals.get('consignor_partner_id'), context=context)
            vals['purchase_ok'] = True
            vals['property_account_income'] =\
                partner.consignment_account_id.id
            vals['property_account_expense'] =\
                partner.consignment_account_id.id
            vals['seller_ids'] = [[0, False, {
                'name': vals.get('consignor_partner_id'),
                'company_id': partner.company_id.id,
                'pricelist_ids': [],
                'package_qty': 1,  # FIXME
            }]]
        return vals

    def create(self, cr, uid, vals, context=None):
        vals = self._update_vals_consignor(cr, uid, vals, context=context)
        return super(product_template, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        vals = self._update_vals_consignor(cr, uid, vals, context=context)
        return super(product_template, self).write(
            cr, uid, ids, vals, context=context)

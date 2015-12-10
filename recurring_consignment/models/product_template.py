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


class product_template(Model):
    _inherit = 'product.template'

    # Compute Section
    def get_is_consignment(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for template in self.browse(cr, uid, ids, context=context):
            res[template.id] = (template.consignor_id.id != False)
        print res
        return res

    # Columns Section
    _columns = {
        'consignor_id': fields.many2one(
            'res.partner', string='Consignor',
            domain="[('is_consignor', '=', True)]"),
        'is_consignment': fields.function(
            get_is_consignment, type='boolean', string='Is Consignment',
            readonly=True, store=True),
        # Overload to update domain constraint
        'tax_group_id': fields.many2one(
            'tax.group', 'Tax Group',
            domain="[('company_id', '=', company_id),"
            "('consignor_id', '=', consignor_id)]",
            # TODO set redaonly if consignor_id is set
#            readonly="",
            help="Specify the combination of taxes for this product."
            " This field is required. If you dont find the correct Tax"
            " Group, Please create a new one or ask to your account"
            " manager if you don't have the access right."),
    }

###    # Constraint Section
###    def _check_consignor_id_fields(self, cr, uid, ids, context=None):
###        print "CHECK"
###        for template in self.browse(cr, uid, ids, context=context):
###            if template.consignor_id:
###                if template.standard_price:
###                    return False
###                elif len(template.seller_ids) != 0:
###                    return False
###                elif template.seller_ids[0].name.id\
###                        != template.consignor_id.id:
###                    return False
###        return True

###    _constraints = [
###        (
###            _check_consignor_id_fields,
###            "A consigned product must have null Cost Price.\n"
###            "A consigned product must have a uniq supplier.\n"
###            "The supplier of the consigned product should be the consignor.\n",
###            ['consignor_id', 'seller_ids']),
###    ]

    def update_vals_consignor(self, cr, uid, vals, context=None):
        partner_obj = self.pool['res.partner']
        if vals.get('consignor_id', False):
            partner = partner_obj.browse(
                cr, uid, vals.get('consignor_id'), context=context)
            vals['purchase_ok'] = True
            vals['property_account_income'] =\
                partner.property_account_payable.id
            vals['property_account_expense'] =\
                partner.property_account_payable.id
            vals
        return vals

#    def update_product_consignor(self, cr, uid, ids, vals, context=None):
#        product_obj = self.pool['product.product']

#        if vals.get('consignor_id', False):
#            for template in self.browse(cr, uid, ids, context=context):
#                if template.is_consignment:
#                    product_ids = product_obj.search(
#                        cr, uid, [('product_tmpl_id', '=', template.id)],
#                        context=context)
#                    product_obj.write(cr, uid, product_ids, {
#                        'cost_price': 0,
#                    }, context=context)
                
    def create(self, cr, uid, vals, context=None):
        print "**********************************"
        print "CREATE"
        print vals
        vals = self.update_vals_consignor(cr, uid, vals, context=context)
        print "*******"
        print vals
        return super(product_template, self).create(
            cr, uid, vals, context=context)


    def write(self, cr, uid, ids, vals, context=None):
        print "**********************************"
        print "WRITE"
        print vals
        vals = self.update_vals_consignor(cr, uid, vals, context=context)
        return super(product_template, self).write(
            cr, uid, ids, vals, context=context)

    # Custom Section
    def set_consignment(
            self, cr, uid, ids, consignor_id, tax_group_id, context=None):
        for template in self.browse(cr, uid, ids, context=context):
            if template.consignor_id:
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not change consignor. Please create a"
                    " new product"))
        self.write(cr, uid, ids, {
            'consignor_id': consignor_id,
            'tax_group_id': tax_group_id,
            'purchase_ok': True,
        }, context=None)

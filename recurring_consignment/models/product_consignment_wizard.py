# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recurring Consignment module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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


from openerp.osv import fields
from openerp.osv.orm import TransientModel
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class product_consigment_wizard(TransientModel):
    _name = 'product.consigment.wizard'

    # Columns Section
    _columns = {
        'consignor_id': fields.many2one(
            'res.partner', string='Consignor', required=True),
        'tax_group_id': fields.many2one(
            'tax.group', string='Tax Group', required=True),
    }

    # Cosntraint section
    def _check_consignor_id_tax_group(self, cr, uid, ids, context=None):
        for wizard in self.browse(cr, uid, ids, context=context):
            if (wizard.tax_group_id.id != wizard.consignor_id.id):
                return False
        return True

    _constraints = [
        (
            _check_consignor_id_tax_group,
            "Please select a Tax Group linked to the selected Consignor.",
            ['tax_group_id', 'consignor_id'])
    ]


    # Custom Section
    def apply(self, cr, uid, ids, context=None):
        product_obj = self.pool['product.product']
        template_obj = self.pool['product.template']
        wizard = self.browse(cr, uid, ids[0], context=context)

        # convert product ids into template ids
        products = product_obj.browse(
            cr, uid, context.get('active_ids'), context=context)
        template_ids = list(set([x.product_tmpl_id.id for x in products]))

        template_obj.set_consignment(
            cr, uid, template_ids, wizard.consignor_id.id,
            wizard.tax_group_id.id, context=context)

        return {'type': 'ir.actions.act_window_close'}

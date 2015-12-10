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


class tax_group(Model):
    _inherit = 'tax.group'

    # Columns Section
    _columns = {
        'consignor_id': fields.many2one(
            'res.partner', string='Consignor',
            domain="[('is_consignor', '=', True)]"),
    }

    # Constraint Section
    def _check_consignor_supplier_tax_ids(self, cr, uid, ids, context=None):
        for tax_group in self.browse(cr, uid, ids, context=context):
            if (tax_group.consignor_id and len(tax_group.supplier_tax_ids)):
                return False
        return True

    _constraints = [
        (
            _check_consignor_supplier_tax_ids,
            "You can not set Supplier Taxes for tax groups used for"
            " consignment", ['supplier_tax_ids', 'consignor_id'])
    ]

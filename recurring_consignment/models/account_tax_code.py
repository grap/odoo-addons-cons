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


class account_tax_code(Model):
    _inherit = 'account.tax.code'

    # Columns Section
    _columns = {
        'consignment_product_id': fields.many2one(
            'product.product', string='Consignment Product',
            domain="[('type', '=', 'service')]",
            help="Set a 'Sales commission' product for consignment sales.\n"
            "If not set, transaction will not be commissioned. (this case is"
            " usefull to avoid to commission taxes transaction, because in"
            " most cases, commissions are computed on without taxes amount)."
            ),
    }

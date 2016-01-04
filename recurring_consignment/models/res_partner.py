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
        'consignment_commission': fields.float('Consignment Commission'),
    }

    # Constraint Section
    def _check_consignor_fields(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.is_consignor:
                if not partner.consignment_commission:
                    return False
            else:
                if partner.consignment_commission:
                    return False
        return True

    _constraints = [
        (
            _check_consignor_fields,
            "Is Consignor and Consignment commission should be set both.",
            ['is_consignor', 'consignment_commission']),
    ]

    # Cosntraint section
    def write(self, cr, uid, ids, vals, context=None):
        if 'is_consignor' in vals and vals.get('is_consignor') is False:
            for partner in self.browse(cr, uid, ids, context=context):
                if partner.is_consignor:
                    raise except_osv(_('Error!'), _(
                        "You can not unset consignor setting on partner.\n"
                        " Please create a new one if you want to do so."))
        return super(res_partner, self).write(
            cr, uid, ids, vals, context=context)

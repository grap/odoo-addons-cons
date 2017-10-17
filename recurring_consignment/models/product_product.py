# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model

# TODO, check if it is necessary
##class product_product(Model):
##    _inherit = 'product.product'

##    # View Section
##    def onchange_consignor_partner_id(
##            self, cr, uid, ids, consignor_partner_id, context=None):
##        """Set to False Tax group_id to force user to set correct new tax
##        group depending of the context"""
##        if consignor_partner_id:
##            return {'value': {'tax_group_id': False}}
##        else:
##            return True

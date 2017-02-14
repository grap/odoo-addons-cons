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

{
    'name': 'Sale - Recurring Consignment',
    'version': '0.1',
    'summary': 'Manage recurring consignment',
    'category': 'Sale',
    'description': """
Manage recurring consignment
============================

For more information about consigment see:
https://en.wikipedia.org/wiki/Consignment

This module manage recurring consignment: A product will allways be provided
by the same consignor and can not be provided by another way.

For other implementation of consigment you could see:

* (vendor_consignment_stock)[https://github.com/OCA/purchase-workflow];


Functionality
-------------

TODO :
- basic user can only change location and email.
Partner Model

* Add a 'is_consignor' field on Partner;

Product Model

* Add a consignor_partner_id field (res.partner), indicating which partner
  provide the product;
* if consignor_partner_id is defined:
    * The product can not have seller_ids defined;
    * The product has a special VAT defined;

TODO :

- Ajouter le justificatif de commission dans le mail à envoyer.
(surcharger account.invoice ?)

Copyright, Authors and Licence:
-------------------------------

* Copyright: 2015-Today, GRAP: Groupement Régional Alimentaire de Proximité;
* Author: Sylvain LE GAL (https://twitter.com/legalsylvain);
* Licence: AGPL-3 (http://www.gnu.org/licenses/);
""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product_taxes_group',
        'simple_tax_account',
        'purchase',
        'account_voucher',
        'point_of_sale',
        'sale',
        'report_webkit',
    ],
    'data': [
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'views/report.xml',
        'views/action_popup.xml',
        'views/view_account_invoice.xml',
        'views/view_account_tax.xml',
        'views/view_account_tax_code.xml',
        'views/view_tax_group.xml',
        'views/view_product_product.xml',
        'views/view_product_template.xml',
        'views/view_invoice_commission_wizard.xml',
        'views/view_res_partner.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/account_account.yml',
        'demo/res_partner.yml',
        'demo/account_tax_code.yml',
        'demo/account_tax.yml',
        'demo/tax_group.yml',
        'demo/product_product.yml',
        'demo/account_invoice.xml',
    ],
    'css': [
        'static/src/css/recurring_consignment.css',
    ],
    'installable': True,
}

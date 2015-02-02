# -*- encoding: utf-8 -*-
##############################################################################
#
#    MRP To Purchase module for Odoo
#    Copyright (C) 2015-Today Akretion (http://www.akretion.com)
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
    'name': 'MRP To Purchase',
    'version': '0.1',
    'category': 'mrp',
    'summary': 'Transform a Production Order into Purchase Order',
    'description': """
Transform a Production Order into Purchase Order
================================================

Features :
----------
    * TODO Write Description;

Use Case with Demo Data:
------------------------
    * TODO Write User Case;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2015, Akretion;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'mrp',
        'purchase',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_template.yml',
        'demo/product_product.yml',
        'demo/product_supplierinfo.yml',
        'demo/mrp_bom.yml',
    ],
    'data': [
        'view/view.xml',
    ],
}

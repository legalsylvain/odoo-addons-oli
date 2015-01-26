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

from openerp.tests.common import TransactionCase


class Test(TransactionCase):

    # Overload Section
    def setUp(self):
        super(Test, self).setUp()

        # Get Registries
        self.imd_obj = self.registry('ir.model.data')

        # Get ids from xml_ids
        # self.id = self.imd_obj.get_object_reference(
        #     self.cr, self.uid, '', '')[1]

    # Test Section
    def test_01_mrp_to_purchase(self):
        """[Functional Test] TODO WRITE DESCRIPTION"""
        # cr, uid = self.cr, self.uid
        self.assertEqual(
            True, True,
            "TO WRITE.")

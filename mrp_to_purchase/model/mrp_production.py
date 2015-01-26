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

from openerp.osv.orm import Model
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class mrp_production(Model):
    _inherit = 'mrp.production'

    def mrp_to_purchase(self, cr, uid, ids, context=None):
        """
        This function cancel the Production Orders, create Purchase Orders
        associated to Procurement and returns an action that display new
        Purchase Orders.
        """
        pro_obj = self.pool['procurement.order']
        imd_obj = self.pool['ir.model.data']
        iaaw_obj = self.pool['ir.actions.act_window']

        pur_ids = []

        for mp in self.browse(cr, uid, ids, context=context):
            # Check that the production is not running
            if mp.state not in ('draft', 'confirmed'):
                raise except_osv(_('Error: Incorrect State!'), _(
                    "The Manufacturing Order %s can not be transformed into"
                    " a Purchase Order because the production is in a pending"
                    " state") % (
                        mp.name))

            # Get Procurement Order that has generated the Production Order
            pro_ids = pro_obj.search(cr, uid, [
                ('production_id', '=', mp.id),
            ], context=context)
            if len(pro_ids) != 1:
                raise except_osv(_('Error: Procurement Not Found!'), _(
                    "The associated Procurement Order has not be found for"
                    " the Manufacturing Order %s.\n In that case, please"
                    " simply cancel this Production Order and create a"
                    "Purchase Order.") % (mp.name))
            pro = pro_obj.browse(cr, uid, pro_ids[0], context=context)

            # Check that product has a Seller defined
            if not pro.product_id.seller_id:
                raise except_osv(_('Error: Seller Not Found!'), _(
                    "The product %s has no Seller associated. Please"
                    " associate a Seller to this product in the procurement"
                    " view of the product.") % (
                        pro.product_id.name))

            # Create a Purchase Order
            tmp = pro_obj.make_po(cr, uid, pro_ids, context=context)
            pur_ids.append(tmp[pro.id])

        # Get Action to return to the Client
        iaaw_id = imd_obj.get_object_reference(
            cr, uid, 'purchase', 'purchase_form_action')[1]
        res = iaaw_obj.read(cr, uid, [iaaw_id], context=context)[0]

        # Choose the view_mode accordingly
        if len(pur_ids) > 1:
            res['domain'] =\
                "[('id','in',[" + ','.join(map(str, pur_ids)) + "])]"
        else:
            res['views'] = [(False, 'form')]
            res['res_id'] = pur_ids[0]

        return res

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

from openerp import netsvc

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

        wf_service = netsvc.LocalService('workflow')
        sm_obj = self.pool['stock.move']
        sp_obj = self.pool['stock.picking']
        proc_obj = self.pool['procurement.order']
        imd_obj = self.pool['ir.model.data']
        iaaw_obj = self.pool['ir.actions.act_window']
        purl_obj = self.pool['purchase.order.line']

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
            proc_ids = proc_obj.search(cr, uid, [
                ('production_id', '=', mp.id),
            ], context=context)
            if len(proc_ids) != 1:
                raise except_osv(_('Error: Procurement Not Found!'), _(
                    "The associated Procurement Order has not be found for"
                    " the Manufacturing Order %s.\n In that case, please"
                    " simply cancel this Production Order and create a"
                    "Purchase Order.") % (mp.name))
            proc = proc_obj.browse(cr, uid, proc_ids[0], context=context)
            good_move_id = proc.move_id.id

            # Check that product has a Seller defined
            if not proc.product_id.seller_id:
                raise except_osv(_('Error: Seller Not Found!'), _(
                    "The product %s has no Seller associated. Please"
                    " associate a Seller to this product in the procurement"
                    " view of the product.") % (
                        proc.product_id.name))

            # Unlink the production_id from the Procurement Order to avoid
            # that cancel mrp.production impact the initial Procurement Order
            proc_obj.write(cr, uid, [proc.id], {
                'production_id': False}, context=context)

            # Unlink the move_prod_id from the Production Order to avoid
            # that cancel mrp.production impact the good Stock Move
            self.write(cr, uid, [mp.id], {
                'move_prod_id': False}, context=context)

            # Get moves associated to the picking to unlink
            sm_ids_extra = sm_obj.search(cr, uid, [
                ('picking_id', '=', mp.picking_id.id)], context=context)

            # Get Extra Procurement Order to Cancel
            proc_ids_to_cancel = proc_obj.search(cr, uid, [
                ('move_id', 'in', sm_ids_extra)], context=context)

            proc_obj.action_cancel(
                cr, uid, proc_ids_to_cancel)

            # Cancel Picking associated to the mrp.production
            wf_service.trg_validate(
                uid, 'stock.picking', mp.picking_id.id, 'button_cancel', cr)

            # Cancel Production Order
            self.action_cancel(cr, uid, [mp.id], context=context)

            # Set the Procurement in the correct state:
            # from 'produce' to 'confirm'
            act_produce_id = imd_obj.get_object_reference(
                cr, uid, 'mrp', 'act_produce')[1]
            act_confirm_id = imd_obj.get_object_reference(
                cr, uid, 'procurement', 'act_confirm')[1]
            cr.execute("""
                SELECT id
                FROM wkf_workitem
                WHERE inst_id = (
                    SELECT id
                    FROM wkf_instance
                    WHERE res_id = %s)
                AND act_id = %s;
                """, (proc.id, act_produce_id))
            proc_item_id = cr.fetchone()[0]
            cr.execute("""
                UPDATE wkf_workitem
                SET subflow_id = Null, state='complete', act_id = %s
                WHERE id = %s""", (act_confirm_id, proc_item_id))

            proc_obj.write(cr, uid, [proc.id], {
                'state': 'confirmed'}, context=context)
            # Create a Purchase Order by the classic process
            pur_id = proc_obj.make_po(
                cr, uid, [proc.id], context=context)[proc.id]

            pur_ids.append(pur_id)

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

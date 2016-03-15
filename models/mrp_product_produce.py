# _*_ coding: utf-8 _*_
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class ProductLine(models.Model):
    _inherit = "mrp.product.produce.line"

    # qty_available = fields.Float(compute="_compute_qty_available")
    #
    # @api.multi
    # @api.depends("product_id")
    # def _compute_qty_available(self):
    #     production_id = self.env.context.get('active_id', False)
    #     production = self.env["mrp.production"].browse(production_id)
    #     routing_location_id = production.routing_id.location_id.id if production.routing_id else None
    #     for line in self:
    #         if production_id:
    #             move = production.move_lines.filtered(lambda m: m.product_id.id == line.product_id.id)
    #             if move and len(move) == 1:
    #                 location_ids = [production.location_src_id.id]
    #                 if routing_location_id:
    #                     location_ids.append(routing_location_id)
    #
    #                 quants = self.env["stock.quant"].search(
    #                         [("location_id", "in", location_ids), ("product_id", "=", line.product_id.id)])
    #
    #                 line.qty_available = sum(quants.mapped("qty"))


class Produce(models.Model):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        self.ensure_one()
        for line in self.consume_lines:
            production_id = self.env.context.get('active_id', False)
            production = self.env["mrp.production"].browse(production_id)
            assigned_count = production.get_assigned_count(line.product_id.id)
            if line.product_qty > assigned_count:
                raise Warning(_("product %s quality %d not available") % (line.product_id.name, line.product_qty))


        return super(Produce, self).do_produce()

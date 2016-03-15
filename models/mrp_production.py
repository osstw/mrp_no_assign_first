# _*_ coding: utf-8 _*_
from openerp import models, fields, api


class Production(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def test_ready(self):
        return True

    @api.multi
    def get_assigned_count(self, product_id):
        self.ensure_one()
        if not isinstance(product_id, int):
            return None

        move = self.move_lines.filtered(lambda m: m.product_id.id == product_id)
        move.ensure_one()
        if move:
            return sum(quant.qty for quant in move.reserved_quant_ids)

# _*_ coding: utf-8 _*_
from openerp import models, fields, api


class Production(models.Model):
    _inherit = "mrp.production"

    @api.multi
    def test_ready(self):
        return True

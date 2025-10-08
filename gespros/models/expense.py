# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import AccessError

class ProduitDepartement(models.Model):
    _inherit = "product.product"

    departement_id = fields.Many2one("hr.department", string="Departement")
# -*- coding: utf-8 -*-
from odoo import models, fields

from .projets import TYPE_D_SELECTION

class ProduitDepartement(models.Model):
    _inherit = "product.product"

    type_d = fields.Selection(
        TYPE_D_SELECTION,
        string="Type de Dossier",
        default='operations',
        help="Type de dossier associé à ce produit.",
    )

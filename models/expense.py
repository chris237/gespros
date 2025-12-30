# -*- coding: utf-8 -*-
from odoo import models, fields, api

from .projets import TYPE_D_SELECTION

class ProduitDepartement(models.Model):
    _inherit = "product.product"

    type_d = fields.Selection(
        TYPE_D_SELECTION,
        string="Type de Dossier",
        default='operations',
        help="Type de dossier associé à ce produit.",
    )


class HrExpense(models.Model):
    _inherit = "hr.expense"

    def _prepare_move_values(self):
        self.ensure_one()
        res = super()._prepare_move_values()
        proj_num = self.proj_id.num_d if self.proj_id else False
        if proj_num:
            existing_ref = res.get('ref')
            res['ref'] = f"{existing_ref} - {proj_num}" if existing_ref else proj_num
            res['proj_id'] = self.proj_id.id
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    proj_id = fields.Many2one("gespros.project", string='Dossier N')
    report_lang = fields.Selection(
        selection=lambda self: self.env['res.lang'].get_installed(),
        string="Langue du document",
        default=lambda self: self._get_default_report_lang(),
        tracking=True,
    )

    @api.model
    def _get_default_report_lang(self):
        partner_lang = self.partner_id.lang if self.partner_id else False
        return partner_lang or self.env.lang

    @api.onchange('partner_id')
    def _onchange_partner_language(self):
        if self.partner_id:
            self.report_lang = self.partner_id.lang or self.env.lang

    def _get_report_base_filename(self):
        self.ensure_one()
        report_lang = self.report_lang or self.env.lang
        return super(AccountMove, self.with_context(lang=report_lang))._get_report_base_filename()

    def action_invoice_print(self):
        report_lang = self.report_lang or self.env.lang
        return super(AccountMove, self.with_context(lang=report_lang)).action_invoice_print()

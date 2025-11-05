# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.exceptions import AccessError

class Projets(models.Model):
    _name = "gespros.project"
    _description = "Projets Operation"
    _rec_name = "num_d"
    _inherit = [
        'portal.mixin',
        'mail.thread.cc',
        'mail.activity.mixin',
        'mail.tracking.duration.mixin',
        'html.field.history.mixin',
    ]

    num_d = fields.Char(string='Numero de Dossier', required=True, tracking=True)
    client_id = fields.Many2one("res.partner", string='Client', tracking=True)
    pc = fields.Char(string="P/C", required=True, tracking=True)
    date = fields.Date(string="Date", tracking=True)
    ref = fields.Char(string="Ref Client", tracking=True)
    bl = fields.Char(string="BL/AWB N", required=True, tracking=True)
    typ = fields.Char(string="Type TC", required=True, tracking=True)
    description = fields.Char(string="Description Marchandise", required=True, tracking=True)
    quantite = fields.Char(string="Quantite", required=True, tracking=True)
    poids = fields.Char(string="POIDS", required=True, tracking=True)
    valeur = fields.Monetary('Valeur Douanes', currency_field='currency_id' , tracking=True)
    state = fields.Selection([
        ('draft', 'Brouillons'),
        ('in_progress', 'En cours'),
        ('done', 'Terminee'),
        ('cancel', 'Annule')
    ], string='Status', copy=False, default='draft', tracking=True)

    Type_d = fields.Selection([
        ('operations', 'Operations'),
        ('lcl', 'LCL'),
        ('shipping', 'Shipping')
    ], string='Type de Dossier', copy=False, default='operations', tracking=True)


    line_ids = fields.One2many('hr.expense', 
                               'proj_id', 
                               string='Fees Collection Details',
                               tracking=True)

    date = fields.Date(string="Date de debut ", default=fields.Date.context_today, tracking=True)
    datef = fields.Date(string="Date de Fin ", readonly = True, tracking=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="resp. Prededouanement ", precompute=True, store=True, readonly=False,
        check_company=True,
        tracking=True,
    )

    dedouanement_id = fields.Many2one(
        comodel_name='hr.employee',
        string="resp. Dedouanement ", precompute=True, store=True, readonly=False,
        check_company=True,
        tracking=True,
    )

    date_dedoua = fields.Date(string="Date de debut Dedouanement ", tracking=True)


    transport_id = fields.Many2one(
        comodel_name='hr.employee',
        string="resp. Transport ", precompute=True, store=True, readonly=False,
        check_company=True,
        tracking=True,
    )
    
    date_tra = fields.Date(string="Date de debut Transport", tracking=True)

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.currency_id = \
                template.company_id.sudo().currency_id.id or main_company.currency_id.id

    bl_num = fields.Char(string="BL N°", tracking=True)
    shipping_line = fields.Char(string="SHIPPING LINE°", tracking=True)
    vessel = fields.Char(string="VESSEL NAME°", tracking=True)
    voyage = fields.Char(string="VOYAGE N°", tracking=True)
    container = fields.Char(string="CONTAINER N°", tracking=True)
    date_prealert = fields.Date(string="DATE DE PREALERT", tracking=True)
    eta = fields.Date(string="ETA Douala", tracking=True)
    state_cle = fields.Date(string="STATUS OF CLEARANCE", tracking=True)
    comple_cle = fields.Date(string="CLEARANCE COMPLETED  ETC", tracking=True)
    ship_trans = fields.Date(string="SHIPMENT TRANSFER TO ASSA WH", tracking=True)
    sortie = fields.Date(string="SORTIE AUTORISE DANS LE SYSTÈME", tracking=True)
    storage = fields.Date(string="STORAGE  DATE", tracking=True)


    currency_id = fields.Many2one(
        'res.currency', string='Devise',
        default=lambda self: self.env.user.company_id.currency_id.id)

    def confirm(self):
        if self.state == 'draft':
            self.state = "in_progress"
        else:
            raise AccessError(_("Je suis curieux de savoir comment tu as fait pour voir ce bouton à cette étape."))

    def cancel(self):
        if self.state != 'done':
            self.state = 'cancel'
        else:
            raise AccessError(_("Désolé, vous ne pouvez pas annuler un dossier déjà terminé."))

    def close(self):
        if self.state == 'in_progress':
            self.state = 'done'
        else:
            raise AccessError(_("Je suis curieux de savoir comment tu as fait pour voir ce bouton à cette étape."))

    def reset_to_draft(self):
        if self.state != 'draft':
            self.state = 'draft'
        else:
            raise AccessError(_("Je suis curieux de savoir comment tu as fait pour voir ce bouton à cette étape."))


    @api.onchange('state')
    def _onchange_state(self):
        """Override the view readonly depending on state."""
        for record in self:
            record._compute_readonly()

    def _compute_readonly(self):
        """Helper to compute readonly in form view via attrs."""
        pass  # La logique se gère dans la vue via attrs="{'readonly': [('state', '!=', 'draft')]}".


class HrExpense(models.Model):
    _inherit = "hr.expense"

    proj_id = fields.Many2one("gespros.project", string='Dossier N', required=True)

    departement_id = fields.Many2one("hr.department", string="Departement")

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Category",
        tracking=True,
        check_company=True,
        domain=[('can_be_expensed', '=', True)],
        ondelete='restrict',
    )

class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    proj_id = fields.Many2one("gespros.project", string='Dossier N', 
                            #   compute = '_proj_c',
                              )

    departement_id = fields.Many2one("hr.department", string="Departement")

    # @api.depends('')
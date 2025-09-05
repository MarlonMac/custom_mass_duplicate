# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    target_company_id = fields.Many2one('res.company', string='Target Company', required=True)
    target_website_id = fields.Many2one('website', string='Target Website', required=True, domain="[('company_id', '=', target_company_id)]")
    copy_cost = fields.Boolean(string="Copy Cost Price", default=True)

    apply_price_markup = fields.Boolean(string="Adjust Sale Price", help="Check this box to apply a percentage increase to the sale price...")
    price_markup_percent = fields.Float(string="Sale Price Markup (%)")

    source_currency_id = fields.Many2one('res.currency', string="Source Currency", compute='_compute_currency_info')
    target_currency_id = fields.Many2one('res.currency', string="Target Currency", compute='_compute_currency_info')
    rate_display = fields.Char(string="Exchange Rate", compute='_compute_currency_info')
    conversion_needed = fields.Boolean(compute='_compute_currency_info')
    
    use_manual_rate = fields.Boolean(string="Use Manual Exchange Rate")
    manual_rate_type = fields.Selection([
        ('divisor', 'Divisor (e.g., 7.79)'),
        ('multiplier', 'Multiplier (e.g., 0.128)')
    ], string="Manual Rate Type", default='divisor')
    manual_rate = fields.Float(string="Manual Rate", digits='(12, 10)')

    @api.depends('target_company_id')
    def _compute_currency_info(self):
        for wizard in self:
            source_company = self.env.company
            wizard.source_currency_id = source_company.currency_id
            rate_text = _("No conversion needed.")
            needs_conversion = False
            if wizard.target_company_id:
                target_company = wizard.target_company_id
                wizard.target_currency_id = target_company.currency_id
                if wizard.source_currency_id and wizard.target_currency_id and wizard.source_currency_id != wizard.target_currency_id:
                    needs_conversion = True
                    try:
                        rate = wizard.source_currency_id._get_conversion_rate(
                            wizard.source_currency_id, wizard.target_currency_id,
                            target_company, fields.Date.today()
                        )
                        rate_text = _("Odoo Rate (Multiplier): %s") % (round(rate, 10))
                    except UserError:
                        rate_text = _("Warning: No Odoo rate configured.")
            else:
                wizard.target_currency_id = False
            wizard.rate_display = rate_text
            wizard.conversion_needed = needs_conversion

    def action_duplicate_products(self):
        product_ids = self.env.context.get('active_ids', [])
        
        if self.use_manual_rate and self.manual_rate <= 0:
            raise UserError(_("The manual exchange rate must be a positive number."))
        if self.apply_price_markup and self.price_markup_percent == 0:
            raise UserError(_("Sale Price Markup is checked but the percentage is zero."))

        job_vals = {
            'product_template_ids': [(6, 0, product_ids)],
            'target_company_id': self.target_company_id.id,
            'target_website_id': self.target_website_id.id,
            'user_id': self.env.user.id,
            'copy_cost': self.copy_cost,
        }
        
        if self.conversion_needed:
            if self.use_manual_rate:
                job_vals['exchange_rate_to_use'] = self.manual_rate
                job_vals['rate_type'] = self.manual_rate_type
            else:
                rate_mult = self.source_currency_id._get_conversion_rate(
                    self.source_currency_id, self.target_currency_id,
                    self.target_company_id, fields.Date.today()
                )
                if not rate_mult:
                     raise UserError(_("Could not determine the Odoo exchange rate. Please set a manual rate to proceed."))
                job_vals['exchange_rate_to_use'] = rate_mult
                job_vals['rate_type'] = 'multiplier'
        
        if self.apply_price_markup:
            job_vals['apply_price_markup'] = True
            job_vals['price_markup_percent'] = self.price_markup_percent

        self.env['product.duplication.job'].create(job_vals)
        return {
            'type': 'ir.actions.client', 'tag': 'display_notification',
            'params': { 'title': _("Operation Scheduled"), 'message': _("Duplication of %d products has been scheduled.") % len(product_ids), 'type': 'success', 'sticky': True }
        }
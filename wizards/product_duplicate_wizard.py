# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    # ... (campos existentes sin cambios) ...
    target_company_id = fields.Many2one('res.company', string='Target Company', required=True)
    target_website_id = fields.Many2one('website', string='Target Website', required=True, domain="[('company_id', '=', target_company_id)]")
    copy_cost = fields.Boolean(
        string="Copy Cost Price", 
        default=True,
        help="If checked, the cost price ('standard_price') of the products will be copied and converted to the target company's currency. Leave unchecked to set the cost to 0."
    )
    source_currency_id = fields.Many2one('res.currency', string="Source Currency", compute='_compute_currency_info')
    target_currency_id = fields.Many2one('res.currency', string="Target Currency", compute='_compute_currency_info')
    rate_display = fields.Char(string="Exchange Rate", compute='_compute_currency_info')
    conversion_needed = fields.Boolean(compute='_compute_currency_info')
    use_manual_rate = fields.Boolean(string="Use Manual Exchange Rate")
    manual_rate = fields.Float(string="Manual Rate", digits='(12, 6)')

    # --- NUEVO CAMPO PARA LA ETIQUETA ---
    manual_rate_label = fields.Char(string="Rate Label", compute='_compute_currency_info')

    @api.depends('target_company_id')
    def _compute_currency_info(self):
        """Calcula y muestra la información de monedas y si la conversión es necesaria."""
        for wizard in self:
            source_company = self.env.company
            wizard.source_currency_id = source_company.currency_id
            
            rate_text = _("No conversion needed.")
            needs_conversion = False
            label = ""
            
            if wizard.target_company_id:
                target_company = wizard.target_company_id
                wizard.target_currency_id = target_company.currency_id

                if wizard.source_currency_id and wizard.target_currency_id and wizard.source_currency_id != wizard.target_currency_id:
                    needs_conversion = True
                    # Construimos la etiqueta para la tasa manual
                    label = f"1 {wizard.source_currency_id.symbol} ="
                    try:
                        rate = wizard.source_currency_id._get_conversion_rate(
                            wizard.source_currency_id, wizard.target_currency_id,
                            target_company, fields.Date.today()
                        )
                        rate_text = _("1 %s = %s %s (Odoo Rate)") % (
                            wizard.source_currency_id.symbol, round(rate, 6), wizard.target_currency_id.symbol
                        )
                    except UserError:
                        rate_text = _("Warning: No rate configured in Odoo.")
            else:
                wizard.target_currency_id = False

            wizard.rate_display = rate_text
            wizard.conversion_needed = needs_conversion
            wizard.manual_rate_label = label

    def action_duplicate_products(self):
        # ... (Este método no necesita cambios) ...
        """Crea el job con toda la configuración del wizard."""
        product_ids = self.env.context.get('active_ids', [])
        
        if self.use_manual_rate and self.manual_rate <= 0:
            raise UserError(_("The manual exchange rate must be a positive number."))

        job_vals = {
            'product_template_ids': [(6, 0, product_ids)],
            'target_company_id': self.target_company_id.id,
            'target_website_id': self.target_website_id.id,
            'user_id': self.env.user.id,
            'copy_cost': self.copy_cost,
        }
        
        if self.use_manual_rate:
            job_vals['manual_exchange_rate'] = self.manual_rate

        self.env['product.duplication.job'].create(job_vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Operation Scheduled"),
                'message': _("Duplication of %d products has been scheduled to run in the background.") % len(product_ids),
                'type': 'success',
                'sticky': True,
            }
        }
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    target_company_id = fields.Many2one('res.company', string='Target Company', required=True)
    target_website_id = fields.Many2one('website', string='Target Website', required=True, domain="[('company_id', '=', target_company_id)]")
    copy_cost = fields.Boolean(
        string="Copy Cost Price", 
        default=False,
        help="If checked, the cost price ('standard_price') of the products will be copied and converted to the target company's currency. Leave unchecked to set the cost to 0."
    )

    def action_duplicate_products(self):
        """Ahora esta acción solo crea un job y lo pone en la cola."""
        product_ids = self.env.context.get('active_ids', [])
        
        self.env['product.duplication.job'].create({
            'product_template_ids': [(6, 0, product_ids)],
            'target_company_id': self.target_company_id.id,
            'target_website_id': self.target_website_id.id,
            'user_id': self.env.user.id,
            'copy_cost': self.copy_cost, # <-- PASAMOS EL NUEVO VALOR
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Operation Scheduled"),
                'message': _("Duplication of %d products has been scheduled to run in the background. Check status under Inventory > Operations > Duplication Jobs.") % len(product_ids),
                'type': 'success',
                'sticky': True,
            }
        }
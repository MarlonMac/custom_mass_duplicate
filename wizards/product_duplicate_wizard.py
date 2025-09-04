# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    target_company_id = fields.Many2one(
        'res.company', 
        string='Target Company', 
        required=True,
        help="The company to which the products will be duplicated."
    )
    target_website_id = fields.Many2one(
        'website', 
        string='Target Website', 
        required=True,
        domain="[('company_id', '=', target_company_id)]",
        help="The website where the new products will be published."
    )

    def action_duplicate_products(self):
        product_template_ids = self.env.context.get('active_ids', [])
        if not product_template_ids:
            raise UserError(_("You must select at least one product to duplicate."))

        templates = self.env['product.template'].browse(product_template_ids)
        
        for template in templates:
            default_values = {
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
            }
            # Usamos sudo() para evitar problemas de permisos al copiar a otra compañía.
            new_template = template.sudo().copy(default_values)

            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    
                    # Usamos sudo() de nuevo para la búsqueda y escritura en la otra compañía.
                    existing = self.env['product.product'].sudo().search([
                        ('default_code', '=', original_variant.default_code),
                        ('company_id', '=', self.target_company_id.id),
                        ('id', '!=', new_variant.id)
                    ], limit=1)
                    
                    if not existing and original_variant.default_code:
                        # Actualizamos el código interno solo si no existe en la compañía destino.
                        new_variant.sudo().write({'default_code': original_variant.default_code})
        
        return {'type': 'ir.actions.act_window_close'}
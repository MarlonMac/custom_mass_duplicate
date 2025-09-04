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
        """
        Main method to perform the duplication.
        It iterates through the selected product.template records and uses
        the Odoo ORM's copy() method, which is the standard and safe way
        to duplicate records. It handles the duplication of related fields
        (like secondary images) automatically.
        """
        product_template_ids = self.env.context.get('active_ids', [])
        if not product_template_ids:
            raise UserError(_("You must select at least one product to duplicate."))

        templates = self.env['product.template'].browse(product_template_ids)
        
        for template in templates:
            # Prepare the dictionary with values to override in the new copy.
            default_values = {
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
                # By not specifying 'name' or 'default_code', we let the copy()
                # method handle them. We will then update the default_code
                # of the variants manually to ensure it's preserved.
            }
            
            # The copy() method is secure as it runs within the ORM's
            # access rights framework. It safely duplicates the record
            # and its related one2many fields (like product_template_image_ids).
            new_template = template.copy(default_values)

            # Odoo's default copy() might alter the default_code on variants
            # to avoid unique constraint errors. We will restore them.
            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    # Check if a product with the same internal reference already exists
                    # in the target company to avoid unique constraint errors.
                    existing = self.env['product.product'].search([
                        ('default_code', '=', original_variant.default_code),
                        ('company_id', '=', self.target_company_id.id),
                        ('id', '!=', new_variant.id)
                    ], limit=1)
                    
                    if not existing and original_variant.default_code:
                        new_variant.write({'default_code': original_variant.default_code})
        
        return {'type': 'ir.actions.act_window_close'}
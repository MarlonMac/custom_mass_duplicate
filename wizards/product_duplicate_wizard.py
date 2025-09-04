# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

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
        original_templates = self.env['product.template'].browse(self.env.context.get('active_ids', []))
        if not original_templates:
            raise UserError(_("You must select at least one product to duplicate."))

        # --- PASADA 1: CREAR TODOS LOS PRODUCTOS Y CONSTRUIR MAPAS DE IDs ---
        template_id_map = {} # Mapa de {original_tmpl_id: new_tmpl_id}
        variant_id_map = {}  # Mapa de {original_variant_id: new_variant_id}

        for template in original_templates:
            # Usamos el comando (6, 0, []) que significa "reemplazar con una lista vacía".
            # Este es más seguro que (5, 0, 0) y evita conflictos de Foreign Key.
            default_values = {
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
                'accessory_product_ids': [(6, 0, [])],
                'alternative_product_ids': [(6, 0, [])],
                'optional_product_ids': [(6, 0, [])],
            }
            new_template = template.sudo().copy(default_values)
            template_id_map[template.id] = new_template.id

            # Mapear variantes y corregir sus default_code
            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    variant_id_map[original_variant.id] = new_variant.id
                    
                    # Corregir default_code
                    existing = self.env['product.product'].sudo().search([
                        ('default_code', '=', original_variant.default_code),
                        ('company_id', '=', self.target_company_id.id),
                        ('id', '!=', new_variant.id)
                    ], limit=1)
                    
                    if not existing and original_variant.default_code:
                        new_variant.sudo().write({'default_code': original_variant.default_code})

        _logger.info(f"Pasada 1 completada. {len(template_id_map)} productos y {len(variant_id_map)} variantes mapeadas.")

        # --- PASADA 2: RECONSTRUIR LAS RELACIONES ---
        ProductProduct = self.env['product.product'].sudo()
        ProductTemplate = self.env['product.template'].sudo()

        for original_template in original_templates:
            new_template = ProductTemplate.browse(template_id_map.get(original_template.id))
            if not new_template:
                continue

            # --- Mapeo de Productos Alternativos (product.template -> product.template) ---
            if original_template.alternative_product_ids:
                target_alternative_ids = []
                for alt_tmpl in original_template.alternative_product_ids:
                    if alt_tmpl.id in template_id_map:
                        target_alternative_ids.append(template_id_map[alt_tmpl.id])
                    else:
                        # Fallback a buscar por referencia del template (si existe y es única)
                        if alt_tmpl.default_code:
                            found = ProductTemplate.search([('default_code', '=', alt_tmpl.default_code), ('company_id', '=', self.target_company_id.id)], limit=1)
                            if found:
                                target_alternative_ids.append(found.id)
                if target_alternative_ids:
                    new_template.write({'alternative_product_ids': [(6, 0, target_alternative_ids)]})

            # --- Mapeo de Accesorios y Opcionales (product.template -> product.product) ---
            m2m_variant_fields = ['accessory_product_ids', 'optional_product_ids']
            for field_name in m2m_variant_fields:
                original_variants = original_template.sudo()[field_name]
                if original_variants:
                    target_variant_ids = []
                    for original_variant in original_variants:
                        if original_variant.id in variant_id_map:
                            target_variant_ids.append(variant_id_map[original_variant.id])
                        else:
                            # Fallback a buscar por referencia interna de la variante
                            if original_variant.default_code:
                                found = ProductProduct.search([('default_code', '=', original_variant.default_code), ('company_id', '=', self.target_company_id.id)], limit=1)
                                if found:
                                    target_variant_ids.append(found.id)
                    if target_variant_ids:
                        new_template.write({field_name: [(6, 0, target_variant_ids)]})

        _logger.info("Pasada 2 completada. Relaciones reconstruidas.")

        return {'type': 'ir.actions.act_window_close'}
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    # ... (los campos del wizard no cambian)
    target_company_id = fields.Many2one('res.company', string='Target Company', required=True)
    target_website_id = fields.Many2one('website', string='Target Website', required=True, domain="[('company_id', '=', target_company_id)]")

    def _get_target_template_ids(self, original_templates, id_map):
        """
        Finds the corresponding target templates.
        First, it checks the map of newly created products.
        If not found, it falls back to searching by default_code.
        """
        target_ids = []
        ProductTemplate = self.env['product.template'].sudo()
        
        for original_tmpl in original_templates:
            # Prioridad 1: Buscar en el mapa de productos recién creados en este lote
            if original_tmpl.id in id_map:
                target_ids.append(id_map[original_tmpl.id])
            # Prioridad 2: Buscar por referencia interna si no estaba en el lote
            elif original_tmpl.default_code:
                # Nota: Buscamos product.template directamente por default_code
                target_tmpl = ProductTemplate.search([
                    ('default_code', '=', original_tmpl.default_code),
                    ('company_id', '=', self.target_company_id.id),
                ], limit=1)
                if target_tmpl:
                    target_ids.append(target_tmpl.id)
        return target_ids

    def action_duplicate_products(self):
        original_templates = self.env['product.template'].browse(self.env.context.get('active_ids', []))
        if not original_templates:
            raise UserError(_("You must select at least one product to duplicate."))

        # --- PASADA 1: CREAR TODOS LOS PRODUCTOS Y CONSTRUIR UN MAPA DE IDs ---
        id_map = {} # Mapa de {original_tmpl_id: new_tmpl_id}
        new_templates_to_process = self.env['product.template']

        for template in original_templates:
            default_values = {
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
                # Limpiamos las relaciones para llenarlas en la Pasada 2
                'accessory_product_ids': [(5, 0, 0)],
                'alternative_product_ids': [(5, 0, 0)],
                'optional_product_ids': [(5, 0, 0)],
            }
            new_template = template.sudo().copy(default_values)
            id_map[template.id] = new_template.id
            new_templates_to_process |= new_template

            # Corregir la referencia interna de las variantes sigue siendo importante aquí
            # ... (código de corrección de default_code)

        _logger.info(f"Pasada 1 completada. {len(id_map)} productos creados.")

        # --- PASADA 2: RECONSTRUIR LAS RELACIONES USANDO EL MAPA ---
        for original_template in original_templates:
            new_template = self.env['product.template'].sudo().browse(id_map[original_template.id])
            
            # Mapear productos accesorios
            if original_template.accessory_product_ids:
                target_accessory_ids = self._get_target_template_ids(original_template.accessory_product_ids, id_map)
                if target_accessory_ids:
                    new_template.write({'accessory_product_ids': [(6, 0, target_accessory_ids)]})

            # Mapear productos alternativos
            if original_template.alternative_product_ids:
                target_alternative_ids = self._get_target_template_ids(original_template.alternative_product_ids, id_map)
                if target_alternative_ids:
                    new_template.write({'alternative_product_ids': [(6, 0, target_alternative_ids)]})

            # Mapear productos opcionales
            if original_template.optional_product_ids:
                # Los opcionales son product.product, manejamos la lógica un poco diferente
                target_optional_ids = self._get_target_template_ids(original_template.optional_product_ids.mapped('product_tmpl_id'), id_map)
                if target_optional_ids:
                    # Necesitamos los product.product, no los templates
                    final_variants = self.env['product.template'].browse(target_optional_ids).mapped('product_variant_id')
                    new_template.write({'optional_product_ids': [(6, 0, final_variants.ids)]})

        _logger.info(f"Pasada 2 completada. Relaciones reconstruidas.")

        return {'type': 'ir.actions.act_window_close'}
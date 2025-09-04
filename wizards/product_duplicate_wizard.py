# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ProductDuplicateWizard(models.TransientModel):
    _name = 'product.duplicate.wizard'
    _description = 'Wizard to Mass Duplicate Products to a Company'

    target_company_id = fields.Many2one('res.company', string='Target Company', required=True)
    target_website_id = fields.Many2one('website', string='Target Website', required=True, domain="[('company_id', '=', target_company_id)]")

    def action_duplicate_products(self):
        original_templates = self.env['product.template'].browse(self.env.context.get('active_ids', []))
        if not original_templates:
            raise UserError(_("You must select at least one product to duplicate."))

        # --- PASADA 1: CREAR TODOS LOS PRODUCTOS BÁSICOS (SIN RELACIONES) ---
        template_id_map = {} # Mapa de {original_tmpl_id: new_tmpl_id}
        variant_id_map = {}  # Mapa de {original_variant_id: new_variant_id}

        for template in original_templates:
            copy_data = template.sudo().copy_data()[0]
            
            # Excluimos los campos de relación para reconstruirlos después.
            # 'optional_product_ids' se excluye permanentemente en v1.0.0 para evitar errores.
            fields_to_pop = ['accessory_product_ids', 'alternative_product_ids', 'optional_product_ids']
            for field in fields_to_pop:
                copy_data.pop(field, None)

            copy_data.update({
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
            })
            
            new_template = self.env['product.template'].sudo().create(copy_data)
            template_id_map[template.id] = new_template.id

            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    variant_id_map[original_variant.id] = new_variant.id
                    if original_variant.default_code:
                        existing = self.env['product.product'].sudo().search([
                            ('default_code', '=', original_variant.default_code),
                            ('company_id', '=', self.target_company_id.id),
                            ('id', '!=', new_variant.id)
                        ], limit=1)
                        if not existing:
                            new_variant.sudo().write({'default_code': original_variant.default_code})
                        else:
                            _logger.warning(f"Conflicto de Ref. Interna omitido para: {original_variant.default_code}")

        _logger.info(f"Pasada 1 completada. {len(template_id_map)} productos y {len(variant_id_map)} variantes mapeadas.")

        # --- PASADA 2: RECONSTRUIR LAS RELACIONES (EXCEPTO OPCIONALES) ---
        ProductProduct = self.env['product.product'].sudo()
        ProductTemplate = self.env['product.template'].sudo()

        for original_template in original_templates:
            new_template = ProductTemplate.browse(template_id_map.get(original_template.id))
            if not new_template: continue

            # Mapeo de Productos Alternativos (product.template -> product.template)
            if original_template.alternative_product_ids:
                target_alternative_ids = []
                for alt_tmpl in original_template.alternative_product_ids:
                    target_id = template_id_map.get(alt_tmpl.id)
                    if target_id:
                        target_alternative_ids.append(target_id)
                    elif alt_tmpl.product_variant_count > 0 and alt_tmpl.product_variant_id.default_code:
                        found = ProductProduct.search([
                            ('default_code', '=', alt_tmpl.product_variant_id.default_code), 
                            ('company_id', '=', self.target_company_id.id)
                        ], limit=1)
                        if found:
                            target_alternative_ids.append(found.product_tmpl_id.id)
                if target_alternative_ids:
                    new_template.write({'alternative_product_ids': [(6, 0, target_alternative_ids)]})

            # Mapeo de Accesorios (product.template -> product.product)
            if original_template.accessory_product_ids:
                target_variant_ids = []
                for original_variant in original_template.accessory_product_ids:
                    target_id = variant_id_map.get(original_variant.id)
                    if target_id:
                        target_variant_ids.append(target_id)
                    elif original_variant.default_code:
                        found = ProductProduct.search([
                            ('default_code', '=', original_variant.default_code),
                            ('company_id', '=', self.target_company_id.id)
                        ], limit=1)
                        if found:
                            target_variant_ids.append(found.id)
                if target_variant_ids:
                    new_template.write({'accessory_product_ids': [(6, 0, target_variant_ids)]})

        _logger.warning("El campo 'optional_product_ids' se omite intencionadamente en v1.0.0 debido a una restricción de BD en ciertos entornos.")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Duplication Complete"),
                'message': _("Successfully duplicated %d products. Optional products must be linked manually.") % len(template_id_map),
                'type': 'success',
                'sticky': True, # Hacemos la notificación "pegajosa" para que el usuario lea el mensaje.
            }
        }
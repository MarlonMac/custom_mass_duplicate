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
            # CLAVE: Usar copy_data() para obtener los datos y luego modificarlos
            # antes de crear el registro. Esto evita que copy() intente duplicar
            # las relaciones problemáticas.
            copy_data = template.sudo().copy_data()[0]
            
            # Remover las relaciones problemáticas de los datos de copia
            problematic_fields = [
                'accessory_product_ids', 
                'alternative_product_ids', 
                'optional_product_ids'
            ]
            for field in problematic_fields:
                copy_data.pop(field, None)
            
            # Establecer la empresa y website de destino
            copy_data.update({
                'company_id': self.target_company_id.id,
                'website_id': self.target_website_id.id,
            })
            
            # Crear el nuevo template con los datos limpios
            new_template = self.env['product.template'].sudo().create(copy_data)
            template_id_map[template.id] = new_template.id

            # Mapear variantes y corregir sus default_code si es necesario
            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    variant_id_map[original_variant.id] = new_variant.id
                    
                    # Verificar y establecer default_code si no hay conflicto
                    if original_variant.default_code:
                        existing = self.env['product.product'].sudo().search([
                            ('default_code', '=', original_variant.default_code),
                            ('company_id', '=', self.target_company_id.id),
                            ('id', '!=', new_variant.id)
                        ], limit=1)
                        
                        if not existing:
                            new_variant.sudo().write({'default_code': original_variant.default_code})
                        else:
                            _logger.warning(f"Referencia interna '{original_variant.default_code}' ya existe en la empresa destino. Se omite para evitar conflictos.")

        _logger.info(f"Pasada 1 completada. {len(template_id_map)} productos y {len(variant_id_map)} variantes mapeadas.")

        # --- PASADA 2: RECONSTRUIR LAS RELACIONES DE FORMA SEGURA ---
        ProductProduct = self.env['product.product'].sudo()
        ProductTemplate = self.env['product.template'].sudo()

        for original_template in original_templates:
            new_template = ProductTemplate.browse(template_id_map.get(original_template.id))
            if not new_template:
                continue

            # --- Relaciones Template -> Template (Productos Alternativos) ---
            if original_template.alternative_product_ids:
                target_alternative_ids = []
                for alt_tmpl in original_template.alternative_product_ids:
                    target_id = template_id_map.get(alt_tmpl.id)
                    if target_id:
                        target_alternative_ids.append(target_id)
                    elif alt_tmpl.product_variant_count > 0 and alt_tmpl.product_variant_id.default_code:
                        # Búsqueda por la referencia de la variante, que es más fiable
                        found = ProductProduct.search([
                            ('default_code', '=', alt_tmpl.product_variant_id.default_code), 
                            ('company_id', '=', self.target_company_id.id)
                        ], limit=1)
                        if found:
                            target_alternative_ids.append(found.product_tmpl_id.id)
                
                if target_alternative_ids:
                    new_template.write({'alternative_product_ids': [(6, 0, target_alternative_ids)]})

            # --- Relaciones Template -> Product (Accesorios y Opcionales) ---
            m2m_variant_fields = ['accessory_product_ids', 'optional_product_ids']
            for field_name in m2m_variant_fields:
                original_variants = original_template.sudo()[field_name]
                if original_variants:
                    target_variant_ids = []
                    for original_variant in original_variants:
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
                        new_template.write({field_name: [(6, 0, target_variant_ids)]})

        _logger.info("Pasada 2 completada. Relaciones reconstruidas de forma segura.")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Duplication Complete"),
                'message': _("Successfully duplicated %d products to %s") % (len(template_id_map), self.target_company_id.name),
                'type': 'success',
                'sticky': False,
            }
        }
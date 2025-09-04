# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import traceback

_logger = logging.getLogger(__name__)

class ProductDuplicationJob(models.Model):
    _name = 'product.duplication.job'
    # ... (resto de la definición del modelo) ...
    _description = 'Mass Product Duplication Job'
    _order = 'create_date desc'

    name = fields.Char(compute='_compute_name', store=True)
    state = fields.Selection([
        ('pending', 'Pending'), ('in_progress', 'In Progress'),
        ('done', 'Done'), ('failed', 'Failed'),
    ], default='pending', index=True, required=True, copy=False)
    user_id = fields.Many2one('res.users', string='Requested by', default=lambda self: self.env.user, readonly=True)
    product_template_ids = fields.Many2many('product.template', string='Products to Duplicate', readonly=True)
    target_company_id = fields.Many2one('res.company', string='Target Company', readonly=True)
    target_website_id = fields.Many2one('website', string='Target Website', readonly=True)
    error_log = fields.Text(string='Error Log', readonly=True)
    
    # --- CAMPOS ACTUALIZADOS ---
    copy_cost = fields.Boolean(string="Copy Cost Price", readonly=True, default=False)
    manual_exchange_rate = fields.Float(string="Manual Exchange Rate", digits='(12, 6)', readonly=True)

    @api.depends('create_date', 'user_id')
    def _compute_name(self):
        for job in self:
            job.name = f"Job-{job.user_id.name or 'generic'}-{job.create_date.strftime('%Y-%m-%d %H:%M') if job.create_date else job.id}"

    # ... _process_pending_jobs (sin cambios) ...
    @api.model
    def _process_pending_jobs(self):
        job_to_process = self.search([('state', '=', 'pending')], limit=1)
        if not job_to_process:
            return
        try:
            job_to_process.write({'state': 'in_progress'})
            self.env.cr.commit()
            job_to_process._execute_duplication()
            job_to_process.write({'state': 'done'})
            self.env.cr.commit()
        except Exception as e:
            _logger.error(f"Fallo en el job de duplicación {job_to_process.name}: {traceback.format_exc()}")
            self.env.cr.rollback()
            error_message = f"{type(e).__name__}: {e}"
            job_to_process.write({'state': 'failed', 'error_log': f"{error_message}\n\n{traceback.format_exc()}"})
            self.env.cr.commit()

    def _execute_duplication(self):
        self.ensure_one()
        original_templates = self.product_template_ids
        
        source_company = original_templates.sudo()[0].company_id if original_templates else self.env.company
        target_company = self.target_company_id.sudo()
        
        source_currency = source_company.currency_id
        target_currency = target_company.currency_id
        
        perform_conversion = source_currency and target_currency and source_currency != target_currency
        
        template_id_map = {}
        variant_id_map = {}

        for template in original_templates:
            copy_data = template.sudo().copy_data()[0]
            
            if self.copy_cost:
                copy_data['standard_price'] = template.standard_price
            
            fields_to_pop = ['accessory_product_ids', 'alternative_product_ids', 'optional_product_ids']
            for field in fields_to_pop:
                copy_data.pop(field, None)

            copy_data.update({'company_id': self.target_company_id.id, 'website_id': self.target_website_id.id})
            
            if perform_conversion:
                rate = 0.0
                if self.manual_exchange_rate > 0:
                    rate = self.manual_exchange_rate
                    _logger.info(f"Job {self.name}: Usando tasa manual {rate} para producto {template.name}")
                else:
                    try:
                        rate = source_currency._get_conversion_rate(source_currency, target_currency, target_company, fields.Date.today())
                    except UserError as e:
                        raise UserError(_("Currency conversion failed: No rate configured in Odoo. You can set a manual rate in the wizard.")) from e
                
                # Conversión de precios
                copy_data['list_price'] = copy_data.get('list_price', 0.0) * rate
                if 'standard_price' in copy_data:
                    copy_data['standard_price'] = copy_data['standard_price'] * rate

            assert copy_data['company_id'] == self.target_company_id.id, "Security Check Failed"

            new_template = self.env['product.template'].sudo().create(copy_data)
            template_id_map[template.id] = new_template.id

            # ... resto de la pasada 1 (sin cambios) ...
            if len(template.product_variant_ids) == len(new_template.product_variant_ids):
                for i, original_variant in enumerate(template.product_variant_ids):
                    new_variant = new_template.product_variant_ids[i]
                    variant_id_map[original_variant.id] = new_variant.id
                    if original_variant.default_code:
                        existing = self.env['product.product'].sudo().search([('default_code', '=', original_variant.default_code),('company_id', '=', self.target_company_id.id),('id', '!=', new_variant.id)], limit=1)
                        if not existing:
                            new_variant.sudo().write({'default_code': original_variant.default_code})

        _logger.info(f"Job {self.name}: Pasada 1 completada.")

        # ... PASADA 2 (sin cambios) ...
        ProductProduct = self.env['product.product'].sudo()
        ProductTemplate = self.env['product.template'].sudo()

        for original_template in original_templates:
            new_template = ProductTemplate.browse(template_id_map.get(original_template.id))
            if not new_template: continue

            if original_template.alternative_product_ids:
                target_alternative_ids = []
                for alt_tmpl in original_template.alternative_product_ids:
                    target_id = template_id_map.get(alt_tmpl.id)
                    if target_id:
                        target_alternative_ids.append(target_id)
                    elif alt_tmpl.product_variant_count > 0 and alt_tmpl.product_variant_id.default_code:
                        found = ProductProduct.search([('default_code', '=', alt_tmpl.product_variant_id.default_code), ('company_id', '=', self.target_company_id.id)], limit=1)
                        if found:
                            target_alternative_ids.append(found.product_tmpl_id.id)
                if target_alternative_ids:
                    new_template.write({'alternative_product_ids': [(6, 0, target_alternative_ids)]})
                    
            if original_template.accessory_product_ids:
                target_variant_ids = []
                for original_variant in original_template.accessory_product_ids:
                    target_id = variant_id_map.get(original_variant.id)
                    if target_id:
                        target_variant_ids.append(target_id)
                    elif original_variant.default_code:
                        found = ProductProduct.search([('default_code', '=', original_variant.default_code),('company_id', '=', self.target_company_id.id)], limit=1)
                        if found:
                            target_variant_ids.append(found.id)
                if target_variant_ids:
                    new_template.write({'accessory_product_ids': [(6, 0, target_variant_ids)]})
        
        _logger.warning(f"Job {self.name}: 'optional_product_ids' field is intentionally omitted.")
        _logger.info(f"Job {self.name} completed successfully.")

    def action_requeue(self):
        self.write({'state': 'pending', 'error_log': False})
# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooAnimalMeal(models.Model):
    _name = "zoo.animal.meal"
    _description = "Animal Meal"
    
    animal_id = fields.Many2one(comodel_name='zoo.animal', string='Animal', ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string='Food', ondelete='cascade')
    volume = fields.Float('Volume (kg)', required=True)
    meal_time = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night')
    ], string='Meal Time', default=False, required=False)
    state = fields.Selection([('unhealthy', 'Unhealthy'), ('healthy', 'Healthy')], string='Status', readonly=True, tracking=True, default='healthy')

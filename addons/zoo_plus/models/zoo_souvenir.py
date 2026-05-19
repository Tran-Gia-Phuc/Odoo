# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooSouvenir(models.Model):
    _name = "zoo.souvenir"
    _inherits = {'zoo.animal': 'zoo_animal_id'}
    _description = "Zoo Souvenir"
    
    zoo_animal_id = fields.Many2one(
        'zoo.animal', 'Animal',
        auto_join=True, index=True, ondelete="cascade", required=True)
    
    gift_type = fields.Selection([
        ('toy', 'Toy'),
        ('decoration', 'Decoration'),
        ('paper', 'Paper'),
        ('cotton', 'Cotton'),
        ('balloon', 'Balloon')
    ], string='Type', default='toy', required=True)
    
    gift_color = fields.Selection([
        ('white', 'White'),
        ('black', 'Black'),
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('cyan', 'Cyan'),
        ('indigo', 'Indigo'),
        ('violet', 'Violet'),
        ('rainbow', 'Rainbow'),
    ], string='Color', default='white', required=True)
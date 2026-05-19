# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class ZooDomainCategory(models.Model):
    _name = "zoo.dummy.categ"
    _description = "Zoo Dummy Categ"
    # https://stackoverflow.com/a/59600362/3973224 
    _parent_name = "parent_categ_id" # default value = "parent_id"
    _parent_store = True

    name = fields.Char('Name', required=True)
    parent_categ_id = fields.Many2one('zoo.dummy.categ', 'Parent Category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_categ_ids = fields.One2many('zoo.dummy.categ', 'parent_categ_id', 'Child Categories')

    dummy_ids = fields.One2many('zoo.dummy', 'categ_id', 'Dummies')

class ZooDomain(models.Model):
    _name = "zoo.dummy"
    _description = "Zoo Dummy Data"
    
    name = fields.Char('Name', required=True)
    a = fields.Float('A')
    b = fields.Float('B')
    c = fields.Float('C')

    date = fields.Date('Date')
    state = fields.Selection([
        ('first', 'First State'),
        ('second', 'Second State'),
        ('third', 'Third State')
    ], string='State', default='first', required=False)
    dtime = fields.Datetime('Date Time')
    is_online = fields.Boolean('Is Online', default=True)

    categ_id = fields.Many2one(comodel_name='zoo.dummy.categ', string='Categ')    
    categ_name = fields.Char('Categ Name', related='categ_id.name')
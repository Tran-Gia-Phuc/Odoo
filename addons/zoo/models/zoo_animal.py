
# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import datetime

class ZooAnimal(models.Model):
    _name = "zoo.animal"
    _description = "Animal in the zoo"

    name = fields.Char('Animal Name', required=True)    
    description = fields.Text('Description')
    dob = fields.Date('DOB', required=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', default='male', required=True)
    feed_time = fields.Datetime('Feed Time', copy=False)
    is_alive = fields.Boolean('Is Alive', default=True)
    image = fields.Binary("Image", attachment=True, help="Animal Image")
    weight = fields.Float('Weight (kg)')
    weight_pound = fields.Float('Weight (pounds)')
    introduction = fields.Text('Introduction (EN)')    
    
    age = fields.Integer('Pet Age', compute='_compute_age')    
    
    mother_id = fields.Many2one(comodel_name='zoo.animal', string='Mother', ondelete='set null') # ondelete: 'set null', 'restrict', 'cascade'
    mother_name = fields.Char('Mother Name', related='mother_id.name')
    female_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='mother_id', string='Female Children')

    toy_ids = fields.Many2many(comodel_name='product.product', 
                                string="Toys", 
                                relation='animal_product_toy_rel',
                                column1='col_animal_id',
                                column2='col_product_id')

    creature_id = fields.Many2one(comodel_name='zoo.creature', string='Creature')
    cage_id = fields.Many2one(comodel_name='zoo.cage', string='Cage', ondelete='set null')
    
    

    @api.depends('dob')
    def _compute_age(self):
        now = datetime.datetime.now()
        current_year = now.year
        for record in self:
            dob = record.dob
            if dob:
                dob_year = dob.year
                delta_year = current_year - dob_year
                if delta_year < 0:
                    raise ValidationError(_("Negative age: current year < DOB year!"))
                record.age = delta_year
            else:
                record.age = 0
        pass

    @api.constrains('dob')
    def _check_dob(self):
        for record in self:
            if record.dob and record.dob.year < 1900:
                raise ValidationError(_("Invalid DOB!"))

    @api.onchange('weight')
    def _update_weight_pound(self):
        self.weight_pound = self.weight * 2.204623

    @api.onchange('weight_pound')
    def _update_weight_kg(self):
        self.weight = self.weight_pound / 2.204623
        
    #exercise========================================================================================
    beensold = fields.Boolean('Been Sold', default=False)

    nickname = fields.Char('Nickname')
    description_en = fields.Text('Description (EN)')
    price = fields.Float('Price')
    father_id = fields.Many2one(comodel_name='zoo.animal', string='Father', ondelete='set null') 
    father_name = fields.Char('Father Name', related='father_id.name')
    male_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='father_id', string='Male Children')
    number_of_children = fields.Integer('Number of Children', compute="_compute_children_count", store=True)
    doctor_id = fields.Many2one('res.partner', string='Doctor')
    state = fields.Selection([('unhealthy', 'Unhealthy'), ('healthy', 'Healthy')], string='Status', readonly=True, tracking=True, default='healthy')
    def report_sickness(self):
        for rec in self:
            rec.state = 'unhealthy'

    def recovered_health(self):
        for rec in self:
            rec.state = 'healthy'
    def action_update_feed_time(self):
        for rec in self:
            rec.feed_time = fields.Datetime.now()
    def _cron_feed(self):
        animals = self.search([('id', '>', 0)])
        for rec in animals:
            rec.feed_time = fields.Datetime.now()
        pass

    meal_ids = fields.One2many(comodel_name='zoo.animal.meal', inverse_name='animal_id', string='Meals')

    @api.depends('female_children_ids', 'male_children_ids')
    def _compute_children_count(self):
        for record in self:
            record.number_of_children = len(record.female_children_ids) + len(record.male_children_ids)

    @api.constrains('father_id', 'mother_id')
    def _check_parent_ids(self):
        for record in self:
            if record.father_id and record.mother_id and record.father_id.id == record.mother_id.id:
                raise ValidationError(_("Father and mother cannot be the same animal!"))
            if record.father_id and record.father_id.id == record.id:
                raise ValidationError(_("Animal cannot be its own father!"))
            if record.mother_id and record.mother_id.id == record.id:
                raise ValidationError(_("Animal cannot be its own mother!"))
            if record in (record.father_id, record.mother_id):
                raise ValidationError(_("Animal cannot be its own parent!"))
            
    @api.constrains('female_children_ids', 'male_children_ids', 'gender')
    def _check_children_ids(self):
        for record in self:
            # if record.female_children_ids and record.male_children_ids:
            #     raise ValidationError(_("An animal cannot have both male and female children!"))
            if (record.female_children_ids and record.gender == 'male') or (record.female_children_ids and record.gender == 'Male'):
                raise ValidationError(_("Invalid female child"))
            if (record.male_children_ids and record.gender == 'female') or (record.male_children_ids and record.gender == 'Female'):
                raise ValidationError(_("Invalid male child"))
            
    @api.model
    def get_table_title(self, value=""):
        return "Title from server (%s)" % str(value)
    
    
    

# # -*- coding: utf-8 -*-
# import time
# import datetime

# from odoo import api, fields, models, tools, _
# from odoo.exceptions import UserError, ValidationError

# class ZooAnimal(models.Model):
#     _name = "zoo.animal"
#     _description = "Animal in the zoo"

#     name = fields.Char('Animal Name', required=True)    
#     description = fields.Text('Description')
#     dob = fields.Date('DOB', required=False)
#     gender = fields.Selection([
#         ('male', 'Male'),
#         ('female', 'Female')
#     ], string='Gender', default='male', required=True)
#     feed_time = fields.Datetime('Feed Time', copy=False)
#     is_alive = fields.Boolean('Is Alive', default=True)
#     image = fields.Binary("Image", attachment=True, help="Animal Image")
#     weight = fields.Float('Weight (kg)')
#     weight_pound = fields.Float('Weight (pounds)')
#     introduction = fields.Text('Introduction (EN)')
    
#     age = fields.Integer('Pet Age', compute='_compute_age') # computed field    
#     mother_id = fields.Many2one(comodel_name='zoo.animal', string='Mother', ondelete='set null') # ondelete: 'set null', 'restrict', 'cascade'
#     mother_name = fields.Char('Mother Name', related='mother_id.name')
#     female_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='mother_id', string='Female Children')
    
#     toy_ids = fields.Many2many(comodel_name='product.product', 
#                                 string="Toys", 
#                                 relation='animal_product_toy_rel',
#                                 column1='col_animal_id',
#                                 column2='col_product_id')
    
#     creature_id = fields.Many2one(comodel_name='zoo.creature', string='Creature')
    
#     @api.depends('dob')
#     def _compute_age(self):
#         now = datetime.datetime.now()
#         current_year = now.year
#         for record in self:
#             dob = record.dob
#             if dob:
#                 dob_year = dob.year
#                 delta_year = current_year - dob_year
#                 if delta_year < 0:
#                     raise ValidationError(_("Negative age: current year < DOB year!"))
#                 record.age = delta_year
#             else:
#                 record.age = False
#         pass
    
#     @api.constrains('dob')
#     def _check_dob(self):
#         for record in self:
#             if record.dob and record.dob.year < 1900:
#                 raise ValidationError(_("Invalid DOB!"))

#     @api.onchange('weight')
#     def _update_weight_pound(self):
#         self.weight_pound = self.weight * 2.204623
    
#     @api.onchange('weight_pound')
#     def _update_weight_kg(self):
#         self.weight = self.weight_pound / 2.204623
    
#     # exercise
#     nickname = fields.Char('Nickname')
#     introduction_vn = fields.Text('Introduction (VN)')
#     is_buy = fields.Boolean('Buy', default=False)
#     price = fields.Float('Price')
    
#     father_id = fields.Many2one(comodel_name='zoo.animal', string='Father', ondelete='set null')
#     male_children_ids = fields.One2many(comodel_name='zoo.animal', inverse_name='father_id', string='Male Children')
    
#     number_of_children = fields.Integer('Number of children', compute='_compute_number_of_children') # computed field    
#     doctor_id = fields.Many2one('res.partner', string='Doctor')

#     meal_ids = fields.One2many(comodel_name='zoo.animal.meal', inverse_name='animal_id', string='Meals')
#     cage_id = fields.Many2one(comodel_name='zoo.cage', string='Cage', ondelete='set null')
    
#     @api.depends('female_children_ids', 'male_children_ids')
#     def _compute_number_of_children(self):
#         for record in self:
#             record.number_of_children = len(record.female_children_ids) + len(record.male_children_ids)
    
#     @api.constrains('mother_id', 'father_id')
#     def _check_parent(self):
#         for record in self:
#             if record.mother_id and record.father_id and record.mother_id.id == record.father_id.id:
#                 raise ValidationError(_('Father and mother cannot be the same!'))
#             if record.mother_id and record.mother_id.id == record.id:
#                 raise ValidationError(_('Invalid mother!'))
#             if record.father_id and record.father_id.id == record.id:
#                 raise ValidationError(_('Invalid father!'))
    
#     @api.constrains('gender', 'female_children_ids', 'male_children_ids')
#     def _check_gender(self):
#         for record in self:
#             if len(record.female_children_ids) > 0 and len(record.male_children_ids) > 0:
#                 raise ValidationError(_('Animal has both female children and male children!'))
#             if record.gender == 'male' and len(record.female_children_ids) > 0:
#                 raise ValidationError(_('Animal is male, but it has female children!'))
#             if record.gender == 'female' and len(record.male_children_ids) > 0:
#                 raise ValidationError(_('Animal is female but it has male children!'))

